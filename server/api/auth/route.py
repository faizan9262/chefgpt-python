from fastapi import APIRouter,status,Depends,Request,Response
from sqlalchemy.orm import Session
from database import get_db
from schemas.schema import RegisterInput,RegisterResponse,LoginInput,UserOut
from .controller import register_user,login_user,get_user_profile,logout_user

router = APIRouter()

@router.post('/register',status_code=status.HTTP_201_CREATED, response_model=RegisterResponse)
async def register(user_credentials:RegisterInput,db: Session = Depends(get_db)):
    return await register_user(user_credentials,db)

@router.post('/login',status_code=status.HTTP_200_OK, response_model=RegisterResponse)
async def login(user_credentials:LoginInput,db: Session = Depends(get_db)):
    return await login_user(user_credentials,db)

@router.post('/verify',status_code=status.HTTP_200_OK,response_model=UserOut)
async def verify(request:Request,db: Session = Depends(get_db)):
    return await get_user_profile(request,db)

@router.post('/logout',status_code=status.HTTP_200_OK)
async def logout(request:Request,response:Response):
    return await logout_user(request,response)