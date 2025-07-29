from pymongo import MongoClient
import pandas as pd
import logging
from datetime import date
from .utils import log_error_with_traceback

class MongoDBHandler:
    def __init__(self, mongo_uri, db_name, collection_name, config_collection_name="workflow_config"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.config_collection_name = config_collection_name

    def get_collection_count(self):
        """Check if the MongoDB collection has any data."""
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db[self.collection_name]
            count = collection.count_documents({})
            client.close()
            return count
        except Exception as e:
            log_error_with_traceback(
                f"Error connecting to MongoDB collection {self.collection_name}", 
                e, 
                {"connection_uri": self.mongo_uri, "db_name": self.db_name}
            )
            return 0  # Assume collection is empty if there's an error

    def get_last_executed_date(self):
        """Retrieve the last executed date from the configuration collection."""
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            config_collection = db[self.config_collection_name]

            # Look for the last execution record
            config = config_collection.find_one({"config_type": "last_execution"})
            client.close()

            if config and "last_date" in config:
                # Convert string date to date object
                last_date_str = config["last_date"]
                return date.fromisoformat(last_date_str)
            return None
        except Exception as e:
            log_error_with_traceback(
                "Error retrieving last executed date from MongoDB", 
                e, 
                {"config_collection": self.config_collection_name}
            )
            return None

    def get_start_date_config(self):
        """Retrieve the start date from the configuration collection."""
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            config_collection = db[self.config_collection_name]

            # Look for the start date configuration
            config = config_collection.find_one({"config_type": "start_date"})
            client.close()

            if config and "date" in config:
                # Convert string date to date object
                start_date_str = config["date"]
                return date.fromisoformat(start_date_str)
            return None
        except Exception as e:
            log_error_with_traceback(
                "Error retrieving start date from MongoDB", 
                e, 
                {"config_collection": self.config_collection_name}
            )
            return None

    def write_to_mongodb(self, df, collection_name=None, keep_latest_only=True):
        """
        Write DataFrame to MongoDB collection.
        
        Args:
            df (pandas.DataFrame): DataFrame to write to MongoDB
            collection_name (str, optional): Name of the collection to write to, defaults to self.collection_name
            keep_latest_only (bool): If True, keep only records for symbols in the latest creation date
        
        Returns:
            bool: True if successful, False otherwise
        """
        if df is None or df.empty:
            logging.info(f"No data to write to {collection_name or self.collection_name}.")
            return False
        
        if collection_name is None:
            collection_name = self.collection_name
        
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            collection = db[collection_name]

            # Convert DataFrame to Dictionary for MongoDB
            records = df.to_dict(orient="records")
            if records:
                collection.insert_many(records)
                logging.info(f"Inserted {len(records)} records into {collection_name} successfully.")
            
            if keep_latest_only:
                # Find the latest creation date in the collection
                latest_date_result = collection.find().sort("CREATION_DATE", -1).limit(1)
                latest_date_doc = next(latest_date_result, None)
                
                if latest_date_doc and "CREATION_DATE" in latest_date_doc:
                    latest_date = latest_date_doc["CREATION_DATE"]
                    
                    # Get all symbols with the latest creation date
                    latest_symbols_cursor = collection.distinct("SYMBOL", {"CREATION_DATE": latest_date})
                    latest_symbols = list(latest_symbols_cursor)
                    
                    # Delete all records for symbols not in the latest creation date
                    delete_result = collection.delete_many({
                        "SYMBOL": {"$nin": latest_symbols}
                    })
                    
                    logging.info(f"Deleted {delete_result.deleted_count} records of symbols not present in the latest creation date ({latest_date.strftime('%Y-%m-%d')}) from {collection_name}")
            
            client.close()
            return True
        except Exception as e:
            log_error_with_traceback(
                f"Error inserting into MongoDB collection {collection_name}", 
                e, 
                {"record_count": len(df) if df is not None else 0}
            )
            return False

    def update_last_executed_date(self, execution_date):
        """Update the last executed date in the configuration collection."""
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            config_collection = db[self.config_collection_name]

            # Update or insert the last execution record
            config_collection.update_one(
                {"config_type": "last_execution"},
                {"$set": {"last_date": execution_date.isoformat(), "updated_at": pd.Timestamp.now().isoformat()}},
                upsert=True
            )
            
            logging.info(f"Updated last executed date to {execution_date} in configuration collection.")
            client.close()
            return True
        except Exception as e:
            log_error_with_traceback(
                "Error updating last executed date in MongoDB", 
                e, 
                {"config_collection": self.config_collection_name}
            )
            return False

    def update_last_bhavcopy_date(self, collection_name=None):
        """Update the last bhavcopy date in the configuration collection."""
        if collection_name is None:
            collection_name = self.collection_name
            
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            config_collection = db[self.config_collection_name]
            collection = db[collection_name]

            # Find the most recent record based on CREATION_DATE
            latest_record = collection.find_one(
                {}, 
                sort=[("CREATION_DATE", -1)]
            )
            
            if latest_record and "DATE1" in latest_record:
                from datetime import datetime
                last_bhavcopy_date = latest_record["DATE1"]
                date_obj = datetime.strptime(last_bhavcopy_date, "%d-%b-%Y")
                last_bhavcopy_date = date_obj.date().isoformat()
                
                # Update or insert the last bhavcopy date record
                config_collection.update_one(
                    {"config_type": "last_bhavcopy_date"},
                    {
                        "$set": {
                            "last_date": last_bhavcopy_date,
                            "updated_at": pd.Timestamp.now().isoformat()
                        }
                    },
                    upsert=True
                )
                logging.info(f"Updated last bhavcopy date to {last_bhavcopy_date} in configuration collection.")
                client.close()
                return True
            else:
                logging.warning("Could not find DATE1 column in the latest record")
                client.close()
                return False
        except Exception as e:
            log_error_with_traceback(
                "Error updating last bhavcopy date in MongoDB", 
                e, 
                {"collection": collection_name}
            )
            return False
