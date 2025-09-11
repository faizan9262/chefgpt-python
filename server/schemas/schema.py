from pydantic import BaseModel

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