from fastapi import APIRouter,status
from .controller import suggest_based_on_prompt,suggest_based_on_ingredients,get_full_recipe,generate_static_image
from schemas.schema import Prompt,Ingredients,FullRecipe,ImagePrompt

router = APIRouter()

@router.post('/prompt',status_code=status.HTTP_200_OK)
async def get_suggetions(text:Prompt):
    return await suggest_based_on_prompt(text)

@router.post('/ingredients',status_code=status.HTTP_200_OK)
async def get_suggetions(item:Ingredients):
    return await suggest_based_on_ingredients(item)

@router.post('/get-recipe',status_code=status.HTTP_200_OK)
async def full_recipe(recipe:FullRecipe,ingredients:list[str]):
    return await get_full_recipe(recipe,ingredients)

@router.post("/generate-image")
async def generate_image(prompt:ImagePrompt):
    return await generate_static_image(prompt)
