# 💻 Development Setup

## Επισκόπηση

Οδηγός για setup του development environment για το PowerSave.

---

## Prerequisites

### Backend Requirements

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.10+ | Runtime |
| pip | Latest | Package manager |
| Docker | 24+ | Containers |
| Docker Compose | 2.x | Multi-container |

### Frontend Requirements

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | 18+ | Runtime |
| npm | 9+ | Package manager |

---

## Backend Setup

### 1. Clone Repository

```bash
git clone https://github.com/powersave-cyprus/powersave-backend.git
cd powersave-backend
```

### 2. Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### 4. Environment Configuration

```bash
# Create .env file
cp .env.example .env
```

Edit `.env`:

```bash
# .env
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256

# Energy calculations
GRID_EMISSION_FACTOR=0.65
DEFAULT_TARIFF_RATE=0.34

# Database (Docker)
DATABASE_URL=postgresql://powersave:powersave@localhost:5432/powersave_db

# Redis (Docker)
REDIS_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Debug
DEBUG=true
LOG_LEVEL=DEBUG
```

### 5. Start Infrastructure (Docker)

```bash
# Start PostgreSQL and Redis
docker-compose up -d db redis

# Verify containers are running
docker-compose ps
```

### 6. Initialize Database

```bash
# Run migrations
alembic upgrade head

# Seed demo data
python scripts/seed_demo_data.py
```

### 7. Start Development Server

```bash
# Start FastAPI with hot reload
uvicorn main:app --reload --port 8000

# API available at http://127.0.0.1:8000
# Docs available at http://127.0.0.1:8000/docs
```

### 8. Start Celery Worker (optional)

```bash
# In a new terminal
source venv/bin/activate
celery -A tasks worker --loglevel=debug
```

---

## Frontend Setup (Admin Dashboard)

### 1. Clone Repository

```bash
git clone https://github.com/powersave-cyprus/powersave-admin.git
cd powersave-admin
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Environment Configuration

```bash
# Create .env file (optional)
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env
```

### 4. Start Development Server

```bash
npm run dev

# Dashboard available at http://localhost:5173
```

---

## Project Structure

### Backend

```
powersave-backend/
├── main.py                 # FastAPI entry point
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker services
├── alembic/                # Database migrations
│   ├── versions/
│   └── alembic.ini
├── models/                 # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   ├── session.py
│   ├── garden.py
│   └── challenge.py
├── schemas/                # Pydantic schemas
│   ├── __init__.py
│   ├── user.py
│   ├── session.py
│   └── response.py
├── routers/                # API endpoints
│   ├── __init__.py
│   ├── auth.py
│   ├── sessions.py
│   ├── garden.py
│   ├── challenges.py
│   ├── wallet.py
│   └── admin/
│       ├── users.py
│       ├── stats.py
│       └── challenges.py
├── services/               # Business logic
│   ├── baseline.py         # Baseline calculation
│   ├── savings.py          # Savings calculation
│   ├── gamification.py     # Points & badges
│   └── notifications.py    # Push notifications
├── tasks/                  # Celery tasks
│   ├── __init__.py
│   ├── session_start.py
│   └── session_end.py
├── utils/                  # Helper functions
│   ├── security.py
│   ├── database.py
│   └── ahk_api.py
├── tests/                  # Test suite
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_sessions.py
│   └── test_gamification.py
└── scripts/                # Utility scripts
    ├── seed_demo_data.py
    └── cleanup.py
```

### Frontend (Admin Dashboard)

```
powersave-admin/
├── src/
│   ├── main.jsx            # Entry point
│   ├── App.jsx             # Root component
│   ├── components/         # Reusable components
│   │   ├── Layout/
│   │   ├── Charts/
│   │   └── Tables/
│   ├── pages/              # Page components
│   │   ├── Dashboard.jsx
│   │   ├── Users.jsx
│   │   ├── Sessions.jsx
│   │   └── Challenges.jsx
│   ├── hooks/              # Custom hooks
│   ├── services/           # API calls
│   │   └── api.js
│   ├── store/              # State management
│   └── utils/              # Helpers
├── public/
├── package.json
├── vite.config.js
└── tailwind.config.js
```

---

## Demo Credentials

### Consumer App

| Field | Value |
|-------|-------|
| Account Number | `123456789` |
| Password | `password` |

### Admin Dashboard

| Field | Value |
|-------|-------|
| Email | `admin@ahk.com.cy` |
| Password | `adminpass` |

---

## Useful Commands

### Backend

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Format code
black .

# Lint
flake8 .

# Type checking
mypy .

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Reset database
alembic downgrade base && alembic upgrade head
```

### Frontend

```bash
# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint
npm run lint

# Format
npm run format
```

### Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Clean up volumes
docker-compose down -v
```

---

## Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_sessions.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Structure

```python
# tests/test_sessions.py
import pytest
from fastapi.testclient import TestClient

def test_create_session(client: TestClient, auth_headers: dict):
    """Test creating a new saving session."""
    response = client.post(
        "/sessions",
        json={
            "startTime": "2025-01-15T17:00:00Z",
            "endTime": "2025-01-15T20:00:00Z"
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "SCHEDULED"
    assert "sessionId" in data

def test_create_session_invalid_time(client: TestClient, auth_headers: dict):
    """Test creating session with end time before start time."""
    response = client.post(
        "/sessions",
        json={
            "startTime": "2025-01-15T20:00:00Z",
            "endTime": "2025-01-15T17:00:00Z"  # End before start
        },
        headers=auth_headers
    )
    
    assert response.status_code == 422
```

---

## Debugging

### API Debugging

```bash
# Enable debug mode in .env
DEBUG=true
LOG_LEVEL=DEBUG

# View detailed logs
uvicorn main:app --reload --log-level debug
```

### Database Debugging

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U powersave powersave_db

# View all users
SELECT * FROM "user" LIMIT 10;

# View recent sessions
SELECT * FROM saving_session ORDER BY created_at DESC LIMIT 10;
```

### Redis Debugging

```bash
# Connect to Redis CLI
docker-compose exec redis redis-cli

# View queued tasks
KEYS celery*

# View queue length
LLEN celery
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Database connection refused | Check Docker: `docker-compose ps` |
| Celery tasks not running | Start worker: `celery -A tasks worker` |
| CORS errors | Check `CORS_ORIGINS` in `.env` |
| Import errors | Activate venv: `source venv/bin/activate` |
| Migration errors | Reset: `alembic downgrade base && alembic upgrade head` |

### Reset Development Environment

```bash
# Stop all containers
docker-compose down -v

# Remove venv
rm -rf venv

# Start fresh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
docker-compose up -d
alembic upgrade head
python scripts/seed_demo_data.py
```

---

## IDE Configuration

### VS Code

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

### Recommended Extensions

- Python
- Pylance
- Black Formatter
- SQLTools
- Docker
- REST Client

---

*Για τα εργαλεία της πλατφόρμας, δείτε [Platform Tools](./08_PLATFORM_TOOLS.md)*
