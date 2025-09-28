# GeoPulse Pipeline Management (Simplified)

.PHONY: help build up down restart logs clean status

help:
	@echo "GeoPulse Dashboard Management"
	@echo ""
	@echo "Available commands:"
	@echo "  up         - Start the dashboard"
	@echo "  down       - Stop the dashboard"
	@echo "  restart    - Restart the dashboard"
	@echo "  logs       - View dashboard logs"
	@echo "  clean      - Clean up containers"
	@echo "  status     - Show dashboard status"

up:
	@echo "Starting GeoPulse dashboard..."
	docker-compose up -d
	@echo "Dashboard starting..."
	@echo "Dashboard will be available at: http://localhost:8501"

down:
	@echo "Stopping GeoPulse dashboard..."
	docker-compose down

restart:
	@echo "Restarting GeoPulse dashboard..."
	docker-compose restart

logs:
	@echo "Showing dashboard logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning up containers..."
	docker-compose down
	docker system prune -f

status:
	@echo "Dashboard status:"
	docker-compose ps

# Quick start
start: up
	@echo ""
	@echo "🚀 GeoPulse Dashboard is starting!"
	@echo ""
	@echo "📊 Dashboard: http://localhost:8501"
	@echo ""
	@echo "💡 Add CSV files to data/input/ to see them in the dashboard!"