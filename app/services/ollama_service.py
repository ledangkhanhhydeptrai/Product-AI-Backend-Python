# import ollama
#
# def chat_with_ai(message: str):
#     response = ollama.chat(
#         model="llama3",
#         messages=[
#             {"role": "user", "content": message}
#         ]
#     )
#
#     return response["message"]["content"]
from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def chat_with_ai(message: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
    )

    return response.text