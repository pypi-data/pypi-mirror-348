import os
import re
import pandas as pd
import glob
import time
from datetime import datetime, date, timedelta
import logging
from dotenv import load_dotenv
from jugaad_data.nse import bhavcopy_index_save

from .utils import log_error_with_traceback, setup_logging


class IndexStartStep:
    def __init__(self):
        """
        Initialize the index start step.
        Processes index bhavcopy files and maps columns to standardized format.
        """
        # Load environment variables
        load_dotenv()
        self.LOCAL_DIR_BHAVCOPY_INDEX = os.getenv("LOCAL_DIR_BHAVCOPY_INDEX")
        self.INPUT_DIR_INDEX = os.getenv("INPUT_DIR_INDEX")
        self.OUTPUT_DIR_INDEX = os.getenv("OUTPUT_DIR_INDEX")
        setup_logging()
        
        # Column mapping from source to target
        self.column_mapping = {
            'Index Name': 'SYMBOL',
            'Index Date': 'DATE1',
            'Open Index Value': 'OPEN_PRICE',
            'High Index Value': 'HIGH_PRICE',
            'Low Index Value': 'LOW_PRICE',
            'Closing Index Value': 'CLOSE_PRICE',
            'Volume': 'TTL_TRD_QNTY',
            'Turnover (Rs. Cr.)': 'TURNOVER_LACS'
        }
        
        # List of columns to keep in the output
        self.output_columns = list(self.column_mapping.values())
        
    def clean_error_files(self):
        """
        Check for error messages in downloaded files and delete them.
        Specifically looks for 'The resource you are looking for has been removed' message.
        """
        if not os.path.exists(self.LOCAL_DIR_BHAVCOPY_INDEX):
            logging.warning(f"Directory not found: {self.LOCAL_DIR_BHAVCOPY_INDEX}")
            return
            
        # Get all CSV files in the directory
        csv_files = glob.glob(os.path.join(self.LOCAL_DIR_BHAVCOPY_INDEX, "*.csv"))
        
        if not csv_files:
            logging.info(f"No CSV files found in {self.LOCAL_DIR_BHAVCOPY_INDEX} to check for errors")
            return
            
        error_files = 0
        for file_path in csv_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Check if file contains error message
                if "The resource you are looking for has been removed" in content:
                    logging.warning(f"Found error message in {os.path.basename(file_path)}, deleting file")
                    os.remove(file_path)
                    error_files += 1
            except Exception as e:
                logging.error(f"Error checking file {file_path}: {str(e)}")
                
        if error_files > 0:
            logging.info(f"Deleted {error_files} files containing error messages")
        else:
            logging.info("No files with error messages found")
    
    def process_index_file(self, file_path):
        """
        Process a single index bhavcopy file and map columns.
        
        Args:
            file_path (str): Path to the index bhavcopy file
            
        Returns:
            pd.DataFrame: Processed dataframe with mapped columns
        """
        try:
            logging.info(f"Processing index file: {file_path}")
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Print column names for debugging
            logging.debug(f"Original columns: {df.columns.tolist()}")
            
            # Check if required columns exist in the dataframe
            missing_columns = [col for col in self.column_mapping.keys() if col not in df.columns]
            if missing_columns:
                logging.warning(f"Missing columns in {os.path.basename(file_path)}: {missing_columns}")
                if len(missing_columns) > len(self.column_mapping) / 2:
                    logging.error(f"Too many missing columns in {os.path.basename(file_path)}, skipping file")
                    return None
            
            # Create a new DataFrame with only the columns we want
            new_df = pd.DataFrame()
            
            # Map each source column to target column
            for source_col, target_col in self.column_mapping.items():
                if source_col in df.columns:
                    # Copy the column values
                    new_df[target_col] = df[source_col]
                    
                    # Convert dash characters to NaN in numeric columns
                    if target_col in ['OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'TTL_TRD_QNTY', 'TURNOVER_LACS']:
                        # Replace dash characters and other non-numeric placeholders with NaN
                        new_df[target_col] = new_df[target_col].replace(['-', 'NA', 'N/A', ''], pd.NA)
                        # Convert to numeric, coercing any remaining non-numeric values to NaN
                        new_df[target_col] = pd.to_numeric(new_df[target_col], errors='coerce')
                        
                        if target_col in ['TTL_TRD_QNTY', 'TURNOVER_LACS'] and new_df[target_col].isna().all():
                            logging.info(f"All values in {target_col} are non-numeric or missing for this index file")
                else:
                    # If source column is missing, add an empty column
                    new_df[target_col] = None
            
            # Check if the new dataframe has any data
            if new_df.empty or new_df.dropna(how='all').empty:
                logging.warning(f"No data after mapping columns in {os.path.basename(file_path)}")
                return None
                
            # Use the new dataframe for further processing
            df = new_df
            
            # Additional check for empty dataframe
            if df.empty:
                logging.warning(f"No columns could be mapped in {file_path}")
                return None
            
            # Ensure all required columns exist
            for target_col in self.column_mapping.values():
                if target_col not in df.columns:
                    logging.warning(f"Column {target_col} not found in processed dataframe")
            
            return df
            
        except Exception as e:
            log_error_with_traceback(f"Error processing index file {file_path}: {str(e)}")
            return None
    
    def clean_column_names(self, df):
        """
        Clean up column names to remove spaces and special characters.
        
        Args:
            df (pd.DataFrame): DataFrame with original column names
            
        Returns:
            pd.DataFrame: DataFrame with cleaned column names
        """
        # Create a mapping of old column names to new column names
        column_mapping = {}
        for col in df.columns:
            # Replace spaces and special characters with underscores
            new_col = re.sub(r'[^\w]', '_', col)
            # Convert to uppercase to match the format of other data
            new_col = new_col.upper()
            # Remove consecutive underscores
            new_col = re.sub(r'_+', '_', new_col)
            # Remove leading/trailing underscores
            new_col = new_col.strip('_')
            column_mapping[col] = new_col
        
        # Rename columns
        return df.rename(columns=column_mapping)
    
    def format_date_column(self, df):
        """
        Ensure DATE1 column is properly formatted as YYYY-MM-DD.
        
        Args:
            df (pd.DataFrame): DataFrame with DATE1 column
            
        Returns:
            pd.DataFrame: DataFrame with formatted DATE1 column
        """
        if 'DATE1' in df.columns:
            # Convert to datetime if it's not already
            if not pd.api.types.is_datetime64_any_dtype(df['DATE1']):
                try:
                    # Try to parse the date with various formats
                    df['DATE1'] = pd.to_datetime(df['DATE1'], errors='coerce', format='%d-%m-%Y')
                except:
                    # If specific format fails, try automatic parsing
                    df['DATE1'] = pd.to_datetime(df['DATE1'], errors='coerce')
            
            # Convert to string in YYYY-MM-DD format
            df['DATE1'] = df['DATE1'].dt.strftime('%Y-%m-%d')
        
        return df
    
    def save_processed_file(self, df, original_file_path):
        """
        Save processed dataframe to the input directory.
        
        Args:
            df (pd.DataFrame): Processed dataframe
            original_file_path (str): Path to the original file
            
        Returns:
            str: Path to the saved file, or None if saving failed
        """
        try:
            # Create input directory if it doesn't exist
            os.makedirs(self.INPUT_DIR_INDEX, exist_ok=True)
            
            # Get the filename without extension
            filename = os.path.basename(original_file_path)
            base_filename = os.path.splitext(filename)[0]
            
            # Create the output path
            # output_path = os.path.join(self.INPUT_DIR_INDEX, f"processed_{base_filename}.csv")
            
            # Save to CSV
            df.to_csv(original_file_path, index=False)
            
            logging.info(f"Saved processed file to {original_file_path}")
            return original_file_path
            
        except Exception as e:
            logging.error(f"Error saving processed file: {str(e)}")
            return None
            
    def save_symbol_files(self, combined_df):
        """
        Split the combined dataframe by symbol and save individual files.
        
        Args:
            combined_df (pd.DataFrame): Combined dataframe with all index data
            
        Returns:
            int: Number of symbol files created
        """
        try:
            # Filter out records where HIGH_PRICE, LOW_PRICE, or CLOSE_PRICE is empty, NaN, or contains '-'
            initial_count = len(combined_df)
            
            # First drop NaN values
            combined_df = combined_df.dropna(subset=['HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE'])
            
            # Then filter out records with '-' in price fields
            price_columns = ['HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE']
            for col in price_columns:
                # Check if column contains string data
                if combined_df[col].dtype == 'object':
                    # Remove rows where the price field contains '-'
                    combined_df = combined_df[~combined_df[col].astype(str).str.contains('-')]
            
            # Convert price columns to numeric, coercing errors to NaN
            for col in price_columns:
                combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')
            
            # Drop any rows where conversion to numeric resulted in NaN
            combined_df = combined_df.dropna(subset=price_columns)
            
            filtered_count = len(combined_df)
            if initial_count > filtered_count:
                logging.info(f"Filtered out {initial_count - filtered_count} records with missing or invalid price data")
            
            # Delete existing input_index directory if it exists
            if os.path.exists(self.INPUT_DIR_INDEX):
                logging.info(f"Deleting existing directory: {self.INPUT_DIR_INDEX}")
                import shutil
                shutil.rmtree(self.INPUT_DIR_INDEX)
            
            # Create fresh output directory for index data
            logging.info(f"Creating fresh directory: {self.INPUT_DIR_INDEX}")
            os.makedirs(self.INPUT_DIR_INDEX, exist_ok=True)
            
            # Get unique symbols
            symbols = combined_df['SYMBOL'].unique()
            logging.info(f"Found {len(symbols)} unique index symbols")
            
            files_created = 0
            skipped_symbols = 0
            for symbol in symbols:
                # Skip symbols containing 'Shariah'
                if 'Shariah' in symbol:
                    logging.info(f"Skipping Shariah index: {symbol}")
                    skipped_symbols += 1
                    continue
                    
                # Filter data for this symbol
                symbol_df = combined_df[combined_df['SYMBOL'] == symbol].copy()
                
                # Sort by date
                if 'DATE1' in symbol_df.columns:
                    symbol_df = symbol_df.sort_values('DATE1')
                
                # Create filename - replace spaces and special characters
                safe_symbol = re.sub(r'[^\w]', '_', symbol)
                filename = f"{safe_symbol}.csv"
                filepath = os.path.join(self.INPUT_DIR_INDEX, filename)
                
                # Save to CSV
                symbol_df.to_csv(filepath, index=False)
                logging.info(f"Saved index data for {symbol} to {filepath}")
                files_created += 1
            
            if skipped_symbols > 0:
                logging.info(f"Skipped {skipped_symbols} Shariah indices")
                
            return files_created
            
        except Exception as e:
            logging.error(f"Error saving symbol files: {str(e)}")
            return 0
    
    def _cleanup_directories(self, dirs_to_clean=None):
        """
        Clean up and recreate specified directories.
        
        Args:
            dirs_to_clean (list, optional): List of directory paths to clean up.
                                         If None, cleans all standard directories.
        
        Returns:
            float: Duration of the cleanup operation in seconds
        """
        import shutil
        import time
        
        cleanup_start_time = time.time()
        
        # If no specific directories are provided, clean all standard directories
        if dirs_to_clean is None:
            dirs_to_clean = [
                self.LOCAL_DIR_BHAVCOPY_INDEX,
                self.INPUT_DIR_INDEX,
            ]
        
        # Clean up each directory
        for directory in dirs_to_clean:
            if os.path.exists(directory):
                logging.info(f"Deleting existing directory: {directory}")
                shutil.rmtree(directory)
            
            # Recreate the directory
            os.makedirs(directory, exist_ok=True)
        
        cleanup_end_time = time.time()
        cleanup_duration = cleanup_end_time - cleanup_start_time
        logging.info(f"Created fresh directories: {', '.join(dirs_to_clean)} in {cleanup_duration:.2f} seconds")
        
        return cleanup_duration

    def download_index_files(self, start_date, end_date):
        """
        Download index bhavcopy files for the given date range.
        
        Args:
            start_date: Start date for data extraction
            end_date: End date for data extraction
            
        Returns:
            bool: True if any files were downloaded successfully, False otherwise
        """
        import time
        download_start_time = time.time()
        if start_date is None or end_date is None:
            logging.info("Skipping index bhavcopy extraction as dates are not set.")
            return False
        
        # Clean up directories before downloading
        self._cleanup_directories()
            
        current_date = start_date
        downloaded_files = 0
        
        while current_date <= end_date:
            try:
                logging.info(f"Downloading Bhavcopy Index for {current_date}...")
                full_bhavcopy_index_path = bhavcopy_index_save(current_date, self.LOCAL_DIR_BHAVCOPY_INDEX)
                logging.info(f"Downloaded Bhavcopy Index to {full_bhavcopy_index_path}...")
                downloaded_files += 1
                
                # Check if file contains error message
                if os.path.exists(full_bhavcopy_index_path):
                    with open(full_bhavcopy_index_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_content = f.read(200)  # Read more content to ensure we catch the error message
                        # Use a more general check for error messages
                        if "file you are trying to access" in file_content or "Error tokenizing data" in file_content or "<!DOCTYPE html>" in file_content:
                            logging.warning(f"Bhavcopy Index for {current_date} is not available or has invalid format. Deleting file and skipping.")
                            # Delete the invalid file
                            try:
                                os.remove(full_bhavcopy_index_path)
                                logging.info(f"Deleted invalid file: {full_bhavcopy_index_path}")
                                downloaded_files -= 1
                            except Exception as e:
                                logging.error(f"Error deleting file {full_bhavcopy_index_path}: {str(e)}")
                            current_date += timedelta(days=1)
                            continue
            except Exception as e:
                log_error_with_traceback(
                    f"Error downloading bhavcopy index for {current_date}", 
                    e, 
                    {"date": str(current_date), "local_dir": self.LOCAL_DIR_BHAVCOPY_INDEX}
                )
            
            current_date += timedelta(days=1)
        
        download_end_time = time.time()
        download_duration = download_end_time - download_start_time
        logging.info(f"Downloaded bhavcopy index files for {downloaded_files} days in {download_duration:.2f} seconds")
        
        # Save the last executed date locally (optional, for logging)
        if downloaded_files > 0:
            logging.info(f"Finished downloading up to {end_date}")
            return True
        return False
        
    def find_latest_file_date(self):
        """Find the latest file date from INPUT_DIR_INDEX in format ind_close_all_DDMMYYYY.csv
        
        Returns:
            date: The date of the latest file, or a default date if no files found
        """
        try:
            # Default date if no files are found
            default_date = date(2024, 4, 1)
            
            # Check if directory exists
            if not os.path.exists(self.INPUT_DIR_INDEX):
                logging.warning(f"INPUT_DIR_INDEX does not exist: {self.INPUT_DIR_INDEX}")
                return default_date
                
            # Find all files matching the pattern
            file_pattern = os.path.join(self.INPUT_DIR_INDEX, "ind_close_all_*.csv")
            files = glob.glob(file_pattern)
            
            if not files:
                logging.info(f"No index files found in {self.INPUT_DIR_INDEX}, using default date")
                return default_date
                
            # Extract dates from filenames
            dates = []
            for file_path in files:
                filename = os.path.basename(file_path)
                # Extract date part (DDMMYYYY) from ind_close_all_DDMMYYYY.csv
                match = re.search(r'ind_close_all_(\d{8})\.csv', filename)
                if match:
                    date_str = match.group(1)
                    try:
                        # Convert DDMMYYYY to date object
                        file_date = datetime.strptime(date_str, "%d%m%Y").date()
                        dates.append(file_date)
                    except ValueError:
                        logging.warning(f"Could not parse date from filename: {filename}")
            
            if not dates:
                logging.info("No valid dates found in filenames, using default date")
                return default_date
                
            # Find the latest date
            latest_date = max(dates)
            logging.info(f"Latest file date found: {latest_date}")
            
            # Return the day after the latest date to avoid reprocessing
            return latest_date + timedelta(days=1)
            
        except Exception as e:
            logging.error(f"Error finding latest file date: {str(e)}")
            return date(2020, 1, 1)

    def execute(self, end_date=None):
        """
        Execute the index start step.
        Download and process all index bhavcopy files.
        
        Args:
            start_date (date, optional): Start date for downloading index files. Default is April 1, 2024.
            end_date (date, optional): End date for downloading index files. Default is today.
            
        Returns:
            bool: True if execution was successful, False otherwise
        """
        try:
            logging.info("Starting IndexStartStep execution")
            
            # Create required directories (but don't delete input_index here, we'll do that later)
            # We'll keep OUTPUT_DIR_INDEX as is since it might contain important processed data
            os.makedirs(self.OUTPUT_DIR_INDEX, exist_ok=True)
            
            # Find the latest file date from INPUT_DIR_INDEX
            start_date = self.find_latest_file_date()

            # Set default dates if not provided
            if end_date is None:
                end_date = date.today()
            
            # Download new bhavcopy index files if needed
            downloaded = self.download_index_files(start_date, end_date)
            if downloaded:
                logging.info(f"Successfully downloaded new bhavcopy index files from {start_date} to {end_date}")
                
                # Check for error messages in downloaded files and delete them
                self.clean_error_files()
            else:
                logging.info(f"No new bhavcopy index files were downloaded for the period {start_date} to {end_date}")
            
            # Check if directory exists
            if not os.path.exists(self.LOCAL_DIR_BHAVCOPY_INDEX):
                logging.error(f"Directory not found: {self.LOCAL_DIR_BHAVCOPY_INDEX}")
                return False
                
            # Get all CSV files in the directory
            csv_files = glob.glob(os.path.join(self.LOCAL_DIR_BHAVCOPY_INDEX, "*.csv"))
            
            if not csv_files:
                logging.warning(f"No CSV files found in {self.LOCAL_DIR_BHAVCOPY_INDEX}")
                return False
                
            logging.info(f"Found {len(csv_files)} CSV files to process")
            
            # Initialize list to store all processed dataframes
            all_dfs = []
            
            # Process each file
            processed_files = 0
            for file_path in csv_files:
                # Process the file
                df = self.process_index_file(file_path)
                
                # Save processed file and add to list of dataframes
                if df is not None:
                    saved_path = self.save_processed_file(df, file_path)
                    if saved_path:
                        processed_files += 1
                        all_dfs.append(df)
            
            logging.info(f"Successfully processed {processed_files} out of {len(csv_files)} files")
            
            # If we have processed files, combine them and create symbol-specific files
            if all_dfs:
                # Combine all dataframes
                logging.info("Combining all processed index data")
                combined_df = pd.concat(all_dfs, ignore_index=True)
                
                # Clean up column names
                combined_df = self.clean_column_names(combined_df)
                
                # Format date column
                combined_df = self.format_date_column(combined_df)
                
                # Remove duplicates
                before_count = len(combined_df)
                combined_df = combined_df.drop_duplicates(subset=['SYMBOL', 'DATE1'], keep='last')
                after_count = len(combined_df)
                if before_count > after_count:
                    logging.info(f"Removed {before_count - after_count} duplicate records")
                
                # Save individual files for each symbol
                symbol_files = self.save_symbol_files(combined_df)
                logging.info(f"Created {symbol_files} symbol-specific files in {self.INPUT_DIR_INDEX}")
                
                return symbol_files > 0
            
            return processed_files > 0
            
        except Exception as e:
            log_error_with_traceback(f"Error in IndexStartStep execution: {str(e)}")
            return False


if __name__ == "__main__":
    # For standalone testing
    from datetime import date, timedelta
    
    # Set date range for the last 30 days
    end_date = date.today()
    
    index_step = IndexStartStep()
    success = index_step.execute(end_date)
    print(f"Execution {'successful' if success else 'failed'}")
