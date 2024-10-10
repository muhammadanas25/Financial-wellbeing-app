# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.pyobject_id import PyObjectId
from bson import ObjectId

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: Optional[PyObjectId] = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}
