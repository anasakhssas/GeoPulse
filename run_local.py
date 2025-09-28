#!/usr/bin/env python3
"""
Local GeoPulse Dashboard Test
Run this locally to test without Docker
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    packages = ['streamlit', 'pandas', 'plotly']
    for package in packages:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    print("🚀 Starting GeoPulse Local Test")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("streamlit_app/simple_dashboard.py").exists():
        print("❌ Please run this from the geopulse project root directory")
        return
    
    # Check if data directory exists
    data_dir = Path("data/input")
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
        print("📁 Created data/input directory")
    
    # Check for CSV files
    csv_files = list(data_dir.glob("*.csv"))
    print(f"📊 Found {len(csv_files)} CSV files")
    
    if not csv_files:
        print("⚠️  No CSV files found. Creating sample data...")
        sample_data = """name,country,city,date
John Doe,United States,New York,2024-01-15
Jane Smith,United Kingdom,London,2024-01-16
Pierre Dubois,France,Paris,2024-01-17
Maria Garcia,Spain,Madrid,2024-01-18
Giovanni Rossi,Italy,Rome,2024-01-19"""
        
        with open(data_dir / "sample.csv", "w") as f:
            f.write(sample_data)
        print("✅ Created sample.csv")
    
    # Try to install requirements
    try:
        print("📦 Installing requirements...")
        install_requirements()
    except Exception as e:
        print(f"⚠️  Could not install packages: {e}")
        print("Please run: pip install streamlit pandas plotly")
    
    print("\n🌍 Starting GeoPulse Dashboard...")
    print("🎯 Dashboard will be available at: http://localhost:8501")
    print("🔄 Auto-refresh is enabled - add CSV files to data/input/")
    print("\n" + "=" * 40)
    
    # Change to streamlit_app directory and run
    os.chdir("streamlit_app")
    subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'simple_dashboard.py'])

if __name__ == "__main__":
    main()