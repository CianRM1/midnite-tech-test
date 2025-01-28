from django.core.cache import cache

from .constants import ALERT_CODES

# We could potentially store key user actions in a database
# The below approach is used to keep it simple but still cache actions


def store_user_action(user_id, action_type, amount, timestamp):
    # Stores user action in cache - FIFO approach
    key = f"user_{user_id}_actions"
    actions = cache.get(key, [])
    actions.append({"type": action_type, "amount": amount, "time": timestamp})

    # Keep only the last 10 actions
    if len(actions) > 10:
        actions.pop(0)

    cache.set(key, actions, timeout=3600)
    return actions


def check_alerts(user_id, action_type, amount, timestamp):
    # Checks all alert conditions based on stored user actions
    actions = store_user_action(user_id, action_type, amount, timestamp)
    alerts = []

    # Rule 1: Withdrawal over 100
    if action_type == "withdraw" and amount > 100:
        alerts.append(ALERT_CODES["WITHDRAWAL_LIMIT"])

    # Rule 2: Three consecutive withdrawals
    if len(actions) >= 3 and all(a["type"] == "withdraw" for a in actions[-3:]):
        alerts.append(ALERT_CODES["CONSECUTIVE_WITHDRAWALS"])

    # Rule 3: Three consecutive increasing deposits
    deposits = [a["amount"] for a in actions if a["type"] == "deposit"]
    if len(deposits) >= 3 and deposits[-3] < deposits[-2] < deposits[-1]:
        alerts.append(ALERT_CODES["INCREASING_DEPOSITS"])

    # Rule 4: Deposits exceeding 200 within 30 seconds
    total_deposits = sum(
        a["amount"] for a in actions if a["type"] == "deposit" and timestamp - a["time"] <= 30
    )
    if total_deposits > 200:
        alerts.append(ALERT_CODES["TOTAL_DEPOSITS_EXCEEDED"])

    return alerts
