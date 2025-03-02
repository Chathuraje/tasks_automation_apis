import openai
from app.core.config import config

openai.api_key = config.CHATGPT_API_KEY

async def chat_with_gpt(prompt: str):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return {"response": response["choices"][0]["message"]["content"]}