import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GEMINI_API_KEY")


import openai

prompt = input("Ask something: ")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

print("AI:", response.choices[0].message.content)