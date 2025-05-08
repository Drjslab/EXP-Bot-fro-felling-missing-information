from fastapi import FastAPI, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from suggestionEngine.suggestionEngine import suggestionEngine
import os
import uuid

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()
sugg_engine = suggestionEngine(api_key=API_KEY)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Bot logic - coroutine-safe
async def bot_reply(prompt: str, user: str) -> dict:
    return await sugg_engine.get_strategy_recommendation(prompt, user)

# Root route
@app.get("/", tags=["Info"])
def get_version_info():
    return JSONResponse(content={
        "agent": "Memory Agent",
        "version": "1.0",
        "deployed_date": "2025-05-06"
    })

# Health check
@app.get("/health", tags=["Health"])
def health_check():
    return JSONResponse(content={"status": "healthy"}, status_code=200)

# Chat endpoint (no DB, no record save)
class ChatRequest(BaseModel):
    prompt: str
    user: str

@app.post("/chat", tags=["Chat"])
async def chat_with_bot(data: ChatRequest):
    try:
        reply_text = await bot_reply(data.prompt, data.user)
        return {
            "type": "success",
            "speaker": "Bot",
            "text": reply_text,
            "unique_id": str(uuid.uuid4())
        }
    except Exception as e:
        return {
            "type": "error",
            "speaker": "Bot",
            "text": str(e),
            "unique_id": str(uuid.uuid4())
        }

# Run server (development only)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)
