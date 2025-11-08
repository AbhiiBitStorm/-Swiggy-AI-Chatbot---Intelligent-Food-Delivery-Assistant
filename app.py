from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime
import asyncio

from llm_handler import SwiggyBot
from data_manager import data_manager

app = FastAPI(title="Swiggy Chatbot API - FAST")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize bot once (singleton)
print("🤖 Initializing Fast Chatbot...")
bot = SwiggyBot()
print("✅ Ready!")

# Session storage
chat_sessions = {}

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    session_id: str
    response_time: Optional[float] = None

@app.get("/")
def root():
    return {
        "status": "⚡ Swiggy Chatbot FAST",
        "version": "3.0",
        "optimizations": ["Rule-based", "Caching", "Fast LLM"]
    }

@app.post("/chat")
async def chat(chat_message: ChatMessage, background_tasks: BackgroundTasks):
    start_time = datetime.now()
    
    try:
        session_id = chat_message.session_id
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        # Add user message
        chat_sessions[session_id].append({
            "role": "user",
            "content": chat_message.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Generate response (optimized)
        response = bot.generate_response(
            chat_message.message,
            chat_sessions[session_id]
        )
        
        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Save to file in background (non-blocking)
        background_tasks.add_task(
            data_manager.save_conversation,
            session_id,
            chat_message.message,
            response
        )
        
        # Add bot response
        chat_sessions[session_id].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Limit history
        if len(chat_sessions[session_id]) > 20:
            chat_sessions[session_id] = chat_sessions[session_id][-20:]
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            response_time=round(response_time, 2)
        )
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "healthy", "speed": "optimized"}

if __name__ == "__main__":
    print("⚡ Starting FAST Swiggy Chatbot...")
    print("🌐 http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)