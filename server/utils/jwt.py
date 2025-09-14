import os
from dotenv import load_dotenv
from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException,status

load_dotenv()

jwt_secret = os.getenv('JWT_SECRET')
jwt_algorithm = os.getenv('JWT_ALGORITHM')
jwt_exipry = int(os.getenv("JWT_EXIPRY", 7))

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=jwt_exipry)
    to_encode.update({"exp":expire})
    
    token = jwt.encode(to_encode,jwt_secret,algorithm=jwt_algorithm)
    
    return token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret, algorithms=jwt_algorithm)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired"
        )