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

async def select_best_news(articles):
    """
    Sends a list of news articles to ChatGPT and selects the best one based on relevance and impact.
    """
    messages = [
        {
            "role": "system",
            "content": "You analyze crypto news articles and select the best one based on relevance, uniqueness, and impact."
        },
        {
            "role": "user",
            "content": "Here are some news articles. Choose the best one and return its title and URL in JSON format:\n\n"
        }
    ]
    
    for i, article in enumerate(articles):
        messages.append({
            "role": "user",
            "content": f"{i+1}. {article['title']} ({article['url']})"
        })

    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "best_crypto_article",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "description": "The title of the best crypto news article.",
                        "type": "string"
                    },
                    "url": {
                        "description": "The URL of the best crypto news article.",
                        "type": "string"
                    }
                },
                "required": ["title", "url"],
                "additionalProperties": False
            }
        }
    }

    response = await chat_with_gpt(messages, response_format)
    
    return {
        "title" : response["response"]["title"],
        "url" : response["response"]["url"]  # Return the title and URL as a dictionary for simplicity. You can modify this to return the full article object if needed.
    }

async def generate_script(article):
    """
    Generates a 1-minute YouTube script based on the selected news article.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a professional scriptwriter for YouTube. Generate a concise, engaging 1-minute script based on the given news article. The script should be in natural spoken language, without stage directions, music cues, emojis, or calls to action like 'like and subscribe.'"
        },
        {
            "role": "user",
            "content": f"Write a 1-minute YouTube script summarizing the following news article:\n\n"
                       f"Title: {article['title']}\n"
                       f"URL: {article['url']}\n\n"
                       "The script should be engaging, easy to follow, and sound natural when spoken. Do not include any music cues, stage directions, emojis, or phrases like 'subscribe for more.' Just provide a clean spoken script and include an interesting hook at the start."
        }
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "youtube_script",
            "schema": {
                "type": "object",
                "properties": {
                    "script": {
                        "description": "The generated 1-minute YouTube script summarizing the news article.",
                        "type": "string"
                    }
                },
                "required": ["script"],
                "additionalProperties": False
            }
        }
    }

    response = await chat_with_gpt(messages, response_format)
    print(response)
    return response["response"]["script"]

async def process_news_articles(articles):
    """
    Main function to process news articles, select the best one, summarize it, and generate a script.
    """
    best_article = await select_best_news(articles)
    if best_article:
        script = await generate_script(best_article)
        return {"title": best_article["title"], "url": best_article["url"], "script": script}
    
    return {"error": "No suitable news article found."}
