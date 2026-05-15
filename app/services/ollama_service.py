import ollama

def chat_with_ai(message: str):
    response = ollama.chat(
        model="llama3",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return response["message"]["content"]