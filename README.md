# GeoPulse - Real-time Client Analytics Pipeline

GeoPulse is an end-to-end data pipeline that automatically processes client data from CSV files and provides real-time analytics through an interactive dashboard.

## 🚀 Features

- **Dockerized Infrastructure**: All components run in isolated Docker containers
- **Automated Data Ingestion**: PySpark monitors input directory for new CSV files
- **Real-time Processing**: Distributed data processing with Apache Spark
- **Interactive Dashboard**: Streamlit-based visualization with two main views:
  - Global client distribution by countries
  - City-level distribution with country filtering
- **Data Persistence**: PostgreSQL database for reliable data storage
- **Scalable Architecture**: Easy to scale with additional Spark workers

## 📊 Data Schema

CSV files should contain the following columns:
- `id`: Client identifier
- `name`: Client name
- `country`: Client's country
- `city`: Client's city
- `date`: Registration/entry date (YYYY-MM-DD format)

## 🏗️ Architecture

```
CSV Files → PySpark Processing → PostgreSQL → Streamlit Dashboard
    ↓              ↓                  ↓             ↓
data/input → Distributed ETL → Relational DB → Web Interface
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB of available RAM

### 1. Clone and Setup
```bash
cd geopulse
```

### 2. Start the Pipeline
```bash
docker-compose up -d
```

### 3. Access the Dashboard
Open your browser and navigate to: `http://localhost:8501`

### 4. Add Data
Place CSV files in the `data/input/` directory. They will be automatically processed.

## 📁 Project Structure

```
geopulse/
├── docker-compose.yml          # Container orchestration
├── .env                       # Environment configuration
├── data/
│   ├── input/                 # CSV files for processing
│   └── processed/             # Successfully processed files
├── spark/
│   ├── Dockerfile             # Spark cluster image
│   ├── Dockerfile.processor   # Data processor image
│   └── data_processor.py      # Main processing logic
├── streamlit_app/
│   ├── Dockerfile
│   ├── main.py               # Dashboard main application
│   ├── database.py           # Database connection manager
│   └── requirements.txt
└── postgres/
    └── init.sql              # Database initialization
```

## 🔧 Services

### PostgreSQL Database
- **Port**: 5432
- **Database**: geopulse
- **User**: geopulse_user
- **Password**: geopulse_password

### Spark Cluster
- **Master UI**: http://localhost:8080
- **Master Port**: 7077
- **Workers**: 1 (configurable)

### Streamlit Dashboard
- **URL**: http://localhost:8501
- **Features**:
  - Country distribution world map
  - Top countries bar chart
  - City-level filtering
  - Real-time data refresh

### Data Processor
- Monitors `data/input/` directory
- Validates CSV schema
- Cleans and transforms data
- Loads data into PostgreSQL
- Moves processed files to `data/processed/`

## 📈 Dashboard Features

### Country Distribution Page
- Interactive world map showing client distribution
- Top 10 countries bar chart
- Complete country statistics table

### City Distribution Page
- Country filter dropdown
- Horizontal bar chart for cities
- Summary metrics
- Detailed city statistics table

## 🛠️ Configuration

### Environment Variables
Edit `.env` file to customize:
- Database credentials
- Spark configuration
- Processing intervals

### Scaling
Add more Spark workers in `docker-compose.yml`:
```yaml
spark-worker-2:
  build: 
    context: ./spark
    dockerfile: Dockerfile
  environment:
    - SPARK_MODE=worker
    - SPARK_MASTER_URL=spark://spark-master:7077
  # ... other configurations
```

## 📝 Sample Data

A sample CSV file is included in `data/input/sample_clients.csv` with 10 records from different countries.

## 🔍 Monitoring

- **Spark UI**: http://localhost:8080 - Monitor Spark jobs and cluster status
- **Database**: Connect to PostgreSQL on port 5432 for direct data access
- **Logs**: Use `docker-compose logs [service-name]` to view logs

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 5432, 8080, 8501, and 7077 are available
2. **Memory Issues**: Increase Docker memory limit to at least 4GB
3. **File Permissions**: Ensure the `data/` directory is writable

### Useful Commands

```bash
# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs streamlit

# Restart services
docker-compose restart

# Scale Spark workers
docker-compose up -d --scale spark-worker=2

# Access database directly
docker exec -it geopulse_postgres psql -U geopulse_user -d geopulse
```

## 🔄 Data Processing Flow

1. **File Detection**: Watchdog monitors `data/input/` for new CSV files
2. **Validation**: PySpark validates CSV schema and data quality
3. **Transformation**: Data cleaning and standardization
4. **Loading**: Insert/update records in PostgreSQL
5. **Archival**: Move processed files to `data/processed/`
6. **Visualization**: Streamlit dashboard refreshes every 30 seconds

## 🎯 Use Cases

- **Customer Analytics**: Analyze client geographical distribution
- **Market Research**: Understand regional market penetration
- **Business Intelligence**: Real-time insights into customer base
- **Data Pipeline**: Template for CSV-based ETL processes

## 📊 Performance

- **Processing**: Can handle thousands of records per CSV file
- **Scalability**: Horizontal scaling with additional Spark workers
- **Real-time**: Near real-time dashboard updates (30-second refresh)
- **Storage**: Efficient PostgreSQL indexing for fast queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the troubleshooting section
2. Review Docker logs
3. Verify CSV file format
4. Ensure all ports are available

---

**GeoPulse** - Transform your client data into actionable insights! 🌍📊