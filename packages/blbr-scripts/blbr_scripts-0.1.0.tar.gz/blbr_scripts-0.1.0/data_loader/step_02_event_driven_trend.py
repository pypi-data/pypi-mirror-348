#!/usr/bin/env python3
"""
Step to calculate BLBR trend using the event-driven approach.
This processes each symbol file individually and is more memory efficient.
"""
import os
import logging
import time
import pandas as pd
from datetime import datetime
import psutil
from dotenv import load_dotenv
from .utils import log_error_with_traceback, setup_logging

class EventDrivenTrendStep:
    def __init__(self, input_dir=None, output_dir=None):
        """
        Initialize the event-driven trend calculation step.
        
        Args:
            input_dir (str, optional): Directory containing input CSV files. Defaults to None (uses env variable).
            output_dir (str, optional): Directory to save output files. Defaults to None (uses env variable).
        """
        # Load environment variables
        load_dotenv()
        self.LOCAL_DIR = os.getenv("LOCAL_DIR")
        
        # Use provided directories if available, otherwise use environment variables
        self.INPUT_DIR = input_dir if input_dir is not None else os.getenv("INPUT_DIR")
        self.OUTPUT_DIR = output_dir if output_dir is not None else os.getenv("OUTPUT_DIR")
        
        logging.info(f"Using INPUT_DIR: {self.INPUT_DIR}")
        logging.info(f"Using OUTPUT_DIR: {self.OUTPUT_DIR}")
        
        setup_logging()
        
    def execute(self, all_data=None, index_all_data=None):
        """
        Process all symbol files in INPUT_DIR using event-driven approach.
        
        Args:
            all_data: Optional dictionary with symbol data (used when called from workflow)
            index_all_data: Optional list of DataFrames with index data (used when called from workflow)
            
        Returns:
            dict: Dictionary with symbol as key and processed DataFrame as value
        """
        # Ensure output directory exists
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        
        # Process all files in the input directory
        start_time = datetime.now()
        memory_before = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        logging.info(f"Starting event-driven trend calculation at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logging.info(f"Memory usage before trend calculation: {memory_before:.2f} MB")
        
        try:
            # Get list of all CSV files in the input directory
            input_files = [f for f in os.listdir(self.INPUT_DIR) if f.endswith('.csv')]
            total_files = len(input_files)
            processed_count = 0
            error_count = 0
            
            logging.info(f"Found {total_files} symbol files to process")
            
            # Process each file
            for filename in input_files:
                try:
                    file_path = os.path.join(self.INPUT_DIR, filename)
                    symbol = os.path.splitext(filename)[0]
                    
                    # Process the file
                    success = self._process_file(file_path, symbol)
                    
                    if success:
                        processed_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
                    log_error_with_traceback(
                        f"Error processing file {filename}",
                        e,
                        {"filename": filename}
                    )
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            memory_after = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            memory_used = memory_after - memory_before
            
            logging.info(f"Completed event-driven trend calculation in {duration:.2f} seconds")
            logging.info(f"Memory usage: Before={memory_before:.2f} MB, After={memory_after:.2f} MB, Used={memory_used:.2f} MB")
            logging.info(f"Successfully processed {processed_count} out of {total_files} files. Errors: {error_count}")
            
            return {"processed_count": processed_count, "total_files": total_files, "error_count": error_count}
            
        except Exception as e:
            log_error_with_traceback(
                "Error in event-driven trend calculation",
                e,
                {"input_dir": self.INPUT_DIR, "output_dir": self.OUTPUT_DIR}
            )
            return None
    
    def _process_file(self, file_path, symbol):
        """
        Process a single symbol file using the event-driven approach.
        
        Args:
            file_path: Path to the input CSV file
            symbol: Symbol name
            
        Returns:
            bool: True if processing was successful, False otherwise
        """
        try:
            start_time = time.time()
            
            # Read the input file
            df = pd.read_csv(file_path)
            
            # Ensure required columns exist
            required_columns = ["OPEN_PRICE", "HIGH_PRICE", "LOW_PRICE", "CLOSE_PRICE"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                logging.error(f"Missing required columns for {symbol}: {missing_columns}")
                return False
            
            # Import process_data_frame from blbr_trend_db
            from data_loader.blbr_trend_db import process_data_frame
            
            # Process the data
            try:
                processed_df = process_data_frame(df)
                
                # Add back the symbol and other metadata
                processed_df["SYMBOL"] = symbol
                
                # Add MTF and other columns if they exist in the original data
                for col in ["MTF", "MARGIN", "LEVERAGE", "MARKETCAP", "CATEGORY"]:
                    if col in df.columns:
                        processed_df[col] = df[col].iloc[0] if len(df) > 0 else None
                
                # Ensure Trend values are stored as strings
                if "Trend" in processed_df.columns:
                    processed_df["Trend"] = processed_df["Trend"].astype(str)
                
                # Save the processed data to OUTPUT_DIR
                output_file = os.path.join(self.OUTPUT_DIR, f"{symbol}.csv")
                
                # Clean up the DataFrame before saving
                # 1. Remove any unnamed columns
                cols_to_drop = [col for col in processed_df.columns if 'Unnamed' in str(col)]
                if cols_to_drop:
                    processed_df = processed_df.drop(columns=cols_to_drop)
                
                # 2. Ensure column names are clean and unique
                processed_df.columns = [col.strip() for col in processed_df.columns]
                processed_df.columns = pd.Series(processed_df.columns).drop_duplicates(keep='first').tolist()
                
                # 3. Fill NaN values appropriately
                processed_df = processed_df.fillna(value={
                    'MARKETCAP': 0,
                    'CATEGORY': '',
                    'MARGIN': 0,
                    'LEVERAGE': 0,
                    'ADX': 0,
                    'PLUS_DI': 0,
                    'MINUS_DI': 0
                })
                
                # 4. Write to CSV using a more robust approach
                with open(output_file, 'w', newline='') as f:
                    # Write header
                    f.write(','.join(processed_df.columns) + '\n')
                    
                    # Write data rows
                    for _, row in processed_df.iterrows():
                        values = []
                        for col in processed_df.columns:
                            val = row[col]
                            if pd.isna(val):
                                values.append('')
                            elif isinstance(val, (int, float)):
                                values.append(str(val))
                            else:
                                values.append(str(val))
                        f.write(','.join(values) + '\n')
                
                end_time = time.time()
                duration = end_time - start_time
                
                memory_usage = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
                logging.info(f"Successfully processed {symbol} in {duration:.2f} seconds")
                logging.info(f"Memory usage: {memory_usage:.2f} MB")
                logging.info(f"Saved processed data to {output_file}")
                
                return True
                
            except Exception as e:
                log_error_with_traceback(
                    f"Error processing trend data for {symbol}",
                    e,
                    {"symbol": symbol, "file_path": file_path}
                )
                return False
                
        except Exception as e:
            log_error_with_traceback(
                f"Error reading file for {symbol}",
                e,
                {"symbol": symbol, "file_path": file_path}
            )
            return False

def main():
    """Run the event-driven trend calculation step independently."""
    step = EventDrivenTrendStep()
    result = step.execute()
    if result:
        logging.info(f"Successfully processed {result['processed_count']} out of {result['total_files']} files")
    else:
        logging.error("Event-driven trend calculation failed")

if __name__ == "__main__":
    main()
