from pydantic import BaseModel,EmailStr

class Prompt(BaseModel):
    text:str
    
class Ingredients(BaseModel):
    item:list[str]
    info:str

class FullRecipe(BaseModel):
    name:str
    description:str
    
class ImagePrompt(BaseModel):
    text:str
    
class RegisterInput(BaseModel):
    username:str
    email:EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True

class RegisterResponse(BaseModel):
    user: UserOut
    message: str

    
class LoginInput(BaseModel):
    email:EmailStr
    password:str
    
class AddFavorite(BaseModel):
    name:str
    description:str
    recipe:list[str]
    image:str

class RemoveFavorite(BaseModel):
    id:int