from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime

app = FastAPI(title="Swiggy Chatbot API - Simple")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    session_id: str

@app.get("/")
def root():
    return {"status": "Swiggy Chatbot Running", "version": "1.0"}

@app.post("/chat")
def chat(chat_message: ChatMessage):
    # Simple echo response for testing
    response = f"You said: {chat_message.message}. (This is a test response)"
    
    return ChatResponse(
        response=response,
        timestamp=datetime.now().isoformat(),
        session_id=chat_message.session_id
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Starting Simple Swiggy Chatbot Server...")
    print("📍 Server URL: http://localhost:8000")
    print("📍 Health Check: http://localhost:8000/health")
    print("📍 API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)