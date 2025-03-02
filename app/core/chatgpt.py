from openai import OpenAI
from app.core.config import config
import json

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)

async def chat_with_gpt(messages, response_format):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        response_format=response_format
    )
    # Assuming `response` is the API response object
    message_content = response.choices[0].message.content

    # Parse the JSON string inside message.content
    parsed_content = json.loads(message_content)

    # Return the parsed content
    return {"response": parsed_content}