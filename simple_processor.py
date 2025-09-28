#!/usr/bin/env python3
"""
Simple CSV Processor for GeoPulse
Monitors data/input directory and processes CSV files automatically
"""

import os
import time
import pandas as pd
import psycopg2
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'postgres'),
    'database': os.getenv('POSTGRES_DB', 'geopulse'),
    'user': os.getenv('POSTGRES_USER', 'geopulse_user'),
    'password': os.getenv('POSTGRES_PASSWORD', 'geopulse_password'),
    'port': 5432
}

# Paths
INPUT_DIR = Path("/app/data/input")
PROCESSED_DIR = Path("/app/data/processed")

def wait_for_database():
    """Wait for database to be ready"""
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            logger.info("✅ Database connection successful!")
            return True
        except Exception as e:
            logger.info(f"⏳ Waiting for database... (attempt {attempt + 1}/{max_attempts})")
            time.sleep(2)
    
    logger.error("❌ Database connection failed after max attempts")
    return False

def connect_to_db():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def process_csv_file(file_path):
    """Process a single CSV file"""
    try:
        logger.info(f"📄 Processing file: {file_path}")
        
        # Read CSV file
        df = pd.read_csv(file_path)
        logger.info(f"📊 Found {len(df)} rows in CSV")
        
        # Validate columns (flexible column names)
        df.columns = df.columns.str.lower().str.strip()
        required_cols = ['name', 'country', 'city', 'date']
        
        # Check for variations in column names
        col_mapping = {}
        for req_col in required_cols:
            found = False
            for col in df.columns:
                if req_col in col or col in req_col:
                    col_mapping[req_col] = col
                    found = True
                    break
            if not found:
                logger.error(f"❌ Missing required column: {req_col}")
                logger.info(f"Available columns: {list(df.columns)}")
                return False
        
        # Connect to database
        conn = connect_to_db()
        if not conn:
            return False
        
        cursor = conn.cursor()
        
        # Insert data
        success_count = 0
        for _, row in df.iterrows():
            try:
                # Parse date (handle different formats)
                date_str = str(row[col_mapping['date']])
                try:
                    # Try common date formats
                    parsed_date = pd.to_datetime(date_str, format='%m/%d/%Y').date()
                except:
                    try:
                        parsed_date = pd.to_datetime(date_str).date()
                    except:
                        logger.warning(f"⚠️ Could not parse date: {date_str}, using today")
                        parsed_date = pd.Timestamp.now().date()
                
                cursor.execute("""
                    INSERT INTO clients (client_id, name, country, city, date) 
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (client_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        country = EXCLUDED.country,
                        city = EXCLUDED.city,
                        date = EXCLUDED.date,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    str(row.get('id', f"auto_{success_count + 1}")),
                    str(row[col_mapping['name']]).strip(),
                    str(row[col_mapping['country']]).strip(),
                    str(row[col_mapping['city']]).strip(),
                    parsed_date
                ))
                success_count += 1
            except Exception as e:
                logger.warning(f"⚠️ Failed to insert row: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ Successfully processed {success_count} records from {file_path.name}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error processing {file_path}: {e}")
        return False

def move_processed_file(file_path):
    """Move processed file to processed directory"""
    try:
        PROCESSED_DIR.mkdir(exist_ok=True)
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{timestamp}_{file_path.name}"
        new_path = PROCESSED_DIR / new_name
        file_path.rename(new_path)
        logger.info(f"📁 Moved {file_path.name} to processed/{new_name}")
    except Exception as e:
        logger.error(f"❌ Failed to move file {file_path}: {e}")

def monitor_input_directory():
    """Monitor input directory for new CSV files"""
    logger.info("👀 Starting CSV file monitor...")
    INPUT_DIR.mkdir(exist_ok=True)
    PROCESSED_DIR.mkdir(exist_ok=True)
    
    logger.info(f"📂 Monitoring directory: {INPUT_DIR}")
    logger.info("✨ Drop CSV files here for automatic processing!")
    
    while True:
        try:
            # Look for CSV files
            csv_files = list(INPUT_DIR.glob("*.csv"))
            
            if csv_files:
                logger.info(f"🔍 Found {len(csv_files)} CSV files to process")
                
                for csv_file in csv_files:
                    if process_csv_file(csv_file):
                        move_processed_file(csv_file)
                    else:
                        logger.error(f"❌ Failed to process {csv_file.name}")
            
            # Wait before checking again
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            logger.info("🛑 Stopping CSV processor...")
            break
        except Exception as e:
            logger.error(f"❌ Error in monitor loop: {e}")
            time.sleep(30)  # Wait longer if there's an error

if __name__ == "__main__":
    logger.info("🚀 GeoPulse CSV Processor Starting...")
    
    # Wait for database to be ready
    if not wait_for_database():
        exit(1)
    
    # Start monitoring
    monitor_input_directory()