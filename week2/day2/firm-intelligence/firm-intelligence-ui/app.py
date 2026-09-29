import streamlit as st
import requests
import json

st.title("Firm Intelligence")

agentQuestion = st.text_input("Ask a question", key="agent_question")

if st.button("Ask Agent"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/agent/ask",
            json={
                "question": agentQuestion,
            },
        )
        if response.status_code == 504:
            st.error("The agent timed out. Please try again.")
        elif response.status_code == 429:
            st.error("Too many requests. Please try again shortly.")
        elif response.status_code == 502:
            st.error("The agent provider is currently unavailable.")
        elif response.status_code != 200:
            st.error("The request failed.")
        else:
            data = response.json()
            st.write(data["answer"])

            st.sidebar.header("Agent Stats")
            st.sidebar.write("Tool calls made:", data["tool_calls_made"])
            st.sidebar.write("Input Tokens:", data["input_tokens"])
            st.sidebar.write("Output Tokens:", data["output_tokens"])
    except requests.exceptions.RequestException:
        st.error("Could not connect to the agent service. Please try again.")


searchQuestion = st.text_input("Ask a question", key="search_question")

if st.button("Search Agent"):
    response = requests.post(
        "http://127.0.0.1:8000/knowledge/search",
        json={
            "question": searchQuestion,
            "top_k": 3,
        },
    )
    if response.status_code == 409:
        st.warning("The knowledge index has not been built yet.")
    elif response.status_code != 200:
        st.error("Search failed.")
    else:
        data = json.loads(response.text)

        for result in data["results"]:
            st.write(result["title"])
            st.write(result["text"])
            st.write(result["score"])
            st.write("")

firmId = st.text_input("Which firm would you like the summary of?", key="firm_id")

if st.button("Get summary"):
    url = f"http://127.0.0.1:8000/firms/{firmId}/summary/stream"
    placeholder = st.empty()
    summary = ""
    try:
        with requests.get(url, stream=True, timeout=60) as response:
            response.raise_for_status()

            for chunk in response.iter_content(
                chunk_size=None,
                decode_unicode=True,
            ):
                if chunk:
                    summary += chunk
                    placeholder.markdown(summary)

    except requests.exceptions.RequestException as error:
        st.error(f"Could not retrieve the summary: {error}")
