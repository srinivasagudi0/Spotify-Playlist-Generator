# Convert input-> empotion, 
# Generate:
# 1. mood
# 2. genre
# 3. keywords
# 4. song suggestions

from openai import OpenAI
import os


def convert_to_emotion(user_input):
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )
    prompt = """
You are a helpful assistant that converts user input into an emotion.
Retrun only in the following json format:
{
"emotion": "here emotion",
"mood": "here mood",
"keywords": ["music-ready", "keywords"],
"energy": "low/medium/high"
}
Give me only the json response without any explanation and the json should be working and should be parsable.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": f"Convert the following user input into an emotion: {user_input}",
            },
        ],
    )
    emotion = response.choices[0].message.content.strip()
    return emotion
