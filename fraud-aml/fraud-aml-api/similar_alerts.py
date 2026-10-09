from data import ALERTS


# Function to get all reviewed alerts
def get_reviewed_alerts():
    reviewed_alerts = []

    for alert in ALERTS:
        if alert["reviewed_outcome"] is not None:
            reviewed_alerts.append(alert)
    return reviewed_alerts
