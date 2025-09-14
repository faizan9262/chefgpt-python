from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.suggest import route as suggest_route
from api.auth import route as auth_route
from api.favorite import route as favorite_route
from database import Base, engine
from api.auth.models import User 
from api.favorite.models import Favorite
from config import cloudinary_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://chefgpt-python.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)


app.include_router(suggest_route.router, prefix="/suggest", tags=["Suggestion"])
app.include_router(auth_route.router, prefix="/auth", tags=["Auth"])
app.include_router(favorite_route.router, prefix="/favorite", tags=["Favorite"])

@app.get("/")
async def root():
    return {"message": "Welcome to chef-gpt root api."}
