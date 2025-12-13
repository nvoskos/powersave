# PowerSave Waste Fee Offset API Documentation

## Overview

The PowerSave Waste Fee Offset API enables municipalities and energy providers to integrate with the waste fee payment system. Users can pay their annual municipal waste fees through energy savings.

**Base URL:** `http://localhost:5000/api`

**Version:** 1.0.0

---

## Authentication

Currently, the API uses user_id based authentication. In production, implement OAuth 2.0 or API keys.

---

## Municipalities API

### Get All Municipalities

```http
GET /api/municipalities
```

**Response:**
```json
{
  "success": true,
  "municipalities": [
    {
      "id": "nicosia",
      "name": "Δήμος Λευκωσίας",
      "name_en": "Nicosia Municipality",
      "annual_fee": 185.00,
      "region": "Λευκωσία"
    }
  ]
}
```

### Get Municipality Details

```http
GET /api/municipalities/{municipality_id}
```

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| municipality_id | string | Municipality identifier (e.g., "nicosia") |

---

## Property Registration API

### Register Property

Register a premises for waste fee offset.

```http
POST /api/properties/register
```

**Request Body:**
```json
{
  "user_id": "user123",
  "municipality_id": "nicosia",
  "property_number": "12345-NIC",
  "address": "Makarios Ave 123, Nicosia"
}
```

**Response:**
```json
{
  "success": true,
  "property": {
    "id": "uuid",
    "user_id": "user123",
    "municipality_id": "nicosia",
    "property_number": "12345-NIC",
    "annual_fee": 185.00,
    "verified": false
  },
  "wallet_id": "uuid",
  "message": "Property registered successfully"
}
```

### Register via QR Scan

```http
POST /api/properties/scan
```

**Request Body:**
```json
{
  "user_id": "user123",
  "qr_data": "nicosia:12345-NIC:Makarios Ave 123"
}
```

**QR Data Format:** `MUNICIPALITY:PROPERTY_NUMBER:ADDRESS`

---

## Waste Wallet API

### Get Wallet

```http
GET /api/wallet/{wallet_id}
```

**Response:**
```json
{
  "success": true,
  "wallet": {
    "id": "uuid",
    "balance": 45.30,
    "total_earned": 67.80,
    "total_paid": 22.50,
    "annual_target": 185.00,
    "year": 2025
  },
  "progress_percent": 25.0,
  "remaining": 139.70
}
```

### Get User Wallets

```http
GET /api/wallet/user/{user_id}
```

### Add Funds to Wallet

```http
POST /api/wallet/{wallet_id}/add
```

**Request Body:**
```json
{
  "amount": 0.68,
  "kwh_saved": 2.0,
  "session_id": "session_20251207_18"
}
```

### Get Transaction History

```http
GET /api/wallet/{wallet_id}/transactions
```

---

## Savings Session API

### Check Active Session

```http
GET /api/sessions/active
```

**Response (Active):**
```json
{
  "success": true,
  "active": true,
  "session": {
    "id": "session_20251207_18",
    "status": "active",
    "start_time": "2025-12-07T17:00:00",
    "end_time": "2025-12-07T19:00:00",
    "is_double_points": false
  }
}
```

**Response (No Active Session):**
```json
{
  "success": true,
  "active": false,
  "next_session": {
    "start": "2025-12-08T17:00:00"
  }
}
```

### Join Session

```http
POST /api/sessions/{session_id}/join
```

**Request Body:**
```json
{
  "user_id": "user123",
  "wallet_id": "wallet_uuid"
}
```

**Response:**
```json
{
  "success": true,
  "participant": {
    "user_id": "user123",
    "baseline_kwh": 2.5,
    "joined_at": "2025-12-07T17:15:00"
  },
  "tips": [
    "Αναβάλετε τη χρήση του πλυντηρίου",
    "Κλείστε τον θερμοσίφωνα"
  ]
}
```

### Complete Session

```http
POST /api/sessions/{session_id}/complete
```

**Request Body:**
```json
{
  "user_id": "user123",
  "actual_kwh": 0.5
}
```

**Response:**
```json
{
  "success": true,
  "result": {
    "kwh_saved": 2.0,
    "eur_earned": 0.68,
    "is_double_points": false,
    "message": "Μπράβο! Κέρδισες €0.68 στο Waste Wallet σου!"
  }
}
```

---

## Payment API

### Auto-Transfer to Municipality

Monthly automatic transfer of wallet balance to municipality.

```http
POST /api/payments/auto-transfer
```

**Request Body:**
```json
{
  "wallet_id": "wallet_uuid"
}
```

**Response:**
```json
{
  "success": true,
  "payment": {
    "id": "uuid",
    "amount": 22.50,
    "receipt_number": "PS-202512-ABC123",
    "status": "completed"
  },
  "message": "Πληρώθηκε έναντι Τελών Σκυβάλων: €22.50",
  "new_balance": 0,
  "total_paid": 45.00,
  "remaining": 140.00
}
```

### Get Payment History

```http
GET /api/payments/{wallet_id}/history
```

---

## Surplus Handling API

### Handle Surplus

When user has paid more than annual target.

```http
POST /api/surplus/handle
```

**Request Body:**
```json
{
  "wallet_id": "wallet_uuid",
  "action": "rollover"  // or "donate"
}
```

**Response (Rollover):**
```json
{
  "success": true,
  "action": "rollover",
  "surplus_amount": 15.00,
  "message": "€15.00 μεταφέρθηκε για τα τέλη του 2026",
  "new_year": 2026
}
```

**Response (Donate):**
```json
{
  "success": true,
  "action": "donate",
  "donation_amount": 15.00,
  "donation_id": "uuid",
  "message": "€15.00 δωρήθηκε στο Κοινωνικό Ταμείο"
}
```

---

## Double Points API

### Check Status

```http
GET /api/double-points/status
```

**Response:**
```json
{
  "success": true,
  "is_double_points": true,
  "multiplier": 2.0,
  "reason": "Σαββατοκύριακο - Διπλοί Πόντοι!",
  "next_double_day": "2025-12-14"
}
```

---

## Energy Tips API

### Get All Tips

```http
GET /api/tips
```

### Get Tips by Category

```http
GET /api/tips/{category}
```

**Categories:** `thermosifonas`, `klimatistiko`, `fournos`, `plyntirio`

---

## FAQ API

### Get All FAQ

```http
GET /api/faq
```

### Filter by Category

```http
GET /api/faq?category=surplus
```

**Categories:** `surplus`, `billing`, `algorithm`, `rewards`, `payments`

---

## Annual Goal API

### Get Goal Progress

```http
GET /api/goal/{wallet_id}
```

**Response:**
```json
{
  "success": true,
  "goal": {
    "annual_target": 185.00,
    "total_paid": 46.25,
    "remaining": 138.75,
    "progress_percent": 25.0,
    "expected_progress": 91.7,
    "on_track": false,
    "monthly_target": 15.42,
    "year": 2025
  },
  "municipality": {
    "name": "Δήμος Λευκωσίας"
  }
}
```

---

## Receipts API

### Get Receipt

```http
GET /api/receipts/{payment_id}
```

**Response:**
```json
{
  "success": true,
  "receipt": {
    "receipt_number": "PS-202512-ABC123",
    "payment_date": "2025-12-01T00:00:00",
    "amount": 22.50,
    "recipient": {
      "name": "Δήμος Λευκωσίας",
      "type": "Municipal Waste Fees"
    },
    "status": "PAID"
  }
}
```

---

## Notifications API

### Subscribe to Notifications

```http
POST /api/notifications/subscribe
```

**Request Body:**
```json
{
  "user_id": "user123",
  "device_token": "fcm_token",
  "device_type": "android"
}
```

### Get User Notifications

```http
GET /api/notifications/{user_id}?limit=20&offset=0
```

### Mark as Read

```http
PUT /api/notifications/{notification_id}/read
```

### Trigger Session Alert (Admin)

```http
POST /api/notifications/trigger/session-start
```

---

## Calculation Logic

### kWh to EUR Conversion

```
EUR = kWh_saved × KWH_TO_EUR_RATE × multiplier

Where:
- KWH_TO_EUR_RATE = €0.34 per kWh
- multiplier = 2.0 on Double Points Days, 1.0 otherwise
```

### Baseline Algorithm

The baseline is calculated as the average consumption of the last 10 days:

```
baseline = sum(last_10_days_consumption) / 10
```

### Savings Calculation

```
kWh_saved = max(0, baseline - actual_consumption)
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `404` - Resource Not Found
- `500` - Internal Server Error

---

## Rate Limits

| Endpoint Type | Limit |
|--------------|-------|
| Read (GET) | 100 req/min |
| Write (POST/PUT) | 30 req/min |
| Session Operations | 10 req/min |

---

## Webhooks (Coming Soon)

Municipalities can register webhooks to receive:
- Payment notifications
- Monthly reports
- User registrations

---

## Contact

For API support and municipality integration:
- Email: api@powersave.cy
- Documentation: https://docs.powersave.cy
