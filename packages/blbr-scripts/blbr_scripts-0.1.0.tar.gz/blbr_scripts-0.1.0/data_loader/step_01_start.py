import os
import logging
import glob
import re
from datetime import date, timedelta, datetime
import pandas as pd
from jugaad_data.nse import full_bhavcopy_save
from dotenv import load_dotenv

from .utils import log_error_with_traceback, setup_logging


class StartStep:
    def __init__(self):
        """
        Initialize the start step.
        """
        # Load environment variables
        load_dotenv()
        self.LOCAL_DIR = os.getenv("LOCAL_DIR")
        self.LOCAL_DIR_BHAVCOPY = os.getenv("LOCAL_DIR_BHAVCOPY")
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR")
        self.INPUT_DIR = os.getenv("INPUT_DIR")
        setup_logging()

        
    def execute(self):
        """
        Determine the date range, download new bhavcopy files, read existing files,
        and process them into symbol-specific files.
        
        Returns:
            tuple: (start_date, end_date, all_data)
        """
        import time
        overall_start_time = time.time()
        logging.info("Starting execution of StartStep")

        start_date = date(2024, 4, 1)  # Default to April 1, 2024
        end_date = date.today()

        # Download new bhavcopy files if needed
        downloaded_data = self.download_bhavcopy_files(start_date, end_date)
        if downloaded_data:
            logging.info(f"Successfully downloaded new bhavcopy files from {start_date} to {end_date}")
        else:
            logging.info(f"No new bhavcopy files were downloaded for the period {start_date} to {end_date}")
        
        # Read all existing bhavcopy files
        logging.info("Reading all existing bhavcopy files...")
        read_start_time = time.time()
        all_data = self.read_bhavcopy_files()
        read_end_time = time.time()
        read_duration = read_end_time - read_start_time
        logging.info(f"Read {len(all_data)} bhavcopy files in {read_duration:.2f} seconds")
        
        if all_data:
            # Process the data and create symbol-specific files
            logging.info("Processing bhavcopy data and creating symbol-specific files...")
            processing_start_time = time.time()
            combined_df = self.process_bhavcopy_data(all_data)
            processing_end_time = time.time()
            processing_duration = processing_end_time - processing_start_time
            logging.info(f"Successfully processed {len(combined_df)} records from {len(all_data)} bhavcopy files in {processing_duration:.2f} seconds")
            
            # Return the processed data
            overall_end_time = time.time()
            overall_duration = overall_end_time - overall_start_time
            logging.info(f"StartStep execution completed in {overall_duration:.2f} seconds")
            return start_date, end_date, all_data
        else:
            logging.info("No bhavcopy files found to process.")
            overall_end_time = time.time()
            overall_duration = overall_end_time - overall_start_time
            logging.info(f"StartStep execution completed in {overall_duration:.2f} seconds")
            return None, None, []

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
            dirs_to_clean = []
            # Only add directories that are not None
            if self.LOCAL_DIR_BHAVCOPY:
                dirs_to_clean.append(self.LOCAL_DIR_BHAVCOPY)
            else:
                logging.warning("LOCAL_DIR_BHAVCOPY environment variable is not set")
                
            if self.INPUT_DIR:
                dirs_to_clean.append(self.INPUT_DIR)
            else:
                logging.warning("INPUT_DIR environment variable is not set")
                
            if self.OUTPUT_DIR:
                dirs_to_clean.append(self.OUTPUT_DIR)
            else:
                logging.warning("OUTPUT_DIR environment variable is not set")
        
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
    
    def extract_date_from_filename(self, filename):
        """
        Extract date from bhavcopy filename.
        
        Args:
            filename: Bhavcopy filename
            
        Returns:
            str: Extracted date in YYYY-MM-DD format or None if extraction fails
        """
        try:
            # Extract date part from the filename
            # Expected format: sec_bhavdata_full_01Oct2024bhav.csv
            match = re.search(r'full_(\d{2}[A-Za-z]{3}\d{4})bhav', filename)
            if match:
                date_str = match.group(1)
                date_obj = datetime.strptime(date_str, '%d%b%Y')
                return date_obj.strftime('%Y-%m-%d')
            
            # Try alternative formats if the first pattern doesn't match
            alt_match = re.search(r'(\d{2}[A-Za-z]{3}\d{4})', filename)
            if alt_match:
                date_str = alt_match.group(1)
                date_obj = datetime.strptime(date_str, '%d%b%Y')
                return date_obj.strftime('%Y-%m-%d')
                
            # If no pattern matches, use file modification time as fallback
            file_path = os.path.join(self.LOCAL_DIR_BHAVCOPY, filename)
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                date_obj = datetime.fromtimestamp(mod_time)
                logging.info(f"Using file modification date for {filename}: {date_obj.strftime('%Y-%m-%d')}")
                return date_obj.strftime('%Y-%m-%d')
            
            raise ValueError(f"Date pattern not found in filename {filename}")
        except Exception as e:
            logging.warning(f"Could not extract date from filename {filename}: {str(e)}")
            # Return today's date as a last resort
            return datetime.now().strftime('%Y-%m-%d')
    
    def read_bhavcopy_files(self):
        """
        Read all bhavcopy CSV files from the bhavcopy directory.
        
        Returns:
            list: List of DataFrames with bhavcopy data
        """
        import time
        read_start_time = time.time()
        
        all_data = []
        
        # Find all CSV files in the bhavcopy directory
        csv_files = glob.glob(os.path.join(self.LOCAL_DIR_BHAVCOPY, "*.csv"))
        bhavcopy_files = csv_files
        logging.info(f"Found {len(bhavcopy_files)} bhavcopy files to process")
        
        processing_start_time = time.time()
        total_records = 0
        for file_path in bhavcopy_files:
            try:
                logging.info(f"Reading bhavcopy file: {file_path}")
                try:
                    # First try with standard settings
                    df = pd.read_csv(file_path)
                except Exception as e:
                    try:
                        # Try with C engine and error handling
                        logging.warning(f"Retrying file {file_path} with C engine and error handling")
                        df = pd.read_csv(
                            file_path,
                            on_bad_lines='skip',    # Skip bad lines
                            encoding='utf-8',       # Explicitly set encoding
                            low_memory=False        # Avoid dtype guessing on chunks
                        )
                    except Exception as e2:
                        try:
                            # Try with Python engine as last resort
                            logging.warning(f"Retrying file {file_path} with Python engine")
                            df = pd.read_csv(
                                file_path,
                                on_bad_lines='skip',    # Skip bad lines
                                delimiter=None,         # Try to infer delimiter
                                engine='python',        # Use the python engine which is more forgiving
                                encoding='utf-8'        # Explicitly set encoding
                            )
                        except Exception as e3:
                            # If all attempts fail, try to read line by line
                            logging.warning(f"Attempting to read {file_path} line by line")
                            try:
                                # Read the file manually, line by line
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    # Read the header line
                                    header = f.readline().strip().split(',')
                                    # Initialize data dictionary
                                    data = {col: [] for col in header}
                                    # Read data lines
                                    for line in f:
                                        try:
                                            values = line.strip().split(',')
                                            # Only process lines with correct number of fields
                                            if len(values) == len(header):
                                                for i, col in enumerate(header):
                                                    data[col].append(values[i])
                                        except Exception:
                                            # Skip problematic lines
                                            pass
                                # Create DataFrame from collected data
                                df = pd.DataFrame(data)
                            except Exception as e4:
                                # If all methods fail, log and re-raise
                                log_error_with_traceback(
                                    f"All methods failed to read bhavcopy file {file_path}", 
                                    e4, 
                                    {"file_path": file_path, "original_errors": [str(e), str(e2), str(e3)]}
                                )
                                raise
                
                # Process the DataFrame
                df.columns = df.columns.str.strip()
                if "SYMBOL" in df.columns:
                    df["SYMBOL"] = df["SYMBOL"].str.upper()
                
                # Try to extract date from filename if CREATION_DATE is not present
                if "CREATION_DATE" not in df.columns:
                    try:
                        date_str = self.extract_date_from_filename(os.path.basename(file_path))
                        df["CREATION_DATE"] = pd.to_datetime(date_str)
                    except Exception as e:
                        logging.warning(f"Could not extract date from filename {file_path}: {str(e)}")
                        # Use file modification time as fallback
                        file_mtime = os.path.getmtime(file_path)
                        df["CREATION_DATE"] = pd.to_datetime(file_mtime, unit='s')
                
                all_data.append(df)
                total_records += len(df)
                logging.info(f"Processed file {file_path}, found {len(df)} records")
                
            except Exception as e:
                log_error_with_traceback(
                    f"Error reading bhavcopy file {file_path}", 
                    e, 
                    {"file_path": file_path}
                )
        
        processing_end_time = time.time()
        processing_duration = processing_end_time - processing_start_time
        logging.info(f"Processed {len(all_data)} bhavcopy files with {total_records} records in {processing_duration:.2f} seconds")
        return all_data
    
    def process_bhavcopy_data(self, all_data):
        """
        Process bhavcopy data and write output files specific to each symbol.
        Join with market capitalization and MTF approved securities data.
        
        Args:
            all_data: List of DataFrames with bhavcopy data
            
        Returns:
            pandas.DataFrame: Combined and processed DataFrame with additional columns
        """
        import time
        process_start_time = time.time()
        if not all_data:
            logging.info("No bhavcopy data to process")
            return None
            
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Clean up column names to remove any spaces or special characters
        combined_df.columns = [col.strip() for col in combined_df.columns]
        
        if "DATE1" in combined_df.columns:
            # First strip any whitespace
            combined_df["DATE1"] = combined_df["DATE1"].str.strip()
            
            # Convert from DD-MMM-YYYY format to YYYY-MM-DD format
            combined_df["DATE1"] = pd.to_datetime(combined_df["DATE1"], format="%d-%b-%Y").dt.strftime("%Y-%m-%d")
        
        combined_df = combined_df.sort_values(by="CREATION_DATE", ascending=True)
        
        # Explicitly select only the columns we want to keep to avoid any unnamed columns
        columns_to_keep = [col for col in combined_df.columns if col and not col.startswith('Unnamed:')]
        combined_df = combined_df[columns_to_keep]

        # Trim spaces from header column names and remove any HTML content
        combined_df.columns = [col.split('<')[0].strip() for col in combined_df.columns]

        # Filter SERIES based on required values
        valid_series = ["EQ", "BE", "BZ", "SM", "ST", "SO", "SZ"]
        series_pattern = "^(E)"  # Matches any SERIES starting with E

        if "SERIES" in combined_df.columns:
            combined_df["SERIES"] = combined_df["SERIES"].str.strip()
            combined_df = combined_df[
                combined_df["SERIES"].isin(valid_series) | combined_df["SERIES"].str.match(series_pattern,
                                                                                         na=False)]
            logging.info("Filtered SERIES to include EQ, BE, BZ, SM, ST, SO, and those starting with E or X")

        # Define columns to remove and ensure they exist before dropping
        columns_to_remove = {"PREV_CLOSE", "LAST_PRICE", "AVG_PRICE", "NO_OF_TRADES", "DELIV_QTY"}
        existing_columns = set(combined_df.columns)
        columns_to_drop = list(columns_to_remove.intersection(existing_columns))

        if columns_to_drop:
            combined_df.drop(columns=columns_to_drop, inplace=True)
            logging.info(f"Removed columns: {columns_to_drop}")

        # Ensure DATE1 is properly formatted and remove duplicates
        if "DATE1" in combined_df.columns:
            combined_df["DATE1"] = combined_df["DATE1"].astype(str)
            combined_df.drop_duplicates(subset=["SYMBOL", "DATE1"], keep="first", inplace=True)
        
           
        # Load instrument_security_id data
        try:
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            security_id_file = os.path.join(project_dir, "data", "static_data_db.instrument_security_id.csv")
            logging.info(f"Loading instrument security ID data from {security_id_file}")
            security_id_df = pd.read_csv(security_id_file, dtype={'BSECODE': str})
            
            # Rename symbol to SYMBOL for joining
            # security_id_df = security_id_df.rename(columns={"symbol": "SYMBOL"})
            
            # Join with instrument_security_id data (left join)
            logging.info("Joining with instrument security ID data")
            combined_df = pd.merge(
                combined_df,
                security_id_df[["SYMBOL", "BSECODE","INDUSTRY", "COMPANY_NAME", "MARKETCAP"]],
                on="SYMBOL",
                how="left"
            )
            logging.info(f"Added security ID data: {len(security_id_df)} records processed")
        except Exception as e:
            logging.error(f"Error loading instrument security ID data: {str(e)}")
    

        # Load MTF approved securities data
        try:
            # Use project directory path instead of LOCAL_DIR
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            mtf_file = os.path.join(project_dir, "data", "static_data_db.mtf_approved_securities.csv")
            logging.info(f"Loading MTF approved securities data from {mtf_file}")
            mtf_df = pd.read_csv(mtf_file)
            
            # Rename TRADINGSYMBOL to SYMBOL for joining
            mtf_df = mtf_df.rename(columns={"TRADINGSYMBOL": "SYMBOL"})
            
            # Join with MTF approved securities data (left join)
            logging.info("Joining with MTF approved securities data")
            combined_df = pd.merge(
                combined_df,
                mtf_df[["SYMBOL", "CATEGORY", "MARGIN", "LEVERAGE"]],
                on="SYMBOL",
                how="left"
            )
            
            # Add MTF flag based on match with SYMBOL
            combined_df["MTF"] = "N"  # Default value is N
            combined_df.loc[combined_df["SYMBOL"].isin(mtf_df["SYMBOL"]), "MTF"] = "Y"
            
            # Fill NaN values to prevent extra commas in CSV
            combined_df["CATEGORY"] = combined_df["CATEGORY"].fillna("")
            combined_df["MARGIN"] = combined_df["MARGIN"].fillna(0)
            combined_df["LEVERAGE"] = combined_df["LEVERAGE"].fillna(0)
            
            logging.info(f"Added CATEGORY, MARGIN, LEVERAGE columns and MTF flag to {len(combined_df)} records")
        except Exception as e:
            log_error_with_traceback(
                "Error loading or joining MTF approved securities data",
                e,
                {"file": mtf_file if 'mtf_file' in locals() else "unknown"}
            )
            # Add empty columns if the join fails
            combined_df["CATEGORY"] = ""
            combined_df["MARGIN"] = 0
            combined_df["LEVERAGE"] = 0
            combined_df["MTF"] = "N"  # Default to N if joining fails
            logging.warning("Added empty CATEGORY, MARGIN, LEVERAGE columns and default MTF flag due to data loading error")
            
        # Clear the contents of INPUT_DIR without deleting the directory itself
        import shutil
        if os.path.exists(self.INPUT_DIR):
            shutil.rmtree(self.INPUT_DIR)

        # Create INPUT_DIR if it doesn't exist
        logging.info(f"Creating INPUT_DIR: {self.INPUT_DIR}")
        os.makedirs(self.INPUT_DIR, exist_ok=True)
        
        # Get unique symbols
        unique_symbols = combined_df["SYMBOL"].unique()
        logging.info(f"Processing {len(unique_symbols)} unique symbols")
        
        # Create a file for each symbol
        for symbol in unique_symbols:
            try:
                # Filter data for this symbol
                symbol_df = combined_df[combined_df["SYMBOL"] == symbol].sort_values("CREATION_DATE")
                
                if not symbol_df.empty:
                    # Clean column headers to remove any HTML content
                    clean_columns = [col.split('<')[0].strip() for col in symbol_df.columns]
                    symbol_df.columns = clean_columns
                    
                    # Create symbol-specific file in INPUT_DIR
                    symbol_file = os.path.join(self.INPUT_DIR, f"{symbol}.csv")
                    
                    # Clean up the DataFrame before saving
                    # 1. Remove any unnamed columns
                    cols_to_drop = [col for col in symbol_df.columns if 'Unnamed' in str(col)]
                    if cols_to_drop:
                        symbol_df = symbol_df.drop(columns=cols_to_drop)
                        logging.info(f"Dropped unnamed columns: {cols_to_drop}")
                    
                    # 2. Ensure column names are clean and unique
                    symbol_df.columns = [col.strip() for col in symbol_df.columns]
                    symbol_df.columns = pd.Series(symbol_df.columns).drop_duplicates(keep='first').tolist()
                    
                    # 3. Fill NaN values appropriately
                    symbol_df = symbol_df.fillna(value={
                        'MARKETCAP': 0,
                        'CATEGORY': '',
                        'MARGIN': 0,
                        'LEVERAGE': 0
                    })
                    
                    # 4. Explicitly select only the columns we want to keep
                    valid_columns = [col for col in symbol_df.columns if col and not col.startswith('Unnamed:')]
                    symbol_df = symbol_df[valid_columns]
                    
                    # 5. Write to CSV using a more robust approach
                    # First convert to records and then manually write the CSV to have full control
                    with open(symbol_file, 'w', newline='') as f:
                        # Write header
                        f.write(','.join(symbol_df.columns) + '\n')
                        
                        # Write data rows
                        for _, row in symbol_df.iterrows():
                            values = []
                            for col in symbol_df.columns:
                                val = row[col]
                                if pd.isna(val):
                                    values.append('')
                                elif isinstance(val, (int, float)):
                                    values.append(str(val))
                                else:
                                    values.append(str(val))
                            f.write(','.join(values) + '\n')
                    logging.info(f"Saved {len(symbol_df)} records for symbol {symbol} to {symbol_file}")
            except Exception as e:
                log_error_with_traceback(
                    f"Error processing symbol {symbol}", 
                    e, 
                    {"symbol": symbol, "record_count": len(symbol_df) if 'symbol_df' in locals() else 0}
                )
        
        logging.info(f"Successfully created symbol-specific files in {self.INPUT_DIR}")
        return combined_df
        
    def download_bhavcopy_files(self, start_date, end_date):
        """
        Download Bhavcopy files for the given date range.
        
        Args:
            start_date: Start date for data extraction
            end_date: End date for data extraction
            
        Returns:
            list: List of DataFrames with downloaded bhavcopy data
        """
        import time
        download_start_time = time.time()
        if start_date is None or end_date is None:
            logging.info("Skipping bhavcopy extraction as dates are not set.")
            return []
        
        # Clean up directories before downloading
        self._cleanup_directories()
            
        current_date = start_date
        all_data = []
        
        while current_date <= end_date:
            try:
                logging.info(f"Downloading Bhavcopy for {current_date}...")
                full_bhavcopy_path = full_bhavcopy_save(current_date, self.LOCAL_DIR_BHAVCOPY)
                logging.info(f"Downloaded Bhavcopy to {full_bhavcopy_path}...")

                # Check if file contains error message
                with open(full_bhavcopy_path, 'r', encoding='utf-8', errors='ignore') as f:
                    file_content = f.read(200)  # Read more content to ensure we catch the error message
                    # Use a more general check for error messages
                    if "file you are trying to access" in file_content or "Error tokenizing data" in file_content or "<!DOCTYPE html>" in file_content:
                        logging.warning(f"Bhavcopy for {current_date} is not available or has invalid format. Deleting file and skipping.")
                        # Delete the invalid file
                        try:
                            os.remove(full_bhavcopy_path)
                            logging.info(f"Deleted invalid file: {full_bhavcopy_path}")
                        except Exception as e:
                            logging.error(f"Error deleting file {full_bhavcopy_path}: {str(e)}")
                        current_date += timedelta(days=1)
                        continue

                # Trim spaces from header columns
                try:
                    df = pd.read_csv(full_bhavcopy_path)
                    df.columns = df.columns.str.strip()
                    df["SYMBOL"] = df["SYMBOL"].str.upper()
                    df["CREATION_DATE"] = pd.to_datetime(current_date)
                    all_data.append(df)
                except Exception as e:
                    log_error_with_traceback(
                        f"Error processing bhavcopy for {current_date}",
                        e,
                        {"date": str(current_date), "file_path": full_bhavcopy_path}
                    )
                
            except Exception as e:
                log_error_with_traceback(
                    f"Error downloading bhavcopy for {current_date}", 
                    e, 
                    {"date": str(current_date), "local_dir": self.LOCAL_DIR_BHAVCOPY}
                )
            
            current_date += timedelta(days=1)
        
        download_end_time = time.time()
        download_duration = download_end_time - download_start_time
        logging.info(f"Downloaded bhavcopy files for {len(all_data)} days in {download_duration:.2f} seconds")
        
        # Save the last executed date locally (optional, for logging)
        if all_data:
            logging.info(f"Finished downloading up to {end_date}")
        return all_data
    



def main():
    """Run the start step independently."""
    step = StartStep()
    start_date, end_date, all_data = step.execute()
    
    if start_date is not None:
        logging.info(f"Successfully determined date range: {start_date} to {end_date}")
        logging.info(f"Downloaded bhavcopy files to {step.LOCAL_DIR_BHAVCOPY}")
    else:
        logging.info("No new data to download or today's data already processed.")
    
    logging.info("Start step completed successfully.")
    return True


if __name__ == "__main__":
    main()
