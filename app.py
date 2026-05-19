from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SentimentRequest(BaseModel):
    sentences: List[str]

def detect_sentiment(text: str) -> str:
    text = text.lower()

    if any(w in text for w in ["love", "great", "awesome", "good", "amazing", "happy"]):
        return "happy"

    if any(w in text for w in ["bad", "sad", "terrible", "hate", "worst"]):
        return "sad"

    return "neutral"

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    return {
        "results": [
            {"sentence": s, "sentiment": detect_sentiment(s)}
            for s in req.sentences
        ]
    }
