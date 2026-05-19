from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class SentimentRequest(BaseModel):
    sentences: List[str]

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

    for word in happy_words:
        if word in text:
            return "happy"

    for word in sad_words:
        if word in text:
            return "sad"

    return "neutral"


@app.post("/sentiment")
async def sentiment(data: SentimentRequest):
    results = []

    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": detect_sentiment(sentence)
        })

    return {"results": results}


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
    