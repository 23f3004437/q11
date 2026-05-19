from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


class SentimentRequest(BaseModel):
    sentences: List[str]


@app.get("/")
def home():
    return {"message": "API is running"}


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


@app.post("/sentiment")
def sentiment(req: SentimentRequest):
    results = [
        {
            "sentence": s,
            "sentiment": detect_sentiment(s)
        }
        for s in req.sentences
    ]
    return {"results": results}
