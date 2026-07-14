# from ollama import Client
#
# from app.models.product import Product
#
# client = Client(host="http://localhost:11434")
#
#
# class EmbeddingService:
#
#     @staticmethod
#     def generate_product_embedding(product: Product):
#         text = f"""
#         Name: {product.name}
#         Description: {product.description}
#         """
#         response = client.embed(
#             model="nomic-embed-text",
#             input=text,
#         )
#         embedding = response["embeddings"][0]
#         print(type(embedding))
#         print(len(embedding))
#         print("Embedding dimension:", len(embedding))
#
#         return embedding
import os

from google.genai import types

from app.models.product import Product
from google import genai
import inspect

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class EmbeddingService:
    @staticmethod
    def generate_product_embedding(product: Product):
        print("===== EmbeddingService START =====")

        text = f"""
            Name: {product.name}
            Description: {product.description}
            """

        print("Calling Gemini...")

        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=768
            ),
        )

        print("Gemini returned")

        embedding = response.embeddings[0].values

        print("Dimension:", len(embedding))

        return embedding
