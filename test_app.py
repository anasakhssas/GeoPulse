#!/usr/bin/env python3
"""
Quick test script to verify GeoPulse database connection and data
"""
import psycopg2
import pandas as pd

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'geopulse',
    'user': 'geopulse_user',
    'password': 'geopulse_password'
}

def test_connection():
    """Test database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Database connection successful!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def test_data(conn):
    """Test data retrieval"""
    cursor = conn.cursor()
    
    # Test clients table
    print("\n📊 Testing clients table:")
    cursor.execute("SELECT COUNT(*) FROM clients")
    count = cursor.fetchone()[0]
    print(f"   Total clients: {count}")
    
    # Test country stats
    print("\n🌍 Country Statistics:")
    cursor.execute("SELECT * FROM country_stats ORDER BY client_count DESC LIMIT 5")
    results = cursor.fetchall()
    for country, client_count, city_count in results:
        print(f"   {country}: {client_count} clients, {city_count} cities")
    
    # Test city stats
    print("\n🏙️ City Statistics (Top 5):")
    cursor.execute("SELECT country, city, client_count FROM city_stats ORDER BY client_count DESC LIMIT 5")
    results = cursor.fetchall()
    for country, city, client_count in results:
        print(f"   {city}, {country}: {client_count} clients")
    
    cursor.close()

def main():
    print("🧪 GeoPulse Database Test")
    print("=" * 30)
    
    # Test connection
    conn = test_connection()
    if conn:
        test_data(conn)
        conn.close()
        
        print("\n✅ All tests passed!")
        print("\n🎯 Next Steps:")
        print("   1. Dashboard URL: http://localhost:8501 (when ready)")
        print("   2. Add CSV files to data/input/ for processing")
        print("   3. Check Spark UI: http://localhost:8080 (when available)")
    else:
        print("\n❌ Tests failed - check Docker containers")

if __name__ == "__main__":
    main()