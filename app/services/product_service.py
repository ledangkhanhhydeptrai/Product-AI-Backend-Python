from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product_schema import ProductCreateRequest
from app.services.upload_service import UploadService


class ProductService:
    @staticmethod
    def get_product(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_public(db: Session):
        return db.query(Product).all()

    @staticmethod
    def create_product(db: Session, product: ProductCreateRequest, file: UploadFile):
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
        return new_product
