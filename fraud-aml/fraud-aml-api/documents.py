"""Synthetic company documents used to build the AML knowledge index."""

from typing import Any


DOCUMENTS: list[dict[str, Any]] = [
    {
        "document_id": "doc-001",
        "title": "Structuring and Rapid Movement Typology Guide",
        "document_type": "typology_guide",
        "content": (
            "Structuring is the deliberate splitting of funds into smaller payments "
            "to avoid monitoring thresholds or reduce scrutiny. Indicators include "
            "repeated transfers just below a threshold, several payments sent within "
            "a short period, use of multiple counterparties with no clear commercial "
            "reason, and funds leaving an account soon after they arrive. Analysts "
            "should assess the combined value and pattern rather than treating each "
            "payment in isolation. A new account, an unexplained increase in activity, "
            "or movement through several countries increases concern. A single "
            "indicator does not prove suspicious activity. The analyst should compare "
            "the activity with the account profile, expected use, and any available "
            "source-of-funds information before deciding whether to escalate or request "
            "more information."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-002",
        "title": "Unusual Payment Corridors and Counterparty Risk Guide",
        "document_type": "typology_guide",
        "content": (
            "An unusual payment corridor is one that does not match the customer's "
            "known location, business activity, or historic transaction pattern. Risk "
            "may be higher where funds pass through several jurisdictions, where the "
            "counterparty has no obvious connection to the account holder, or where "
            "payment descriptions are vague or inconsistent. Analysts should review "
            "the origin and destination countries, transaction amount, frequency, "
            "counterparty history, account balance, and the rule that triggered the "
            "alert. A high-risk corridor should prompt closer review but must not be "
            "used as the sole reason for escalation. Legitimate explanations may "
            "include supplier payments, family support, relocation, or an established "
            "cross-border business relationship. Evidence should be recorded for both "
            "risk indicators and plausible legitimate explanations."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-003",
        "title": "Standard Alert Investigation Procedure",
        "document_type": "investigation_procedure",
        "content": (
            "Begin by confirming the alert details, including the triggered rule, "
            "amount, corridor, counterparty, risk score, and creation time. Review the "
            "linked account's status, country, balance, expected activity, and recent "
            "transaction history. Determine whether the alert reflects an isolated "
            "transaction or a wider pattern. Search relevant company guidance and "
            "compare the case with previously reviewed alerts, while treating previous "
            "outcomes only as supporting evidence. Record facts that support suspicion "
            "and facts that support a legitimate explanation. If key context is "
            "missing, request information rather than assuming intent. The available "
            "outcomes are escalate, request further information, or recommend closure "
            "as a likely false positive. An AI recommendation may support the review, "
            "but the assigned analyst must make and record the final decision."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-004",
        "title": "Information Request and Evidence Checklist",
        "document_type": "investigation_procedure",
        "content": (
            "Request further information when the transaction may be legitimate but "
            "the available evidence is insufficient to reach a supported outcome. "
            "Depending on the alert, useful evidence may include the purpose of the "
            "payment, source of funds, invoices, contracts, proof of relationship to "
            "the counterparty, and an explanation for changes in account activity. "
            "Requests should be specific and proportionate to the identified risk. "
            "Analysts must not disclose internal monitoring rules, risk thresholds, or "
            "whether a suspicious activity report is being considered. When evidence "
            "is received, verify that names, dates, amounts, and counterparties match "
            "the observed activity. Missing, altered, contradictory, or implausible "
            "evidence should be documented and may justify escalation."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-005",
        "title": "Sanctions Screening Alert Guidance",
        "document_type": "sanctions_guidance",
        "content": (
            "A sanctions screening alert must be reviewed to determine whether it is a "
            "true match or a false positive. Compare the account holder or counterparty "
            "against the screened record using all available identifiers, including "
            "full name, aliases, date of birth, nationality, address, registration "
            "details, and country. A name-only match is not sufficient to confirm a "
            "true match, particularly where the name is common. Material identifier "
            "matches, ownership or control concerns, or links to a sanctioned country "
            "must be escalated immediately to the sanctions team. Analysts must not "
            "tell the customer that sanctions screening caused the review. They must "
            "also avoid releasing, rejecting, or otherwise acting on funds solely from "
            "an AI recommendation. Any restriction or reporting decision requires "
            "authorised human review under the applicable sanctions procedure."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-006",
        "title": "Suspicious Activity Escalation and Reporting Steps",
        "document_type": "sar_procedure",
        "content": (
            "Where an investigation identifies reasonable grounds for suspicion, the "
            "analyst should escalate the case to the nominated financial crime team. "
            "The case record should contain a concise chronology, relevant transaction "
            "amounts and dates, account and counterparty details, the triggered rules, "
            "supporting documents, and a clear explanation of why the activity is "
            "unusual or inconsistent with the account profile. Separate verified facts "
            "from assumptions and include any reasonable explanation considered. The "
            "nominated team decides whether an external suspicious activity report is "
            "required; the investigating analyst and the AI assistant do not submit "
            "one automatically. The customer must not be informed that a report is "
            "being considered or has been made. All decisions, including a decision "
            "not to report, must be documented with an audit trail."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-007",
        "title": "False Positive Case Note: Established Payroll Payments",
        "document_type": "false_positive_case_note",
        "content": (
            "A business account triggered a high-volume payment alert after sending "
            "multiple similar-value transfers to domestic counterparties on the final "
            "working day of the month. The combined amount was materially higher than "
            "the alert threshold. Review showed that the counterparties were established "
            "employees, the payment references matched payroll records, and the same "
            "monthly pattern had occurred for more than a year. The account balance "
            "and business profile supported the activity, and no unusual international "
            "corridor or rapid onward movement was identified. The analyst recommended "
            "closure as a false positive and recorded payroll evidence as the reason. "
            "This outcome should not be applied automatically to other batch-payment "
            "alerts; new counterparties, irregular timing, or unexplained value changes "
            "would require further investigation."
        ),
        "created_at": "2026-09-30",
    },
    {
        "document_id": "doc-008",
        "title": "False Positive Case Note: Common-Name Sanctions Match",
        "document_type": "false_positive_case_note",
        "content": (
            "An international payment triggered a sanctions screening alert because "
            "the counterparty's name resembled a listed individual. The analyst compared "
            "the available identifiers and found that the counterparty had a different "
            "date of birth, nationality, address, and middle name. The payment corridor "
            "was consistent with the customer's established supplier activity, and "
            "invoices supported the commercial relationship. After authorised sanctions "
            "review, the alert was closed as a false positive caused by a common-name "
            "match. The decision was based on conflicting identifiers, not merely on "
            "the customer's explanation. Future alerts involving the same name should "
            "still be checked against the current sanctions record because list entries "
            "and identifying information can change."
        ),
        "created_at": "2026-09-30",
    },
]
