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


if __name__ == "__main__":
    main()
