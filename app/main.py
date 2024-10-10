from fastapi import FastAPI

from app.api.endpoints import journals, users, news, sentiment, reflect

app = FastAPI(
    title="Financial Well-being App",
    description="An app for journaling and personalized financial learning.",
    version="1.0.0",
)

app.include_router(journals.router, prefix="/journals", tags=["journals"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(news.router, prefix="/news", tags=["news"])
app.include_router(sentiment.router, prefix="/sentiment", tags=["sentiment"])
app.include_router(reflect.router, prefix="/reflect", tags=["reflect"])
