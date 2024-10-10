# app/schemas/journal.py
from datetime import datetime
from pydantic import BaseModel
from typing import List,Optional

class JournalBase(BaseModel):
    content: str

class JournalCreate(JournalBase):
    pass

class Journal(JournalBase):
    id: int
    created_at: datetime
    emotions: Optional[List[str]]
    user_id: int
    class Config:
        orm_mode = True
