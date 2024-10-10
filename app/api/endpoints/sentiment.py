# app/api/endpoints/sentiment.py
from fastapi import APIRouter, HTTPException
from app.schemas.sentiment import SentimentCreate, Sentiment
from app.db.mongo import user_collection, sentiment_collection
from typing import List
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/mood/{user_id}", response_model=Sentiment)
async def create_user_sentiment(user_id: str, sentiment_data: SentimentCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    sentiment_entry = {
        "mood": sentiment_data.mood,
        "additional_notes": sentiment_data.additional_notes,
        "user_id": ObjectId(user_id),
        "timestamp": datetime.utcnow()
    }

    result = await sentiment_collection.insert_one(sentiment_entry)
    new_sentiment = await sentiment_collection.find_one({"_id": result.inserted_id})

    return Sentiment(**new_sentiment)
