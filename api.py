# FastAPI REST backend exposing agent functions

"""
FastAPI server that provides REST endpoints for the AI agent.
"""
import os
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agent
from agent import SimpleAgent

# Initialize FastAPI app / server
# Auto-Documentation: FastAPI generates interactive API docs

app = FastAPI(
    title="Simple AI Agent API",
    description="A beginner-friendly AI agent that can fetch advice and search books",
    version="1.0.0"
)

# Initialize agent
try:
    agent = SimpleAgent()
except Exception as e:
    print(f"Failed to initialize agent: {e}")
    agent = None

# Pydantic models
# Input Validation: Pydantic models ensure data integrity

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    used_tool: Optional[str] = None
    tool_result: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    model: str
    agent_ready: bool

# API endpoints
@app.get("/", response_model=dict)
def root():
    """Root endpoint with API information."""
    return {
        "message": "Simple AI Agent API",
        "version": "1.0.0",
        "endpoints": ["/health", "/chat"],
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    model_name = os.environ.get("LLAMA_MODEL", "llama3.2:3b")
    return HealthResponse(
        status="ok",
        model=model_name,
        agent_ready=agent is not None
    )

# Chat Endpoint

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """
    Main chat endpoint that processes user messages through the agent.
    """
    if not agent:
        raise HTTPException(
            status_code=500,
            detail="Agent not initialized. Please check your GROQ_API_KEY."
        )

    try:
        result = agent.call_agent(req.message)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Agent processing failed: {str(e)}"
        )

@app.get("/tools")
def get_available_tools():
    """Get information about available tools."""
    return {
        "tools": [
            {
                "name": "get_advice",
                "description": "Fetches random advice from adviceslip.com",
                "parameters": {}
            },
            {
                "name": "search_books",
                "description": "Searches Google Books API and returns top 3 results",
                "parameters": {
                    "query": "string - search query for books"
                }
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", "8000"))

    print(f"Starting FastAPI server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
