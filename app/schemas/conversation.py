# app/schemas/conversation.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.pyobject_id import PyObjectId
from bson import ObjectId

class Message(BaseModel):
    role: str  # Either "user" or "assistant"
    content: str
    timestamp: datetime

class Conversation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    messages: List[Message]

    class Config:
        json_encoders = {ObjectId: str}
