# 🗄️ Database Schema

## Επισκόπηση

Το PowerSave χρησιμοποιεί **PostgreSQL** ως primary database. Το schema είναι σχεδιασμένο για:
- High-volume transaction processing
- Efficient querying για analytics
- Data integrity για financial calculations

---

## Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────────┐
│    User     │───────│  SavingSession   │       │  PlantCatalog   │
└─────────────┘       └──────────────────┘       └─────────────────┘
      │                                                   │
      │       ┌──────────────────┐                       │
      ├───────│ UserPlantedItem  │───────────────────────┘
      │       └──────────────────┘
      │
      │       ┌──────────────────┐       ┌─────────────────┐
      ├───────│UserChallengeProgress│────│    Challenge    │
      │       └──────────────────┘       └─────────────────┘
      │
      │       ┌──────────────────┐       ┌─────────────────┐
      └───────│    UserBadge     │───────│     Badge       │
              └──────────────────┘       └─────────────────┘
```

---

## Core Tables

### User

Κεντρικός πίνακας για όλους τους χρήστες της πλατφόρμας.

```sql
CREATE TABLE "user" (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ahk_account_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    
    -- Gamification
    green_points_balance INTEGER DEFAULT 0,
    total_kwh_saved DECIMAL(10,2) DEFAULT 0,
    total_eur_saved DECIMAL(10,2) DEFAULT 0,
    total_co2_saved DECIMAL(10,2) DEFAULT 0,
    
    -- Waste Wallet
    waste_wallet_balance DECIMAL(10,2) DEFAULT 0,
    annual_waste_fee DECIMAL(10,2),
    
    -- Metadata
    is_active BOOLEAN DEFAULT true,
    is_vulnerable_household BOOLEAN DEFAULT false,
    municipality_id UUID REFERENCES municipality(municipality_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

CREATE INDEX idx_user_account ON "user"(ahk_account_number);
CREATE INDEX idx_user_municipality ON "user"(municipality_id);
```

| Column | Type | Description |
|--------|------|-------------|
| user_id | UUID | Primary key |
| ahk_account_number | VARCHAR(20) | ΑΗΚ account number (unique) |
| green_points_balance | INTEGER | Current green points |
| waste_wallet_balance | DECIMAL | € accumulated for waste fee |
| is_vulnerable_household | BOOLEAN | Για Social Energy Solidarity |

---

### SavingSession

Κάθε saving session που δημιουργείται από χρήστη.

```sql
CREATE TABLE saving_session (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(user_id),
    
    -- Status
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    -- SCHEDULED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    
    -- Timing
    scheduled_start TIMESTAMP NOT NULL,
    scheduled_end TIMESTAMP NOT NULL,
    actual_start TIMESTAMP,
    actual_end TIMESTAMP,
    
    -- Baseline
    baseline_kwh DECIMAL(10,4),
    baseline_calculation_method VARCHAR(50),
    
    -- Results
    actual_kwh DECIMAL(10,4),
    saved_kwh DECIMAL(10,4),
    saved_eur DECIMAL(10,4),
    saved_co2_kg DECIMAL(10,4),
    
    -- Gamification
    green_points_earned INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT
);

CREATE INDEX idx_session_user ON saving_session(user_id);
CREATE INDEX idx_session_status ON saving_session(status);
CREATE INDEX idx_session_scheduled ON saving_session(scheduled_start);
```

| Column | Type | Description |
|--------|------|-------------|
| status | VARCHAR | SCHEDULED → IN_PROGRESS → COMPLETED/FAILED |
| baseline_kwh | DECIMAL | Calculated baseline consumption |
| saved_kwh | DECIMAL | actual - baseline (if positive) |
| saved_eur | DECIMAL | saved_kwh × tariff rate |
| saved_co2_kg | DECIMAL | saved_kwh × emission factor |

---

### PlantCatalog

Κατάλογος διαθέσιμων φυτών για το Green Garden.

```sql
CREATE TABLE plant_catalog (
    plant_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    cost_in_green_points INTEGER NOT NULL,
    growth_stages INTEGER DEFAULT 5,
    image_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Data:**
| plant_id | name | cost_in_green_points | growth_stages |
|----------|------|---------------------|---------------|
| sunflower | Sunflower | 100 | 5 |
| olive_tree | Cyprus Olive Tree | 500 | 7 |
| rose | Rose Bush | 150 | 4 |
| cactus | Cactus | 75 | 3 |
| lemon_tree | Lemon Tree | 400 | 6 |

---

### UserPlantedItem

Φυτά που έχει φυτέψει ο χρήστης στον κήπο του.

```sql
CREATE TABLE user_planted_item (
    planted_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(user_id),
    plant_id VARCHAR(50) NOT NULL REFERENCES plant_catalog(plant_id),
    
    -- Position in garden grid
    position_x INTEGER NOT NULL,
    position_y INTEGER NOT NULL,
    
    -- Growth
    current_growth_stage INTEGER DEFAULT 1,
    last_watered_at TIMESTAMP,
    
    -- Metadata
    planted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, position_x, position_y)
);

CREATE INDEX idx_planted_user ON user_planted_item(user_id);
```

---

### Challenge

Ορισμοί challenges για gamification.

```sql
CREATE TABLE challenge (
    challenge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Goal
    goal_type VARCHAR(50) NOT NULL,
    -- TOTAL_KWH_SAVED, SESSION_COUNT, CONSECUTIVE_DAYS, COMMUNITY_GOAL
    goal_value DECIMAL(10,2) NOT NULL,
    
    -- Duration
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    -- Rewards
    reward_green_points INTEGER DEFAULT 0,
    reward_badge_id VARCHAR(50) REFERENCES badge(badge_id),
    
    -- Scope
    scope VARCHAR(20) DEFAULT 'INDIVIDUAL',
    -- INDIVIDUAL, COMMUNITY, SCHOOL, CORPORATE
    community_id UUID,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_challenge_dates ON challenge(start_date, end_date);
CREATE INDEX idx_challenge_active ON challenge(is_active);
```

| goal_type | Περιγραφή | Παράδειγμα |
|-----------|-----------|------------|
| TOTAL_KWH_SAVED | Σύνολο kWh εξοικονόμησης | Save 50 kWh |
| SESSION_COUNT | Αριθμός sessions | Complete 20 sessions |
| CONSECUTIVE_DAYS | Συνεχόμενες ημέρες | 7-day streak |
| COMMUNITY_GOAL | Ομαδικός στόχος | Neighborhood saves 1000 kWh |

---

### UserChallengeProgress

Πρόοδος χρήστη σε κάθε challenge.

```sql
CREATE TABLE user_challenge_progress (
    progress_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(user_id),
    challenge_id UUID NOT NULL REFERENCES challenge(challenge_id),
    
    -- Progress
    current_value DECIMAL(10,2) DEFAULT 0,
    status VARCHAR(20) DEFAULT 'IN_PROGRESS',
    -- IN_PROGRESS, COMPLETED, EXPIRED
    
    -- Metadata
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    UNIQUE(user_id, challenge_id)
);

CREATE INDEX idx_progress_user ON user_challenge_progress(user_id);
CREATE INDEX idx_progress_challenge ON user_challenge_progress(challenge_id);
```

---

### Badge

Metadata για badges.

```sql
CREATE TABLE badge (
    badge_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    category VARCHAR(50),
    -- BEGINNER, ACHIEVEMENT, STREAK, COMMUNITY, SPECIAL
    rarity VARCHAR(20) DEFAULT 'COMMON',
    -- COMMON, RARE, EPIC, LEGENDARY
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Sample Badges:**
| badge_id | name | category | rarity |
|----------|------|----------|--------|
| first_session | First Step | BEGINNER | COMMON |
| week_streak | Weekly Warrior | STREAK | RARE |
| month_streak | Monthly Master | STREAK | EPIC |
| community_hero | Community Hero | COMMUNITY | EPIC |
| green_champion | Green Champion | ACHIEVEMENT | LEGENDARY |

---

### UserBadge

Join table για earned badges.

```sql
CREATE TABLE user_badge (
    user_badge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(user_id),
    badge_id VARCHAR(50) NOT NULL REFERENCES badge(badge_id),
    
    -- Metadata
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    earning_session_id UUID REFERENCES saving_session(session_id),
    earning_challenge_id UUID REFERENCES challenge(challenge_id),
    
    UNIQUE(user_id, badge_id)
);

CREATE INDEX idx_user_badge_user ON user_badge(user_id);
```

---

## Supporting Tables

### Municipality

```sql
CREATE TABLE municipality (
    municipality_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    district VARCHAR(50),
    annual_waste_fee DECIMAL(10,2),
    bank_account VARCHAR(50),
    is_active BOOLEAN DEFAULT true
);
```

### WalletTransaction

```sql
CREATE TABLE wallet_transaction (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES "user"(user_id),
    type VARCHAR(20) NOT NULL,
    -- CREDIT (from savings), DEBIT (payment), DONATION
    amount DECIMAL(10,2) NOT NULL,
    balance_after DECIMAL(10,2) NOT NULL,
    
    -- Reference
    session_id UUID REFERENCES saving_session(session_id),
    donation_recipient_id UUID,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_wallet_user ON wallet_transaction(user_id);
CREATE INDEX idx_wallet_date ON wallet_transaction(created_at);
```

### SocialEnergyFund

```sql
CREATE TABLE social_energy_fund (
    fund_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    municipality_id UUID REFERENCES municipality(municipality_id),
    balance DECIMAL(12,2) DEFAULT 0,
    total_donations DECIMAL(12,2) DEFAULT 0,
    total_disbursements DECIMAL(12,2) DEFAULT 0,
    households_helped INTEGER DEFAULT 0
);
```

---

## Indexes Summary

| Table | Index | Columns | Purpose |
|-------|-------|---------|---------|
| user | idx_user_account | ahk_account_number | Fast login lookup |
| saving_session | idx_session_user | user_id | User history queries |
| saving_session | idx_session_status | status | Status filtering |
| user_challenge_progress | idx_progress_user | user_id | User challenges |
| wallet_transaction | idx_wallet_date | created_at | Transaction history |

---

## Data Retention

| Data Type | Retention Period |
|-----------|------------------|
| Saving Sessions | 5 years |
| Wallet Transactions | 7 years (legal) |
| User Activity Logs | 2 years |
| Smart Meter Data | 3 years |

---

*Για το lifecycle των sessions, δείτε [Saving Session Lifecycle](./05_SAVING_SESSION_LIFECYCLE.md)*
