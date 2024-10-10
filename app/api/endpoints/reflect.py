from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List

from bson import ObjectId
from app.schemas.conversation import Conversation, Message
from app.db.mongo import user_collection, conversation_collection
from openai import OpenAI
from core.config import settings
from datetime import datetime
from app.services.transcription import transcribe_audio

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)
router = APIRouter()

@router.post("/reflect/{user_id}", response_model=Message)
async def reflect_conversation(user_id: str, user_message: str, rag: bool = False):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Check if user exists
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve or initialize the user's conversation history
    conversation = await conversation_collection.find_one({"user_id": ObjectId(user_id)})
    if not conversation:
        conversation = {
            "user_id": ObjectId(user_id),
            "messages": []
        }
        result = await conversation_collection.insert_one(conversation)
        conversation = await conversation_collection.find_one({"_id": result.inserted_id})
    
    # Add the user's message to the conversation
    user_message_entry = {
        "role": "user",
        "content": user_message,
        "timestamp": datetime.utcnow()
    }
    await conversation_collection.update_one(
        {"_id": conversation["_id"]},
        {"$push": {"messages": user_message_entry}}
    )

    # Prepare the conversation context for the model
    messages_for_model = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
    messages_for_model.append({"role": "user", "content": user_message})

    # Constructing the prompt for the OpenAI model
    system_message = (
        "You are an empathetic assistant helping a user reflect on their daily challenges and find solutions. "
        "You respond with understanding, provide thoughtful feedback, and suggest small actions that can make the user feel better."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Replace with "gpt-o1" if applicable
        messages=[
            {"role": "system", "content": system_message},
            *messages_for_model  # Add the message context from previous history
        ],
        max_tokens=150,
        temperature=0.7,
        n=1
    )

    assistant_reply = response.choices[0].message.content.strip()

    # Add the assistant's reply to the conversation
    assistant_message_entry = {
        "role": "assistant",
        "content": assistant_reply,
        "timestamp": datetime.utcnow()
    }
    await conversation_collection.update_one(
        {"_id": conversation["_id"]},
        {"$push": {"messages": assistant_message_entry}}
    )

    return Message(**assistant_message_entry)

# Retrieve chat history for a user - GET /reflect/history/{user_id}
@router.get("/reflect/history/{user_id}", response_model=List[Message])
async def get_chat_history(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Check if the user exists
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve the conversation history
    conversation = await conversation_collection.find_one({"user_id": ObjectId(user_id)})
    if not conversation:
        raise HTTPException(status_code=404, detail="No conversation history found for this user")

    # Return messages in the correct order
    messages = conversation["messages"]

    return [Message(**msg) for msg in messages]

router.post("/reflect/voice/{user_id}", response_model=Message)
async def reflect_voice_conversation(user_id: str, audio_file: UploadFile = File(...), rag: bool = False):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Check if user exists
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Transcribe the audio
    try:
        transcript = await transcribe_audio(audio_file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

    # Continue with the existing reflection flow using the transcribed text
    # Retrieve or initialize the user's conversation history
    conversation = await conversation_collection.find_one({"user_id": ObjectId(user_id)})
    if not conversation:
        conversation = {
            "user_id": ObjectId(user_id),
            "messages": []
        }
        result = await conversation_collection.insert_one(conversation)
        conversation = await conversation_collection.find_one({"_id": result.inserted_id})

    # Add the user's message to the conversation
    user_message_entry = {
        "role": "user",
        "content": transcript,
        "timestamp": datetime.utcnow()
    }
    await conversation_collection.update_one(
        {"_id": conversation["_id"]},
        {"$push": {"messages": user_message_entry}}
    )

    # Prepare the conversation context for the model
    messages_for_model = [{"role": msg["role"], "content": msg["content"]} for msg in conversation["messages"]]
    messages_for_model.append({"role": "user", "content": transcript})

    # Constructing the prompt for the OpenAI model
    system_message = (
        "You are an empathetic assistant helping a user reflect on their daily challenges and find solutions. "
        "You respond with understanding, provide thoughtful feedback, and suggest small actions that can make the user feel better."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            *messages_for_model
        ],
        max_tokens=150,
        temperature=0.7,
        n=1
    )

    assistant_reply = response.choices[0].message.content.strip()

    # Add the assistant's reply to the conversation
    assistant_message_entry = {
        "role": "assistant",
        "content": assistant_reply,
        "timestamp": datetime.utcnow()
    }
    await conversation_collection.update_one(
        {"_id": conversation["_id"]},
        {"$push": {"messages": assistant_message_entry}}
    )

    return Message(**assistant_message_entry)