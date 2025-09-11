from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.suggest import route as suggest_route
from database import Base, engine
from api.auth.models import User 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)


app.include_router(suggest_route.router, prefix="/suggest", tags=["Suggestion"])

@app.get("/")
async def root():
    return {"message": "Welcome to chef-gpt root api."}
