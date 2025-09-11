from schemas.schema import Prompt,Ingredients,FullRecipe,ImagePrompt
from fastapi import HTTPException,status
from helper import ask_open_router
import os
from dotenv import load_dotenv
import asyncio
import httpx

load_dotenv()

API_KEY = os.getenv("STABLE_HORDE_API_KEY")


async def suggest_based_on_ingredients(item:Ingredients):
    try:
        result = ", ".join(item.item)
        user_message = f"""I have these ingredients: {result}. 
            Suggest 3 unique but realistic dish ideas that can actually be prepared using only these items.  
            Each dish should be practical, tasty, and creative — but avoid using rare, fantasy, or impossible ingredients.  

            Here is some additional information to use for better suggestions: {item.info}  

            Return ONLY a JSON array of exactly 3 objects.  
            Each object must have:
            - title: short, clear dish name
            - description: 2–3 lines explaining what makes it special
            - image_prompt: short description to generate a realistic food image

            Do not include any text before or after the array."""
            
        response = await ask_open_router(user_message)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to generate suggestions based on ingredients: {str(e)}")

async def suggest_based_on_prompt(text:Prompt):
    try:
        user_messsage=f"""Based on this input: "${text.text}", suggest 3 unique but realistic dish ideas that can actually be prepared using commonly available ingredients.  
        Each dish should be practical, tasty, and creative — but avoid using rare, fantasy, or impossible ingredients.  

        Return ONLY a JSON array of exactly 3 objects.  
        Each object must have:
        - title: short, clear dish name
        - description: 2–3 lines explaining what makes it special
        - image_prompt: short description to generate a realistic food image

        Do not include any text before or after the array."""

        response = await ask_open_router(user_messsage)
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to generate suggestions based on prompt: {str(e)}")
    
async def get_full_recipe(recipe:FullRecipe,ingredients:list[str]):
    try:
        recipe_dict = recipe.dict()
        ingredients_str = ", ".join(ingredients) if ingredients else ""

        ingredient_text = f" I have these ingredients: {ingredients_str}. Use only these if possible." if ingredients_str else ""

        recipe_prompt = f"""I want a full, step-by-step recipe for the dish "{recipe_dict['name']}". 
        The description is: "{recipe_dict['description']}".{ingredient_text} 
        Provide beginner-friendly, numbered steps. 

        Return ONLY the numbered instructions, with no extra text before or after."""
        
        response = await ask_open_router(recipe_prompt)
        
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Failed to generate full recipe: {str(e)}")
    
async def generate_static_image(prompt:ImagePrompt):

    async with httpx.AsyncClient(timeout=60) as client:
        # Step 1: Submit generation request
        submit_resp = await client.post(
            "https://stablehorde.net/api/v2/generate/async",
            headers={"apikey": API_KEY},
            json={
                "prompt": prompt.text,
                "params": {"steps": 30},
                "nsfw": False,
                "censor_nsfw": True,
                "models": ["stable_diffusion"]
            }
        )

        if submit_resp.status_code != 202:
            raise HTTPException(status_code=submit_resp.status_code, detail="Failed to submit generation request")

        job_id = submit_resp.json().get("id")
        if not job_id:
            raise HTTPException(status_code=500, detail="No job ID returned from Stable Horde")

        # Step 2: Poll for completion
        while True:
            status_resp = await client.get(f"https://stablehorde.net/api/v2/generate/status/{job_id}")
            if status_resp.status_code != 200:
                raise HTTPException(status_code=status_resp.status_code, detail="Failed to get job status")

            data = status_resp.json()
            if data.get("done"):
                generations = data.get("generations", [])
                if not generations:
                    raise HTTPException(status_code=500, detail="No images generated")
                return {"image_url": generations[0].get("img")}  # <- change here

            await asyncio.sleep(4) 
