"""
Database Seeding Script

Creates sample data for testing the PowerSave application:
- Municipalities
- Users with different profiles
- Plant catalog
- Badges
- Sample saving sessions
- Sample challenges
"""
import sys
from datetime import datetime, timedelta
from decimal import Decimal
import random

from sqlalchemy.orm import Session
from backend.database import SessionLocal, init_db
from backend.models.municipality import Municipality
from backend.models.user import User
from backend.models.saving_session import SavingSession
from backend.models.wallet import WasteWallet, WalletTransaction
from backend.models.gamification import PlantCatalog, Badge, Challenge
from backend.models.social_fund import SocialEnergyFund


def seed_municipalities(db: Session):
    """Seed Cyprus municipalities"""
    print("🏛️  Seeding municipalities...")

    municipalities = [
        {
            "name": "Δήμος Λευκωσίας",
            "district": "Λευκωσία",
            "annual_waste_fee": Decimal("120.00"),
            "monthly_waste_fee": Decimal("10.00"),
            "bank_account": "CY17002001280000001200527600",
            "is_active": True
        },
        {
            "name": "Δήμος Λεμεσού",
            "district": "Λεμεσός",
            "annual_waste_fee": Decimal("115.00"),
            "monthly_waste_fee": Decimal("9.58"),
            "bank_account": "CY17002001280000001200527601",
            "is_active": True
        },
        {
            "name": "Δήμος Λάρνακας",
            "district": "Λάρνακα",
            "annual_waste_fee": Decimal("110.00"),
            "monthly_waste_fee": Decimal("9.17"),
            "bank_account": "CY17002001280000001200527602",
            "is_active": True
        },
        {
            "name": "Δήμος Πάφου",
            "district": "Πάφος",
            "annual_waste_fee": Decimal("108.00"),
            "monthly_waste_fee": Decimal("9.00"),
            "bank_account": "CY17002001280000001200527603",
            "is_active": True
        },
        {
            "name": "Δήμος Αμμοχώστου",
            "district": "Αμμόχωστος",
            "annual_waste_fee": Decimal("105.00"),
            "monthly_waste_fee": Decimal("8.75"),
            "bank_account": "CY17002001280000001200527604",
            "is_active": True
        }
    ]

    created = []
    for muni_data in municipalities:
        muni = Municipality(**muni_data)
        db.add(muni)
        created.append(muni)

    db.commit()
    print(f"   ✅ Created {len(created)} municipalities")
    return created


def seed_users(db: Session, municipalities):
    """Seed sample users with different profiles"""
    print("👥 Seeding users...")

    nicosia = municipalities[0]
    limassol = municipalities[1]

    users_data = [
        {
            "ahk_account_number": "10-123456",
            "email": "andreas.georgiou@example.com",
            "password_hash": "hashed_password_1",
            "first_name": "Ανδρέας",
            "last_name": "Γεωργίου",
            "phone": "+35799123456",
            "property_number": "12/345",
            "property_address": "Λεωφόρος Μακαρίου 15, Λευκωσία",
            "municipality_id": nicosia.municipality_id,
            "annual_waste_fee": Decimal("120.00"),
            "green_points_balance": 450,
            "total_kwh_saved": Decimal("15.50"),
            "total_eur_saved": Decimal("4.65"),
            "total_co2_saved": Decimal("10.85"),
            "waste_wallet_balance": Decimal("4.65"),
            "is_vulnerable_household": False
        },
        {
            "ahk_account_number": "10-234567",
            "email": "maria.papadopoulou@example.com",
            "password_hash": "hashed_password_2",
            "first_name": "Μαρία",
            "last_name": "Παπαδοπούλου",
            "phone": "+35799234567",
            "property_number": "23/456",
            "property_address": "Οδός Ληδρας 42, Λευκωσία",
            "municipality_id": nicosia.municipality_id,
            "annual_waste_fee": Decimal("120.00"),
            "green_points_balance": 820,
            "total_kwh_saved": Decimal("28.30"),
            "total_eur_saved": Decimal("8.49"),
            "total_co2_saved": Decimal("19.81"),
            "waste_wallet_balance": Decimal("8.49"),
            "is_vulnerable_household": False
        },
        {
            "ahk_account_number": "10-345678",
            "email": "nikos.constantinou@example.com",
            "password_hash": "hashed_password_3",
            "first_name": "Νίκος",
            "last_name": "Κωνσταντίνου",
            "phone": "+35799345678",
            "property_number": "34/567",
            "property_address": "Λεωφόρος Γρίβα Διγενή 89, Λεμεσός",
            "municipality_id": limassol.municipality_id,
            "annual_waste_fee": Decimal("115.00"),
            "green_points_balance": 1250,
            "total_kwh_saved": Decimal("42.70"),
            "total_eur_saved": Decimal("12.81"),
            "total_co2_saved": Decimal("29.89"),
            "waste_wallet_balance": Decimal("12.81"),
            "is_vulnerable_household": False
        },
        {
            "ahk_account_number": "08-456789",
            "email": "elena.michaelidou@example.com",
            "password_hash": "hashed_password_4",
            "first_name": "Έλενα",
            "last_name": "Μιχαηλίδου",
            "phone": "+35799456789",
            "property_number": "45/678",
            "property_address": "Οδός Ζήνωνος 23, Λευκωσία",
            "municipality_id": nicosia.municipality_id,
            "annual_waste_fee": Decimal("120.00"),
            "green_points_balance": 120,
            "total_kwh_saved": Decimal("3.20"),
            "total_eur_saved": Decimal("0.96"),
            "total_co2_saved": Decimal("2.24"),
            "waste_wallet_balance": Decimal("0.00"),
            "is_vulnerable_household": True  # Vulnerable household
        },
        {
            "ahk_account_number": "10-567890",
            "email": "christos.ioannou@example.com",
            "password_hash": "hashed_password_5",
            "first_name": "Χρήστος",
            "last_name": "Ιωάννου",
            "phone": "+35799567890",
            "property_number": "56/789",
            "property_address": "Λεωφόρος Αρχιεπισκόπου Μακαρίου 156, Λευκωσία",
            "municipality_id": nicosia.municipality_id,
            "annual_waste_fee": Decimal("120.00"),
            "green_points_balance": 2100,
            "total_kwh_saved": Decimal("67.50"),
            "total_eur_saved": Decimal("20.25"),
            "total_co2_saved": Decimal("47.25"),
            "waste_wallet_balance": Decimal("20.25"),
            "is_vulnerable_household": False
        }
    ]

    created = []
    for user_data in users_data:
        user = User(**user_data)
        db.add(user)
        created.append(user)

    db.commit()
    print(f"   ✅ Created {len(created)} users")
    return created


def seed_waste_wallets(db: Session, users):
    """Create waste wallets for users"""
    print("💰 Seeding waste wallets...")

    created = []
    for user in users:
        wallet = WasteWallet(
            user_id=user.user_id,
            current_balance=user.waste_wallet_balance,
            total_earned=user.total_eur_saved,
            total_spent=Decimal("0.00"),
            sessions_contributed=random.randint(5, 25)
        )
        db.add(wallet)
        created.append(wallet)

    db.commit()
    print(f"   ✅ Created {len(created)} waste wallets")
    return created


def seed_saving_sessions(db: Session, users):
    """Create sample saving sessions for users"""
    print("⚡ Seeding saving sessions...")

    created = []
    base_date = datetime.utcnow()

    for user in users[:3]:  # First 3 users
        # Create 10 completed sessions in the past
        for i in range(10):
            days_ago = random.randint(1, 30)
            scheduled_start = base_date - timedelta(days=days_ago, hours=random.choice([17, 18, 19]))
            scheduled_end = scheduled_start + timedelta(hours=3)

            baseline = Decimal(str(random.uniform(1.5, 2.5)))
            actual = Decimal(str(random.uniform(0.8, baseline - 0.3)))
            saved = baseline - actual

            session = SavingSession(
                user_id=user.user_id,
                status="COMPLETED",
                scheduled_start=scheduled_start,
                scheduled_end=scheduled_end,
                actual_start=scheduled_start,
                actual_end=scheduled_end,
                baseline_kwh=baseline,
                baseline_calculation_method="10_DAY_AVERAGE",
                actual_kwh=actual,
                saved_kwh=saved,
                saved_eur=saved * Decimal("0.30"),
                saved_co2_kg=saved * Decimal("0.70"),
                green_points_earned=int(saved * 10),
                is_double_points_day="N",
                allocation_type="WASTE_WALLET",
                completed_at=scheduled_end
            )
            db.add(session)
            created.append(session)

        # Create 1 scheduled session in the future
        future_start = base_date + timedelta(days=1, hours=17)
        future_session = SavingSession(
            user_id=user.user_id,
            status="SCHEDULED",
            scheduled_start=future_start,
            scheduled_end=future_start + timedelta(hours=3),
            allocation_type="WASTE_WALLET"
        )
        db.add(future_session)
        created.append(future_session)

    db.commit()
    print(f"   ✅ Created {len(created)} saving sessions")
    return created


def seed_plant_catalog(db: Session):
    """Seed plant catalog for Green Garden"""
    print("🌱 Seeding plant catalog...")

    plants = [
        {
            "plant_id": "sunflower",
            "name": "Ηλιοτρόπιο",
            "description": "Όμορφο ηλιοτρόπιο που ακολουθεί τον ήλιο",
            "cost_in_green_points": 100,
            "growth_stages": 5,
            "image_url": "/assets/plants/sunflower.png",
            "is_active": True
        },
        {
            "plant_id": "olive_tree",
            "name": "Κυπριακή Ελιά",
            "description": "Παραδοσιακό δέντρο της Κύπρου",
            "cost_in_green_points": 500,
            "growth_stages": 7,
            "image_url": "/assets/plants/olive_tree.png",
            "is_active": True
        },
        {
            "plant_id": "rose",
            "name": "Τριανταφυλλιά",
            "description": "Όμορφη τριανταφυλλιά με κόκκινα άνθη",
            "cost_in_green_points": 150,
            "growth_stages": 4,
            "image_url": "/assets/plants/rose.png",
            "is_active": True
        },
        {
            "plant_id": "cactus",
            "name": "Κάκτος",
            "description": "Ανθεκτικό φυτό που χρειάζεται λίγο νερό",
            "cost_in_green_points": 75,
            "growth_stages": 3,
            "image_url": "/assets/plants/cactus.png",
            "is_active": True
        },
        {
            "plant_id": "lemon_tree",
            "name": "Λεμονιά",
            "description": "Μυρωδάτη λεμονιά με φρέσκα λεμόνια",
            "cost_in_green_points": 400,
            "growth_stages": 6,
            "image_url": "/assets/plants/lemon_tree.png",
            "is_active": True
        },
        {
            "plant_id": "lavender",
            "name": "Λεβάντα",
            "description": "Αρωματικό φυτό με μωβ άνθη",
            "cost_in_green_points": 200,
            "growth_stages": 4,
            "image_url": "/assets/plants/lavender.png",
            "is_active": True
        }
    ]

    created = []
    for plant_data in plants:
        plant = PlantCatalog(**plant_data)
        db.add(plant)
        created.append(plant)

    db.commit()
    print(f"   ✅ Created {len(created)} plants")
    return created


def seed_badges(db: Session):
    """Seed badge catalog"""
    print("🏆 Seeding badges...")

    badges = [
        {
            "badge_id": "first_session",
            "name": "Πρώτο Βήμα",
            "description": "Ολοκλήρωσες την πρώτη σου saving session",
            "image_url": "/assets/badges/first_session.png",
            "category": "BEGINNER",
            "rarity": "COMMON",
            "is_active": True
        },
        {
            "badge_id": "week_streak",
            "name": "Εβδομαδιαίος Πολεμιστής",
            "description": "7 συνεχόμενες μέρες με sessions",
            "image_url": "/assets/badges/week_streak.png",
            "category": "STREAK",
            "rarity": "RARE",
            "is_active": True
        },
        {
            "badge_id": "month_streak",
            "name": "Μηνιαίος Master",
            "description": "30 συνεχόμενες μέρες με sessions",
            "image_url": "/assets/badges/month_streak.png",
            "category": "STREAK",
            "rarity": "EPIC",
            "is_active": True
        },
        {
            "badge_id": "eco_warrior",
            "name": "Πολεμιστής του Περιβάλλοντος",
            "description": "Εξοικονόμησες 100 kWh συνολικά",
            "image_url": "/assets/badges/eco_warrior.png",
            "category": "ACHIEVEMENT",
            "rarity": "EPIC",
            "is_active": True
        },
        {
            "badge_id": "community_hero",
            "name": "Ήρωας της Κοινότητας",
            "description": "Δώρισες €50 στο Ταμείο Αλληλεγγύης",
            "image_url": "/assets/badges/community_hero.png",
            "category": "COMMUNITY",
            "rarity": "EPIC",
            "is_active": True
        },
        {
            "badge_id": "green_champion",
            "name": "Πράσινος Πρωταθλητής",
            "description": "Κέρδισες 5000 Green Points",
            "image_url": "/assets/badges/green_champion.png",
            "category": "ACHIEVEMENT",
            "rarity": "LEGENDARY",
            "is_active": True
        },
        {
            "badge_id": "waste_free",
            "name": "Απαλλαγμένος από Τέλη",
            "description": "Κάλυψες το 100% των τελών σκυβάλων",
            "image_url": "/assets/badges/waste_free.png",
            "category": "ACHIEVEMENT",
            "rarity": "LEGENDARY",
            "is_active": True
        }
    ]

    created = []
    for badge_data in badges:
        badge = Badge(**badge_data)
        db.add(badge)
        created.append(badge)

    db.commit()
    print(f"   ✅ Created {len(created)} badges")
    return created


def seed_challenges(db: Session):
    """Seed active challenges"""
    print("🎯 Seeding challenges...")

    today = datetime.utcnow().date()

    challenges = [
        {
            "name": "Χειμερινή Πρόκληση 2025",
            "description": "Εξοικονόμησε 50 kWh τον Δεκέμβριο",
            "goal_type": "TOTAL_KWH_SAVED",
            "goal_value": Decimal("50.00"),
            "start_date": today.replace(day=1),
            "end_date": today.replace(day=31),
            "reward_green_points": 500,
            "scope": "INDIVIDUAL",
            "is_active": True
        },
        {
            "name": "20 Sessions Challenge",
            "description": "Ολοκλήρωσε 20 saving sessions αυτόν τον μήνα",
            "goal_type": "SESSION_COUNT",
            "goal_value": Decimal("20.00"),
            "start_date": today.replace(day=1),
            "end_date": today.replace(day=31),
            "reward_green_points": 300,
            "reward_badge_id": "eco_warrior",
            "scope": "INDIVIDUAL",
            "is_active": True
        },
        {
            "name": "Γειτονιά Λευκωσίας - 1000 kWh",
            "description": "Ας εξοικονομήσουμε μαζί 1000 kWh!",
            "goal_type": "COMMUNITY_GOAL",
            "goal_value": Decimal("1000.00"),
            "start_date": today.replace(day=1),
            "end_date": today.replace(day=31),
            "reward_green_points": 200,
            "scope": "COMMUNITY",
            "is_active": True
        }
    ]

    created = []
    for challenge_data in challenges:
        challenge = Challenge(**challenge_data)
        db.add(challenge)
        created.append(challenge)

    db.commit()
    print(f"   ✅ Created {len(created)} challenges")
    return created


def seed_social_fund(db: Session, municipalities):
    """Seed Social Energy Solidarity Fund"""
    print("🤝 Seeding Social Energy Fund...")

    nicosia = municipalities[0]

    fund = SocialEnergyFund(
        municipality_id=nicosia.municipality_id,
        balance=Decimal("2500.00"),
        total_donations=Decimal("3500.00"),
        total_disbursements=Decimal("1000.00"),
        households_helped=12,
        total_kwh_donated=Decimal("11666.67")  # 3500 / 0.30
    )

    db.add(fund)
    db.commit()
    print(f"   ✅ Created Social Energy Fund with €{fund.balance} balance")
    return fund


def main():
    """Main seeding function"""
    print("\n" + "="*60)
    print("🌱 PowerSave Database Seeding")
    print("="*60 + "\n")

    # Initialize database
    print("📊 Initializing database...")
    init_db()
    print("   ✅ Database initialized\n")

    # Create session
    db = SessionLocal()

    try:
        # Seed data
        municipalities = seed_municipalities(db)
        users = seed_users(db, municipalities)
        wallets = seed_waste_wallets(db, users)
        sessions = seed_saving_sessions(db, users)
        plants = seed_plant_catalog(db)
        badges = seed_badges(db)
        challenges = seed_challenges(db)
        fund = seed_social_fund(db, municipalities)

        print("\n" + "="*60)
        print("✅ Database seeding completed successfully!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Municipalities:     {len(municipalities)}")
        print(f"   • Users:              {len(users)}")
        print(f"   • Waste Wallets:      {len(wallets)}")
        print(f"   • Saving Sessions:    {len(sessions)}")
        print(f"   • Plants:             {len(plants)}")
        print(f"   • Badges:             {len(badges)}")
        print(f"   • Challenges:         {len(challenges)}")
        print(f"   • Social Fund:        €{fund.balance}")
        print("\n🎉 You can now start the API and test with sample data!\n")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
