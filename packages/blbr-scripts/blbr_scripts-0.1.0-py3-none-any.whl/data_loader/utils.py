import logging
import os
import traceback
import json
import shutil

def log_error_with_traceback(error_message, error, context=None):
    """
    Log error with full traceback and context information.
    
    Args:
        error_message (str): Human-readable error message
        error (Exception): The exception object
        context (dict, optional): Additional context data to include in the log
    """
    error_details = {
        "error_message": error_message,
        "error_type": type(error).__name__,
        "error_args": str(error.args),
    }
    
    if context:
        error_details["context"] = context
    
    error_json = json.dumps(error_details, default=str)
    logging.error(f"{error_message}: {error}\nContext: {error_json}\nTraceback: {traceback.format_exc()}")


def remove_dir(dir_path):
    """Remove a directory if it exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        logging.info(f"Deleted: {dir_path}")
    else:
        logging.info(f"Directory does not exist: {dir_path}")


def setup_logging():
    """Configure and set up logging."""
    # Configure Logging
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create log formatters
    from datetime import datetime
    detailed_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s"
    )
    console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Clear any existing handlers
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Create file handler for all logs
    log_file = os.path.join(LOG_DIR, f"blbr_trend_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)

    # Create file handler for error logs
    error_log_file = os.path.join(LOG_DIR, f"blbr_trend_errors_{datetime.now().strftime('%Y%m%d')}.log")
    error_file_handler = logging.FileHandler(error_log_file)
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_file_handler)

    logging.info(f"Logging initialized. Info logs: {log_file}, Error logs: {error_log_file}")
    
    return log_file, error_log_file
