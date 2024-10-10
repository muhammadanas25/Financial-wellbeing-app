# app/api/endpoints/users.py
from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, User
from app.db.mongo import user_collection
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel

router = APIRouter()

# User Authentication Schema
class UserAuth(BaseModel):
    email: str
    password: str

# User registration - POST /users/
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Check if the user already exists by email
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Insert the user into the database
    user_dict = user.dict()
    result = await user_collection.insert_one(user_dict)

    # Retrieve the newly created user by its generated ID
    created_user = await user_collection.find_one({"_id": result.inserted_id})
    return User(**created_user)

# User login - POST /users/login
@router.post("/login", response_model=User)
async def login_user(auth_details: UserAuth):
    # Retrieve the user by email and password
    user = await user_collection.find_one({"email": auth_details.email, "password": auth_details.password})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return User(**user)

# Get user by ID - GET /users/{user_id}
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

# Get user by email - GET /users/by-email/{email}
@router.get("/by-email/{email}", response_model=User)
async def get_user_by_email(email: str):
    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)
