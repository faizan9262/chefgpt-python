from schemas.schema import RegisterInput,LoginInput
from fastapi import HTTPException,status,Request,Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .models import User
from utils.utils import hash_password,verify_password
from utils.jwt import create_access_token,verify_access_token


async def register_user(user_credentials: RegisterInput, db: Session):
    existing_user = db.query(User).filter(User.email == user_credentials.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered.")
    
    hashed_password = hash_password(user_credentials.password)
    new_user = User(
        username=user_credentials.username,
        email=user_credentials.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(data={"user_id": new_user.id})

    # ✅ Instead of returning the token in JSON, set it in cookie
    response = JSONResponse(
        content={
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
            },
            "message": "Registration successful"
        }
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  
        secure=False,   
        samesite="Lax",  
        max_age=60 * 60 * 24 * 7 ,
        path="/"
    )

    return response


async def login_user(user_credentials:LoginInput,db:Session):
    existing_user = db.query(User).filter(user_credentials.email == User.email).first()
    
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User does not exists")
    
    
    if not verify_password(user_credentials.password, existing_user.password):
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid credentials"
    )
        
    access_token = create_access_token(data=({"user_id":existing_user.id}))
    
    response = JSONResponse(
        content={
            "user": {
                "id": existing_user.id,
                "username": existing_user.username,
                "email": existing_user.email,
            },
            "message": "Login successful"
        }
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  
        secure=False,     
        samesite="Lax",  
        max_age=60 * 60 * 24 * 7  ,
        path="/"
    )
    
    
    return response

async def get_user_profile(request:Request,db:Session):
    cookie = request.cookies.get('access_token')
    
    if not cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_access_token(cookie)
    
    user_id:int = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
        
    user = db.query(User).filter(User.id == user_id).first()
    
    return user


async def logout_user(request:Request,response:Response):
    cookie = request.cookies.get('access_token')
    if not cookie:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = verify_access_token(cookie)
    
    user_id:int = payload.get("user_id")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    response.delete_cookie("access_token")
    
    return {"message":"Logout Successful"}