#!/usr/bin/env python3
"""
Step to sync all files in OUTPUT_DIR with MongoDB database.
"""
import os
import logging
import glob
import pandas as pd
import time
from datetime import datetime
from pymongo import MongoClient, InsertOne
from dotenv import load_dotenv
from .utils import log_error_with_traceback, setup_logging

class SyncMongoDBStep:
    def __init__(self, output_dirs=None):
        """
        Initialize the MongoDB sync step.
        
        Args:
            output_dirs (list, optional): List of output directories to process.
                                         If None, uses the OUTPUT_DIR from environment variables.
        """
        # Load environment variables
        load_dotenv()
        
        # Use provided output_dirs if specified, otherwise use environment variable
        if output_dirs is None:
            self.OUTPUT_DIRS = [os.getenv("OUTPUT_DIR"), os.getenv("OUTPUT_DIR_INDEX")]
        elif isinstance(output_dirs, list):
            self.OUTPUT_DIRS = output_dirs
        else:
            # If a single string is provided, convert to list
            self.OUTPUT_DIRS = [output_dirs]
        
        # Filter out None values
        self.OUTPUT_DIRS = [d for d in self.OUTPUT_DIRS if d is not None]
        
        self.MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://laabhum:Metacoins123@localhost:27017/")
        self.DB_NAME = os.getenv("MONGODB_DATABASE", "stock_data")
        self.COLLECTION_NAME = os.getenv("BLBR_TREND_COLLECTION", "blbr_trend_data")
        self.CONFIGURATION_COLLECTION_NAME = os.getenv("CONFIGURATION_COLLECTION_NAME", "configuration")
        self.BATCH_SIZE = 1000  # Optimal batch size for bulk operations
        setup_logging()
        
    def _convert_to_datetime(self, date_value):
        """
        Convert various date formats to datetime objects for MongoDB time series collection.
        Always returns datetime in the ISO format YYYY-MM-DDTHH:MM:SS.zzz
        
        Args:
            date_value: The date value to convert (can be string, datetime, timestamp, etc.)
            
        Returns:
            datetime: A properly formatted datetime object for MongoDB in ISO format
        """
        from datetime import datetime
        import pytz
        
        # Function to standardize datetime format for MongoDB
        def format_datetime(dt):
            # Ensure datetime has no timezone info and no microseconds
            # MongoDB expects a naive datetime object for time series
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt.replace(microsecond=0)  # Remove microseconds for consistency
        
        # If no date value provided, use current time
        if date_value is None:
            return format_datetime(datetime.now())
            
        # Handle string date formats
        if isinstance(date_value, str):
            try:
                # Try standard date format
                dt = datetime.strptime(date_value, "%Y-%m-%d")
                # Set time to midnight
                return format_datetime(dt.replace(hour=0, minute=0, second=0))
            except ValueError:
                try:
                    # Try datetime format
                    dt = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")
                    return format_datetime(dt)
                except ValueError:
                    logging.warning(f"Could not parse date string: {date_value}")
                    # Use current time as fallback
                    return format_datetime(datetime.now())
        
        # Handle datetime objects
        if isinstance(date_value, datetime):
            return format_datetime(date_value)
            
        # Handle pandas Timestamp or other date-like objects
        try:
            dt = datetime.fromtimestamp(pd.Timestamp(date_value).timestamp())
            return format_datetime(dt)
        except:
            logging.warning(f"Could not convert to datetime: {date_value}")
            return format_datetime(datetime.now())
    
    def _get_latest_creation_date(self, collection):
        """
        Get the latest creation_date from the MongoDB collection.
        
        Args:
            collection: MongoDB collection to query
            
        Returns:
            datetime: The latest creation_date found in the collection, or None if no records
        """
        from datetime import datetime
        
        try:
            # Find the latest creation_date using aggregation pipeline
            pipeline = [
                {"$sort": {"creation_date": -1}},  # Sort by creation_date in descending order
                {"$limit": 1},  # Get only the first document
                {"$project": {"_id": 0, "creation_date": 1}}  # Project only the creation_date field
            ]
            
            result = list(collection.aggregate(pipeline))
            
            if result and "creation_date" in result[0]:
                return result[0]["creation_date"]
            else:
                logging.warning("No creation_date found in collection")
                return None
        except Exception as e:
            logging.error(f"Error getting latest creation_date: {str(e)}")
            return None
    
    def _update_configuration(self, db, latest_date):
        """
        Update the configuration collection with the latest creation date.
        
        Args:
            db: MongoDB database instance
            latest_date: The latest creation date to store in configuration
        """
        from datetime import datetime
        
        try:
            config_collection = db[self.CONFIGURATION_COLLECTION_NAME]
            
            # Check if the configuration entry exists
            config_entry = config_collection.find_one({
                "namespace": "trend_data",
                "key": "last_sync_date"
            })
            
            current_time = datetime.now()
            
            if config_entry:
                # Update existing configuration entry
                config_collection.update_one(
                    {"namespace": "trend_data", "key": "last_sync_date"},
                    {
                        "$set": {
                            "value": latest_date.isoformat(),
                            "updated_at": current_time
                        }
                    }
                )
                logging.info("Updated existing configuration entry for last_sync_date")
            else:
                # Create new configuration entry
                config_collection.insert_one({
                    "namespace": "trend_data",
                    "key": "last_sync_date",
                    "value": latest_date.isoformat(),
                    "value_type": "date",
                    "description": "Latest creation date in the trend data collection",
                    "created_at": current_time,
                    "updated_at": current_time
                })
                logging.info("Created new configuration entry for last_sync_date")
                
        except Exception as e:
            logging.error(f"Error updating configuration: {str(e)}")
        
    def execute(self):
        """
        Sync all files in OUTPUT_DIRS with MongoDB database.
        Truncates existing collection data before inserting new data.
        
        Returns:
            bool: True if sync was successful, False otherwise
        """
        try:
            overall_start_time = time.time()
            logging.info(f"Starting MongoDB sync from directories: {', '.join(self.OUTPUT_DIRS)}")
            
            # Check if all output directories exist
            missing_dirs = [d for d in self.OUTPUT_DIRS if not os.path.exists(d)]
            if missing_dirs:
                logging.error(f"The following directories do not exist: {', '.join(missing_dirs)}")
                return False
            
            # Find all CSV files in all output directories
            csv_files = []
            for output_dir in self.OUTPUT_DIRS:
                dir_files = glob.glob(os.path.join(output_dir, "*.csv"))
                logging.info(f"Found {len(dir_files)} CSV files in {output_dir}")
                csv_files.extend(dir_files)
                
            if not csv_files:
                logging.warning(f"No CSV files found in any of the specified directories")
                return False
                
            logging.info(f"Found {len(csv_files)} CSV files to sync with MongoDB")
            logging.info(f"Connecting to MongoDB at {self.MONGODB_URI}")

            # Connect to MongoDB with proper write concern for better performance
            connection_start_time = time.time()
            client = MongoClient(self.MONGODB_URI, 
                               maxPoolSize=50,  # Increase connection pool size
                               socketTimeoutMS=30000,  # Increase socket timeout
                               connectTimeoutMS=30000)  # Increase connection timeout
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            connection_end_time = time.time()
            connection_duration = connection_end_time - connection_start_time
            logging.info(f"MongoDB connection established in {connection_duration:.2f} seconds")
            
            # Check if collection exists and is a time series collection
            collections_list = db.list_collection_names()
            
            if self.COLLECTION_NAME not in collections_list:
                # Create time series collection if it doesn't exist
                logging.info(f"Creating time series collection {self.COLLECTION_NAME}")
                db.create_collection(
                    self.COLLECTION_NAME,
                    timeseries={
                        'timeField': 'creation_date',
                        'metaField': 'symbol',
                        # Valid values for granularity are: 'seconds', 'minutes', 'hours'
                        'granularity': 'hours'
                    }
                )
                # Create indexes for faster querying
                collection.create_index([("symbol", 1), ("creation_date", 1)])
                collection.create_index("creation_date")
            
            # Truncate existing collection - use efficient bulk delete
            truncate_start_time = time.time()
            logging.info(f"Truncating collection {self.COLLECTION_NAME} in database {self.DB_NAME}")
            collection.delete_many({})
            truncate_end_time = time.time()
            truncate_duration = truncate_end_time - truncate_start_time
            logging.info(f"Collection truncated in {truncate_duration:.2f} seconds")
            
            # Process each CSV file and insert into MongoDB
            processing_start_time = time.time()
            total_records = 0
            total_batches = 0
            file_metrics = {}
            for file_path in csv_files:
                try:
                    file_name = os.path.basename(file_path)
                    file_start_time = time.time()
                    logging.info(f"Processing file: {file_name}")
                    
                    # Read CSV file
                    read_start_time = time.time()
                    df = pd.read_csv(file_path)
                    read_end_time = time.time()
                    read_duration = read_end_time - read_start_time
                    
                    # Convert numeric columns to appropriate types for better storage and query performance
                    numeric_columns = [
                        'OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY', 
                        'TURNOVER_LACS', 'DELIV_PER', 'MARKETCAP', 'MARGIN', 'LEVERAGE',
                        'RSI', 'GAIN', 'LOSS', 'TR', 'ATR', 'BASIC_UPPERBAND', 'BASIC_LOWERBAND',
                        'FINAL_UPPERBAND', 'FINAL_LOWERBAND', 'SUPERTREND', 'EMA_20', 'EMA_50',
                        'EMA_100', 'EMA_200', 'AVG_VOL_30', 'AVG_VOL_100', 'AVG_VOL_200',
                        'ADX', 'PLUS_DI', 'MINUS_DI',
                    ]
                    
                    for col in numeric_columns:
                        if col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    
                    # Process in batches for better performance
                    records = []
                    batch_count = 0
                    last_valid_trend = ""

                    for _, row in df.iterrows():
                        # Handle creation_date first to ensure it's properly formatted for time series
                        creation_date = self._convert_to_datetime(row.get("DATE1"))
                        current_trend = str(row.get("Trend", ""))
                        
                        # Update last_valid_trend if current trend is valid
                        if current_trend and current_trend.strip() and current_trend.lower() not in ["nan", "none", "null", ""]:
                            last_valid_trend = current_trend
                        # Determine EXCHANGE value based on BSECODE
                        bsecode = row.get("BSECODE", "")
                        # Check if BSECODE is null, empty or nan
                        if pd.isna(bsecode) or str(bsecode).strip() == "" or str(bsecode).lower() == "nan":
                            exchange_value = ["NSE"]
                        else:
                            exchange_value = ["NSE", "BSE"]
                            
                        # Create structured document with proper numeric types
                        document = {
                            "symbol": str(row.get("SYMBOL", "")),  # Ensure string type
                            "company_name": str(row.get("COMPANY_NAME", "")),
                            "series": str(row.get("SERIES", "")),
                            "actual_date": str(row.get("DATE1", "")),
                            "open_price": float(row.get("OPEN_PRICE", 0) or 0),  # Convert to float, handle None
                            "high_price": float(row.get("HIGH_PRICE", 0) or 0),
                            "low_price": float(row.get("LOW_PRICE", 0) or 0),
                            "close_price": float(row.get("CLOSE_PRICE", 0) or 0),
                            "ttl_trd_qnty": int(row.get("TTL_TRD_QNTY", 0) or 0),  # Convert to int
                            "turnover_lacs": float(row.get("TURNOVER_LACS", 0) or 0),
                            "deliv_percent": float(row.get("DELIV_PER", 0) or 0),
                            "marketcap": float(row.get("MARKETCAP", 0) or 0),
                            "industry": str(row.get("INDUSTRY", "")),
                            "exchange": exchange_value,  # Use the determined exchange value
                            "category": str(row.get("CATEGORY", "")),
                            "margin": float(row.get("MARGIN", 0) or 0),
                            "leverage": float(row.get("LEVERAGE", 0) or 0),
                            "mtf": str(row.get("MTF", "")),
                            "rsi": {
                                "rsi_value": float(row.get("RSI", 0) or 0),
                                "gain": float(row.get("Gain", 0) or 0),
                                "loss": float(row.get("Loss", 0) or 0),
                                "avg_gain": float(row.get("AVG_GAIN", 0) or 0),
                                "avg_loss": float(row.get("AVG_LOSS", 0) or 0)
                            },
                            "trend": {
                                "trend_value": str(row.get("Trend", "")),
                                "last_valid_trend": last_valid_trend,
                                "bull": float(row.get("Bull", 0) or 0),
                                "bear": float(row.get("Bear", 0) or 0),
                                "bull_percent": str(row.get("Bull %", "0%")),
                                "bear_percent": str(row.get("Bear %", "0%"))
                            },
                            "supertrend": {
                                "tr": float(row.get("TR", 0) or 0),
                                "atr": float(row.get("ATR", 0) or 0),
                                "basic_upperband": float(row.get("BASIC_UPPERBAND", 0) or 0),
                                "basic_lowerband": float(row.get("BASIC_LOWERBAND", 0) or 0),
                                "final_upperband": float(row.get("FINAL_UPPERBAND", 0) or 0),
                                "final_lowerband": float(row.get("FINAL_LOWERBAND", 0) or 0),
                                "supertrend_value": float(row.get("SUPERTREND", 0) or 0)
                            },
                            "ema": {
                                "ema_20": float(row.get("EMA_20", 0) or 0),
                                "ema_20_ind": str(row.get("EMA_20_IND", "")),
                                "ema_50": float(row.get("EMA_50", 0) or 0),
                                "ema_50_ind": str(row.get("EMA_50_IND", "")),
                                "ema_100": float(row.get("EMA_100", 0) or 0),
                                "ema_100_ind": str(row.get("EMA_100_IND", "")),
                                "ema_200": float(row.get("EMA_200", 0) or 0),
                                "ema_200_ind": str(row.get("EMA_200_IND", ""))
                            },
                            "avg_vol": {
                                "avg_vol_30": float(row.get("AVG_VOL_30", 0) or 0),
                                "avg_vol_100": float(row.get("AVG_VOL_100", 0) or 0),
                                "avg_vol_200": float(row.get("AVG_VOL_200", 0) or 0)
                            },
                            "adx": {
                                "adx": float(row.get("ADX", 0) or 0),
                                "plus_di": float(row.get("PLUS_DI", 0) or 0),
                                "minus_di": float(row.get("MINUS_DI", 0) or 0)
                            },
                            # Always set creation_date for time series collection
                            "creation_date": creation_date
                        }
                        
                        records.append(document)
                        
                        # Process in batches for better performance
                        if len(records) >= self.BATCH_SIZE:
                            try:
                                # Use bulk write operation for better performance
                                bulk_operations = [InsertOne(doc) for doc in records]
                                result = collection.bulk_write(bulk_operations, ordered=False)
                                batch_count += 1
                                total_batches += 1
                                total_records += len(records)
                                logging.info(f"Inserted batch {batch_count} with {len(records)} records from {file_name}")
                                records = []  # Clear records after insertion
                            except Exception as e:
                                logging.error(f"Error inserting batch {batch_count}: {str(e)}")
                    
                    # Insert any remaining records
                    if records:
                        try:
                            bulk_operations = [InsertOne(doc) for doc in records]
                            result = collection.bulk_write(bulk_operations, ordered=False)
                            batch_count += 1
                            total_batches += 1
                            total_records += len(records)
                            logging.info(f"Inserted final batch {batch_count} with {len(records)} records from {file_name}")
                        except Exception as e:
                            logging.error(f"Error inserting final batch: {str(e)}")
                    else:
                        logging.warning(f"No records found in {file_name}")
                    
                    # Calculate and store file metrics
                    file_end_time = time.time()
                    file_duration = file_end_time - file_start_time
                    file_metrics[file_name] = {
                        'records': len(df),
                        'batches': batch_count,
                        'read_time': read_duration,
                        'total_time': file_duration,
                        'records_per_second': len(df) / file_duration if file_duration > 0 else 0
                    }
                        
                except Exception as e:
                    log_error_with_traceback(
                        f"Error processing file {file_path}",
                        e,
                        {"file_path": file_path}
                    )
            # Calculate and log overall metrics
            processing_end_time = time.time()
            processing_duration = processing_end_time - processing_start_time
            overall_end_time = time.time()
            overall_duration = overall_end_time - overall_start_time
            
            # Calculate and log overall metrics
            processing_end_time = time.time()
            processing_duration = processing_end_time - processing_start_time
            overall_end_time = time.time()
            overall_duration = overall_end_time - overall_start_time
            
            # Calculate average processing rates
            avg_records_per_second = total_records / processing_duration if processing_duration > 0 else 0
            avg_files_per_second = len(csv_files) / processing_duration if processing_duration > 0 else 0
            
            # Log performance metrics
            logging.info(f"Successfully synced {total_records} records to MongoDB collection {self.COLLECTION_NAME}")
            logging.info(f"Performance metrics:")
            logging.info(f"  - Total duration: {overall_duration:.2f} seconds")
            logging.info(f"  - Connection time: {connection_duration:.2f} seconds")
            logging.info(f"  - Truncation time: {truncate_duration:.2f} seconds")
            logging.info(f"  - Processing time: {processing_duration:.2f} seconds")
            logging.info(f"  - Files processed: {len(csv_files)}")
            logging.info(f"  - Total batches: {total_batches}")
            logging.info(f"  - Records per second: {avg_records_per_second:.2f}")
            logging.info(f"  - Files per second: {avg_files_per_second:.2f}")
            
            # Update configuration with latest creation date
            latest_date = self._get_latest_creation_date(collection)
            if latest_date:
                self._update_configuration(db, latest_date)
                logging.info(f"Updated configuration with latest creation date: {latest_date}")
            
            # Find slowest and fastest files
            if file_metrics:
                slowest_file = max(file_metrics.items(), key=lambda x: x[1]['total_time'])
                fastest_file = min(file_metrics.items(), key=lambda x: x[1]['total_time'])
                largest_file = max(file_metrics.items(), key=lambda x: x[1]['records'])
                
                logging.info(f"  - Slowest file: {slowest_file[0]} ({slowest_file[1]['total_time']:.2f} seconds, {slowest_file[1]['records']} records)")
                logging.info(f"  - Fastest file: {fastest_file[0]} ({fastest_file[1]['total_time']:.2f} seconds, {fastest_file[1]['records']} records)")
                logging.info(f"  - Largest file: {largest_file[0]} ({largest_file[1]['records']} records, {largest_file[1]['total_time']:.2f} seconds)")
            client.close()
            return True
            
        except Exception as e:
            # Calculate error timing if possible
            try:
                error_time = time.time()
                error_duration = error_time - overall_start_time
                logging.error(f"Error occurred after {error_duration:.2f} seconds of processing")
            except Exception:
                pass
                
            log_error_with_traceback(
                "Error syncing data with MongoDB", 
                e, 
                {"output_dirs": self.OUTPUT_DIRS, "db_name": self.DB_NAME, "collection_name": self.COLLECTION_NAME}
            )
            logging.info("Failed to sync data with MongoDB.")
            return False

def main():
    """Run the MongoDB sync step independently."""
    step = SyncMongoDBStep()
    success = step.execute()
    if success:
        logging.info("MongoDB sync completed successfully")
    else:
        logging.error("MongoDB sync failed")

if __name__ == "__main__":
    main()
