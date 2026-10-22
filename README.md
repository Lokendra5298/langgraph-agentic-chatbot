# LangGraph ReAct AI Agent

A simple AI chatbot built with **LangChain/LangGraph**, **Groq**, **FastAPI**, and **Streamlit**. It supports custom system instructions, model selection, and optional web search using Tavily.

## Project structure

```text
p6_react_agents/
├── ai_agent.py       # Groq-powered agent with optional Tavily search
├── backend.py        # FastAPI endpoint
├── frontend.py       # Streamlit interface (rename as needed)
├── requirements.txt
├── .env               # Local API keys; do not commit
└── README.md
```

> The Streamlit file is called `frontend.py` here as an example. Use its **actual filename** when running it. If your agent file is named `ai_agant.py`, either rename it to `ai_agent.py` or update the import in `backend.py`.

## Requirements

- Python **3.10+** (Python 3.12 is supported by the core stack).
- A [Groq API key](https://console.groq.com/keys).
- A [Tavily API key](https://app.tavily.com/) **only if web search is enabled**.

## Setup

From your project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit `.env` to version control. Add it to `.gitignore`.

## Run the app

**Terminal 1 — FastAPI backend:**

```bash
python backend.py
```

The example backend serves at **http://127.0.0.1:9999**. API documentation is available at **http://127.0.0.1:9999/docs**.

**Terminal 2 — Streamlit UI:**

```bash
streamlit run frontend.py
```

Open the URL printed by Streamlit (usually **http://localhost:8501**).

If your UI file is named `app.py`, run `streamlit run app.py` instead.

## Models

The example backend allows these Groq model IDs:

- `openai/gpt-oss-120b`
- `openai/gpt-oss-20b`
- `qwen/qwen3.8-27b`

Model access and tool-calling support may vary by account. Make sure the model lists in the backend and Streamlit interface match.

## API

**POST** `/chat`

Request example:

```json
{
  "model_name": "openai/gpt-oss-120b",
  "model_provider": "Groq",
  "system_prompt": "You are a helpful AI assistant.",
  "messages": ["Explain LangGraph in simple words."],
  "allow_search": false
}
```

Successful response shape:

```json
{
  "response": "<AI-generated answer>"
}
```

You can test the API at `/docs`, or use `curl`:

```bash
curl -X POST http://127.0.0.1:9999/chat \
  -H 'Content-Type: application/json' \
  -d '{"model_name":"openai/gpt-oss-120b","model_provider":"Groq","system_prompt":"You are helpful.","messages":["Hello!"],"allow_search":false}'
```

The root URL `/` returns `404 Not Found` unless you add a `GET /` route; use `/docs` to explore the API.

## How it works

```text
Streamlit UI -> FastAPI /chat -> LangChain agent -> Groq LLM
                                            |-> Tavily search (optional)
                                            |-> Final response
```

- **Streamlit:** Collects the model, system prompt, query, and search preference.
- **FastAPI:** Validates the request and invokes the agent.
- **Agent:** Generates an answer with Groq and can call Tavily when enabled.

## Troubleshooting

- **`404 Not Found` at `/`:** Open `/docs` instead.
- **`model_not_found`:** Use a model ID available to your Groq API key.
- **`ModuleNotFoundError: ai_agent`:** Check the filename and import spelling (`ai_agent.py` versus `ai_agant.py`).
- **Frontend connection error:** Ensure `backend.py` is running on port `9999` and `API_URL` matches.
- **Missing API key:** Check `.env` and restart the backend. Tavily is only needed when search is enabled.
