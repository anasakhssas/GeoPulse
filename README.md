# GeoPulse - Real-time Client Analytics Dashboard

GeoPulse is a simplified, real-time client analytics dashboard that automatically reads CSV files and provides interactive visualizations without requiring a database.

## 🚀 Features

- **📊 Direct CSV Reading**: No database required - reads CSV files directly
- **🔄 Auto-refresh**: Dashboard updates every 10 seconds when new CSV files are added
- **🐳 Dockerized**: Single container deployment
- **🌍 Interactive Visualizations**:
  - Global client distribution with world map
  - City-level distribution with country filtering
- **📁 File Monitoring**: Automatically detects new CSV files in the input directory
- **🎯 Simple Setup**: One command to start

## 📊 Data Schema

CSV files should contain the following columns:
- `name`: Client name
- `country`: Client's country
- `city`: Client's city  
- `date`: Registration/entry date (YYYY-MM-DD format)

Example:
```csv
name,country,city,date
John Doe,United States,New York,2024-01-15
Jane Smith,United Kingdom,London,2024-01-16
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed

### 1. Start the Dashboard
```bash
docker-compose up -d
```

### 2. Access the Dashboard
Open your browser: `http://localhost:8501`

### 3. Add Data
Place CSV files in the `data/input/` directory - they will appear in the dashboard within 10 seconds!

## 📁 Project Structure

```
geopulse/
├── docker-compose.yml         # Simple container setup
├── data/
│   └── input/                 # Place CSV files here
├── streamlit_app/
│   ├── main.py               # Dashboard application
│   └── requirements.txt      # Python dependencies
├── run_local.py              # Run locally without Docker
├── Makefile                  # Easy management commands
└── README.md
```

## �️ Configuration

### Dashboard Features
- **Auto-refresh**: Updates every 10 seconds
- **Country Distribution**: Interactive world map with client counts
- **City Distribution**: Filterable by country with detailed statistics
- **File Monitoring**: Shows loaded CSV files and their status

### Adding Data
Simply drop CSV files into `data/input/` and watch them appear in the dashboard automatically!

## 📝 Management Commands

Using the included Makefile:

```bash
# Start dashboard
make up

# View logs
make logs

# Stop dashboard  
make down

# Restart
make restart

# Clean up
make clean
```

## 🏠 Local Development

Run without Docker:

```bash
python run_local.py
```

This will:
- Install required Python packages
- Create sample data if none exists
- Start the dashboard on `http://localhost:8501`

## 🧪 Testing

Sample CSV files are included in `data/input/`. Try adding new files:

```csv
name,country,city,date
Alice Johnson,Canada,Toronto,2024-01-20
Bob Wilson,Australia,Sydney,2024-01-21
```

Watch the dashboard update automatically!

## � Dashboard Features

### Country Distribution Page
- Interactive world map showing client distribution
- Top countries bar chart
- Complete country statistics table

### City Distribution Page  
- Country filter dropdown
- Horizontal bar chart for cities within selected country
- Summary metrics and statistics
- Detailed city information

## 🔧 Troubleshooting

### Common Issues

1. **Dashboard not loading**: Wait ~30 seconds for container to start
2. **CSV not appearing**: Ensure proper column names (name, country, city, date)
3. **Port conflicts**: Ensure port 8501 is available

### Useful Commands

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs dashboard

# Restart if stuck
docker-compose restart

# Clean slate restart
docker-compose down && docker-compose up -d
```

## 🎯 Use Cases

- **Client Analytics**: Visualize customer geographical distribution
- **Market Research**: Analyze regional market penetration  
- **Sales Reporting**: Track client acquisition by location
- **Data Exploration**: Quick insights from CSV client data

## � Performance

- **Lightweight**: Single container, minimal resource usage
- **Fast Loading**: Direct CSV reading, no database overhead
- **Responsive**: Real-time updates, 10-second refresh cycle
- **Scalable**: Handles thousands of client records efficiently

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your CSV files for testing
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the sample CSV format
3. Verify Docker is running properly
4. Create an issue on GitHub

---

**GeoPulse** - Transform your CSV client data into beautiful insights! 🌍📊