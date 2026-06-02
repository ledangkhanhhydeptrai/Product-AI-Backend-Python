from ollama import Client

from app.models.product import Product

client = Client(host="http://localhost:11434")


class EmbeddingService:

    @staticmethod
    def generate_product_embedding(product: Product):
        text = f"""
        Name: {product.name}
        Description: {product.description}
        """
        response = client.embed(
            model="nomic-embed-text",
            input=text,
        )
        embedding = response["embeddings"][0]
        print(type(embedding))
        print(len(embedding))
        print("Embedding dimension:", len(embedding))

        return embedding
