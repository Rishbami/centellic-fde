"""Synthetic in-memory data for the Fraud AML prototype."""

from typing import Any


ACCOUNTS: list[dict[str, Any]] = [
    {
        "account_id": "ACC-001",
        "account_holder_name": "Northbridge Imports Ltd",
        "balance": 184250.75,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-002",
        "account_holder_name": "Amelia Clarke",
        "balance": 14320.40,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-003",
        "account_holder_name": "Pacific Components UK Ltd",
        "balance": 612480.10,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-004",
        "account_holder_name": "Jonas Weber",
        "balance": 27840.00,
        "country": "DE",
        "status": "restricted",
    },
    {
        "account_id": "ACC-005",
        "account_holder_name": "Cedar Property Group Ltd",
        "balance": 934500.25,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-006",
        "account_holder_name": "Sophie Bennett",
        "balance": 3860.15,
        "country": "GB",
        "status": "restricted",
    },
    {
        "account_id": "ACC-007",
        "account_holder_name": "Chinedu Okafor",
        "balance": 52120.80,
        "country": "NG",
        "status": "under_review",
    },
    {
        "account_id": "ACC-008",
        "account_holder_name": "Atlas Digital Services Ltd",
        "balance": 246700.00,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-009",
        "account_holder_name": "Harbour Medical Supplies Ltd",
        "balance": 428900.60,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-010",
        "account_holder_name": "Lena Foster",
        "balance": 8960.32,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-011",
        "account_holder_name": "Orion Freight Solutions Ltd",
        "balance": 318250.90,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-012",
        "account_holder_name": "Maya Iqbal",
        "balance": 22140.00,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-013",
        "account_holder_name": "Westmere Hospitality Ltd",
        "balance": 156870.44,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-014",
        "account_holder_name": "Elias Haddad",
        "balance": 67400.50,
        "country": "AE",
        "status": "under_review",
    },
    {
        "account_id": "ACC-015",
        "account_holder_name": "Greenfield Community Trust",
        "balance": 88320.16,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-016",
        "account_holder_name": "Horizon Payroll Services Ltd",
        "balance": 1204500.00,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-017",
        "account_holder_name": "Noah Williams",
        "balance": 12450.75,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-018",
        "account_holder_name": "Sakura Education Consulting Ltd",
        "balance": 76400.20,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-019",
        "account_holder_name": "Fatima Al-Mansouri",
        "balance": 112800.00,
        "country": "AE",
        "status": "active",
    },
    {
        "account_id": "ACC-020",
        "account_holder_name": "Baltic Timber Exchange Ltd",
        "balance": 573200.30,
        "country": "EE",
        "status": "under_review",
    },
    {
        "account_id": "ACC-021",
        "account_holder_name": "Rosa Martinez",
        "balance": 19870.84,
        "country": "ES",
        "status": "active",
    },
    {
        "account_id": "ACC-022",
        "account_holder_name": "Summit Travel Group Ltd",
        "balance": 287450.15,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-023",
        "account_holder_name": "Kofi Mensah",
        "balance": 34800.50,
        "country": "GH",
        "status": "active",
    },
    {
        "account_id": "ACC-024",
        "account_holder_name": "Redwood Technology Ltd",
        "balance": 824300.00,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-025",
        "account_holder_name": "Anika Patel",
        "balance": 6450.60,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-026",
        "account_holder_name": "Blue Coast Exporters Ltd",
        "balance": 391720.10,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-027",
        "account_holder_name": "Oliver Grant",
        "balance": 940.25,
        "country": "GB",
        "status": "restricted",
    },
    {
        "account_id": "ACC-028",
        "account_holder_name": "Amina Yusuf",
        "balance": 28650.00,
        "country": "GB",
        "status": "active",
    },
    {
        "account_id": "ACC-029",
        "account_holder_name": "Nova Asset Management Ltd",
        "balance": 2450800.75,
        "country": "GB",
        "status": "under_review",
    },
    {
        "account_id": "ACC-030",
        "account_holder_name": "Meadow Foods Wholesale Ltd",
        "balance": 217600.40,
        "country": "GB",
        "status": "active",
    },
]


ANALYSTS: list[dict[str, Any]] = [
    {
        "analyst_id": "ANL-001",
        "name": "Aisha Rahman",
        "team": "AML Investigations",
        "status": "active",
    },
    {
        "analyst_id": "ANL-002",
        "name": "Daniel Morgan",
        "team": "Fraud Operations",
        "status": "active",
    },
    {
        "analyst_id": "ANL-003",
        "name": "Priya Shah",
        "team": "Sanctions Screening",
        "status": "active",
    },
    {
        "analyst_id": "ANL-004",
        "name": "Marcus Chen",
        "team": "AML Investigations",
        "status": "active",
    },
    {
        "analyst_id": "ANL-005",
        "name": "Elena Petrov",
        "team": "Fraud Operations",
        "status": "away",
    },
    {
        "analyst_id": "ANL-006",
        "name": "Samuel Okafor",
        "team": "Enhanced Due Diligence",
        "status": "active",
    },
    {
        "analyst_id": "ANL-007",
        "name": "Grace Kim",
        "team": "Sanctions Screening",
        "status": "active",
    },
    {
        "analyst_id": "ANL-008",
        "name": "Thomas Bennett",
        "team": "AML Investigations",
        "status": "inactive",
    },
]


def _alert(
    alert_id: str,
    account_id: str,
    analyst_id: str | None,
    amount: float,
    corridor: str,
    rule_triggered: str,
    risk_score: int,
    status: str,
    counterparty: str,
    created_at: str,
    review_outcome: str | None,
) -> dict[str, Any]:
    return {
        "alert_id": alert_id,
        "account_id": account_id,
        "analyst_id": analyst_id,
        "amount": amount,
        "corridor": corridor,
        "rule_triggered": rule_triggered,
        "risk_score": risk_score,
        "status": status,
        "counterparty": counterparty,
        "created_at": created_at,
        "review_outcome": review_outcome,
    }


ALERTS: list[dict[str, Any]] = [
    # Reviewed alerts escalated by an analyst.
    _alert(
        "ALT-001", "ACC-001", "ANL-001", 48500.00, "GB->AE",
        "rapid_funds_movement", 94, "reviewed", "Meridian General Trading", "2026-07-02T09:14:00Z", "escalated",
    ),
    _alert(
        "ALT-002", "ACC-002", "ANL-004", 9900.00, "GB->TR",
        "structuring_pattern", 88, "reviewed", "Bosphorus Exchange Services", "2026-07-05T11:32:00Z", "escalated",
    ),
    _alert(
        "ALT-003", "ACC-003", "ANL-006", 125000.00, "GB->HK",
        "high_risk_corridor", 91, "reviewed", "Eastern Apex Holdings", "2026-07-08T15:46:00Z", "escalated",
    ),
    _alert(
        "ALT-004", "ACC-004", "ANL-003", 18500.00, "DE->GB",
        "sanctions_name_match", 97, "reviewed", "Viktor A. Sokolov", "2026-07-11T08:21:00Z", "escalated",
    ),
    _alert(
        "ALT-005", "ACC-005", "ANL-001", 780000.00, "GB->CY",
        "unusual_transaction_value", 90, "reviewed", "Larnaca Property Ventures", "2026-07-14T13:05:00Z", "escalated",
    ),
    _alert(
        "ALT-006", "ACC-006", "ANL-002", 7450.00, "GB->GB",
        "account_takeover_pattern", 96, "reviewed", "QuickPay Digital Wallet", "2026-07-17T22:41:00Z", "escalated",
    ),
    _alert(
        "ALT-007", "ACC-007", "ANL-006", 33200.00, "NG->GB",
        "rapid_funds_movement", 89, "reviewed", "Westgate Currency Brokers", "2026-07-20T10:18:00Z", "escalated",
    ),
    _alert(
        "ALT-008", "ACC-008", "ANL-004", 24950.00, "GB->AE",
        "multiple_new_counterparties", 87, "reviewed", "Falcon Media FZE", "2026-07-23T16:52:00Z", "escalated",
    ),
    _alert(
        "ALT-009", "ACC-009", "ANL-001", 95000.00, "GB->SG",
        "inconsistent_business_activity", 92, "reviewed", "Lion City Consulting", "2026-07-26T12:27:00Z", "escalated",
    ),
    _alert(
        "ALT-010", "ACC-010", "ANL-002", 4950.00, "GB->LT",
        "structuring_pattern", 86, "reviewed", "Baltic Cash Services", "2026-07-29T09:39:00Z", "escalated",
    ),
    _alert(
        "ALT-011", "ACC-011", "ANL-006", 210000.00, "GB->PA",
        "high_risk_corridor", 95, "reviewed", "Canal Maritime SA", "2026-08-01T14:08:00Z", "escalated",
    ),
    _alert(
        "ALT-012", "ACC-012", "ANL-003", 12750.00, "GB->GB",
        "sanctions_name_match", 93, "reviewed", "M. Al Rashid", "2026-08-04T10:44:00Z", "escalated",
    ),
    _alert(
        "ALT-013", "ACC-020", "ANL-004", 67500.00, "EE->BY",
        "sanctioned_country_exposure", 98, "reviewed", "Minsk Industrial Parts", "2026-08-07T07:56:00Z", "escalated",
    ),
    _alert(
        "ALT-014", "ACC-026", "ANL-001", 41800.00, "GB->NG",
        "round_amount_transfers", 84, "reviewed", "Lagos Commercial Agency", "2026-08-10T17:23:00Z", "escalated",
    ),
    _alert(
        "ALT-015", "ACC-029", "ANL-006", 350000.00, "GB->KY",
        "rapid_funds_movement", 96, "reviewed", "Seven Mile Capital", "2026-08-13T12:12:00Z", "escalated",
    ),

    # Reviewed alerts closed as false positives.
    _alert(
        "ALT-016", "ACC-016", "ANL-004", 286400.00, "GB->GB",
        "high_volume_payments", 73, "reviewed", "Monthly Employee Payroll", "2026-07-03T08:30:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-017", "ACC-017", "ANL-003", 3200.00, "GB->FR",
        "sanctions_name_match", 78, "reviewed", "Mohamed Hassan", "2026-07-06T14:16:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-018", "ACC-018", "ANL-001", 24500.00, "GB->JP",
        "unusual_transaction_value", 69, "reviewed", "Tokyo International University", "2026-07-09T10:05:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-019", "ACC-019", "ANL-004", 40000.00, "AE->GB",
        "new_counterparty", 66, "reviewed", "Al-Mansouri Family Account", "2026-07-12T16:31:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-020", "ACC-021", "ANL-002", 18500.00, "ES->GB",
        "unusual_transaction_value", 72, "reviewed", "Westminster Property Solicitors", "2026-07-15T09:48:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-021", "ACC-022", "ANL-004", 84500.00, "GB->ES",
        "high_volume_payments", 68, "reviewed", "Costa Hotels Group", "2026-07-18T13:22:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-022", "ACC-023", "ANL-001", 12000.00, "GH->GB",
        "rapid_funds_movement", 74, "reviewed", "Mensah Family Savings", "2026-07-21T11:09:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-023", "ACC-024", "ANL-003", 56000.00, "GB->US",
        "sanctions_name_match", 81, "reviewed", "Global Systems Incorporated", "2026-07-24T15:37:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-024", "ACC-025", "ANL-002", 4800.00, "GB->IN",
        "multiple_new_counterparties", 65, "reviewed", "Patel Family Support", "2026-07-27T07:51:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-025", "ACC-015", "ANL-006", 75000.00, "GB->KE",
        "high_risk_corridor", 76, "reviewed", "Nairobi Community Health Project", "2026-07-30T12:43:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-026", "ACC-030", "ANL-004", 118000.00, "GB->NL",
        "round_amount_transfers", 70, "reviewed", "Rotterdam Food Distribution BV", "2026-08-02T09:26:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-027", "ACC-013", "ANL-002", 42500.00, "GB->IE",
        "velocity_spike", 67, "reviewed", "Dublin Events Catering", "2026-08-05T18:02:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-028", "ACC-005", "ANL-001", 325000.00, "GB->GB",
        "unusual_transaction_value", 75, "reviewed", "Cedar Group Client Account", "2026-08-08T14:19:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-029", "ACC-028", "ANL-003", 8900.00, "GB->AE",
        "sanctions_name_match", 79, "reviewed", "A. Yusuf Trading", "2026-08-11T10:57:00Z", "closed_false_positive",
    ),
    _alert(
        "ALT-030", "ACC-009", "ANL-004", 64000.00, "GB->DE",
        "new_counterparty", 71, "reviewed", "Berlin Medical Devices GmbH", "2026-08-14T08:35:00Z", "closed_false_positive",
    ),

    # Reviewed alerts where the analyst requested more information.
    _alert(
        "ALT-031", "ACC-001", "ANL-001", 62000.00, "GB->AE",
        "new_counterparty", 82, "reviewed", "Desert Star Logistics", "2026-08-16T09:11:00Z", "information_requested",
    ),
    _alert(
        "ALT-032", "ACC-003", "ANL-006", 88000.00, "GB->CN",
        "inconsistent_business_activity", 79, "reviewed", "Shenzhen Data Services", "2026-08-18T13:47:00Z", "information_requested",
    ),
    _alert(
        "ALT-033", "ACC-005", "ANL-004", 465000.00, "GB->PT",
        "unusual_transaction_value", 83, "reviewed", "Lisbon Coastal Developments", "2026-08-20T15:28:00Z", "information_requested",
    ),
    _alert(
        "ALT-034", "ACC-007", "ANL-001", 27500.00, "NG->GB",
        "source_of_funds_mismatch", 85, "reviewed", "Okafor Family Holdings", "2026-08-22T10:03:00Z", "information_requested",
    ),
    _alert(
        "ALT-035", "ACC-008", "ANL-004", 19800.00, "GB->AE",
        "multiple_new_counterparties", 77, "reviewed", "Palm Creative Studio", "2026-08-24T17:36:00Z", "information_requested",
    ),
    _alert(
        "ALT-036", "ACC-011", "ANL-006", 145000.00, "GB->MT",
        "high_risk_corridor", 84, "reviewed", "Valletta Shipping Partners", "2026-08-26T11:52:00Z", "information_requested",
    ),
    _alert(
        "ALT-037", "ACC-013", "ANL-002", 36800.00, "GB->FR",
        "velocity_spike", 75, "reviewed", "Paris Hospitality Supply", "2026-08-28T08:42:00Z", "information_requested",
    ),
    _alert(
        "ALT-038", "ACC-014", "ANL-001", 54000.00, "AE->GB",
        "rapid_funds_movement", 86, "reviewed", "Haddad Consulting Ltd", "2026-08-30T14:25:00Z", "information_requested",
    ),
    _alert(
        "ALT-039", "ACC-018", "ANL-004", 31500.00, "GB->KR",
        "new_counterparty", 73, "reviewed", "Seoul Academic Partners", "2026-09-01T09:54:00Z", "information_requested",
    ),
    _alert(
        "ALT-040", "ACC-020", "ANL-006", 92000.00, "EE->GE",
        "inconsistent_business_activity", 88, "reviewed", "Tbilisi Building Materials", "2026-09-03T12:06:00Z", "information_requested",
    ),
    _alert(
        "ALT-041", "ACC-022", "ANL-002", 67500.00, "GB->TR",
        "round_amount_transfers", 78, "reviewed", "Anatolia Travel Services", "2026-09-05T16:18:00Z", "information_requested",
    ),
    _alert(
        "ALT-042", "ACC-024", "ANL-001", 134000.00, "GB->IN",
        "unusual_transaction_value", 80, "reviewed", "Bengaluru Software Labs", "2026-09-07T10:39:00Z", "information_requested",
    ),
    _alert(
        "ALT-043", "ACC-026", "ANL-004", 38500.00, "GB->GH",
        "new_counterparty", 76, "reviewed", "Accra Export Cooperative", "2026-09-09T07:45:00Z", "information_requested",
    ),
    _alert(
        "ALT-044", "ACC-029", "ANL-006", 275000.00, "GB->LU",
        "source_of_funds_mismatch", 89, "reviewed", "Luxembourg Private Markets SA", "2026-09-11T13:58:00Z", "information_requested",
    ),
    _alert(
        "ALT-045", "ACC-030", "ANL-001", 86500.00, "GB->BE",
        "high_volume_payments", 74, "reviewed", "Antwerp Produce Exchange", "2026-09-13T09:17:00Z", "information_requested",
    ),

    # Current queue: unassigned, under review, or awaiting information.
    _alert(
        "ALT-046", "ACC-002", None, 9850.00, "GB->TR",
        "structuring_pattern", 87, "unassigned", "Istanbul Payment Solutions", "2026-09-27T08:15:00Z", None,
    ),
    _alert(
        "ALT-047", "ACC-004", "ANL-003", 16200.00, "DE->GB",
        "sanctions_name_match", 95, "under_review", "Viktor Sokoloff", "2026-09-27T09:42:00Z", None,
    ),
    _alert(
        "ALT-048", "ACC-016", None, 301800.00, "GB->GB",
        "high_volume_payments", 72, "unassigned", "September Employee Payroll", "2026-09-27T10:24:00Z", None,
    ),
    _alert(
        "ALT-049", "ACC-001", "ANL-001", 57500.00, "GB->AE",
        "rapid_funds_movement", 91, "under_review", "Golden Crescent Trading", "2026-09-27T12:09:00Z", None,
    ),
    _alert(
        "ALT-050", "ACC-018", None, 28900.00, "GB->JP",
        "unusual_transaction_value", 74, "unassigned", "Osaka Language Institute", "2026-09-27T14:33:00Z", None,
    ),
    _alert(
        "ALT-051", "ACC-020", "ANL-007", 104000.00, "EE->KZ",
        "sanctioned_country_exposure", 93, "under_review", "Steppe Machinery LLP", "2026-09-28T07:58:00Z", None,
    ),
    _alert(
        "ALT-052", "ACC-024", "ANL-004", 148000.00, "GB->IN",
        "new_counterparty", 81, "under_review", "Pune Cloud Technologies", "2026-09-28T09:21:00Z", None,
    ),
    _alert(
        "ALT-053", "ACC-025", None, 4950.00, "GB->IN",
        "multiple_new_counterparties", 68, "unassigned", "Patel Household Account", "2026-09-28T11:47:00Z", None,
    ),
    _alert(
        "ALT-054", "ACC-006", "ANL-002", 6800.00, "GB->GB",
        "account_takeover_pattern", 98, "under_review", "InstantCoin Exchange", "2026-09-28T18:36:00Z", None,
    ),
    _alert(
        "ALT-055", "ACC-014", None, 61000.00, "AE->GB",
        "source_of_funds_mismatch", 84, "unassigned", "Haddad Property Services", "2026-09-29T08:04:00Z", None,
    ),
    _alert(
        "ALT-056", "ACC-015", "ANL-006", 82000.00, "GB->UG",
        "high_risk_corridor", 79, "under_review", "Kampala Water Initiative", "2026-09-29T10:19:00Z", None,
    ),
    _alert(
        "ALT-057", "ACC-027", None, 925.00, "GB->GB",
        "velocity_spike", 90, "unassigned", "FastVoucher Marketplace", "2026-09-29T13:26:00Z", None,
    ),
    _alert(
        "ALT-058", "ACC-028", "ANL-007", 11200.00, "GB->AE",
        "sanctions_name_match", 82, "under_review", "Amina Youssef Trading", "2026-09-29T15:41:00Z", None,
    ),
    _alert(
        "ALT-059", "ACC-029", "ANL-001", 420000.00, "GB->KY",
        "rapid_funds_movement", 97, "under_review", "Harbour View Investments", "2026-09-30T07:37:00Z", None,
    ),
    _alert(
        "ALT-060", "ACC-030", None, 94000.00, "GB->NL",
        "round_amount_transfers", 77, "unassigned", "Amsterdam Food Logistics BV", "2026-09-30T09:12:00Z", None,
    ),
]
