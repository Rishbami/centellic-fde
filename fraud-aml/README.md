# Fraud AML

A fraud and anti-money laundering alert investigation assistant.

The system allows analysts to review fraud/AML alerts, search relevant guidance, compare alerts with similar previously reviewed cases, and receive an AI-generated recommendation while keeping the final decision with the human analyst.

## Project Structure

- `fraud-aml-api/` - FastAPI backend, alert data, AI features, vector search and agent tools
- `fraud-aml-ui/` - Streamlit user interface
- `README.md` - Project documentation

## Business Problem

A payments company can generate a large number of fraud and anti-money laundering alerts.

Analysts have to review these alerts and decide whether the activity looks suspicious, whether more information is needed, or whether the alert is likely to be a false alarm.

Reviewing every alert manually can take a lot of time, especially when analysts also need to check company guidance and compare the alert with previous cases.

The aim of this project is to help analysts investigate alerts faster while keeping the final decision with the human analyst.

## User

The main user is a fraud or AML analyst.

The analyst needs to:

- Review alerts
- Understand why an alert was raised
- Check relevant company guidance
- Compare alerts with similar previous cases
- Decide what action should be taken

## Main Decision

The system helps the analyst decide whether an alert should be:

- Escalated
- Investigated further / more information requested
- Recommended for closure as a likely false positive

The AI only makes a recommendation. The analyst makes the final decision.

## Planned Features

- View fraud/AML alerts
- View individual alert details
- View account information linked to an alert
- Search company guidance and procedures
- Search similar previously reviewed alerts
- AI recommendation for each alert
- Alert queue interface
- Allow analysts to accept alerts
- View alerts assigned to an analyst
- Human makes the final decision

## Data Model

### Accounts

Accounts provide context for the alerts raised against them.

- `account_id`
- `account_holder_name`
- `balance`
- `country`
- `status`

### Analysts

Analysts review alerts and can accept alerts to make them their own.

- `analyst_id`
- `name`
- `team`
- `status`

### Documents

Documents provide the guidance and procedures that the AI can search when helping with an alert.

- `document_id`
- `title`
- `document_type`
- `content`
- `created_at`

Document types may include:

- Typology guides
- Investigation procedures
- Sanctions guidance
- Suspicious activity reporting steps
- False positive case notes

### Alerts

Alerts represent activity that has already been flagged as potentially suspicious and requires review.

- `alert_id`
- `account_id`
- `analyst_id`
- `amount`
- `corridor`
- `rule_triggered`
- `risk_score`
- `status`
- `counterparty`
- `created_at`
- `review_outcome`

`analyst_id` can be empty when an alert has not yet been accepted by an analyst.

`review_outcome` can be empty while the alert is still being investigated and can later store the decision made by the analyst.

The alert data will be created for the project. The AI does not generate the original alerts.

## Alert Investigation Flow

1. An alert already exists because activity has been flagged for review.
2. The alert appears in the alert queue.
3. An analyst can accept the alert and make it their own.
4. The analyst views the alert and account details.
5. The AI can search relevant company guidance and procedures.
6. The extra agent tool can search previously reviewed alerts for similar cases.
7. The AI uses the guidance, alert details and previous similar cases to make a recommendation.
8. The analyst makes the final decision.
9. The final outcome can be stored with the alert and may later help when reviewing similar alerts.

## AI Responsibilities

The AI will:

- Review the details of an alert
- Search relevant guidance and procedures
- Use similar previously reviewed alerts as additional information
- Summarise the available evidence
- Return a recommendation with reasons

The AI will not:

- Create the original fraud/AML alert
- Automatically close an alert
- Make the final decision for the analyst

## Knowledge Search Tool

The agent will have a knowledge search tool which searches the company documents stored in Chroma.

This allows the AI to answer questions such as:

- What does the investigation procedure say about this alert?
- What guidance exists for this type of activity?
- What steps should the analyst follow?
- Does the guidance describe this type of suspicious behaviour?

Voyage embeddings will be used to convert the documents into embeddings so they can be searched by meaning.

## Extra Agent Tool

The extra agent tool will search previously reviewed alerts for similar cases.

It may compare alerts using information such as:

- The same or similar rule being triggered
- Similar transaction amounts
- Similar payment corridors
- The same counterparty
- Similar account information
- Similar behaviour across multiple alerts

The tool can also return the outcome of those previous alerts.

For example, it could show that several similar alerts were previously escalated, or that similar alerts were previously found to be false positives.

The AI can use this information as extra evidence when making its recommendation.

The previous outcome does not automatically decide the result of the new alert. It is only additional information for the AI and analyst to consider.

## Structured AI Output

The structured analysis will return fields such as:

- `recommendation`
- `risk_level`
- `reasons`
- `similar_alerts`
- `recommended_next_step`

The recommendation may be:

- `escalate`
- `request_information`
- `recommend_close`

## Refusal Rule

The system should refuse to give a grounded answer when it cannot find relevant enough guidance.

If no retrieved document passes the chosen relevance threshold, the system should not call the LLM for the grounded answer.

Instead, it should tell the analyst that there is not enough relevant information available.

## Human-in-the-Loop Rule

The AI can recommend that an alert should be closed, escalated or investigated further, but it cannot make the final decision itself.

A human analyst must make the final decision.

This reduces the risk of action being taken against an account based only on an AI-generated recommendation.

## Custom UI Feature

The Streamlit interface will include an alert queue.

The queue may include:

- Unassigned alerts
- My alerts
- Alert status
- Risk score
- Accept alert button
- Alert details
- Account details
- Similar reviewed alerts
- AI recommendation

An analyst can accept an unassigned alert and make it their own for investigation.

## Success Criteria

The project should allow an analyst to:

1. View available alerts
2. Accept an alert
3. View the alert and account details
4. Search relevant company guidance
5. Find similar previously reviewed alerts
6. See what happened in those previous cases
7. Receive an AI recommendation with reasons
8. Make the final decision themselves
9. Save the outcome of the reviewed alert

## Tech Stack

- Python
- FastAPI
- Streamlit
- Claude
- Chroma
- Voyage embeddings

## Running the Project

Instructions will be added as the backend and frontend are built.