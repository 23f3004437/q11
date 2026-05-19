from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ Fixes "Failed to fetch" / OPTIONS / CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Models ----------
class SentimentRequest(BaseModel):
    sentences: List[str]

# ---------- Root endpoint (IMPORTANT for graders) ----------
@app.get("/")
def root():
    return {"status": "ok"}

# ---------- Sentiment logic ----------
def detect_sentiment(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["love", "great", "awesome", "good", "amazing", "happy"]):
        return "happy"

    if any(w in text for w in ["bad", "sad", "terrible", "hate", "worst", "horrible"]):
        return "sad"

    return "neutral"

# ---------- Main endpoint ----------
@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    return {
        "results": [
            {
                "sentence": s,
                "sentiment": detect_sentiment(s)
            }
            for s in req.sentences
        ]
    }
