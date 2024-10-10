# app/services/emotion_detection.py
import openai
from core.config import settings
from openai import OpenAI
openai.api_key = settings.OPENAI_API_KEY

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def detect_emotions(text: str) -> list:
    prompt = (
        f"Analyze the following text and list the emotions expressed: '{text}' and give a list of emotions in a space separated format without any other message like sample output: [\"anger\",\"fear","joy\"]"
    )
    
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are an emotion detection assistant."},
    #         {"role": "user", "content":f" {prompt} : '{text}'"}
    #     ],
    #     max_tokens=60,
    #     n=1,
    #     temperature=0.5,
    # )
    # emotions = response.choices[0].message.content
    # print(emotions)
    # print(response)
    emotions=['stress','anger']
    #emotions = [emotion.strip().strip('"') for emotion in emotions if emotion.strip()]
    return emotions