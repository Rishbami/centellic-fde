"""Initial labelled benchmark for the synthetic AML guidance corpus.

There are 12 answerable questions across all eight documents and four questions
the corpus cannot answer. This evaluates document retrieval and grounded answers,
not the historical-alert tool or real-world regulatory correctness.

doc_id is the primary retrieval target; evidence is an exact supporting passage.
Unanswerable entries have doc_id/evidence set to None and should receive refusal.
Review apparent retrieval misses: another document may also support an answer,
and these primary labels are not an exhaustive annotation of every valid passage.

Keywords are hints for a later answer checker, not proof of correctness. All list
items are intended to match, with | separating alternatives and a trailing *
allowing word endings, following Firm Intelligence's convention. That matcher
is not implemented here; semantic correctness still needs review.
"""


EVAL_SET = [
    {
        "id": "q01",
        "question": (
            "When investigating possible structuring, should payments be assessed "
            "individually or together?"
        ),
        "doc_id": "doc-001",
        "evidence": (
            "Analysts should assess the combined value and pattern rather than "
            "treating each payment in isolation."
        ),
        "keywords": ["combined|together|aggregate*", "pattern*"],
        "kind": "procedure",
    },
    {
        "id": "q02",
        "question": "Does a single structuring indicator prove suspicious activity?",
        "doc_id": "doc-001",
        "evidence": "A single indicator does not prove suspicious activity.",
        "keywords": ["single", "not|no|cannot|insufficient", "prove|proof"],
        "kind": "negation",
    },
    {
        "id": "q03",
        "question": (
            "Is a high-risk payment corridor sufficient on its own to justify escalation?"
        ),
        "doc_id": "doc-002",
        "evidence": (
            "A high-risk corridor should prompt closer review but must not be "
            "used as the sole reason for escalation."
        ),
        "keywords": ["corridor", "not|no|cannot|insufficient", "alone|sole|own"],
        "kind": "negation",
    },
    {
        "id": "q04",
        "question": "How should previous alert outcomes influence a new investigation?",
        "doc_id": "doc-003",
        "evidence": (
            "Search relevant company guidance and compare the case with previously "
            "reviewed alerts, while treating previous outcomes only as supporting evidence."
        ),
        "keywords": ["support*", "evidence"],
        "kind": "historical_evidence",
    },
    {
        "id": "q05",
        "question": "Who must make and record the final alert decision?",
        "doc_id": "doc-003",
        "evidence": (
            "An AI recommendation may support the review, but the assigned analyst "
            "must make and record the final decision."
        ),
        "keywords": ["analyst", "final", "record*|document*"],
        "kind": "decision_authority",
    },
    {
        "id": "q06",
        "question": (
            "What internal information must analysts avoid disclosing when requesting evidence?"
        ),
        "doc_id": "doc-004",
        "evidence": (
            "Analysts must not disclose internal monitoring rules, risk thresholds, "
            "or whether a suspicious activity report is being considered."
        ),
        "keywords": ["monitoring", "threshold*", "report*|SAR"],
        "kind": "disclosure_restriction",
    },
    {
        "id": "q07",
        "question": "Is a name-only sanctions match enough to confirm a true match?",
        "doc_id": "doc-005",
        "evidence": (
            "A name-only match is not sufficient to confirm a true match, "
            "particularly where the name is common."
        ),
        "keywords": ["name", "not|no|insufficient|cannot"],
        "kind": "negation",
    },
    {
        "id": "q08",
        "question": (
            "What should happen when sanctions review finds material identifier "
            "matches or ownership/control concerns?"
        ),
        "doc_id": "doc-005",
        "evidence": (
            "Material identifier matches, ownership or control concerns, or links "
            "to a sanctioned country must be escalated immediately to the sanctions team."
        ),
        "keywords": ["escalat*", "immediat*", "sanctions", "team"],
        "kind": "escalation_procedure",
    },
    {
        "id": "q09",
        "question": "Who decides whether an external suspicious activity report is required?",
        "doc_id": "doc-006",
        "evidence": (
            "The nominated team decides whether an external suspicious activity "
            "report is required; the investigating analyst and the AI assistant "
            "do not submit one automatically."
        ),
        "keywords": ["nominated", "team"],
        "kind": "decision_authority",
    },
    {
        "id": "q10",
        "question": "What evidence supported the payroll case being treated as a false positive?",
        "doc_id": "doc-007",
        "evidence": (
            "Review showed that the counterparties were established employees, "
            "the payment references matched payroll records, and the same "
            "monthly pattern had occurred for more than a year."
        ),
        "keywords": ["employee*", "payroll", "month*", "year"],
        "kind": "case_evidence",
    },
    {
        "id": "q11",
        "question": (
            "What differences would require further investigation in another batch-payment alert?"
        ),
        "doc_id": "doc-007",
        "evidence": (
            "This outcome should not be applied automatically to other batch-payment "
            "alerts; new counterparties, irregular timing, or unexplained value "
            "changes would require further investigation."
        ),
        "keywords": ["new|unfamiliar", "counterpart*", "timing", "value|amount*"],
        "kind": "exception",
    },
    {
        "id": "q12",
        "question": (
            "Can future sanctions alerts involving a previously cleared name skip another check?"
        ),
        "doc_id": "doc-008",
        "evidence": (
            "Future alerts involving the same name should still be checked against "
            "the current sanctions record because list entries and identifying "
            "information can change."
        ),
        "keywords": ["check*|review*", "current|up-to-date", "change*"],
        "kind": "exception",
    },
    {
        "id": "q13",
        "question": "What exact monetary threshold triggers a structuring alert?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable",
    },
    {
        "id": "q14",
        "question": (
            "Within how many hours must an external suspicious activity report be filed?"
        ),
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable",
    },
    {
        "id": "q15",
        "question": "Have the payroll records for alert ALT-048 been independently verified?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable",
    },
    {
        "id": "q16",
        "question": "Which sanctions list provider does the company use?",
        "doc_id": None,
        "evidence": None,
        "keywords": [],
        "kind": "unanswerable",
    },
]
