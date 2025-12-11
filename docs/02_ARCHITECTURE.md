# 🏗️ Τεχνική Αρχιτεκτονική PowerSave

## Επισκόπηση

Το PowerSave χρησιμοποιεί μια **3-Tier Architecture** που διαχωρίζει καθαρά το presentation, την business logic και τα δεδομένα.

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION TIER                        │
│  ┌─────────────────────┐    ┌─────────────────────────┐    │
│  │   Consumer Mobile   │    │    Admin Web Dashboard  │    │
│  │   (React Native)    │    │    (React 18 + Vite)    │    │
│  └──────────┬──────────┘    └───────────┬─────────────┘    │
└─────────────┼───────────────────────────┼──────────────────┘
              │         REST API          │
              ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION TIER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Python FastAPI Backend                  │   │
│  │  • RESTful API                                       │   │
│  │  • JWT Authentication                                │   │
│  │  • Business Logic                                    │   │
│  │  • Gamification Engine                               │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         │                                   │
│  ┌──────────────────────▼──────────────────────────────┐   │
│  │              Celery Workers                          │   │
│  │  • Background Jobs                                   │   │
│  │  • Session Start/End Processing                      │   │
│  │  • Baseline Calculations                             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
              │                           │
              ▼                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA TIER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐    │
│  │ PostgreSQL  │  │    Redis    │  │  ΑΗΚ Internal    │    │
│  │  Database   │  │   (Queue)   │  │    Systems       │    │
│  └─────────────┘  └─────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Presentation Tier (Clients)

### Consumer Mobile App
| Χαρακτηριστικό | Τεχνολογία |
|----------------|------------|
| Framework | React Native |
| State Management | Context API / Redux |
| Navigation | React Navigation |

**Κύριες Λειτουργίες:**
- Προγραμματισμός Saving Sessions
- Παρακολούθηση εξοικονομήσεων σε πραγματικό χρόνο
- Waste Wallet management
- Green Garden (gamification)
- Badges και Challenges
- Push notifications

### Admin Web Dashboard
| Χαρακτηριστικό | Τεχνολογία |
|----------------|------------|
| Framework | React 18 |
| Build Tool | Vite |
| Styling | TailwindCSS |
| Charts | Recharts |

**Κύριες Λειτουργίες:**
- Διαχείριση χρηστών
- Analytics και KPIs
- Challenge management
- System monitoring
- User support tools

---

## 2. Application Tier (Backend)

### FastAPI Backend

```python
# Δομή Project
backend/
├── main.py              # Entry point
├── config.py            # Configuration
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── routers/             # API endpoints
│   ├── auth.py
│   ├── sessions.py
│   ├── garden.py
│   ├── challenges.py
│   └── admin.py
├── services/            # Business logic
│   ├── baseline.py      # Baseline calculation
│   ├── savings.py       # Savings calculation
│   └── gamification.py  # Points & badges
├── tasks/               # Celery tasks
│   ├── session_start.py
│   └── session_end.py
└── utils/               # Helpers
```

### Βασικά Components

| Component | Περιγραφή |
|-----------|-----------|
| **Authentication** | JWT Bearer tokens με refresh mechanism |
| **Business Logic** | Υπολογισμοί εξοικονόμησης, baseline algorithm |
| **Gamification Engine** | Green Points, Badges, Challenges, Leaderboards |
| **Notification Service** | Push notifications για session results |

### Celery Workers

Οι background workers χειρίζονται:
- **Session Start Job**: Fetch historical data + baseline calculation
- **Session End Job**: Final calculation + gamification rewards
- **Scheduled Reports**: Daily/weekly analytics
- **Data Sync**: Synchronization με ΑΗΚ systems

---

## 3. Data Tier (Persistence)

### PostgreSQL Database
- **Primary database** για όλα τα application data
- ACID compliance για transaction integrity
- Optimized indexes για fast queries

### Redis
- **Message Broker** για Celery job queue
- **Caching layer** για frequently accessed data
- **Session storage** για real-time features

### ΑΗΚ Internal Systems
- Smart meter data pipeline
- Historical consumption data
- Real-time usage monitoring

---

## Tech Stack Summary

| Layer | Technology | Version |
|-------|------------|---------|
| Mobile App | React Native | 0.72+ |
| Admin Dashboard | React | 18.x |
| Build Tool | Vite | 5.x |
| CSS Framework | TailwindCSS | 3.x |
| Charts | Recharts | 2.x |
| Backend | Python | 3.10+ |
| API Framework | FastAPI | 0.100+ |
| Task Queue | Celery | 5.x |
| Message Broker | Redis | 7.x |
| Database | PostgreSQL | 15+ |
| Authentication | JWT | - |
| Containerization | Docker | 24+ |

---

## Security Considerations

### Authentication & Authorization
- JWT tokens με short expiry (15 min access, 7 days refresh)
- Role-based access control (Consumer, Admin, SuperAdmin)
- Rate limiting στα API endpoints

### Data Protection
- Encryption at rest για sensitive data
- TLS 1.3 για all communications
- GDPR compliance για user data

### Infrastructure Security
- Network isolation (VPC)
- Regular security audits
- Automated vulnerability scanning

---

## Scalability Architecture

```
                    ┌─────────────┐
                    │   CDN       │
                    │ (CloudFront)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    ALB      │
                    │(Load Balancer)
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
    ┌────▼────┐       ┌────▼────┐       ┌────▼────┐
    │ API #1  │       │ API #2  │       │ API #3  │
    └────┬────┘       └────┬────┘       └────┬────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │  (Primary)  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  PostgreSQL │
                    │  (Replica)  │
                    └─────────────┘
```

---

## Monitoring & Observability

| Aspect | Tool |
|--------|------|
| Metrics | Prometheus + Grafana |
| Logging | ELK Stack / CloudWatch |
| Tracing | Jaeger / X-Ray |
| Alerting | PagerDuty / OpsGenie |

---

*Για λεπτομέρειες API endpoints, δείτε [API Reference](./03_API_REFERENCE.md)*
