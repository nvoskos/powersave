# PowerSave Makefile
# Convenient commands for development and deployment

.PHONY: help install dev test docker-build docker-up docker-down seed clean

# Default target
help:
	@echo "PowerSave - Available Commands"
	@echo "================================"
	@echo ""
	@echo "Development:"
	@echo "  make install      - Install backend dependencies"
	@echo "  make dev          - Run backend in development mode"
	@echo "  make test         - Run unit tests"
	@echo "  make seed         - Seed database with sample data"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start all services"
	@echo "  make docker-down  - Stop all services"
	@echo "  make docker-logs  - View logs"
	@echo "  make docker-clean - Remove containers and volumes"
	@echo ""
	@echo "Database:"
	@echo "  make db-shell     - Open PostgreSQL shell"
	@echo "  make db-reset     - Reset database"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean        - Clean Python cache files"
	@echo ""

# Development
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt

dev:
	@echo "Starting FastAPI in development mode..."
	cd backend && uvicorn backend.main:app --reload --port 8000

test:
	@echo "Running unit tests..."
	cd backend && pytest tests/ -v --cov=backend

seed:
	@echo "Seeding database with sample data..."
	cd backend && python seed_database.py

# Docker
docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting all services..."
	docker-compose up -d
	@echo ""
	@echo "✅ Services started!"
	@echo "   • API:      http://localhost:8000"
	@echo "   • Docs:     http://localhost:8000/docs"
	@echo "   • pgAdmin:  http://localhost:5050 (with --profile debug)"
	@echo ""

docker-down:
	@echo "Stopping all services..."
	docker-compose down

docker-logs:
	@echo "Viewing logs..."
	docker-compose logs -f

docker-clean:
	@echo "Removing containers and volumes..."
	docker-compose down -v
	docker system prune -f

# Database
db-shell:
	@echo "Opening PostgreSQL shell..."
	docker-compose exec postgres psql -U powersave -d powersave

db-reset:
	@echo "Resetting database..."
	docker-compose exec postgres psql -U powersave -c "DROP DATABASE IF EXISTS powersave;"
	docker-compose exec postgres psql -U powersave -c "CREATE DATABASE powersave;"
	@echo "Database reset. Run 'make seed' to populate with sample data."

# Cleanup
clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	@echo "Cleanup complete!"
