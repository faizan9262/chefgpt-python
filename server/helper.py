from schemas.schema import Prompt

from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio



load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def ask_open_router(message: str):
    completion = await asyncio.to_thread(
        client.chat.completions.create,
        model="deepseek/deepseek-chat-v3-0324:free",
        messages=[{
            "role": "system",
            "content": "You are a professional chef AI.The user will provide an idea, theme, or description related to food (it may or may not be a dish name).",
          },{"role": "user", "content": message}],
    )
    reply = completion.choices[0].message.content
    print(reply)
    return reply



