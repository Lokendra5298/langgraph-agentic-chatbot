# frontend.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import requests

# Step 1: Streamlit UI
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")

st.title("AI Chatbot Agents")
st.write("Create and interact with AI agents!")

# Agent Configuration
system_prompt = st.text_area(
    "Define your AI Agent:",
    value="You are a helpful AI assistant.",
    height=100
)

MODEL_NAMES_GROQ = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b"
]

provider = "Groq"

selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="Ask anything!"
)

API_URL = "http://127.0.0.1:9999/chat"

# Step 2: Send Request to FastAPI Backend
if st.button("Ask Agent!", type="primary"):

    if not user_query.strip():
        st.warning("Please enter a query.")

    else:
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        try:
            with st.spinner("Agent is thinking..."):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                response_data = response.json()

            st.subheader("Agent Response")
            st.markdown(response_data["response"])

        except requests.exceptions.RequestException as e:
            st.error(f"Backend connection/API error: {e}")

        except (KeyError, ValueError) as e:
            st.error(f"Invalid backend response: {e}")