# 🔌 API Reference

## Επισκόπηση

Το PowerSave API ακολουθεί το **OpenAPI 3.0** specification και χρησιμοποιεί **RESTful** conventions.

**Base URL:** `https://api.powersave.cy/v1`

---

## Authentication

### JWT Bearer Token

Όλα τα protected endpoints απαιτούν JWT token στο header:

```http
Authorization: Bearer <access_token>
```

### Token Lifecycle

| Token Type | Expiry | Use Case |
|------------|--------|----------|
| Access Token | 15 minutes | API requests |
| Refresh Token | 7 days | Get new access token |

---

## Auth Endpoints

### Consumer Login

```http
POST /auth/login
Content-Type: application/json

{
  "accountNumber": "123456789",
  "password": "password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "userId": "uuid-here",
    "ahkAccountNumber": "123456789",
    "greenPointsBalance": 1250
  }
}
```

### Admin Login

```http
POST /admin/auth/login
Content-Type: application/json

{
  "email": "admin@ahk.com.cy",
  "password": "adminpass"
}
```

### Refresh Token

```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

## Consumer Endpoints

> ⚠️ Όλα τα endpoints απαιτούν **JWT Authentication**

### Dashboard

```http
GET /dashboard
```

**Response (200 OK):**
```json
{
  "totalSavedKwh": 125.5,
  "totalSavedEur": 42.67,
  "totalSavedCo2Kg": 81.58,
  "wasteWalletBalance": 38.50,
  "greenPointsBalance": 1250,
  "activeSessions": 1,
  "completedSessions": 45,
  "currentChallenge": {
    "challengeId": "uuid",
    "name": "Summer Saver",
    "progress": 0.75,
    "daysRemaining": 5
  }
}
```

---

### Saving Sessions

#### Schedule New Session

```http
POST /sessions
Content-Type: application/json

{
  "startTime": "2025-01-15T17:00:00Z",
  "endTime": "2025-01-15T20:00:00Z"
}
```

**Response (201 Created):**
```json
{
  "sessionId": "uuid-here",
  "status": "SCHEDULED",
  "startTime": "2025-01-15T17:00:00Z",
  "endTime": "2025-01-15T20:00:00Z",
  "createdAt": "2025-01-15T10:30:00Z"
}
```

#### Get Session History

```http
GET /sessions/history?page=1&limit=10&status=COMPLETED
```

**Response (200 OK):**
```json
{
  "sessions": [
    {
      "sessionId": "uuid-here",
      "status": "COMPLETED",
      "startTime": "2025-01-14T17:00:00Z",
      "endTime": "2025-01-14T20:00:00Z",
      "baselineKwh": 4.5,
      "actualKwh": 2.8,
      "savedKwh": 1.7,
      "savedEur": 0.58,
      "savedCo2Kg": 1.11,
      "greenPointsEarned": 17
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 45,
    "totalPages": 5
  }
}
```

#### Get Active Session

```http
GET /sessions/active
```

**Response (200 OK):**
```json
{
  "sessionId": "uuid-here",
  "status": "IN_PROGRESS",
  "startTime": "2025-01-15T17:00:00Z",
  "endTime": "2025-01-15T20:00:00Z",
  "baselineKwh": 4.2,
  "currentKwh": 1.8,
  "estimatedSavingsEur": 0.82,
  "timeRemainingMinutes": 45
}
```

---

### Green Garden

#### Get Garden State

```http
GET /garden
```

**Response (200 OK):**
```json
{
  "greenPointsBalance": 1250,
  "gardenLevel": 5,
  "totalPlantsPlanted": 12,
  "plants": [
    {
      "plantedItemId": "uuid",
      "plantId": "sunflower",
      "positionX": 2,
      "positionY": 3,
      "currentGrowthStage": 3,
      "maxGrowthStage": 5,
      "plantedAt": "2025-01-10T14:00:00Z"
    }
  ]
}
```

#### Get Plant Shop

```http
GET /garden/shop
```

**Response (200 OK):**
```json
{
  "plants": [
    {
      "plantId": "sunflower",
      "name": "Sunflower",
      "description": "A bright and cheerful flower",
      "costInGreenPoints": 100,
      "growthStages": 5,
      "imageUrl": "https://cdn.powersave.cy/plants/sunflower.png"
    },
    {
      "plantId": "olive_tree",
      "name": "Olive Tree",
      "description": "Traditional Cyprus olive tree",
      "costInGreenPoints": 500,
      "growthStages": 7,
      "imageUrl": "https://cdn.powersave.cy/plants/olive_tree.png"
    }
  ]
}
```

#### Plant Item

```http
POST /garden/plant
Content-Type: application/json

{
  "plantId": "sunflower",
  "positionX": 4,
  "positionY": 2
}
```

**Response (201 Created):**
```json
{
  "plantedItemId": "uuid-here",
  "plantId": "sunflower",
  "positionX": 4,
  "positionY": 2,
  "currentGrowthStage": 1,
  "remainingGreenPoints": 1150
}
```

---

### Challenges

#### Get Active Challenges

```http
GET /challenges
```

**Response (200 OK):**
```json
{
  "challenges": [
    {
      "challengeId": "uuid",
      "name": "Summer Energy Champion",
      "description": "Save 50 kWh this month",
      "goalType": "TOTAL_KWH_SAVED",
      "goalValue": 50.0,
      "currentValue": 37.5,
      "progress": 0.75,
      "startDate": "2025-01-01",
      "endDate": "2025-01-31",
      "reward": {
        "greenPoints": 500,
        "badgeId": "summer_champion"
      }
    }
  ]
}
```

---

### Badges

#### Get Earned Badges

```http
GET /badges
```

**Response (200 OK):**
```json
{
  "badges": [
    {
      "badgeId": "first_session",
      "name": "First Step",
      "description": "Complete your first saving session",
      "imageUrl": "https://cdn.powersave.cy/badges/first_session.png",
      "earnedAt": "2025-01-05T18:30:00Z"
    },
    {
      "badgeId": "week_streak",
      "name": "Weekly Warrior",
      "description": "Complete sessions 7 days in a row",
      "imageUrl": "https://cdn.powersave.cy/badges/week_streak.png",
      "earnedAt": "2025-01-12T20:00:00Z"
    }
  ]
}
```

---

### Waste Wallet

#### Get Wallet Status

```http
GET /wallet
```

**Response (200 OK):**
```json
{
  "balance": 38.50,
  "annualWasteFee": 195.00,
  "percentagePaid": 19.74,
  "transactions": [
    {
      "transactionId": "uuid",
      "type": "CREDIT",
      "amount": 0.58,
      "sessionId": "uuid",
      "createdAt": "2025-01-14T20:00:00Z"
    }
  ]
}
```

#### Donate to Social Fund

```http
POST /wallet/donate
Content-Type: application/json

{
  "amount": 5.00
}
```

---

## Admin Endpoints

> ⚠️ Απαιτούν **Admin JWT Token**

### Statistics

```http
GET /admin/stats
```

**Response (200 OK):**
```json
{
  "totalUsers": 15420,
  "activeUsersToday": 3250,
  "totalSessionsCompleted": 125000,
  "totalKwhSaved": 187500.5,
  "totalEurSaved": 63750.17,
  "totalCo2Prevented": 121875.33,
  "socialFundBalance": 12500.00
}
```

### User Management

```http
GET /admin/users?search=john&page=1&limit=20
```

```http
GET /admin/users/{userId}
```

### Session Management

```http
GET /admin/sessions?status=COMPLETED&date=2025-01-15
```

### Challenge Management

```http
GET /admin/challenges
POST /admin/challenges
PUT /admin/challenges/{challengeId}
DELETE /admin/challenges/{challengeId}
```

---

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "startTime",
        "message": "Start time must be in the future"
      }
    ]
  }
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limited |
| 500 | Server Error |

---

## Rate Limiting

| Endpoint Type | Limit |
|---------------|-------|
| Auth endpoints | 10 requests/minute |
| Consumer endpoints | 100 requests/minute |
| Admin endpoints | 200 requests/minute |

---

*Για database schema details, δείτε [Database Schema](./04_DATABASE_SCHEMA.md)*
