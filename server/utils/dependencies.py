# utils/dependencies.py
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from utils.jwt import verify_access_token
from database import get_db
from api.auth.models import User

async def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    cookie = request.cookies.get("access_token")
    if not cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_access_token(cookie)
    user_id: int = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
