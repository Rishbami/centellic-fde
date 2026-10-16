import os
from pathlib import Path

import requests
import streamlit as st
from dotenv import load_dotenv


load_dotenv(Path(__file__).with_name(".env"))
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000").rstrip("/")


class APIError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def request_json(method, path, **kwargs):
    try:
        with requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=(3, 15),
            **kwargs,
        ) as response:
            response.raise_for_status()
            return response.json()
    except requests.exceptions.Timeout as exc:
        raise APIError("The service timed out. Please try again.") from exc
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code
        messages = {
            404: "The requested record or endpoint was not found.",
            409: "The request conflicts with the current service state.",
            422: "Please check the submitted values.",
            429: "Too many requests. Please try again shortly.",
            502: "The AI provider is currently unavailable.",
            504: "The AI request timed out. Please try again.",
        }
        raise APIError(
            messages.get(status, "The service could not complete the request."),
            status_code=status,
        ) from exc
    except requests.exceptions.JSONDecodeError as exc:
        raise APIError("The service returned an invalid response.") from exc
    except requests.exceptions.RequestException as exc:
        raise APIError("Could not connect to the service. Please try again.") from exc


def render_queue(analyst_id, analysts):
    queue_filter = st.radio(
        "Queue",
        ["Unassigned", "My Alerts", "Reviewed"],
        horizontal=True,
        key="queue_filter",
    )
    st.button("Refresh queue", icon=":material/refresh:")

    try:
        alerts = request_json("GET", "/alerts")
    except APIError as exc:
        st.error(str(exc))
        return

    if queue_filter == "Unassigned":
        filtered = [
            alert for alert in alerts
            if alert["status"] == "unassigned" and alert["analyst_id"] is None
        ]
    elif queue_filter == "My Alerts":
        filtered = [
            alert for alert in alerts
            if alert["analyst_id"] == analyst_id and alert["status"] != "reviewed"
        ]
    else:
        filtered = [alert for alert in alerts if alert["status"] == "reviewed"]

    if not filtered:
        st.info("No alerts in this queue.")
        return

    analyst_names = {a["analyst_id"]: a["name"] for a in analysts}
    rows = [{
        "Alert ID": alert["alert_id"],
        "Rule": alert["rule_triggered"],
        "Amount": alert["amount"],
        "Corridor": alert["corridor"],
        "Risk score": alert["risk_score"],
        "Status": alert["status"],
        "Analyst": analyst_names.get(alert["analyst_id"], alert["analyst_id"] or "Unassigned"),
    } for alert in filtered]
    st.dataframe(
        rows,
        hide_index=True,
        width="stretch",
        column_config={"Amount": st.column_config.NumberColumn(format="%.2f")},
    )

    alert_ids = [alert["alert_id"] for alert in filtered]
    selected_id = st.session_state.get("selected_alert_id")
    if st.session_state.get("queue_alert_picker") not in alert_ids:
        st.session_state.queue_alert_picker = (
            selected_id if selected_id in alert_ids else alert_ids[0]
        )
    selected_id = st.selectbox("Alert", alert_ids, key="queue_alert_picker")
    st.session_state.selected_alert_id = selected_id

    try:
        alert = request_json("GET", f"/alerts/{selected_id}")
    except APIError as exc:
        st.error(str(exc))
        return

    alert_column, account_column = st.columns(2)
    with alert_column:
        st.subheader("Alert details")
        st.table([
            {"Field": field.replace("_", " ").capitalize(), "Value": str(value) if value is not None else "Not recorded"}
            for field, value in alert.items()
        ])

    with account_column:
        st.subheader("Account details")
        try:
            account = request_json("GET", f"/accounts/{alert['account_id']}")
        except APIError as exc:
            st.error(str(exc))
            return
        st.table([
            {"Field": field.replace("_", " ").capitalize(), "Value": str(value) if value is not None else "Not recorded"}
            for field, value in account.items()
        ])


def render_search():
    if "guidance_question" not in st.session_state:
        st.session_state.guidance_question = st.session_state.get("last_search_question", "")

    with st.form("guidance_search"):
        question = st.text_input("Question", key="guidance_question")
        submitted = st.form_submit_button("Search", icon=":material/search:")

    if submitted:
        question = question.strip()
        st.session_state.last_search_question = question
        st.session_state.pop("guidance_results", None)
        st.session_state.pop("guidance_feedback", None)

        if not question:
            st.session_state.guidance_feedback = ("warning", "Enter a question to search.")
        else:
            try:
                with st.spinner("Searching guidance..."):
                    result = request_json(
                        "POST",
                        "/knowledge/search",
                        json={"question": question, "top_k": 3},
                    )
                st.session_state.guidance_results = {
                    "question": question,
                    "results": result["results"],
                }
            except APIError as exc:
                if exc.status_code == 409:
                    st.session_state.guidance_feedback = (
                        "warning", "Guidance index has not been built."
                    )
                else:
                    st.session_state.guidance_feedback = ("error", str(exc))

    feedback = st.session_state.get("guidance_feedback")
    if feedback:
        level, message = feedback
        if level == "warning":
            st.warning(message)
        else:
            st.error(message)

    saved = st.session_state.get("guidance_results")
    if saved is None:
        return

    st.caption(f"Results for: {saved['question']}")
    if not saved["results"]:
        st.info("No guidance found.")
        return

    for hit in saved["results"]:
        st.subheader(hit["title"])
        st.caption(f"{hit['id']} | Score: {hit['score']:.3f}")
        st.write(hit["text"])
        st.divider()


def main():
    st.set_page_config(page_title="Fraud AML", layout="wide")
    st.sidebar.title("Fraud AML")
    view = st.sidebar.radio(
        "Workspace",
        ["Alert Queue", "Ask", "Search Guidance", "Streaming Summary"],
        key="current_view",
    )
    st.sidebar.button(
        "Refresh connection",
        icon=":material/refresh:",
        help="Check the service connection again",
    )

    connection_error = None
    try:
        health = request_json("GET", "/health")
        if not isinstance(health, dict) or health.get("status") != "ok":
            raise APIError("The service is not ready. Please try again.")
    except APIError as exc:
        connection_error = str(exc)

    if connection_error:
        st.sidebar.error("API unavailable")
    else:
        st.sidebar.success("API connected")

    st.title(view)
    if connection_error:
        st.error(connection_error)
        return

    try:
        analysts = request_json("GET", "/analysts")
    except APIError as exc:
        st.error(str(exc))
        return

    if not analysts:
        st.warning("No analysts available.")
        return

    analyst_names = {a["analyst_id"]: a["name"] for a in analysts}
    analyst_ids = list(analyst_names)
    if st.session_state.get("analyst_picker") not in analyst_ids:
        previous_id = st.session_state.get("selected_analyst_id")
        st.session_state.analyst_picker = (
            previous_id if previous_id in analyst_ids else analyst_ids[0]
        )
    analyst_id = st.sidebar.selectbox(
        "Analyst",
        analyst_ids,
        format_func=lambda value: analyst_names[value],
        key="analyst_picker",
    )
    st.session_state.selected_analyst_id = analyst_id

    if view == "Alert Queue":
        render_queue(analyst_id, analysts)
    elif view == "Search Guidance":
        render_search()


if __name__ == "__main__":
    main()
