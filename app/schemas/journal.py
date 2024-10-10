# app/schemas/journal.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.pyobject_id import PyObjectId
from bson import ObjectId

class JournalBase(BaseModel):
    content: str

class JournalCreate(JournalBase):
    pass

class Journal(JournalBase):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    created_at: datetime
    emotions: List[str]

    class Config:
        json_encoders = {ObjectId: str}
