from app.features.chatgpt import chat_with_gpt

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
            "content": "Here are some news articles. Choose the best one to use for crypto related youtube channel and return its title and URL in JSON format:\n\n"
        }
    ]
    
    for i, article in enumerate(articles):
        messages.append({
            "role": "user",
            "content": f"{i+1}. {article.title} ({article.url})"
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

async def generate_script_and_seo(article):
    """
    Generates a 1-minute YouTube script and SEO metadata (title, description, tags) in a single API call.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a professional scriptwriter for YouTube. Generate a concise, engaging 1-minute script "
                       "based on the given news article. The script should be in natural spoken language, without "
                       "stage directions, music cues, emojis, or calls to action like 'like and subscribe.'"
        },
        {
            "role": "user",
            "content": f"Write a 1-minute YouTube script summarizing the following news article:\n\n"
                       f"Title: {article.title}\n"
                       f"URL: {article.url}\n\n"
                       "The script should be engaging, easy to follow, and sound natural when spoken. "
                       "Do not include any music cues, stage directions, emojis, or promotional phrases like 'subscribe for more.' "
                       "Just deliver a clean, compelling spoken script that keeps the audience hooked from the very first sentence.'"
                       "Start with a hook that grabs attention instantly—something surprising, a bold claim, or a thought-provoking question."
        },
        {
            "role": "user",
            "content": "Now, based on the above script, generate SEO metadata for YouTube: \n"
                       "- A short but compelling SEO-optimized title (max 60 characters)\n"
                       "- A brief, engaging video description (max 2 sentences)\n"
                       "- A set of relevant tags (max 10 keywords)\n"
                       "Return everything in JSON format."
        },
        {
            "role": "user",
            "content": "Finally, create one image prompt based on the script that can be used to generate AI-generated visuals for the video. "
                       "This prompt should describe a visually compelling scene related to the script."
        }
    ]

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "youtube_script_and_seo",
            "schema": {
                "type": "object",
                "properties": {
                    "script": {
                        "description": "The generated 1-minute YouTube script summarizing the news article.",
                        "type": "string"
                    },
                    "seo_title": {
                        "description": "SEO-optimized YouTube video title (max 60 characters).",
                        "type": "string"
                    },
                    "seo_description": {
                        "description": "SEO-friendly YouTube video description (max 2 sentences).",
                        "type": "string"
                    },
                    "seo_tags": {
                        "description": "List of relevant YouTube video tags (max 10).",
                        "type": "array",
                        "items": {"type": "string"}
                    },
                    "image_prompt": {
                        "description": "The one AI-generated image prompts based on the script.",
                        "type": "string"
                    }
                },
                "required": ["script", "seo_title", "seo_description", "seo_tags", "image_prompts"],
                "additionalProperties": False
            }
        }
    }

    response = await chat_with_gpt(messages, response_format)
    return response["response"]