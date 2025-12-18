# 🌱 PowerSave - National Energy Solidarity Ecosystem

The first operational system for energy behavioral change and social cohesion in Cyprus.

[![CI/CD](https://github.com/nvoskos/powersave/workflows/Backend%20CI/badge.svg)](https://github.com/nvoskos/powersave/actions)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/deploy-ready-brightgreen.svg)](DEPLOYMENT.md)

## 🚀 **Quick Deploy**

**Deploy to GitHub Pages in 2 minutes:**

1. Push latest changes: `git push origin main`
2. Enable GitHub Pages: [Settings → Pages](https://github.com/nvoskos/powersave/settings/pages)
3. Visit: `https://nvoskos.github.io/powersave/`

**Or use the interactive script:**
```bash
./deploy.sh
```

📖 **Full deployment guide:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 🎯 Vision

PowerSave transforms "negative energy" (waste, poverty, grid stress) into "positive impact" through a white-label platform that converts energy savings (Negawatts) into:
- 💰 Digital currency for paying municipal obligations
- 🤝 Social solidarity mechanisms
- 📊 Smart grid management data

**Philosophy:** Social Liberalism - Solving social problems with market tools.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   POWERSAVE ECOSYSTEM                   │
│                                                         │
│  ┌──────────────┐     ┌──────────────┐                 │
│  │  Mobile App  │────▶│   Backend    │                 │
│  │ React Native │     │   FastAPI    │                 │
│  └──────────────┘     └───────┬──────┘                 │
│                               │                         │
│                    ┌──────────┼──────────┐             │
│                    │          │          │             │
│               ┌────▼───┐  ┌───▼───┐  ┌──▼─────┐       │
│               │PostgreSQL Redis  │  │  AHK    │       │
│               │          │       │  │  API    │       │
│               └──────────┘  └───────┘  └────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## 🧠 AI Tools Suite

PowerSave includes **5 AI-powered tools** built with GenSpark AI:

### 1. 🧠 **MindMap Agent** (NEW!)
AI-powered mind mapping with conversational interface
- Create mindmaps via natural language
- Smart context understanding
- Export: JSON, CSV, Markdown
- **Live:** [MindMap Agent](tools/mindmap-agent-genspark.html)

### 2. 📄 **PDF Form Builder**
Build professional forms with AI assistance
- 13 field types (text, email, dropdown, etc.)
- AI chatbot for suggestions
- Export to PDF
- **Live:** [PDF Form Builder](tools/chatbot-genspark.html)

### 3. 🔤 **OCR & Translation**
Extract text from images/PDFs with AI translation
- Multi-page PDF support
- Greek ↔ English translation
- Tesseract.js OCR engine
- **Live:** [OCR Tool](tools/ocr-translator-genspark.html)

### 4. 🌐 **Knowledge Crawler**
Web scraping with AI analysis
- Real web crawling + CORS proxy
- AI summarization & keywords
- Batch crawling support
- **Live:** [Setup Crawler](tools/setup-crawler.html)

### 5. 🔗 **Nexus MindMap Extractor**
Chrome extension for NotebookLM analysis
- 4 AI analysis types
- JSON/CSV export
- **Install:** [GitHub Guide](https://github.com/nvoskos/nexus-mindmap-extractor)

**All tools powered by:** GenSpark OpenAI Proxy (`gpt-5-mini`)  
**Tools Hub:** [/tools/index.html](tools/index.html)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Database:** PostgreSQL 15+ with SQLAlchemy ORM
- **Cache/Queue:** Redis 7+
- **Task Queue:** Celery
- **Validation:** Pydantic v2

### Mobile
- **Framework:** React Native 0.72
- **Navigation:** React Navigation v6
- **State:** React Context API
- **HTTP:** Axios

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Deployment:** Ready for AWS/Azure/GCP

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for mobile development)
- Python 3.11+ (for backend development)

### 1. Clone Repository

```bash
git clone https://github.com/nvoskos/powersave.git
cd powersave
```

### 2. Start with Docker (Recommended)

```bash
# Build and start all services
make docker-up

# Seed database with sample data
docker-compose exec backend python seed_database.py
```

Services will be available at:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Database:** localhost:5432
- **Redis:** localhost:6379

### 3. Run Mobile App

```bash
cd mobile
npm install
npm run android  # or npm run ios
```

---

## 📱 Features

### 1. Waste Fee Offset 🗑️
**Goal:** Citizens pay waste fees by turning off the lights.

**Mechanism:**
- User participates in Saving Sessions (17:00-20:00)
- Savings credited to Waste Wallet
- Monthly auto-payment to municipality
- Coverage: 35-100% of annual fees

**Example:**
- Baseline: 1.8 kWh (3h session)
- Actual: 1.2 kWh
- Savings: 0.6 kWh = **€0.18**
- 20 sessions/month = **€3.60**
- Annual = **€43.20** (covers ~36% of fees)

### 2. Energy Solidarity 🤝
**Goal:** Social welfare through crowdsourcing (no state spending).

**Mechanism:**
- "No Home Cold" campaigns
- Citizens donate savings to National Fund
- Fund pays bills for vulnerable households
- Corporate matching (2x donations)

**Impact:**
- 100,000 participants × €5/month = **€500K/month**
- With corporate matching = **€1M/month**
- Helps 3,000-4,000 vulnerable households

### 3. Solar Sync ☀️
**Goal:** Maximize self-consumption for PV owners.

**Mechanism:**
- Real-time notifications: *"Sun is shining - Run dishwasher FREE!"*
- Bonus points for synchronization
- Avoids exporting to grid (Net Billing optimization)

**Results:**
- Self-consumption: 30% → 70%
- ROI improvement: 7 years → 5 years
- Grid relief: 5 GWh/year

### 4. Local Hero 🏪
**Goal:** Energy becomes "revenue" for the neighborhood.

**Mechanism:**
- Savings → Green Coins
- Redeemable ONLY at local SMEs
- No multinationals
- Geofencing bonus (2km radius)

**Impact:**
- €2M/year circulating locally
- +150 indirect jobs
- Historic center revitalization

### 5. Eco-Stay 🏨
**Goal:** Reduce hotel waste.

**Mechanism:**
- Guest Mode (QR code, no signup)
- Real-time consumption display
- Rewards: Free cocktail, spa discount, late check-out

**Savings:**
- 200 rooms × 20% reduction = **180,000 kWh/year**
- **€54,000** gross - €10,000 rewards = **€44,000 net**

### 6. EV Smart Charge ⚡🚗
**Goal:** Smart charging without grid collapse.

**Mechanism:**
- Incentives for off-peak charging (23:00-06:00)
- Bonus for solar charging (12:00-14:00)
- Integration with CYTA/EAC chargers

**Impact:**
- 80% charging off-peak
- Equivalent to **€15M** infrastructure savings

### 7. Little Guardians 👶
**Secret Weapon:** Kids become energy agents.

**Mechanism:**
- School program (Preschool + 1st Grade)
- Kids earn badges when family saves
- Reverse socialization (kids pressure parents)

**Impact:**
- 50 schools × 200 kids = **10,000 families activated**
- Long-term behavioral change

---

## 📊 Master Pitch Deck

See [docs/MASTER_PITCH_DECK.md](docs/MASTER_PITCH_DECK.md) for the comprehensive presentation designed for:
- **Προεδρικό Μέγαρο** (Presidential Mansion)
- **International Investors**
- **EU Commission**

**Highlights:**
- ROI: **8.6x** (€69M / €8M)
- Target: **50,000 households** (Nicosia pilot)
- Timeline: Launch **January 2026**
- EU Presidency Showcase: **July 2026**

---

## 🗂️ Project Structure

```
powersave/
├── backend/                 # FastAPI backend
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── tests/               # Unit tests
│   ├── Dockerfile           # Backend container
│   ├── requirements.txt     # Python dependencies
│   └── seed_database.py     # Sample data seeding
│
├── mobile/                  # React Native app
│   ├── src/
│   │   ├── screens/         # App screens
│   │   ├── components/      # Reusable components
│   │   ├── services/        # API integration
│   │   ├── context/         # State management
│   │   └── navigation/      # Navigation config
│   ├── App.js               # Main entry point
│   └── package.json         # Dependencies
│
├── docs/                    # Documentation
│   ├── MASTER_PITCH_DECK.md # Presidential presentation
│   ├── 01_README.md         # System overview
│   ├── 02_ARCHITECTURE.md   # Technical architecture
│   ├── 03_API_REFERENCE.md  # API documentation
│   ├── 04_DATABASE_SCHEMA.md# Database design
│   └── ...                  # More documentation
│
├── .github/workflows/       # CI/CD pipelines
│   ├── backend-ci.yml       # Backend tests
│   ├── deploy.yml           # Deployment
│   └── pr-checks.yml        # PR validation
│
├── docker-compose.yml       # Multi-container setup
├── Makefile                 # Convenience commands
└── README.md                # This file
```

---

## 💻 Development

### Backend Development

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn backend.main:app --reload --port 8000

# Run tests
pytest tests/ -v --cov=backend

# Seed database
python seed_database.py
```

### Mobile Development

```bash
cd mobile

# Install dependencies
npm install

# Run on Android
npm run android

# Run on iOS (macOS only)
npm run ios

# Format code
npm run format
```

### Docker Development

```bash
# Start all services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down

# Clean everything
make docker-clean

# Open PostgreSQL shell
make db-shell

# Reset database
make db-reset
```

---

## 🧪 Testing

### Backend Tests

25 unit tests covering core business logic:

```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=backend --cov-report=html

# Specific test file
pytest tests/test_baseline.py -v
```

**Test Coverage:**
- ✅ Baseline calculations (10 tests)
- ✅ Savings calculations (11 tests)
- ✅ Municipality integration (4 tests)

---

## 🚢 Deployment

### Production Deployment

```bash
# Build production images
docker-compose build

# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# Run database migrations
docker-compose exec backend alembic upgrade head
```

### CI/CD Pipeline

GitHub Actions automatically:
1. **Tests** backend code on every push
2. **Builds** Docker images
3. **Scans** for security vulnerabilities
4. **Deploys** to staging/production

See [.github/workflows/](.github/workflows/) for details.

---

## 📖 API Documentation

Once backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

```
# Authentication
POST /api/v1/auth/register
POST /api/v1/auth/register-property

# Waste Wallet
GET  /api/v1/wallet/{userId}/balance
GET  /api/v1/wallet/{userId}/coverage
POST /api/v1/wallet/{userId}/donate

# Saving Sessions
POST /api/v1/sessions
GET  /api/v1/sessions/user/{userId}
POST /api/v1/sessions/{sessionId}/start
POST /api/v1/sessions/{sessionId}/complete
```

---

## 🌍 Environmental Impact

### Pilot Phase (50,000 households, Nicosia 2026)
- **Energy Saved:** 1.2 GWh/year
- **CO₂ Reduction:** 840 tons/year
- **Equivalent to:** 180,000 trees planted

### National Rollout (by 2028)
- **Energy Saved:** 20 GWh/year
- **CO₂ Reduction:** 14,000 tons/year
- **Cost Avoidance:** €6M/year

---

## 💰 Business Model

### Revenue Streams
1. **White-Label Licensing:** €2-5 per citizen/year
2. **Municipality Integration:** €50K setup + €10K/year
3. **Corporate ESG Packages:** €20K-100K/year
4. **EU Funding:** €17M (grants)

### Market Potential
- **Cyprus:** 350,000 households = €700K-1.75M ARR
- **EU Export:** 27 countries × €2/citizen = **€50M ARR potential**

### ROI (5 years)
- **Investment:** €8M
- **Return:** €69M
- **ROI:** **8.6x**

---

## 🏆 Competitive Advantages

1. **First Mover:** No comparable integrated system in EU
2. **Behavioral Tech:** Gamification + social pressure (kids)
3. **Zero Subsidies:** Self-sustaining through market mechanisms
4. **Scalable:** White-label for any country/municipality
5. **Multi-Tool:** 6 tools addressing different stakeholders

---

## 📅 Roadmap

### Phase 1: Pilot (Dec 2025 - Jun 2026)
- ✅ Backend implementation
- ✅ Mobile app MVP
- ✅ Docker deployment
- 🔄 Municipality integration (Nicosia)
- 🔄 Smart meter API integration (AHK)
- 🔄 Little Guardians soft launch (10 schools)

### Phase 2: National Rollout (Sep 2026 - Dec 2027)
- Expand to 3 more municipalities
- Little Guardians nationwide (200 schools)
- Corporate ESG partnerships
- Mobile app v2 (dark mode, multilingual)

### Phase 3: EU Export (2028+)
- White-label customization
- Multi-country deployment
- Advanced AI predictions
- Blockchain integration (optional)

---

## 👥 Team

**Project Lead:** Nikos Voskos
**Tech Stack:** Python, React Native, PostgreSQL, Docker
**Target Market:** Cyprus → EU

---

## 📞 Contact

- **Website:** powersave.cy (TBD)
- **Email:** info@powersave.cy
- **GitHub:** https://github.com/nvoskos/powersave

---

## 📄 License

Proprietary - PowerSave Cyprus 2025

All rights reserved. This software is confidential and proprietary.

---

## 🙏 Acknowledgments

- **Cyprus Energy Authority (RAEK):** Energy data standards
- **EAC (ΑΗΚ):** Smart meter integration support
- **Union of Municipalities:** Waste fee integration
- **EU Commission:** Green Deal alignment

---

## 🎉 Get Started

```bash
# 1. Clone and setup
git clone https://github.com/nvoskos/powersave.git
cd powersave

# 2. Start everything with Docker
make docker-up

# 3. Seed database
docker-compose exec backend python seed_database.py

# 4. Open browser
open http://localhost:8000/docs

# 5. Run mobile app
cd mobile && npm install && npm run android
```

**Welcome to the future of energy solidarity! 🌱⚡💚**
