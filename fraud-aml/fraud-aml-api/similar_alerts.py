from data import ALERTS


# Function to get all reviewed alerts
def get_reviewed_alerts():
    reviewed_alerts = []

    for alert in ALERTS:
        if alert["review_outcome"] is not None:
            reviewed_alerts.append(alert)
    return reviewed_alerts


# Find reviewed alerts that triggered same rule as current alerts
def find_similar_alerts(current_alert, limit=5):
    similar_alerts = []

    for alert in get_reviewed_alerts():
        if alert["alert_id"] == current_alert["alert_id"]:
            continue

        if alert["rule_triggered"] == current_alert["rule_triggered"]:
            similar_alerts.append(alert)

    similar_alerts.sort(
        key=lambda alert: (
            alert["corridor"] != current_alert["corridor"],
            abs(alert["amount"] - current_alert["amount"]),
        )
    )

    results = []

    for alert in similar_alerts[:limit]:
        results.append(
            {
                "alert_id": alert["alert_id"],
                "rule_triggered": alert["rule_triggered"],
                "corridor": alert["corridor"],
                "amount": alert["amount"],
                "review_outcome": alert["review_outcome"],
                "same_corridor": alert["corridor"] == current_alert["corridor"],
                "amount_difference": abs(alert["amount"] - current_alert["amount"]),
            }
        )

    return results
