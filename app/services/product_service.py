from uuid import UUID

from fastapi import UploadFile, HTTPException
from sqlalchemy import null
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product_schema import ProductCreateRequest, ProductUpdateRequest
from app.services.upload_service import UploadService


class ProductService:
    @staticmethod
    def get_product(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_by_id(db: Session, id: UUID):
        return db.query(Product).filter(Product.id == id).first()

    @staticmethod
    def get_product_public(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product_public_by_id(db: Session, id: UUID):
        return db.query(Product).filter(Product.id == id).first()

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
    def delete_product_by_id(db: Session, id: UUID):
        product_admin_id = db.query(Product).filter(Product.id == id).first()
        if not product_admin_id:
            raise HTTPException(status_code=404, detail="Product not found")
        db.delete(product_admin_id)
        db.commit()
        return null
