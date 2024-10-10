
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    user: str = os.getenv("mongo_user", "Anas")
    psswd: str = os.getenv("mongo_psswd", "anas123")
    MONGO_CONNECTION_STRING: str = os.getenv("MONGO_CONNECTION_STRING",f"mongodb://{user}:{psswd}@localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "financial_wellbeing_db")

settings = Settings()
