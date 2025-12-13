# PowerSave Backend API

FastAPI backend for the PowerSave National Energy Solidarity Ecosystem.

## Features

- ✅ **Waste Wallet** - Track savings for waste fee offset
- ✅ **Saving Sessions** - Schedule and track energy saving sessions
- ✅ **Baseline Calculation** - 10-day average with outlier removal
- ✅ **Savings Calculation** - kWh → EUR → Green Points
- ✅ **Municipality Integration** - Property verification and payments
- ✅ **RESTful API** - Full CRUD operations

## Tech Stack

- **Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 15+ with SQLAlchemy ORM
- **Validation:** Pydantic v2
- **Task Queue:** Celery + Redis
- **Testing:** pytest

## Installation

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Setup Database

```bash
# Create PostgreSQL database
createdb powersave

# Run migrations (if using Alembic)
alembic upgrade head
```

### 4. Run Server

```bash
# Development
uvicorn backend.main:app --reload --port 8000

# Production
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Documentation

Once running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration settings
├── database.py          # Database connection
├── models/              # SQLAlchemy models
│   ├── user.py
│   ├── municipality.py
│   ├── saving_session.py
│   ├── wallet.py
│   ├── gamification.py
│   └── social_fund.py
├── schemas/             # Pydantic schemas
│   ├── wallet.py
│   ├── session.py
│   └── user.py
├── routers/             # API endpoints
│   ├── auth.py
│   ├── waste_wallet.py
│   └── sessions.py
├── services/            # Business logic
│   ├── baseline.py      # Baseline calculation
│   ├── savings.py       # Savings calculation
│   ├── municipality.py  # Municipality integration
│   └── wallet.py        # Wallet operations
├── tasks/               # Celery background tasks
└── tests/               # Unit tests
    ├── test_baseline.py
    ├── test_savings.py
    └── test_municipality.py
```

## Key Endpoints

### Waste Wallet

- `GET /api/v1/wallet/{user_id}/balance` - Get wallet balance
- `GET /api/v1/wallet/{user_id}/transactions` - Transaction history
- `POST /api/v1/wallet/{user_id}/credit` - Credit wallet
- `POST /api/v1/wallet/{user_id}/debit` - Debit wallet
- `POST /api/v1/wallet/{user_id}/donate` - Donate to solidarity fund
- `GET /api/v1/wallet/{user_id}/coverage` - Waste fee coverage

### Saving Sessions

- `POST /api/v1/sessions` - Create new session
- `GET /api/v1/sessions/{session_id}` - Get session details
- `GET /api/v1/sessions/user/{user_id}` - Get user's sessions
- `POST /api/v1/sessions/{session_id}/start` - Start session
- `POST /api/v1/sessions/{session_id}/complete` - Complete session
- `GET /api/v1/sessions/user/{user_id}/stats` - User statistics

### Authentication

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/register-property` - Register property
- `GET /api/v1/auth/users/{user_id}` - Get user details

## Testing

```bash
# Run all tests
pytest backend/tests/ -v

# Run with coverage
pytest backend/tests/ --cov=backend --cov-report=html

# Run specific test file
pytest backend/tests/test_baseline.py -v
```

## Business Logic

### Baseline Calculation

The baseline is calculated using a **10-day rolling average** of consumption during the same time window:

```python
# Example: Session scheduled for 17:00-20:00 today
# System looks at consumption during 17:00-20:00 for past 10 days
# Removes outliers (values > 2 std dev from mean)
# Returns average consumption
```

### Savings Calculation

```
saved_kwh = baseline_kwh - actual_kwh
saved_eur = saved_kwh × €0.30
saved_co2_kg = saved_kwh × 0.7 kg/kWh
green_points = saved_kwh × 10 points/kWh

# Double points days: points × 2
```

### Waste Wallet Flow

1. User completes saving session
2. System calculates savings (kWh → EUR)
3. EUR amount credited to Waste Wallet
4. Monthly auto-payment to municipality
5. Surplus can be:
   - Rolled over to next month
   - Donated to Energy Solidarity Fund
   - Converted to Green Coins

## Integration Points

### Municipality API

```
GET  /api/properties/{property_number}          # Verify property
GET  /api/waste-fees/{property_number}/balance  # Get balance
POST /api/waste-fees/{property_number}/payments # Submit payment
POST /api/powersave/registrations               # Register user
```

### Smart Meter API (AHK/EAC)

```
GET /api/consumption/{account_number}/historical  # Historical data
GET /api/consumption/{account_number}/realtime    # Real-time data
```

## Environment Variables

See `.env.example` for all configuration options.

Critical variables:
- `DATABASE_URL` - PostgreSQL connection string
- `KWH_TO_EUR_RATE` - Current electricity rate (€/kWh)
- `MUNICIPALITY_API_BASE_URL` - Municipality API endpoint
- `AHK_API_BASE_URL` - Smart meter API endpoint

## Contributing

1. Follow PEP 8 style guide
2. Add type hints to all functions
3. Write unit tests for new features
4. Update API documentation

## License

Proprietary - PowerSave Cyprus 2025
