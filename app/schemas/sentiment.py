# app/schemas/sentiment.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.pyobject_id import PyObjectId
from bson import ObjectId

class SentimentBase(BaseModel):
    mood: str  # For example, "happy", "sad", "neutral", etc.
    additional_notes: Optional[str] = None

class SentimentCreate(SentimentBase):
    pass

class Sentiment(SentimentBase):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    timestamp: datetime

    class Config:
        json_encoders = {ObjectId: str}
