#!/usr/bin/env python3
"""
PowerSave AI Proxy Server
==========================
Simple FastAPI proxy server to bypass CORS restrictions for AI tools.
This allows browser-based tools to access GenSpark API without CORS issues.

Usage:
    python ai_proxy_server.py

Environment Variables:
    OPENAI_API_KEY: GenSpark API key (gsk-...)
    OPENAI_BASE_URL: GenSpark API base URL
    AI_PROXY_PORT: Port to run the server (default: 8080)
"""

import os
import sys
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://www.genspark.ai/api/llm_proxy/v1')
AI_PROXY_PORT = int(os.getenv('AI_PROXY_PORT', '8080'))
AI_PROXY_CORS_ORIGINS = os.getenv('AI_PROXY_CORS_ORIGINS', '*')

# Validate configuration
if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not set!")
    print("Please set it in .env file or environment variables")
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(
    title="PowerSave AI Proxy",
    description="CORS proxy for GenSpark AI API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if AI_PROXY_CORS_ORIGINS == "*" else AI_PROXY_CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "gpt-5-mini"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2000
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Dict]
    usage: Optional[Dict] = None

# Health check endpoint
@app.get("/")
async def root():
    return {
        "service": "PowerSave AI Proxy",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "chat": "/api/ai/chat",
            "models": "/api/ai/models"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_configured": bool(OPENAI_API_KEY),
        "base_url": OPENAI_BASE_URL
    }

# Chat completion endpoint
@app.post("/api/ai/chat")
async def chat_completion(request: ChatRequest):
    """
    Proxy chat completion requests to GenSpark API.
    This bypasses CORS restrictions for browser-based tools.
    """
    try:
        # Prepare request to GenSpark API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        payload = {
            "model": request.model,
            "messages": [msg.dict() for msg in request.messages],
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "stream": request.stream
        }
        
        # Make request to GenSpark API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )
            
            # Check for errors
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"GenSpark API error: {response.text}"
                )
            
            # Return response
            return response.json()
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Request to GenSpark API timed out"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to GenSpark API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# List available models
@app.get("/api/ai/models")
async def list_models():
    """List available AI models"""
    return {
        "models": [
            {
                "id": "gpt-5-mini",
                "name": "GPT-5 Mini",
                "description": "Fast and efficient model for most tasks"
            },
            {
                "id": "gpt-5",
                "name": "GPT-5",
                "description": "Full GPT-5 model with maximum capabilities"
            },
            {
                "id": "gpt-5-nano",
                "name": "GPT-5 Nano",
                "description": "Ultra-fast lightweight model"
            }
        ]
    }

# Simple test endpoint
@app.post("/api/ai/test")
async def test_api():
    """Test the GenSpark API connection"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                },
                json={
                    "model": "gpt-5-mini",
                    "messages": [{"role": "user", "content": "Hello!"}],
                    "max_tokens": 10
                }
            )
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "message": "GenSpark API is working!",
                    "response": response.json()
                }
            else:
                return {
                    "status": "error",
                    "message": f"API returned status {response.status_code}",
                    "details": response.text
                }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 PowerSave AI Proxy Server")
    print("=" * 60)
    print(f"📡 API Base URL: {OPENAI_BASE_URL}")
    print(f"🔑 API Key: {OPENAI_API_KEY[:20]}...")
    print(f"🌐 Server Port: {AI_PROXY_PORT}")
    print(f"🔓 CORS Origins: {AI_PROXY_CORS_ORIGINS}")
    print("=" * 60)
    print(f"\n✅ Server starting on http://localhost:{AI_PROXY_PORT}")
    print(f"📖 API Docs: http://localhost:{AI_PROXY_PORT}/docs")
    print(f"🏥 Health Check: http://localhost:{AI_PROXY_PORT}/health")
    print(f"💬 Chat Endpoint: http://localhost:{AI_PROXY_PORT}/api/ai/chat")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=AI_PROXY_PORT,
        log_level="info"
    )
