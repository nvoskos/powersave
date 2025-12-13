"""
PowerSave - Waste Fee Offset API
================================
Municipality Integration & Waste Wallet Management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Optional
import json
import uuid

waste_api = Blueprint('waste_api', __name__)

# ============================================================================
# DATABASE MODELS (In-memory for demo - replace with SQLAlchemy in production)
# ============================================================================

# Supported Municipalities
MUNICIPALITIES = {
    "nicosia": {
        "id": "nicosia",
        "name": "Δήμος Λευκωσίας",
        "name_en": "Nicosia Municipality",
        "annual_fee": 185.00,
        "region": "Λευκωσία"
    },
    "limassol": {
        "id": "limassol",
        "name": "Δήμος Λεμεσού",
        "name_en": "Limassol Municipality",
        "annual_fee": 195.00,
        "region": "Λεμεσός"
    },
    "larnaca": {
        "id": "larnaca",
        "name": "Δήμος Λάρνακας",
        "name_en": "Larnaca Municipality",
        "annual_fee": 175.00,
        "region": "Λάρνακα"
    },
    "paphos": {
        "id": "paphos",
        "name": "Δήμος Πάφου",
        "name_en": "Paphos Municipality",
        "annual_fee": 180.00,
        "region": "Πάφος"
    },
    "strovolos": {
        "id": "strovolos",
        "name": "Δήμος Στροβόλου",
        "name_en": "Strovolos Municipality",
        "annual_fee": 190.00,
        "region": "Λευκωσία"
    }
}

# In-memory storage
users_db = {}
properties_db = {}
wallets_db = {}
transactions_db = {}
sessions_db = {}
payments_db = {}

# ============================================================================
# CONVERSION & CALCULATION LOGIC
# ============================================================================

# Current electricity tariff (EUR per kWh) - Cyprus 2025
KWH_TO_EUR_RATE = 0.34  # €0.34 per kWh saved

# Double points multipliers
DOUBLE_POINTS_MULTIPLIER = 2.0

def is_double_points_day():
    """Check if today is a double points day (extreme weather)"""
    # In production: integrate with weather API
    # Demo: weekends are double points
    return datetime.now().weekday() >= 5

def calculate_savings_value(kwh_saved: float) -> float:
    """Convert kWh saved to EUR"""
    multiplier = DOUBLE_POINTS_MULTIPLIER if is_double_points_day() else 1.0
    return round(kwh_saved * KWH_TO_EUR_RATE * multiplier, 2)

def calculate_baseline(consumption_history: List[float]) -> float:
    """Calculate 10-day average baseline consumption"""
    if not consumption_history:
        return 0.0
    # Use last 10 days or all available
    recent = consumption_history[-10:]
    return round(sum(recent) / len(recent), 2)

# ============================================================================
# MUNICIPALITY INTEGRATION API
# ============================================================================

@waste_api.route('/api/municipalities', methods=['GET'])
def get_municipalities():
    """Get list of supported municipalities"""
    return jsonify({
        "success": True,
        "municipalities": list(MUNICIPALITIES.values())
    })

@waste_api.route('/api/municipalities/<municipality_id>', methods=['GET'])
def get_municipality(municipality_id):
    """Get municipality details"""
    if municipality_id not in MUNICIPALITIES:
        return jsonify({"success": False, "error": "Municipality not found"}), 404
    return jsonify({
        "success": True,
        "municipality": MUNICIPALITIES[municipality_id]
    })

# ============================================================================
# PROPERTY REGISTRATION API
# ============================================================================

@waste_api.route('/api/properties/register', methods=['POST'])
def register_property():
    """Register a property (premises) for waste fee offset"""
    data = request.json

    user_id = data.get('user_id')
    municipality_id = data.get('municipality_id')
    property_number = data.get('property_number')  # Αριθμός Υποστατικού
    address = data.get('address', '')

    if not all([user_id, municipality_id, property_number]):
        return jsonify({
            "success": False,
            "error": "Missing required fields: user_id, municipality_id, property_number"
        }), 400

    if municipality_id not in MUNICIPALITIES:
        return jsonify({
            "success": False,
            "error": "Invalid municipality"
        }), 400

    property_id = str(uuid.uuid4())

    properties_db[property_id] = {
        "id": property_id,
        "user_id": user_id,
        "municipality_id": municipality_id,
        "property_number": property_number,
        "address": address,
        "annual_fee": MUNICIPALITIES[municipality_id]["annual_fee"],
        "verified": False,  # Needs verification from municipality
        "created_at": datetime.now().isoformat()
    }

    # Auto-create wallet for this property
    wallet_id = create_wallet(user_id, property_id, municipality_id)

    return jsonify({
        "success": True,
        "property": properties_db[property_id],
        "wallet_id": wallet_id,
        "message": "Property registered successfully. Awaiting municipality verification."
    })

@waste_api.route('/api/properties/scan', methods=['POST'])
def scan_property_qr():
    """Register property via QR code scan"""
    data = request.json
    qr_data = data.get('qr_data')
    user_id = data.get('user_id')

    if not qr_data or not user_id:
        return jsonify({"success": False, "error": "Missing qr_data or user_id"}), 400

    # Parse QR data (format: MUNICIPALITY:PROPERTY_NUMBER:ADDRESS)
    try:
        parts = qr_data.split(':')
        municipality_id = parts[0].lower()
        property_number = parts[1]
        address = parts[2] if len(parts) > 2 else ""

        # Call register_property internally
        return register_property_internal(user_id, municipality_id, property_number, address)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Invalid QR code format: {str(e)}"
        }), 400

def register_property_internal(user_id, municipality_id, property_number, address):
    """Internal property registration helper"""
    property_id = str(uuid.uuid4())

    properties_db[property_id] = {
        "id": property_id,
        "user_id": user_id,
        "municipality_id": municipality_id,
        "property_number": property_number,
        "address": address,
        "annual_fee": MUNICIPALITIES[municipality_id]["annual_fee"],
        "verified": True,  # QR scan = auto-verified
        "created_at": datetime.now().isoformat()
    }

    wallet_id = create_wallet(user_id, property_id, municipality_id)

    return jsonify({
        "success": True,
        "property": properties_db[property_id],
        "wallet_id": wallet_id
    })

@waste_api.route('/api/properties/<user_id>', methods=['GET'])
def get_user_properties(user_id):
    """Get all properties for a user"""
    user_properties = [p for p in properties_db.values() if p["user_id"] == user_id]
    return jsonify({
        "success": True,
        "properties": user_properties
    })

# ============================================================================
# WASTE WALLET API
# ============================================================================

def create_wallet(user_id: str, property_id: str, municipality_id: str) -> str:
    """Create a new waste wallet"""
    wallet_id = str(uuid.uuid4())

    wallets_db[wallet_id] = {
        "id": wallet_id,
        "user_id": user_id,
        "property_id": property_id,
        "municipality_id": municipality_id,
        "balance": 0.0,
        "total_earned": 0.0,
        "total_paid": 0.0,
        "annual_target": MUNICIPALITIES[municipality_id]["annual_fee"],
        "year": datetime.now().year,
        "created_at": datetime.now().isoformat()
    }

    return wallet_id

@waste_api.route('/api/wallet/<wallet_id>', methods=['GET'])
def get_wallet(wallet_id):
    """Get wallet details"""
    if wallet_id not in wallets_db:
        return jsonify({"success": False, "error": "Wallet not found"}), 404

    wallet = wallets_db[wallet_id]
    progress_percent = round((wallet["total_paid"] / wallet["annual_target"]) * 100, 1)

    return jsonify({
        "success": True,
        "wallet": wallet,
        "progress_percent": min(progress_percent, 100),
        "remaining": max(0, wallet["annual_target"] - wallet["total_paid"])
    })

@waste_api.route('/api/wallet/user/<user_id>', methods=['GET'])
def get_user_wallets(user_id):
    """Get all wallets for a user"""
    user_wallets = [w for w in wallets_db.values() if w["user_id"] == user_id]

    result = []
    for wallet in user_wallets:
        progress = round((wallet["total_paid"] / wallet["annual_target"]) * 100, 1)
        result.append({
            **wallet,
            "progress_percent": min(progress, 100),
            "remaining": max(0, wallet["annual_target"] - wallet["total_paid"]),
            "municipality": MUNICIPALITIES.get(wallet["municipality_id"])
        })

    return jsonify({
        "success": True,
        "wallets": result
    })

@waste_api.route('/api/wallet/<wallet_id>/add', methods=['POST'])
def add_to_wallet(wallet_id):
    """Add funds to wallet (from savings session)"""
    if wallet_id not in wallets_db:
        return jsonify({"success": False, "error": "Wallet not found"}), 404

    data = request.json
    amount = data.get('amount', 0)
    kwh_saved = data.get('kwh_saved', 0)
    session_id = data.get('session_id')

    if amount <= 0:
        return jsonify({"success": False, "error": "Amount must be positive"}), 400

    wallet = wallets_db[wallet_id]
    wallet["balance"] += amount
    wallet["total_earned"] += amount

    # Record transaction
    tx_id = str(uuid.uuid4())
    transactions_db[tx_id] = {
        "id": tx_id,
        "wallet_id": wallet_id,
        "type": "credit",
        "amount": amount,
        "kwh_saved": kwh_saved,
        "session_id": session_id,
        "description": f"Savings Session - {kwh_saved} kWh",
        "is_double_points": is_double_points_day(),
        "created_at": datetime.now().isoformat()
    }

    return jsonify({
        "success": True,
        "wallet": wallet,
        "transaction_id": tx_id,
        "message": f"Added €{amount:.2f} to wallet"
    })

@waste_api.route('/api/wallet/<wallet_id>/transactions', methods=['GET'])
def get_wallet_transactions(wallet_id):
    """Get transaction history for a wallet"""
    txs = [t for t in transactions_db.values() if t["wallet_id"] == wallet_id]
    txs.sort(key=lambda x: x["created_at"], reverse=True)

    return jsonify({
        "success": True,
        "transactions": txs
    })

# ============================================================================
# SAVINGS SESSION API
# ============================================================================

@waste_api.route('/api/sessions/active', methods=['GET'])
def get_active_session():
    """Check if there's an active savings session"""
    now = datetime.now()

    # Peak hours: 17:00 - 20:00
    is_peak = 17 <= now.hour < 20

    if is_peak:
        session_id = f"session_{now.strftime('%Y%m%d_%H')}"

        if session_id not in sessions_db:
            sessions_db[session_id] = {
                "id": session_id,
                "status": "active",
                "start_time": now.replace(minute=0, second=0).isoformat(),
                "end_time": (now.replace(minute=0, second=0) + timedelta(hours=2)).isoformat(),
                "is_double_points": is_double_points_day(),
                "participants": [],
                "total_kwh_saved": 0,
                "total_eur_saved": 0
            }

        return jsonify({
            "success": True,
            "active": True,
            "session": sessions_db[session_id],
            "message": "Savings session is active! Join now to earn rewards."
        })

    return jsonify({
        "success": True,
        "active": False,
        "next_session": {
            "start": now.replace(hour=17, minute=0, second=0).isoformat() if now.hour < 17
                     else (now + timedelta(days=1)).replace(hour=17, minute=0, second=0).isoformat()
        },
        "message": "No active session. Next session starts at 17:00."
    })

@waste_api.route('/api/sessions/<session_id>/join', methods=['POST'])
def join_session(session_id):
    """Join an active savings session"""
    if session_id not in sessions_db:
        return jsonify({"success": False, "error": "Session not found"}), 404

    data = request.json
    user_id = data.get('user_id')
    wallet_id = data.get('wallet_id')

    if not user_id or not wallet_id:
        return jsonify({"success": False, "error": "Missing user_id or wallet_id"}), 400

    session = sessions_db[session_id]

    if session["status"] != "active":
        return jsonify({"success": False, "error": "Session is not active"}), 400

    participant = {
        "user_id": user_id,
        "wallet_id": wallet_id,
        "joined_at": datetime.now().isoformat(),
        "baseline_kwh": 2.5,  # Demo: in production, get from smart meter
        "current_kwh": 0,
        "kwh_saved": 0,
        "eur_earned": 0
    }

    session["participants"].append(participant)

    return jsonify({
        "success": True,
        "message": "Successfully joined the session!",
        "participant": participant,
        "tips": [
            "Αναβάλετε τη χρήση του πλυντηρίου",
            "Κλείστε τον θερμοσίφωνα",
            "Ρυθμίστε το A/C στους 26°C"
        ]
    })

@waste_api.route('/api/sessions/<session_id>/complete', methods=['POST'])
def complete_session(session_id):
    """Complete a session and calculate rewards"""
    if session_id not in sessions_db:
        return jsonify({"success": False, "error": "Session not found"}), 404

    data = request.json
    user_id = data.get('user_id')
    actual_kwh = data.get('actual_kwh', 0)  # Actual consumption during session

    session = sessions_db[session_id]

    # Find participant
    participant = None
    for p in session["participants"]:
        if p["user_id"] == user_id:
            participant = p
            break

    if not participant:
        return jsonify({"success": False, "error": "User not in session"}), 400

    # Calculate savings
    kwh_saved = max(0, participant["baseline_kwh"] - actual_kwh)
    eur_earned = calculate_savings_value(kwh_saved)

    participant["current_kwh"] = actual_kwh
    participant["kwh_saved"] = kwh_saved
    participant["eur_earned"] = eur_earned

    # Update session totals
    session["total_kwh_saved"] += kwh_saved
    session["total_eur_saved"] += eur_earned

    # Add to wallet
    if participant["wallet_id"] in wallets_db:
        wallet = wallets_db[participant["wallet_id"]]
        wallet["balance"] += eur_earned
        wallet["total_earned"] += eur_earned

        # Record transaction
        tx_id = str(uuid.uuid4())
        transactions_db[tx_id] = {
            "id": tx_id,
            "wallet_id": participant["wallet_id"],
            "type": "credit",
            "amount": eur_earned,
            "kwh_saved": kwh_saved,
            "session_id": session_id,
            "description": f"Session {session_id}: -{kwh_saved} kWh",
            "is_double_points": session["is_double_points"],
            "created_at": datetime.now().isoformat()
        }

    return jsonify({
        "success": True,
        "result": {
            "kwh_saved": kwh_saved,
            "eur_earned": eur_earned,
            "is_double_points": session["is_double_points"],
            "message": f"Μπράβο! Κέρδισες €{eur_earned:.2f} στο Waste Wallet σου!"
        }
    })

# ============================================================================
# MONTHLY AUTO-PAYMENT API
# ============================================================================

@waste_api.route('/api/payments/auto-transfer', methods=['POST'])
def auto_transfer_to_municipality():
    """Monthly auto-transfer from wallet to municipality"""
    data = request.json
    wallet_id = data.get('wallet_id')

    if wallet_id not in wallets_db:
        return jsonify({"success": False, "error": "Wallet not found"}), 404

    wallet = wallets_db[wallet_id]

    if wallet["balance"] <= 0:
        return jsonify({
            "success": False,
            "error": "Insufficient balance",
            "balance": wallet["balance"]
        }), 400

    transfer_amount = wallet["balance"]

    # Create payment record
    payment_id = str(uuid.uuid4())
    payments_db[payment_id] = {
        "id": payment_id,
        "wallet_id": wallet_id,
        "municipality_id": wallet["municipality_id"],
        "amount": transfer_amount,
        "status": "completed",
        "payment_date": datetime.now().isoformat(),
        "receipt_number": f"PS-{datetime.now().strftime('%Y%m')}-{payment_id[:8].upper()}"
    }

    # Update wallet
    wallet["balance"] = 0
    wallet["total_paid"] += transfer_amount

    # Record transaction
    tx_id = str(uuid.uuid4())
    transactions_db[tx_id] = {
        "id": tx_id,
        "wallet_id": wallet_id,
        "type": "debit",
        "amount": transfer_amount,
        "payment_id": payment_id,
        "description": f"Payment to {MUNICIPALITIES[wallet['municipality_id']]['name']}",
        "created_at": datetime.now().isoformat()
    }

    return jsonify({
        "success": True,
        "payment": payments_db[payment_id],
        "message": f"Πληρώθηκε έναντι Τελών Σκυβάλων: €{transfer_amount:.2f}",
        "new_balance": 0,
        "total_paid": wallet["total_paid"],
        "remaining": max(0, wallet["annual_target"] - wallet["total_paid"])
    })

@waste_api.route('/api/payments/<wallet_id>/history', methods=['GET'])
def get_payment_history(wallet_id):
    """Get payment history for a wallet"""
    wallet_payments = [p for p in payments_db.values() if p["wallet_id"] == wallet_id]
    wallet_payments.sort(key=lambda x: x["payment_date"], reverse=True)

    return jsonify({
        "success": True,
        "payments": wallet_payments
    })

# ============================================================================
# SURPLUS HANDLING API
# ============================================================================

@waste_api.route('/api/surplus/handle', methods=['POST'])
def handle_surplus():
    """Handle surplus funds (rollover or donate)"""
    data = request.json
    wallet_id = data.get('wallet_id')
    action = data.get('action')  # 'rollover' or 'donate'

    if wallet_id not in wallets_db:
        return jsonify({"success": False, "error": "Wallet not found"}), 404

    wallet = wallets_db[wallet_id]
    surplus = wallet["total_paid"] - wallet["annual_target"]

    if surplus <= 0:
        return jsonify({
            "success": False,
            "error": "No surplus to handle",
            "total_paid": wallet["total_paid"],
            "annual_target": wallet["annual_target"]
        }), 400

    if action == "rollover":
        # Rollover to next year
        wallet["year"] += 1
        wallet["total_paid"] = surplus
        wallet["annual_target"] = MUNICIPALITIES[wallet["municipality_id"]]["annual_fee"]

        return jsonify({
            "success": True,
            "action": "rollover",
            "surplus_amount": surplus,
            "message": f"€{surplus:.2f} μεταφέρθηκε για τα τέλη του {wallet['year']}",
            "new_year": wallet["year"]
        })

    elif action == "donate":
        # Donate to social fund
        wallet["total_paid"] = wallet["annual_target"]  # Cap at target

        # Record donation
        donation_id = str(uuid.uuid4())

        return jsonify({
            "success": True,
            "action": "donate",
            "donation_amount": surplus,
            "donation_id": donation_id,
            "message": f"€{surplus:.2f} δωρήθηκε στο Κοινωνικό Ταμείο. Ευχαριστούμε!"
        })

    return jsonify({"success": False, "error": "Invalid action. Use 'rollover' or 'donate'"}), 400

# ============================================================================
# ENERGY SAVING TIPS API
# ============================================================================

ENERGY_TIPS = {
    "thermosifonas": {
        "title": "Θερμοσίφωνας",
        "icon": "droplet",
        "tips": [
            "Κλείστε τον κατά τη διάρκεια των Sessions",
            "Ρυθμίστε στους 60°C αντί για 70°C",
            "Ανάψτε τον 30 λεπτά πριν το μπάνιο"
        ],
        "potential_savings": "€15-25/μήνα"
    },
    "klimatistiko": {
        "title": "Κλιματιστικό",
        "icon": "wind",
        "tips": [
            "26°C το καλοκαίρι, 21°C το χειμώνα",
            "Καθαρίστε τα φίλτρα κάθε μήνα",
            "Κλείστε πόρτες και παράθυρα"
        ],
        "potential_savings": "€20-40/μήνα"
    },
    "fournos": {
        "title": "Φούρνος",
        "icon": "flame",
        "tips": [
            "Αποφύγετε χρήση 18:00-21:00 (ώρες αιχμής)",
            "Χρησιμοποιήστε αερόθερμο αντί για grill",
            "Μην ανοίγετε την πόρτα συχνά"
        ],
        "potential_savings": "€5-10/μήνα"
    },
    "plyntirio": {
        "title": "Πλυντήριο",
        "icon": "shirt",
        "tips": [
            "Πλύνετε σε χαμηλές θερμοκρασίες (30-40°C)",
            "Χρησιμοποιήστε πλήρες φορτίο",
            "Αποφύγετε ώρες αιχμής"
        ],
        "potential_savings": "€5-15/μήνα"
    }
}

@waste_api.route('/api/tips', methods=['GET'])
def get_energy_tips():
    """Get all energy saving tips"""
    return jsonify({
        "success": True,
        "tips": ENERGY_TIPS
    })

@waste_api.route('/api/tips/<category>', methods=['GET'])
def get_tips_by_category(category):
    """Get tips for specific category"""
    if category not in ENERGY_TIPS:
        return jsonify({"success": False, "error": "Category not found"}), 404

    return jsonify({
        "success": True,
        "tip": ENERGY_TIPS[category]
    })

# ============================================================================
# DOUBLE POINTS DAYS API
# ============================================================================

@waste_api.route('/api/double-points/status', methods=['GET'])
def get_double_points_status():
    """Check if today is a double points day"""
    is_double = is_double_points_day()

    return jsonify({
        "success": True,
        "is_double_points": is_double,
        "multiplier": DOUBLE_POINTS_MULTIPLIER if is_double else 1.0,
        "reason": "Σαββατοκύριακο - Διπλοί Πόντοι!" if is_double else None,
        "next_double_day": get_next_double_day()
    })

def get_next_double_day():
    """Get the next double points day"""
    today = datetime.now()
    days_until_saturday = (5 - today.weekday()) % 7
    if days_until_saturday == 0 and today.weekday() < 5:
        days_until_saturday = 5 - today.weekday()
    next_saturday = today + timedelta(days=days_until_saturday)
    return next_saturday.strftime('%Y-%m-%d')

# ============================================================================
# RECEIPTS API
# ============================================================================

@waste_api.route('/api/receipts/<payment_id>', methods=['GET'])
def get_receipt(payment_id):
    """Get receipt for a payment"""
    if payment_id not in payments_db:
        return jsonify({"success": False, "error": "Payment not found"}), 404

    payment = payments_db[payment_id]
    wallet = wallets_db.get(payment["wallet_id"], {})
    municipality = MUNICIPALITIES.get(payment["municipality_id"], {})

    receipt = {
        "receipt_number": payment["receipt_number"],
        "payment_date": payment["payment_date"],
        "amount": payment["amount"],
        "payer": {
            "wallet_id": payment["wallet_id"]
        },
        "recipient": {
            "name": municipality.get("name", "Unknown"),
            "type": "Municipal Waste Fees"
        },
        "status": "PAID",
        "powersave_logo": True,
        "message": "Πληρωμή μέσω PowerSave Waste Fee Offset"
    }

    return jsonify({
        "success": True,
        "receipt": receipt
    })

# ============================================================================
# FAQ API
# ============================================================================

FAQ_DATA = [
    {
        "id": 1,
        "question": "Τι γίνεται αν μαζέψω περισσότερα χρήματα από τα τέλη μου;",
        "answer": "Το πλεόνασμα δεν χάνεται! Μπορείτε να το μεταφέρετε για τα τέλη του επόμενου έτους ή να το δωρίσετε στο Κοινωνικό Ταμείο για ευάλωτες οικογένειες.",
        "category": "surplus"
    },
    {
        "id": 2,
        "question": "Επηρεάζεται ο λογαριασμός της ΑΗΚ;",
        "answer": "Όχι. Πληρώνετε τον λογαριασμό ρεύματος κανονικά στον Πάροχό σας. Το PowerSave είναι ένας επιπλέον κουμπαράς που γεμίζει από την απουσία κατανάλωσης.",
        "category": "billing"
    },
    {
        "id": 3,
        "question": "Πώς ξέρει η εφαρμογή ότι έκανα εξοικονόμηση;",
        "answer": "Χρησιμοποιούμε έναν έξυπνο αλγόριθμο που συγκρίνει τη σημερινή σας κατανάλωση με τον Μέσο Όρο των προηγούμενων 10 ημερών (Baseline). Αν κάψατε λιγότερο, η διαφορά είναι το κέρδος σας!",
        "category": "algorithm"
    },
    {
        "id": 4,
        "question": "Τι είναι τα Double Points Days;",
        "answer": "Σε ημέρες ακραίων καιρικών συνθηκών (καύσωνας ή πολύ κρύο), η αξία της εξοικονόμησης διπλασιάζεται! Αυτές τις μέρες βοηθάτε το δίκτυο να αποφύγει υπερφόρτωση.",
        "category": "rewards"
    },
    {
        "id": 5,
        "question": "Πότε μεταφέρονται τα χρήματα στον Δήμο;",
        "answer": "Στο τέλος κάθε μήνα, το PowerSave αθροίζει τα κέρδη σας και τα μεταφέρει αυτόματα στον Δήμο. Θα λάβετε απόδειξη ηλεκτρονικά.",
        "category": "payments"
    }
]

@waste_api.route('/api/faq', methods=['GET'])
def get_faq():
    """Get all FAQ items"""
    category = request.args.get('category')

    if category:
        filtered = [f for f in FAQ_DATA if f["category"] == category]
        return jsonify({"success": True, "faq": filtered})

    return jsonify({"success": True, "faq": FAQ_DATA})

# ============================================================================
# ANNUAL GOAL TRACKER API
# ============================================================================

@waste_api.route('/api/goal/<wallet_id>', methods=['GET'])
def get_annual_goal(wallet_id):
    """Get annual goal progress for a wallet"""
    if wallet_id not in wallets_db:
        return jsonify({"success": False, "error": "Wallet not found"}), 404

    wallet = wallets_db[wallet_id]
    progress = (wallet["total_paid"] / wallet["annual_target"]) * 100

    # Monthly breakdown
    monthly_target = wallet["annual_target"] / 12
    current_month = datetime.now().month
    expected_progress = (current_month / 12) * 100

    return jsonify({
        "success": True,
        "goal": {
            "annual_target": wallet["annual_target"],
            "total_paid": wallet["total_paid"],
            "remaining": max(0, wallet["annual_target"] - wallet["total_paid"]),
            "progress_percent": round(min(progress, 100), 1),
            "expected_progress": round(expected_progress, 1),
            "on_track": progress >= expected_progress,
            "monthly_target": round(monthly_target, 2),
            "year": wallet["year"]
        },
        "municipality": MUNICIPALITIES.get(wallet["municipality_id"])
    })
