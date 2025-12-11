# 🚀 Deployment Guide

## Επισκόπηση

Οδηγός για deployment του PowerSave σε production environment.

---

## Production Architecture

```
                         ┌─────────────────┐
                         │   CloudFlare    │
                         │      CDN        │
                         └────────┬────────┘
                                  │
                         ┌────────▼────────┐
                         │   AWS ALB       │
                         │ (Load Balancer) │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
      ┌───────▼───────┐   ┌───────▼───────┐   ┌───────▼───────┐
      │  API Pod #1   │   │  API Pod #2   │   │  API Pod #3   │
      │  (FastAPI)    │   │  (FastAPI)    │   │  (FastAPI)    │
      └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
┌───────▼───────┐         ┌───────▼───────┐         ┌───────▼───────┐
│  PostgreSQL   │         │    Redis      │         │Celery Workers │
│   (Primary)   │         │   Cluster     │         │   (3 pods)    │
└───────┬───────┘         └───────────────┘         └───────────────┘
        │
┌───────▼───────┐
│  PostgreSQL   │
│   (Replica)   │
└───────────────┘
```

---

## Docker Configuration

### Backend Dockerfile

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Frontend Dockerfile

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# Build application
COPY . .
RUN npm run build

# Production image
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://powersave:powersave@db:5432/powersave_db
      - REDIS_URL=redis://redis:6379/0
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - GRID_EMISSION_FACTOR=0.65
    depends_on:
      - db
      - redis
    volumes:
      - ./backend:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  celery:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://powersave:powersave@db:5432/powersave_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: celery -A tasks worker --loglevel=info --concurrency=4

  celery-beat:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://powersave:powersave@db:5432/powersave_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: celery -A tasks beat --loglevel=info

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=powersave
      - POSTGRES_PASSWORD=powersave
      - POSTGRES_DB=powersave_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - api

volumes:
  postgres_data:
  redis_data:
```

---

## Environment Variables

### Production Environment

```bash
# .env.production

# Database
DATABASE_URL=postgresql://user:password@db.powersave.cy:5432/powersave_prod
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis.powersave.cy:6379/0
REDIS_PASSWORD=your_redis_password

# Security
JWT_SECRET_KEY=your-very-long-and-random-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Energy Calculations
GRID_EMISSION_FACTOR=0.65
DEFAULT_TARIFF_RATE=0.34

# CORS
CORS_ORIGINS=https://app.powersave.cy,https://admin.powersave.cy

# External APIs
AHK_API_URL=https://api.eac.com.cy/v1
AHK_API_KEY=your_ahk_api_key

# Push Notifications
FIREBASE_CREDENTIALS_PATH=/secrets/firebase-credentials.json

# Monitoring
SENTRY_DSN=https://xxx@sentry.io/xxx
LOG_LEVEL=INFO
```

### Kubernetes Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: powersave-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:password@db:5432/powersave"
  REDIS_URL: "redis://:password@redis:6379/0"
  JWT_SECRET_KEY: "your-secret-key"
  AHK_API_KEY: "your-ahk-api-key"
```

---

## Kubernetes Deployment

### API Deployment

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: powersave-api
  labels:
    app: powersave-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: powersave-api
  template:
    metadata:
      labels:
        app: powersave-api
    spec:
      containers:
      - name: api
        image: powersave/api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: powersave-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: powersave-api
spec:
  selector:
    app: powersave-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

### Celery Worker Deployment

```yaml
# k8s/celery-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: powersave-celery
spec:
  replicas: 3
  selector:
    matchLabels:
      app: powersave-celery
  template:
    metadata:
      labels:
        app: powersave-celery
    spec:
      containers:
      - name: celery
        image: powersave/api:latest
        command: ["celery", "-A", "tasks", "worker", "--loglevel=info", "--concurrency=4"]
        envFrom:
        - secretRef:
            name: powersave-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
```

### Horizontal Pod Autoscaler

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: powersave-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: powersave-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Database Operations

### Initial Setup

```bash
# Create database
psql -U postgres -c "CREATE DATABASE powersave_db;"
psql -U postgres -c "CREATE USER powersave WITH PASSWORD 'secure_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE powersave_db TO powersave;"

# Run migrations
alembic upgrade head

# Seed initial data
python scripts/seed_data.py
```

### Backup Strategy

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/postgres

pg_dump -h db.powersave.cy -U powersave powersave_db | gzip > $BACKUP_DIR/powersave_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/powersave_$DATE.sql.gz s3://powersave-backups/daily/

# Keep only last 30 days locally
find $BACKUP_DIR -type f -mtime +30 -delete
```

### Point-in-Time Recovery

```bash
# Enable WAL archiving in postgresql.conf
archive_mode = on
archive_command = 'aws s3 cp %p s3://powersave-backups/wal/%f'

# Restore to specific point
pg_restore --target-time="2025-01-15 14:30:00" -d powersave_db backup.dump
```

---

## Monitoring Setup

### Prometheus Configuration

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'powersave-api'
    static_configs:
      - targets: ['powersave-api:8000']
    metrics_path: /metrics

  - job_name: 'celery'
    static_configs:
      - targets: ['celery-exporter:9808']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']
```

### Key Metrics to Monitor

| Category | Metric | Alert Threshold |
|----------|--------|-----------------|
| **API** | Response Time (p95) | > 500ms |
| **API** | Error Rate | > 1% |
| **API** | Request Rate | - (baseline) |
| **Celery** | Queue Length | > 1000 |
| **Celery** | Task Failure Rate | > 5% |
| **Database** | Connection Pool | > 80% |
| **Database** | Query Time (p95) | > 100ms |
| **Redis** | Memory Usage | > 80% |

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "PowerSave Production",
    "panels": [
      {
        "title": "API Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total{job='powersave-api'}[5m])"
          }
        ]
      },
      {
        "title": "Session Completions",
        "type": "stat",
        "targets": [
          {
            "expr": "increase(saving_sessions_completed_total[1h])"
          }
        ]
      },
      {
        "title": "Total kWh Saved Today",
        "type": "stat",
        "targets": [
          {
            "expr": "increase(total_kwh_saved[1d])"
          }
        ]
      }
    ]
  }
}
```

---

## CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements-test.txt
          pytest --cov=app tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker image
        run: |
          docker build -t powersave/api:${{ github.sha }} ./backend
          docker push powersave/api:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/powersave-api \
            api=powersave/api:${{ github.sha }}
          kubectl rollout status deployment/powersave-api
```

---

## Security Checklist

- [ ] TLS 1.3 enabled on all endpoints
- [ ] JWT tokens with short expiry
- [ ] Rate limiting configured
- [ ] SQL injection prevention (parameterized queries)
- [ ] CORS properly configured
- [ ] Secrets in Kubernetes Secrets/Vault
- [ ] Regular security audits
- [ ] GDPR compliance verified
- [ ] Penetration testing completed
- [ ] Backup encryption enabled

---

*Για development setup, δείτε [Development Setup](./07_DEVELOPMENT_SETUP.md)*
