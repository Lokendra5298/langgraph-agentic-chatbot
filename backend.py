# backend.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from ai_agent import get_response_from_ai_agent

# Step 1: Request Schema
class RequestState(BaseModel):
    model_name: str
    model_provider: str = "Groq"
    system_prompt: str
    messages: List[str]
    allow_search: bool = False


# Step 2: FastAPI Application
app = FastAPI(title="LangGraph AI Agent")

ALLOWED_MODEL_NAMES = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b"
]


@app.post("/chat")
def chat_endpoint(request: RequestState):

    if request.model_provider.lower() != "groq":
        raise HTTPException(
            status_code=400,
            detail="Only Groq provider is supported"
        )

    if request.model_name not in ALLOWED_MODEL_NAMES:
        raise HTTPException(
            status_code=400,
            detail="Invalid model name"
        )

    response = get_response_from_ai_agent(
        llm_id=request.model_name,
        query="\n".join(request.messages),
        allow_search=request.allow_search,
        system_prompt=request.system_prompt
    )

    return {"response": response}


# Step 3: Run FastAPI
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9999)