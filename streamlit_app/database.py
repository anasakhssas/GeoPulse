"""
Database Manager for GeoPulse Dashboard
"""

import os
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Handle all database operations for the dashboard"""
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'database': os.getenv('POSTGRES_DB', 'geopulse'),
            'user': os.getenv('POSTGRES_USER', 'geopulse_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'geopulse_password'),
            'port': 5432
        }
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def get_all_clients(self):
        """Get all clients data"""
        query = """
        SELECT client_id, name, country, city, date, created_at
        FROM clients
        ORDER BY created_at DESC
        """
        return self._execute_query(query)
    
    def get_country_stats(self):
        """Get country statistics"""
        query = """
        SELECT * FROM country_stats
        ORDER BY client_count DESC
        """
        return self._execute_query(query)
    
    def get_city_stats(self):
        """Get city statistics"""
        query = """
        SELECT * FROM city_stats
        ORDER BY country, client_count DESC
        """
        return self._execute_query(query)
    
    def get_recent_activity(self, days=7):
        """Get recent activity data"""
        query = """
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as new_clients
        FROM clients 
        WHERE created_at >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        """
        return self._execute_query(query, (days,))
    
    def _execute_query(self, query, params=None):
        """Execute a query and return DataFrame"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Convert to DataFrame
            df = pd.DataFrame([dict(row) for row in results])
            
            cursor.close()
            conn.close()
            
            return df
            
        except Exception as e:
            logger.error(f"Query execution error: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error