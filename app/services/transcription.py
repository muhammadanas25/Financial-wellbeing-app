# app/services/transcription.py
import openai
from openai import OpenAI
from core.config import settings

# Initialize the OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def transcribe_audio(audio_file):
    # Assuming audio_file is an UploadFile object from FastAPI
    audio_bytes = await audio_file.read()

    # Transcribing the audio using OpenAI's Whisper API or similar service
    response = client.audio.transcriptions.create(
        file=audio_bytes,
        model="whisper-1"
    )
    
    return response["text"]
