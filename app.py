from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# ✅ FIX: CORS (this prevents "Failed to fetch")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Request model
# -------------------
class SentimentRequest(BaseModel):
    sentences: List[str]

# -------------------
# Root endpoint (for testing)
# -------------------
@app.get("/")
def home():
    return {"message": "API is running"}

# -------------------
# Sentiment logic
# -------------------
def detect_sentiment(text: str) -> str:
    text = text.lower()

    happy_words = [
        "love", "great", "awesome", "happy", "good",
        "excellent", "amazing", "wonderful", "best",
        "fantastic", "nice"
    ]

    sad_words = [
        "sad", "terrible", "bad", "hate", "awful",
        "worst", "horrible", "angry", "upset",
        "disappointed"
    ]

    for w in happy_words:
        if w in text:
            return "happy"

    for w in sad_words:
        if w in text:
            return "sad"

    return "neutral"

# -------------------
# REQUIRED API ENDPOINT
# -------------------
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
