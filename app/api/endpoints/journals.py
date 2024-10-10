# app/api/endpoints/journals.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from bson import ObjectId
from app.schemas import journal as journal_schema
from app.db.mongo import journal_collection, user_collection
from app.services import transcription, emotion_detection
from datetime import datetime


router = APIRouter()

@router.post("/voice/{user_id}", response_model=journal_schema.Journal)
async def create_journal_from_voice(user_id: str, file: UploadFile = File(...)):
    # Validate user_id
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the uploaded file temporarily
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    # Transcribe audio
    try:
        content = transcription.transcribe_audio(file_location)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Transcription failed.")

    # Detect emotions
    emotions = emotion_detection.detect_emotions(content)

    # Create journal entry
    journal_entry = {
        "content": content,
        "user_id": ObjectId(user_id),
        "emotions": emotions,
        "created_at": datetime.utcnow()
    }
    
    result = await journal_collection.insert_one(journal_entry)
    new_journal = await journal_collection.find_one({"_id": result.inserted_id})

    return journal_schema.Journal(**new_journal)
# Create a journal entry from text - POST /journals/text/{user_id}
@router.post("/text/{user_id}", response_model=journal_schema.Journal)
async def create_journal_from_text(user_id: str, entry: journal_schema.JournalCreate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Check if the user exists
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Detect emotions from the journal content
    emotions = emotion_detection.detect_emotions(entry.content)

    # Create a new journal entry
    journal_entry = {
        "content": entry.content,
        "user_id": ObjectId(user_id),
        "emotions": emotions,
        "created_at": datetime.utcnow()
    }
    
    result = await journal_collection.insert_one(journal_entry)
    new_journal = await journal_collection.find_one({"_id": result.inserted_id})

    return journal_schema.Journal(**new_journal)

# Retrieve all journal entries for a user - GET /journals/user/{user_id}
@router.get("/user/{user_id}", response_model=List[journal_schema.Journal])
async def get_user_journals(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Find all journal entries for the given user ID
    journals = await journal_collection.find({"user_id": ObjectId(user_id)}).to_list(length=100)
    if not journals:
        raise HTTPException(status_code=404, detail="No journals found for this user")

    return [journal_schema.Journal(**journal) for journal in journals]


# @router.post("/text/{user_id}", response_model=journal_schema.Journal)
# async def create_journal_from_text(
#     user_id: str,
#     entry: journal_schema.JournalCreate,
#     db = Depends(get_database)
# ):
#     # Validate user_id
#     if not ObjectId.is_valid(user_id):
#         raise HTTPException(status_code=400, detail="Invalid user ID")

#     # Detect emotions
#     emotions = emotion_detection.detect_emotions(entry.content)
    
#     # Create journal entry
#     journal_entry = journal_schema.Journal(
#         user_id=ObjectId(user_id),
#         content=entry.content,
#         emotions=emotions,
#         created_at=datetime.utcnow()
#     )
    
#     # Insert into database
#     result = await db["journals"].insert_one(journal_entry.to_mongo())
    
#     # Fetch the inserted document
#     created_journal = await db["journals"].find_one({"_id": result.inserted_id})
    
#     return journal_schema.Journal.from_mongo(created_journal)





# @router.post("/text/{user_id}", response_model=journal_schema.Journal)
# async def create_journal_from_text(
#     user_id: int,
#     entry: journal_schema.JournalCreate, db: Session = Depends(get_db)
# ):
#     # Detect emotions
#     emotions = emotion_detection.detect_emotions(entry.content)
#     emotionss=",".join(emotions),
#     print(emotions,type(emotions),"--------------------------------------------------------")
#     # Create journal entry
#     journal_entry = journal_model.Journal(
#         user_id=user_id,
#         content=entry.content,
#         emotions=emotions
#     )
#     db.add(journal_entry)
#     db.commit()
#     db.refresh(journal_entry)

#     return journal_entry

# @router.get("/{journal_id}", response_model=journal_schema.Journal)
# async def read_journal(journal_id: int, db: Session = Depends(get_db)):
#     journal_entry = db.query(journal_model.Journal).filter(journal_model.Journal.id == journal_id).first()
#     if not journal_entry:
#         raise HTTPException(status_code=404, detail="Journal entry not found.")
#     return journal_entry

# @router.get("/", response_model=List[journal_schema.Journal])
# async def read_journals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     journals = db.query(journal_model.Journal).offset(skip).limit(limit).all()
#     return journals
