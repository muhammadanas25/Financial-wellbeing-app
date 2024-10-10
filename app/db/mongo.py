# app/db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
database = client[settings.MONGO_DB_NAME]

# Collections
user_collection = database.get_collection("users")
journal_collection = database.get_collection("journals")
sentiment_collection = database.get_collection("sentiments")
conversation_collection = database.get_collection("conversations")
reflect_collection = database.get_collection("reflects")
news_collection = database.get_collection("news")