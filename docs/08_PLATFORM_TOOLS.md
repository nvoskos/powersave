# 🛠️ Platform Tools

## Επισκόπηση

Το PowerSave περιλαμβάνει **8 κύρια εργαλεία** που καλύπτουν διαφορετικές ανάγκες και κοινά-στόχους.

---

## 1. 💰 Waste Fee Offset

### Περιγραφή
Το κεντρικό εργαλείο που μετατρέπει την εξοικονόμηση ενέργειας σε πληρωμή δημοτικών τελών σκυβάλων.

### Πώς Λειτουργεί

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Saving Session │────▶│   Calculation   │────▶│  Waste Wallet   │
│   (User saves)  │     │  €0.34 × kWh    │     │   (€ credited)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │   Annual Fee    │
                                                │   Reduction     │
                                                └─────────────────┘
```

### Μετρικές

| Στοιχείο | Τιμή |
|----------|------|
| Ετήσια τέλη σκυβάλων | €180 - €230 |
| Τιμή kWh | €0.34 |
| Απαιτούμενη εξοικονόμηση | ~1.85 kWh/ημέρα |
| Στόχος | 100% κάλυψη τελών |

### User Journey

1. Χρήστης προγραμματίζει Saving Session
2. Εξοικονομεί ενέργεια κατά τη διάρκεια
3. Τα € πιστώνονται αυτόματα στο Waste Wallet
4. Στο τέλος του έτους, offset τελών σκυβάλων

---

## 2. ☀️ Solar Sync

### Περιγραφή
Ειδοποιήσεις και προτάσεις για βέλτιστη χρήση φωτοβολταϊκών συστημάτων.

### Features

| Feature | Περιγραφή |
|---------|-----------|
| **Peak Production Alerts** | Ειδοποίηση όταν η παραγωγή είναι υψηλή |
| **Load Shifting Tips** | Προτάσεις για μεταφορά κατανάλωσης |
| **Self-Consumption Score** | Ποσοστό αυτοκατανάλωσης |
| **Export Tracking** | Παρακολούθηση εξαγωγής στο δίκτυο |

### Notification Examples

```
☀️ High Solar Alert!
Your panels are producing 4.2 kW right now.
Great time to run the washing machine!

📊 Weekly Solar Report
Self-consumption: 67%
Grid export: 45 kWh
Estimated savings: €15.30
```

### Integration

- Σύνδεση με inverter APIs (Fronius, SMA, Huawei)
- Real-time production data
- Weather forecast integration

---

## 3. 👥 Community Groups

### Περιγραφή
Διαγωνισμοί εξοικονόμησης μεταξύ σχολείων, γειτονιών και ομάδων.

### Group Types

| Τύπος | Παράδειγμα | Μέγεθος |
|-------|------------|---------|
| **Neighborhood** | Έγκωμη, Στρόβολος | 100-500 |
| **School** | Δημοτικό Σχολείο Α' | 200-1000 |
| **Workplace** | ΑΗΚ Employees | 50-500 |
| **Custom** | "Green Warriors" | 10-100 |

### Leaderboard

```
🏆 Nicosia Neighborhood Challenge - Week 3

 #   Group              kWh Saved   Members
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 1   Strovolos North      1,250      127
 2   Engomi Central       1,180      98
 3   Lakatamia West       1,050      145
 4   Agios Dometios         890      76
 5   Pallouriotissa         820      82
```

### Competition Mechanics

- Weekly/Monthly challenges
- Per-capita normalization
- Streak bonuses
- Community rewards pool

---

## 4. 🏢 Corporate ESG Dashboard

### Περιγραφή
Εργαλείο για εταιρείες να συμμετέχουν και να παρακολουθούν την ESG επίδοσή τους.

### Dashboard Metrics

| Metric | Description |
|--------|-------------|
| **Total kWh Saved** | Συνολική εξοικονόμηση εργαζομένων |
| **CO₂ Avoided** | Τόνοι CO₂ που αποφεύχθηκαν |
| **Participation Rate** | % εργαζομένων που συμμετέχουν |
| **Community Impact** | Νοικοκυριά που υποστηρίχθηκαν |

### Features

```
┌─────────────────────────────────────────────────────────┐
│            ACME Corp ESG Dashboard                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📊 Q4 2024 Performance                                  │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━                │
│  Total Employees Enrolled: 245/300 (82%)                 │
│  Total kWh Saved: 12,500 kWh                            │
│  CO₂ Prevented: 8.1 tonnes                              │
│  Social Fund Contribution: €850                          │
│                                                          │
│  🎯 Active Challenges                                    │
│  • "Winter Energy Warriors" - 15 days remaining          │
│  • Department vs Department - Finance leading!           │
│                                                          │
│  📄 Export for ESG Report                   [Download]   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Matching Donations

Η εταιρεία μπορεί να κάνει match τις δωρεές των εργαζομένων:
- Employee donates €10 → Company matches €10 → €20 total to Social Fund

---

## 5. 💝 Social Energy Solidarity

### Περιγραφή
Δυνατότητα δωρεάς εξοικονομήσεων από το Waste Wallet σε ευάλωτα νοικοκυριά.

### Mechanism

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────────┐
│ User Wallet │──────▶│  Social Energy   │──────▶│   Vulnerable    │
│  (Donate)   │       │      Fund        │       │   Household     │
└─────────────┘       └──────────────────┘       └─────────────────┘
```

### Fund Distribution

| Criterion | Weight |
|-----------|--------|
| Income level | 40% |
| Energy consumption vs. baseline | 30% |
| Household composition | 20% |
| Geographic area | 10% |

### Transparency

- Real-time fund balance visible
- Quarterly impact reports
- Anonymized beneficiary statistics

### ΕΣΕΚ Alignment

Υποστηρίζει το **Μέτρο 18** του ΕΣΕΚ:
> 15.1% της εθνικής εξοικονόμησης πρέπει να προέρχεται από ευάλωτα νοικοκυριά

---

## 6. 🎯 Purpose-Driven Groups

### Περιγραφή
Ομάδες που συγκεντρώνουν εξοικονομήσεις για συγκεκριμένο τοπικό project.

### Examples

| Project | Goal | Progress |
|---------|------|----------|
| "AC για το Δημοτικό μας" | €2,500 | 67% |
| "Ηλιακός φωτισμός πάρκου" | €1,200 | 89% |
| "Ψυγείο για κοινοτικό κέντρο" | €800 | 100% ✓ |

### How It Works

```
1. Δημιουργία Project
   └── Define goal, deadline, beneficiary

2. Recruitment
   └── Invite neighbors, friends, colleagues

3. Collective Saving
   └── Each member's savings contribute to pool

4. Achievement
   └── When goal reached, purchase/donation made

5. Celebration
   └── Recognition, badges, local media coverage
```

### Verification

- Municipality approval for public projects
- Receipts and documentation required
- Photo/video of completed project

---

## 7. 👶 PowerSave Kids

### Περιγραφή
Kids Mode στην εφαρμογή με gamification για παιδιά - το "Green Trojan Horse".

### Target Audience

| Age Group | Program | Features |
|-----------|---------|----------|
| 4-7 | Little Guardians | Simple badges, Fotis mascot |
| 8-12 | Energy Agents | Missions, home inspections |
| 13-17 | Green Leaders | Projects, community impact |

### Mascot: Fotis 🔋

Ο Fotis είναι ο ενεργειακός φύλακας - μια φιλική μασκότ που:
- Δίνει tips για εξοικονόμηση
- Επιβραβεύει τα παιδιά
- Μαθαίνει μέσα από παιχνίδια

### School Integration

```
┌─────────────────────────────────────────────────────────┐
│            Little Guardians Classroom                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🌱 Class Green Garden                                   │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━                               │
│  🌻🌻🌻🌳🌳🌷🌷🌷                                        │
│                                                          │
│  📊 This Week's Energy Agents                           │
│  ⭐ Maria K. - 5 home inspections                       │
│  ⭐ Yiannis A. - Turned off 12 lights                   │
│  ⭐ Elena P. - Unplugged 8 devices                      │
│                                                          │
│  🏆 Class Ranking: #3 in Nicosia                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Pester Power Mechanism

Τα παιδιά γίνονται "εσωτερικοί ενεργειακοί επιθεωρητές":
- Ελέγχουν αν οι γονείς κλείνουν τα φώτα
- Αναφέρουν standby συσκευές
- Κερδίζουν badges για κάθε "inspection"
- Οι γονείς πρέπει να συμμετέχουν για να ξεκλειδώσουν rewards

### KPIs for 2026-2027

| Metric | Target |
|--------|--------|
| Participating schools | 100 |
| Active children | 20,000 |
| Home inspections | 50,000 |
| Engaged households | 50,000 |

---

## 8. 🏦 On-Bill Clearinghouse

### Περιγραφή
Κεντρικό σύστημα συμψηφισμού που διασφαλίζει τη ροή χρημάτων μεταξύ ΑΗΚ, Δήμου και χρήστη.

### The Problem It Solves

```
Without Clearinghouse:
───────────────────────
User saves €10 → Utility loses €10 → Municipality never gets paid

With Clearinghouse:
───────────────────────
User saves €10 → Utility charges "PowerSave Transfer" €10 → 
Municipality receives €10 → User's Waste Fee reduced by €10
```

### Money Flow

```
┌──────────────┐                      ┌──────────────┐
│     User     │                      │ Municipality │
│              │                      │              │
│ Electricity  │      On-Bill         │  Waste Fee   │
│    Bill      │◀────Clearinghouse───▶│   Account    │
│              │                      │              │
└──────┬───────┘                      └──────────────┘
       │
       │ €10 savings
       ▼
┌──────────────┐
│   Utility    │
│    (ΑΗΚ)     │
│              │
│ -€10 energy  │
│ +€10 transfer│
│ ────────────│
│ Net: €0     │
└──────────────┘
```

### Bill Example

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        CYPRUS ELECTRICITY AUTHORITY
               MONTHLY BILL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Account: 123456789
Period: January 2025

ENERGY CONSUMPTION
  Consumption: 320 kWh
  Rate: €0.34/kWh
  Subtotal: €108.80

POWERSAVE PROGRAM
  Savings This Month: 12.5 kWh
  Value: -€4.25
  ─────────────────────────────
  PowerSave Transfer: +€4.25  ← Transfer to Municipality

VAT (19%): €20.67

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL DUE: €129.47
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Waste Fee Status:
  Annual Fee: €195.00
  Paid via PowerSave: €38.50 (19.7%)
  Remaining: €156.50
```

### Key Benefits

| Stakeholder | Benefit |
|-------------|---------|
| **User** | Seamless payment, no extra effort |
| **Utility** | Zero cash flow impact |
| **Municipality** | Guaranteed payment, improved collection |
| **System** | Fraud prevention, audit trail |

---

## Tools Summary Matrix

| Tool | User Type | Primary Benefit | ΕΣΕΚ Alignment |
|------|-----------|-----------------|----------------|
| Waste Fee Offset | All consumers | Direct financial relief | Μέτρο 4 |
| Solar Sync | PV owners | Maximize self-consumption | - |
| Community Groups | Groups | Social motivation | Μέτρο 4 |
| Corporate ESG | Companies | ESG reporting | - |
| Social Solidarity | Donors | Help vulnerable | Μέτρο 18 |
| Purpose-Driven | Communities | Local projects | - |
| PowerSave Kids | Families | Long-term change | Μέτρο 4 |
| Clearinghouse | Backend | Financial integrity | - |

---

*Για το Project Nicosia 2026, δείτε [Nicosia 2026](./09_NICOSIA_2026.md)*
