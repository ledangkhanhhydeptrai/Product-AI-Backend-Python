from uuid import UUID

from fastapi import UploadFile, HTTPException
from sqlalchemy import null
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product_schema import ProductCreateRequest, ProductUpdateRequest
from app.services.upload_service import UploadService
from app.models.product_embedding import ProductEmbedding
from app.services.embedding_service import EmbeddingService


class ProductService:
    @staticmethod
    def get_product(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_by_id(db: Session, id: UUID):
        return db.query(Product).filter(Product.id == id).first()

    @staticmethod
    def get_product_embedding_by_id(db: Session, id: UUID):
        embedding = db.query(ProductEmbedding) \
            .filter(ProductEmbedding.product_id == id) \
            .first()

        return {
            "product_id": id,
            "has_embedding": embedding is not None
        }

    @staticmethod
    def get_product_public(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_public_by_id(db: Session, id: UUID):
        return db.query(Product).filter(Product.id == id).first()

    @staticmethod
    def create_product(
            db: Session,
            product: ProductCreateRequest,
            file: UploadFile
    ):
        try:
            product_url = UploadService.upload_image(file)

            new_product = Product(
                name=product.name,
                slug=product.slug,
                description=product.description,
                price=product.price,
                stock=product.stock,
                thumbnail=product.thumbnail,
                category_id=product.category_id,
                brand_id=product.brand_id,
                is_active=product.is_active,
                image_url=product_url
            )

            db.add(new_product)
            db.commit()
            db.refresh(new_product)

            embedding = EmbeddingService.generate_product_embedding(
                new_product
            )

            print(
                f"Product ID: {new_product.id}"
            )

            print(
                f"Embedding length: {len(embedding)}"
            )

            product_embedding = ProductEmbedding(
                product_id=new_product.id,
                embedding=embedding
            )

            db.add(product_embedding)
            db.commit()
            db.refresh(product_embedding)

            print(
                f"Embedding ID: {product_embedding.id}"
            )

            return new_product

        except Exception as e:
            db.rollback()
            print("ERROR:", str(e))
            raise

    @staticmethod
    def update_product_by_id(db: Session, id: UUID, update_product: ProductUpdateRequest):
        product_admin_id = db.query(Product).filter(Product.id == id).first()
        if not product_admin_id:
            raise HTTPException(status_code=404, detail="Product not found")
        product_admin_id.name = update_product.name
        product_admin_id.slug = update_product.slug
        product_admin_id.description = update_product.description
        db.add(product_admin_id)
        db.commit()
        db.refresh(product_admin_id)
        return product_admin_id

    @staticmethod
    def create_embedding_for_product(db: Session, product_id: UUID):

        product = ProductService.get_product_by_id(db, product_id)

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # check trực tiếp bảng embedding (chuẩn nhất)
        exists = (
            db.query(ProductEmbedding)
            .filter(ProductEmbedding.product_id == product_id)
            .first()
        )

        if exists:
            raise HTTPException(
                status_code=400,
                detail="Product already has embedding"
            )

        embedding = EmbeddingService.generate_product_embedding(product)

        product_embedding = ProductEmbedding(
            product_id=product.id,
            embedding=embedding
        )

        db.add(product_embedding)
        db.commit()

        return product_embedding

    @staticmethod
    def delete_product_by_id(db: Session, id: UUID):
        product_admin_id = db.query(Product).filter(Product.id == id).first()
        if not product_admin_id:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product_admin_id)
        db.commit()
        return null
