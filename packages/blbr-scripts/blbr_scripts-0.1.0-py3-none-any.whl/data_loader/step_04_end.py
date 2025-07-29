import logging
import os
from dotenv import load_dotenv
from .utils import log_error_with_traceback, setup_logging
from .mongodb_utils import MongoDBHandler

class EndStep:
    def __init__(self, workflow=None):
        """
        Initialize the end step.
        
        Args:
            workflow: The parent workflow instance or None for standalone mode
        """
        # Load environment variables if running standalone
        if workflow is None:
            load_dotenv()
            self.MONGO_URI = os.getenv("MONGO_URI")
            self.DB_NAME = os.getenv("BHAVCOPY_DB_NAME")
            self.COLLECTION_NAME = os.getenv("BHAVCOPY_COLLECTION_NAME")
            self.CONFIG_COLLECTION_NAME = "workflow_config"
            setup_logging()
        else:
            self.MONGO_URI = workflow.MONGO_URI
            self.DB_NAME = workflow.DB_NAME
            self.COLLECTION_NAME = workflow.COLLECTION_NAME
            self.CONFIG_COLLECTION_NAME = workflow.CONFIG_COLLECTION_NAME
            
        self.workflow = workflow
        self.mongo_handler = MongoDBHandler(
            self.MONGO_URI,
            self.DB_NAME,
            self.COLLECTION_NAME,
            self.CONFIG_COLLECTION_NAME
        )
        
    def execute(self, end_date=None):
        """
        End step - update configuration with last executed date.
        
        Args:
            end_date: The end date of the current workflow run
            
        Returns:
            bool: True if successful, False otherwise
        """
        from datetime import date
        
        # If running standalone and no end_date provided, use today's date
        if end_date is None:
            end_date = date.today()
            logging.info(f"No end date provided, using today's date: {end_date}")
            
        # Store the last executed date in the configuration collection
        success = self.mongo_handler.update_last_executed_date(end_date)
        
        # Update the last bhavcopy date
        bhavcopy_success = self.mongo_handler.update_last_bhavcopy_date(self.COLLECTION_NAME)
            
        logging.info("Workflow completed successfully.")
        
        return success and bhavcopy_success


def main():
    """Run the end step independently."""
    step = EndStep()
    success = step.execute()
    if success:
        logging.info("Successfully updated last executed date and bhavcopy date")
    else:
        logging.info("Failed to update configuration data")


if __name__ == "__main__":
    main()
