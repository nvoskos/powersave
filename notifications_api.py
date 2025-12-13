"""
PowerSave - Push Notifications API
==================================
Session alerts, rewards notifications, payment confirmations
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from typing import List, Dict
import uuid

notifications_api = Blueprint('notifications_api', __name__)

# In-memory notification storage
notifications_db = {}
subscriptions_db = {}
scheduled_notifications = []

# ============================================================================
# NOTIFICATION TYPES
# ============================================================================

NOTIFICATION_TYPES = {
    "session_start": {
        "title": "PowerSave Alert",
        "icon": "zap",
        "color": "#f59e0b",
        "priority": "high"
    },
    "session_reminder": {
        "title": "Session Reminder",
        "icon": "clock",
        "color": "#3b82f6",
        "priority": "normal"
    },
    "session_result": {
        "title": "Session Complete!",
        "icon": "trophy",
        "color": "#10b981",
        "priority": "high"
    },
    "payment_sent": {
        "title": "Payment Sent",
        "icon": "check-circle",
        "color": "#10b981",
        "priority": "normal"
    },
    "double_points": {
        "title": "Double Points Day!",
        "icon": "star",
        "color": "#8b5cf6",
        "priority": "high"
    },
    "goal_milestone": {
        "title": "Goal Milestone!",
        "icon": "flag",
        "color": "#06b6d4",
        "priority": "normal"
    },
    "tip_of_day": {
        "title": "Energy Tip",
        "icon": "lightbulb",
        "color": "#eab308",
        "priority": "low"
    }
}

# ============================================================================
# NOTIFICATION TEMPLATES
# ============================================================================

TEMPLATES = {
    "session_start_el": {
        "title": "PowerSave Alert 🔔",
        "body": "Η ζήτηση ρεύματος είναι υψηλή. Ξεκινάμε Session Εξοικονόμησης για τις επόμενες {duration} ώρες. Συμμετέχεις;",
        "action_text": "Συμμετοχή",
        "action_url": "/session/join"
    },
    "session_result_el": {
        "title": "Μπράβο! 🎉",
        "body": "Κατανάλωσες {kwh_saved} kWh λιγότερο από το συνηθισμένο σου. Κέρδισες €{eur_earned} στο Waste Wallet σου.",
        "action_text": "Δες το Wallet",
        "action_url": "/wallet"
    },
    "payment_sent_el": {
        "title": "Πληρωμή Ολοκληρώθηκε ✅",
        "body": "Πληρώθηκε έναντι Τελών Σκυβάλων: €{amount}. Απομένουν €{remaining} για τον ετήσιο στόχο.",
        "action_text": "Δες Απόδειξη",
        "action_url": "/receipts/{payment_id}"
    },
    "double_points_el": {
        "title": "Διπλοί Πόντοι Σήμερα! ⭐",
        "body": "Λόγω υψηλής ζήτησης, κάθε kWh που εξοικονομείς σήμερα αξίζει διπλά! Μην χάσεις την ευκαιρία.",
        "action_text": "Μάθε Περισσότερα",
        "action_url": "/double-points"
    },
    "goal_50_el": {
        "title": "Μισός Δρόμος! 🚀",
        "body": "Έφτασες το 50% του ετήσιου στόχου Σκυβάλων! Συνέχισε έτσι!",
        "action_text": "Δες Πρόοδο",
        "action_url": "/goal"
    },
    "goal_100_el": {
        "title": "Στόχος Επιτεύχθηκε! 🏆",
        "body": "Κάλυψες πλήρως τα Τέλη Σκυβάλων του {year}! Μπορείς να μεταφέρεις το πλεόνασμα ή να το δωρίσεις.",
        "action_text": "Διαχείριση Πλεονάσματος",
        "action_url": "/surplus"
    }
}

# ============================================================================
# SUBSCRIPTION API
# ============================================================================

@notifications_api.route('/api/notifications/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to push notifications"""
    data = request.json
    user_id = data.get('user_id')
    device_token = data.get('device_token')  # FCM token or similar
    device_type = data.get('device_type', 'web')  # 'ios', 'android', 'web'

    if not user_id:
        return jsonify({"success": False, "error": "user_id required"}), 400

    subscription_id = str(uuid.uuid4())

    subscriptions_db[subscription_id] = {
        "id": subscription_id,
        "user_id": user_id,
        "device_token": device_token,
        "device_type": device_type,
        "preferences": {
            "session_alerts": True,
            "payment_alerts": True,
            "tips": True,
            "double_points": True,
            "quiet_hours": {"start": "22:00", "end": "08:00"}
        },
        "created_at": datetime.now().isoformat()
    }

    return jsonify({
        "success": True,
        "subscription_id": subscription_id,
        "message": "Successfully subscribed to notifications"
    })

@notifications_api.route('/api/notifications/preferences/<user_id>', methods=['GET'])
def get_preferences(user_id):
    """Get notification preferences for a user"""
    user_subs = [s for s in subscriptions_db.values() if s["user_id"] == user_id]

    if not user_subs:
        return jsonify({
            "success": True,
            "subscribed": False,
            "preferences": None
        })

    return jsonify({
        "success": True,
        "subscribed": True,
        "preferences": user_subs[0]["preferences"]
    })

@notifications_api.route('/api/notifications/preferences/<user_id>', methods=['PUT'])
def update_preferences(user_id):
    """Update notification preferences"""
    data = request.json

    user_subs = [s for s in subscriptions_db.values() if s["user_id"] == user_id]

    if not user_subs:
        return jsonify({"success": False, "error": "User not subscribed"}), 404

    sub = user_subs[0]
    sub["preferences"].update(data)

    return jsonify({
        "success": True,
        "preferences": sub["preferences"]
    })

# ============================================================================
# NOTIFICATION SENDING API
# ============================================================================

@notifications_api.route('/api/notifications/send', methods=['POST'])
def send_notification():
    """Send a notification to a user"""
    data = request.json
    user_id = data.get('user_id')
    notification_type = data.get('type')
    template_id = data.get('template_id')
    template_vars = data.get('template_vars', {})
    custom_message = data.get('custom_message')

    if not user_id:
        return jsonify({"success": False, "error": "user_id required"}), 400

    # Check if user is subscribed
    user_subs = [s for s in subscriptions_db.values() if s["user_id"] == user_id]

    # Build notification
    notification_id = str(uuid.uuid4())

    if template_id and template_id in TEMPLATES:
        template = TEMPLATES[template_id]
        title = template["title"]
        body = template["body"].format(**template_vars)
        action_text = template.get("action_text")
        action_url = template.get("action_url", "").format(**template_vars)
    elif custom_message:
        title = custom_message.get("title", "PowerSave")
        body = custom_message.get("body", "")
        action_text = custom_message.get("action_text")
        action_url = custom_message.get("action_url")
    else:
        return jsonify({"success": False, "error": "template_id or custom_message required"}), 400

    notification = {
        "id": notification_id,
        "user_id": user_id,
        "type": notification_type or "general",
        "title": title,
        "body": body,
        "action_text": action_text,
        "action_url": action_url,
        "read": False,
        "created_at": datetime.now().isoformat(),
        "metadata": NOTIFICATION_TYPES.get(notification_type, {})
    }

    notifications_db[notification_id] = notification

    # In production: send to FCM, APNS, or web push service
    # For demo, we just store it

    return jsonify({
        "success": True,
        "notification": notification,
        "delivered_to": len(user_subs)
    })

@notifications_api.route('/api/notifications/broadcast', methods=['POST'])
def broadcast_notification():
    """Send notification to all subscribed users"""
    data = request.json
    notification_type = data.get('type')
    template_id = data.get('template_id')
    template_vars = data.get('template_vars', {})

    sent_count = 0

    for sub in subscriptions_db.values():
        # Check preferences
        prefs = sub.get("preferences", {})

        if notification_type == "session_start" and not prefs.get("session_alerts", True):
            continue
        if notification_type == "double_points" and not prefs.get("double_points", True):
            continue
        if notification_type == "tip_of_day" and not prefs.get("tips", True):
            continue

        # Check quiet hours
        quiet = prefs.get("quiet_hours", {})
        if quiet:
            now = datetime.now().strftime("%H:%M")
            if quiet.get("start", "22:00") <= now or now < quiet.get("end", "08:00"):
                continue

        # Send notification
        notification_id = str(uuid.uuid4())

        template = TEMPLATES.get(template_id, {})

        notification = {
            "id": notification_id,
            "user_id": sub["user_id"],
            "type": notification_type,
            "title": template.get("title", "PowerSave"),
            "body": template.get("body", "").format(**template_vars),
            "action_text": template.get("action_text"),
            "action_url": template.get("action_url", "").format(**template_vars),
            "read": False,
            "created_at": datetime.now().isoformat()
        }

        notifications_db[notification_id] = notification
        sent_count += 1

    return jsonify({
        "success": True,
        "sent_count": sent_count,
        "total_subscribers": len(subscriptions_db)
    })

# ============================================================================
# USER NOTIFICATIONS API
# ============================================================================

@notifications_api.route('/api/notifications/<user_id>', methods=['GET'])
def get_user_notifications(user_id):
    """Get all notifications for a user"""
    user_notifs = [n for n in notifications_db.values() if n["user_id"] == user_id]
    user_notifs.sort(key=lambda x: x["created_at"], reverse=True)

    # Pagination
    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)

    paginated = user_notifs[offset:offset + limit]

    unread_count = len([n for n in user_notifs if not n["read"]])

    return jsonify({
        "success": True,
        "notifications": paginated,
        "total": len(user_notifs),
        "unread_count": unread_count
    })

@notifications_api.route('/api/notifications/<notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    """Mark a notification as read"""
    if notification_id not in notifications_db:
        return jsonify({"success": False, "error": "Notification not found"}), 404

    notifications_db[notification_id]["read"] = True

    return jsonify({
        "success": True,
        "notification": notifications_db[notification_id]
    })

@notifications_api.route('/api/notifications/<user_id>/read-all', methods=['PUT'])
def mark_all_read(user_id):
    """Mark all notifications as read for a user"""
    count = 0
    for notif in notifications_db.values():
        if notif["user_id"] == user_id and not notif["read"]:
            notif["read"] = True
            count += 1

    return jsonify({
        "success": True,
        "marked_read": count
    })

# ============================================================================
# SCHEDULED NOTIFICATIONS
# ============================================================================

@notifications_api.route('/api/notifications/schedule', methods=['POST'])
def schedule_notification():
    """Schedule a notification for later"""
    data = request.json
    user_id = data.get('user_id')
    scheduled_time = data.get('scheduled_time')  # ISO format
    template_id = data.get('template_id')
    template_vars = data.get('template_vars', {})

    if not all([user_id, scheduled_time, template_id]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    schedule_id = str(uuid.uuid4())

    scheduled_notifications.append({
        "id": schedule_id,
        "user_id": user_id,
        "scheduled_time": scheduled_time,
        "template_id": template_id,
        "template_vars": template_vars,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    })

    return jsonify({
        "success": True,
        "schedule_id": schedule_id,
        "scheduled_time": scheduled_time
    })

# ============================================================================
# SESSION ALERT TRIGGERS
# ============================================================================

@notifications_api.route('/api/notifications/trigger/session-start', methods=['POST'])
def trigger_session_start():
    """Trigger session start notifications to all users"""
    data = request.json
    duration = data.get('duration', 2)

    result = broadcast_notification_internal(
        notification_type="session_start",
        template_id="session_start_el",
        template_vars={"duration": duration}
    )

    return jsonify({
        "success": True,
        "message": f"Session start notifications sent",
        "sent_count": result
    })

@notifications_api.route('/api/notifications/trigger/double-points', methods=['POST'])
def trigger_double_points():
    """Trigger double points day notification"""
    result = broadcast_notification_internal(
        notification_type="double_points",
        template_id="double_points_el",
        template_vars={}
    )

    return jsonify({
        "success": True,
        "message": "Double points notifications sent",
        "sent_count": result
    })

def broadcast_notification_internal(notification_type: str, template_id: str, template_vars: dict) -> int:
    """Internal helper for broadcasting notifications"""
    sent_count = 0

    template = TEMPLATES.get(template_id, {})

    for sub in subscriptions_db.values():
        notification_id = str(uuid.uuid4())

        notification = {
            "id": notification_id,
            "user_id": sub["user_id"],
            "type": notification_type,
            "title": template.get("title", "PowerSave"),
            "body": template.get("body", "").format(**template_vars),
            "action_text": template.get("action_text"),
            "action_url": template.get("action_url", "").format(**template_vars),
            "read": False,
            "created_at": datetime.now().isoformat()
        }

        notifications_db[notification_id] = notification
        sent_count += 1

    return sent_count

# ============================================================================
# UTILITY ENDPOINTS
# ============================================================================

@notifications_api.route('/api/notifications/templates', methods=['GET'])
def get_templates():
    """Get all notification templates"""
    return jsonify({
        "success": True,
        "templates": TEMPLATES,
        "types": NOTIFICATION_TYPES
    })

@notifications_api.route('/api/notifications/stats/<user_id>', methods=['GET'])
def get_notification_stats(user_id):
    """Get notification statistics for a user"""
    user_notifs = [n for n in notifications_db.values() if n["user_id"] == user_id]

    by_type = {}
    for n in user_notifs:
        t = n.get("type", "other")
        by_type[t] = by_type.get(t, 0) + 1

    return jsonify({
        "success": True,
        "stats": {
            "total": len(user_notifs),
            "unread": len([n for n in user_notifs if not n["read"]]),
            "by_type": by_type
        }
    })
