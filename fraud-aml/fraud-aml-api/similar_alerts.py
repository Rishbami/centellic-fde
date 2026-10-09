from data import ALERTS


# Function to get all reviewed alerts
def get_reviewed_alerts():
    reviewed_alerts = []

    for alert in ALERTS:
        if alert["review_outcome"] is not None:
            reviewed_alerts.append(alert)
    return reviewed_alerts


# Find reviewed alerts that triggered same rule as current alerts
def find_similar_alerts(current_alert):
    similar_alerts = []

    for alert in get_reviewed_alerts():
        if alert["alert_id"] == current_alert["alert_id"]:
            continue

        if alert["rule_triggered"] == current_alert["rule_triggered"]:
            similar_alerts.append(alert)

    similar_alerts.sort(
        key=lambda alert: abs(alert["amount"] - current_alert["amount"])
    )

    return similar_alerts
