from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# ⚠️ Typo fixed: DATABABASE_URL -> DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Ensure SSL is required for Render Postgres
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"sslmode": "require"}  # <- This forces SSL
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
