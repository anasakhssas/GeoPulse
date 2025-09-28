# GeoPulse Pipeline Management

.PHONY: help build up down restart logs clean status sample-data

help:
	@echo "GeoPulse Pipeline Management"
	@echo ""
	@echo "Available commands:"
	@echo "  build      - Build all Docker images"
	@echo "  up         - Start the entire pipeline"
	@echo "  down       - Stop the entire pipeline"
	@echo "  restart    - Restart all services"
	@echo "  logs       - View logs from all services"
	@echo "  clean      - Clean up containers and volumes"
	@echo "  status     - Show status of all services"
	@echo "  sample-data - Add sample data for testing"

build:
	@echo "Building Docker images..."
	docker-compose build

up:
	@echo "Starting GeoPulse pipeline..."
	docker-compose up -d
	@echo "Services starting..."
	@echo "Dashboard will be available at: http://localhost:8501"
	@echo "Spark UI available at: http://localhost:8080"

down:
	@echo "Stopping GeoPulse pipeline..."
	docker-compose down

restart:
	@echo "Restarting GeoPulse pipeline..."
	docker-compose restart

logs:
	@echo "Showing logs from all services..."
	docker-compose logs -f

logs-streamlit:
	@echo "Showing Streamlit logs..."
	docker-compose logs -f streamlit

logs-spark:
	@echo "Showing Spark logs..."
	docker-compose logs -f spark-master spark-worker data-processor

logs-postgres:
	@echo "Showing PostgreSQL logs..."
	docker-compose logs -f postgres

clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f

status:
	@echo "Service status:"
	docker-compose ps

sample-data:
	@echo "Sample data already available in data/input/sample_clients.csv"
	@echo "You can add more CSV files to data/input/ directory"

# Development commands
dev-shell:
	docker-compose exec data-processor /bin/bash

db-shell:
	docker-compose exec postgres psql -U geopulse_user -d geopulse

# Quick start
start: build up
	@echo ""
	@echo "🚀 GeoPulse is starting up!"
	@echo ""
	@echo "📊 Dashboard: http://localhost:8501"
	@echo "⚡ Spark UI: http://localhost:8080"
	@echo "🗄️  Database: localhost:5432"
	@echo ""
	@echo "💡 Add CSV files to data/input/ to see them processed automatically!"