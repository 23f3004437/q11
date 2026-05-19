from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()


# -------- Request Model --------
class SentimentRequest(BaseModel):
    sentences: List[str]


# -------- Sentiment Logic --------
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


# -------- API Endpoint --------
@app.post("/sentiment")
async def sentiment(data: SentimentRequest):

    results = [
        {
            "sentence": s,
            "sentiment": detect_sentiment(s)
        }
        for s in data.sentences
    ]

    return {"results": results}


# -------- Run Server --------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    