# app/api/endpoints/news.py
from fastapi import APIRouter
from openai import OpenAI
from core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

router = APIRouter()

@router.get("/latest", response_model=dict)
async def get_latest_news():
    prompt = (
        "Give me the latest 5 financial and mental health news headlines with relevant links. "
        "Format the response as a JSON array where each item has 'title' and 'link' keys."
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a news assistant. Provide responses in JSON format."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=250,
        n=1,
        temperature=0.5,
    )
    
    news_content = response.choices[0].message.content
    
    try:
        news_json = json.loads(news_content)
    except json.JSONDecodeError:
        # If JSON parsing fails, return a formatted error message
        return {"error": "Failed to parse news data", "raw_content": news_content}
    
    return {"news": news_json}