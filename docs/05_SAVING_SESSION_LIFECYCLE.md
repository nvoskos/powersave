# ⚡ Saving Session Lifecycle

## Επισκόπηση

Το **Saving Session** είναι η καρδιά του PowerSave - ο μηχανισμός που μετατρέπει την εξοικονόμηση ενέργειας σε χρηματική αξία.

---

## Lifecycle Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                    SAVING SESSION LIFECYCLE                          │
└──────────────────────────────────────────────────────────────────────┘

 User Action              Automated                    Automated
     │                        │                            │
     ▼                        ▼                            ▼
┌─────────┐            ┌─────────────┐              ┌─────────────┐
│   1.    │            │     2.      │              │     3.      │
│SCHEDULING│──────────▶│SESSION START│─────────────▶│ SESSION END │
└─────────┘            └─────────────┘              └─────────────┘
     │                        │                            │
     │                        │                            │
     ▼                        ▼                            ▼
┌─────────────┐        ┌─────────────┐              ┌─────────────┐
│  SCHEDULED  │        │ IN_PROGRESS │              │  COMPLETED  │
│   status    │        │   status    │              │   status    │
└─────────────┘        └─────────────┘              └─────────────┘
     │                        │                            │
     │                        │                            │
     ▼                        ▼                            ▼
 2 Celery jobs           Baseline                    Final calcs
 queued (start/end)     calculated                   + Gamification
                                                     + Push notification
```

---

## Step 1: SCHEDULING (User Action)

### Τι συμβαίνει

Ο χρήστης ανοίγει την εφαρμογή και επιλέγει το χρονικό παράθυρο για εξοικονόμηση.

### User Flow

```
1. User opens app
2. Taps "New Saving Session"
3. Selects time window (e.g., 17:00 - 20:00)
4. Confirms scheduling
5. Sees confirmation screen
```

### API Call

```http
POST /sessions
{
  "startTime": "2025-01-15T17:00:00Z",
  "endTime": "2025-01-15T20:00:00Z"
}
```

### Backend Processing

```python
# routers/sessions.py
@router.post("/sessions")
async def create_session(session_data: SessionCreate, user: User = Depends(get_current_user)):
    # 1. Validate time window
    validate_time_window(session_data.startTime, session_data.endTime)
    
    # 2. Check for overlapping sessions
    check_no_overlap(user.user_id, session_data.startTime, session_data.endTime)
    
    # 3. Create session record
    session = SavingSession(
        user_id=user.user_id,
        scheduled_start=session_data.startTime,
        scheduled_end=session_data.endTime,
        status="SCHEDULED"
    )
    db.add(session)
    db.commit()
    
    # 4. Queue Celery jobs
    schedule_session_start.apply_async(
        args=[session.session_id],
        eta=session_data.startTime
    )
    schedule_session_end.apply_async(
        args=[session.session_id],
        eta=session_data.endTime
    )
    
    return session
```

### Database State

```sql
INSERT INTO saving_session (session_id, user_id, status, scheduled_start, scheduled_end)
VALUES ('uuid', 'user-uuid', 'SCHEDULED', '2025-01-15 17:00:00', '2025-01-15 20:00:00');
```

### Celery Queue

Δύο jobs προστίθενται στο Redis queue:
1. **session_start_job** - ETA: 17:00
2. **session_end_job** - ETA: 20:00

---

## Step 2: SESSION START (Automated)

### Τι συμβαίνει

Στην προγραμματισμένη ώρα έναρξης, ο Celery worker εκτελεί το session start job.

### Celery Task

```python
# tasks/session_start.py
@celery_app.task
def schedule_session_start(session_id: str):
    session = get_session(session_id)
    
    # 1. Fetch historical smart meter data
    historical_data = ahk_api.get_historical_usage(
        account_number=session.user.ahk_account_number,
        days=30,
        hour_of_day=session.scheduled_start.hour,
        day_of_week=session.scheduled_start.weekday()
    )
    
    # 2. Calculate baseline
    baseline_kwh = calculate_baseline(historical_data)
    
    # 3. Update session
    session.status = "IN_PROGRESS"
    session.actual_start = datetime.utcnow()
    session.baseline_kwh = baseline_kwh
    session.baseline_calculation_method = "ROLLING_AVERAGE_30D"
    db.commit()
    
    # 4. Send push notification
    send_push(session.user_id, "🟢 Your saving session has started!")
```

### Baseline Calculation Algorithm

```python
# services/baseline.py
def calculate_baseline(historical_data: List[UsageRecord]) -> Decimal:
    """
    Advanced statistical analysis για fair baseline calculation.
    
    Factors considered:
    - Rolling 30-day average
    - Same hour of day
    - Same day of week
    - Seasonal adjustments
    - Weather correlation
    - Anomaly filtering (vacation, outages)
    """
    
    # 1. Filter anomalies (usage 2+ std deviations from mean)
    filtered_data = filter_anomalies(historical_data)
    
    # 2. Weight recent data more heavily
    weighted_data = apply_time_weights(filtered_data)
    
    # 3. Apply seasonal adjustment
    season_factor = get_seasonal_factor(datetime.now().month)
    
    # 4. Apply weather adjustment
    weather_factor = get_weather_factor(
        current_temp=weather_api.get_current_temp(),
        historical_avg_temp=weather_api.get_historical_avg()
    )
    
    # 5. Calculate final baseline
    raw_baseline = weighted_average(weighted_data)
    adjusted_baseline = raw_baseline * season_factor * weather_factor
    
    return Decimal(adjusted_baseline).quantize(Decimal('0.0001'))
```

### Trust & Fairness

| Factor | Περιγραφή | Impact |
|--------|-----------|--------|
| **Anomaly Filtering** | Αφαιρεί μέρες διακοπών, βλάβες | ±15% |
| **Seasonal Adjustment** | Καλοκαίρι vs Χειμώνας | ±20% |
| **Weather Correlation** | Θερμοκρασία ημέρας | ±10% |
| **Day-of-Week** | Weekday vs Weekend patterns | ±12% |

### Database State

```sql
UPDATE saving_session SET
    status = 'IN_PROGRESS',
    actual_start = '2025-01-15 17:00:05',
    baseline_kwh = 4.2500,
    baseline_calculation_method = 'ROLLING_AVERAGE_30D'
WHERE session_id = 'uuid';
```

---

## Step 3: SESSION END (Automated)

### Τι συμβαίνει

Στην προγραμματισμένη ώρα λήξης, ο Celery worker εκτελεί τους τελικούς υπολογισμούς.

### Celery Task

```python
# tasks/session_end.py
@celery_app.task
def schedule_session_end(session_id: str):
    session = get_session(session_id)
    
    # 1. Fetch actual consumption
    actual_kwh = ahk_api.get_actual_usage(
        account_number=session.user.ahk_account_number,
        start_time=session.actual_start,
        end_time=datetime.utcnow()
    )
    
    # 2. Calculate savings
    saved_kwh = max(0, session.baseline_kwh - actual_kwh)
    saved_eur = saved_kwh * TARIFF_RATE  # €0.34/kWh
    saved_co2_kg = saved_kwh * EMISSION_FACTOR  # 0.65 kg/kWh
    
    # 3. Update session
    session.status = "COMPLETED"
    session.actual_end = datetime.utcnow()
    session.actual_kwh = actual_kwh
    session.saved_kwh = saved_kwh
    session.saved_eur = saved_eur
    session.saved_co2_kg = saved_co2_kg
    session.completed_at = datetime.utcnow()
    
    # 4. Run gamification engine
    green_points = gamification_engine.calculate_points(session)
    badges_earned = gamification_engine.check_badges(session)
    challenges_updated = gamification_engine.update_challenges(session)
    
    session.green_points_earned = green_points
    
    # 5. Update user totals
    user = session.user
    user.total_kwh_saved += saved_kwh
    user.total_eur_saved += saved_eur
    user.total_co2_saved += saved_co2_kg
    user.green_points_balance += green_points
    user.waste_wallet_balance += saved_eur
    
    # 6. Create wallet transaction
    create_wallet_transaction(user.user_id, "CREDIT", saved_eur, session.session_id)
    
    db.commit()
    
    # 7. Send push notification
    send_rich_notification(
        user_id=session.user_id,
        title="🎉 Session Complete!",
        body=f"You saved {saved_kwh:.2f} kWh = €{saved_eur:.2f}",
        data={
            "session_id": session_id,
            "saved_kwh": float(saved_kwh),
            "saved_eur": float(saved_eur),
            "green_points": green_points,
            "badges": badges_earned
        }
    )
```

### Conversion Factors

| Factor | Value | Source |
|--------|-------|--------|
| **TARIFF_RATE** | €0.34/kWh | [ΑΗΚ Τιμολόγια](https://www.eac.com.cy/EL/RegulatedActivities/Supply/tariffs) |
| **EMISSION_FACTOR** | 0.65 kg CO₂/kWh | Cyprus Grid Average |

### Savings Calculation

```python
# Example calculation
baseline_kwh = 4.25      # Expected consumption
actual_kwh = 2.55        # What user actually used
saved_kwh = 4.25 - 2.55  # = 1.70 kWh

saved_eur = 1.70 * 0.34  # = €0.578
saved_co2_kg = 1.70 * 0.65  # = 1.105 kg
```

### Gamification Engine

```python
# services/gamification.py
def calculate_points(session: SavingSession) -> int:
    """
    Green Points calculation:
    - Base: 10 points per kWh saved
    - Streak bonus: +50% for consecutive days
    - Peak hour bonus: +25% during 17:00-20:00
    """
    base_points = int(session.saved_kwh * 10)
    
    # Streak bonus
    streak_days = get_streak_days(session.user_id)
    streak_multiplier = min(1.5, 1 + (streak_days * 0.05))
    
    # Peak hour bonus
    peak_bonus = 1.25 if is_peak_hour(session.actual_start) else 1.0
    
    total_points = int(base_points * streak_multiplier * peak_bonus)
    return total_points

def check_badges(session: SavingSession) -> List[str]:
    """Check and award any newly earned badges."""
    earned = []
    user = session.user
    
    # First session badge
    if user.total_sessions == 1:
        award_badge(user.user_id, "first_session")
        earned.append("first_session")
    
    # Streak badges
    streak = get_streak_days(user.user_id)
    if streak == 7 and not has_badge(user.user_id, "week_streak"):
        award_badge(user.user_id, "week_streak")
        earned.append("week_streak")
    
    # Savings milestones
    if user.total_kwh_saved >= 100 and not has_badge(user.user_id, "century_saver"):
        award_badge(user.user_id, "century_saver")
        earned.append("century_saver")
    
    return earned
```

### Database State (Final)

```sql
UPDATE saving_session SET
    status = 'COMPLETED',
    actual_end = '2025-01-15 20:00:03',
    actual_kwh = 2.5500,
    saved_kwh = 1.7000,
    saved_eur = 0.5780,
    saved_co2_kg = 1.1050,
    green_points_earned = 21,
    completed_at = '2025-01-15 20:00:03'
WHERE session_id = 'uuid';

-- Update user totals
UPDATE "user" SET
    total_kwh_saved = total_kwh_saved + 1.7000,
    total_eur_saved = total_eur_saved + 0.5780,
    total_co2_saved = total_co2_saved + 1.1050,
    green_points_balance = green_points_balance + 21,
    waste_wallet_balance = waste_wallet_balance + 0.5780
WHERE user_id = 'user-uuid';

-- Create wallet transaction
INSERT INTO wallet_transaction (user_id, type, amount, balance_after, session_id)
VALUES ('user-uuid', 'CREDIT', 0.5780, 38.50, 'session-uuid');
```

---

## Step 4: USER REVIEW

### Τι βλέπει ο χρήστης

Ο χρήστης λαμβάνει push notification και μπορεί να δει τα αποτελέσματα στην εφαρμογή.

### Push Notification

```
🎉 Session Complete!
━━━━━━━━━━━━━━━━━━━
You saved 1.70 kWh = €0.58

⚡ Energy saved: 1.70 kWh
💰 Money earned: €0.58
🌱 CO₂ prevented: 1.11 kg
🌟 Points earned: 21

[View Details]
```

### App Dashboard Update

```json
{
  "wasteWalletBalance": 38.50,
  "percentagePaidOff": 19.74,
  "greenPointsBalance": 1271,
  "latestSession": {
    "savedKwh": 1.70,
    "savedEur": 0.58,
    "pointsEarned": 21
  },
  "streak": 5,
  "nextMilestone": {
    "badge": "week_streak",
    "daysRemaining": 2
  }
}
```

---

## Error Handling

### Possible Failures

| Error | Cause | Resolution |
|-------|-------|------------|
| METER_DATA_UNAVAILABLE | ΑΗΚ API timeout | Retry 3x, then mark FAILED |
| BASELINE_CALCULATION_ERROR | Insufficient historical data | Use fallback baseline |
| SESSION_OVERLAP | User scheduled overlapping session | Reject at scheduling |

### Failure Recovery

```python
@celery_app.task(bind=True, max_retries=3)
def schedule_session_end(self, session_id: str):
    try:
        # ... main logic ...
    except AHKAPIError as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    except Exception as e:
        # Mark session as failed
        session = get_session(session_id)
        session.status = "FAILED"
        session.error_message = str(e)
        db.commit()
        
        # Notify user
        send_push(session.user_id, "❌ Session could not be completed. Please contact support.")
```

---

## Performance Considerations

| Metric | Target | Monitoring |
|--------|--------|------------|
| Baseline calculation time | < 2 seconds | Prometheus histogram |
| End-to-end processing | < 10 seconds | Celery task duration |
| Push notification delivery | < 5 seconds | Firebase analytics |
| Concurrent sessions | 10,000+ | Load testing |

---

*Για deployment instructions, δείτε [Deployment Guide](./06_DEPLOYMENT.md)*
