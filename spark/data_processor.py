#!/usr/bin/env python3
"""
GeoPulse Data Processor
Monitors data/input directory for new CSV files and processes them with PySpark
"""

import os
import time
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DateType
import psycopg2
from psycopg2.extras import execute_values

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CSVFileHandler(FileSystemEventHandler):
    """Handle new CSV files in the input directory"""
    
    def __init__(self, processor):
        self.processor = processor
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.csv'):
            logger.info(f"New CSV file detected: {event.src_path}")
            time.sleep(1)  # Wait for file to be fully written
            self.processor.process_csv_file(event.src_path)

class DataProcessor:
    """Main data processing class"""
    
    def __init__(self):
        self.spark = None
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'database': os.getenv('POSTGRES_DB', 'geopulse'),
            'user': os.getenv('POSTGRES_USER', 'geopulse_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'geopulse_password'),
            'port': 5432
        }
        self.input_dir = Path('/app/data/input')
        self.processed_dir = Path('/app/data/processed')
        
        # Create directories if they don't exist
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Spark
        self.init_spark()
        
    def init_spark(self):
        """Initialize Spark session"""
        try:
            self.spark = SparkSession.builder \
                .appName("GeoPulse Data Processor") \
                .config("spark.master", os.getenv('SPARK_MASTER_URL', 'local[*]')) \
                .config("spark.sql.adaptive.enabled", "true") \
                .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
                .getOrCreate()
            
            logger.info("Spark session initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Spark session: {e}")
            raise
            
    def get_db_connection(self):
        """Get PostgreSQL database connection"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise
            
    def validate_csv_schema(self, df):
        """Validate that CSV has required columns"""
        required_columns = {'id', 'name', 'country', 'city', 'date'}
        actual_columns = set(df.columns)
        
        if not required_columns.issubset(actual_columns):
            missing = required_columns - actual_columns
            raise ValueError(f"CSV is missing required columns: {missing}")
            
        return True
        
    def process_csv_file(self, file_path):
        """Process a single CSV file"""
        try:
            logger.info(f"Processing CSV file: {file_path}")
            
            # Read CSV with Spark
            df = self.spark.read.option("header", "true").csv(file_path)
            
            # Validate schema
            self.validate_csv_schema(df)
            
            # Data cleaning and transformation
            df_cleaned = df.select("id", "name", "country", "city", "date") \
                          .filter(df.id.isNotNull() & df.name.isNotNull() & 
                                 df.country.isNotNull() & df.city.isNotNull() & 
                                 df.date.isNotNull()) \
                          .distinct()
            
            # Convert to Pandas for database insertion
            pandas_df = df_cleaned.toPandas()
            
            if len(pandas_df) > 0:
                # Insert into PostgreSQL
                self.insert_to_database(pandas_df)
                
                # Move processed file
                processed_path = self.processed_dir / Path(file_path).name
                Path(file_path).rename(processed_path)
                
                logger.info(f"Successfully processed {len(pandas_df)} records from {file_path}")
            else:
                logger.warning(f"No valid records found in {file_path}")
                
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
            
    def insert_to_database(self, df):
        """Insert DataFrame records into PostgreSQL"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Convert DataFrame to list of tuples
            records = [tuple(row) for row in df.values]
            
            # Insert query
            insert_query = """
                INSERT INTO clients (client_id, name, country, city, date)
                VALUES %s
                ON CONFLICT (client_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    country = EXCLUDED.country,
                    city = EXCLUDED.city,
                    date = EXCLUDED.date,
                    updated_at = CURRENT_TIMESTAMP
            """
            
            execute_values(cursor, insert_query, records, template=None, page_size=1000)
            conn.commit()
            
            logger.info(f"Inserted {len(records)} records into database")
            
        except Exception as e:
            logger.error(f"Error inserting data into database: {e}")
            if conn:
                conn.rollback()
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
    def process_existing_files(self):
        """Process any existing CSV files in input directory"""
        if self.input_dir.exists():
            csv_files = list(self.input_dir.glob('*.csv'))
            if csv_files:
                logger.info(f"Found {len(csv_files)} existing CSV files to process")
                for csv_file in csv_files:
                    self.process_csv_file(str(csv_file))
                    
    def start_monitoring(self):
        """Start monitoring the input directory for new files"""
        logger.info(f"Starting to monitor directory: {self.input_dir}")
        
        # Process existing files first
        self.process_existing_files()
        
        # Set up file system watcher
        event_handler = CSVFileHandler(self)
        observer = Observer()
        observer.schedule(event_handler, str(self.input_dir), recursive=False)
        observer.start()
        
        try:
            while True:
                time.sleep(10)
                logger.debug("Monitoring for new CSV files...")
        except KeyboardInterrupt:
            observer.stop()
            logger.info("Stopping file monitor...")
        
        observer.join()
        
        if self.spark:
            self.spark.stop()

if __name__ == "__main__":
    processor = DataProcessor()
    processor.start_monitoring()