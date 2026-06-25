from uuid import UUID
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from sqlalchemy import asc, null
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.schemas.brand_schema import CreateBrandRequest, UpdateBrandRequest
from app.services.upload_service import UploadService


class BrandService:
    @staticmethod
    def get_brand(db: Session):
        return db.query(Brand).order_by(asc(Brand.id)).all()

    @staticmethod
    def create_brand(db: Session, brand: CreateBrandRequest, logo: UploadFile):
        existing_brand = (
            db.query(Brand)
            .filter(Brand.name == brand.name)
            .first()
        )
        if existing_brand:
            raise HTTPException(status_code=400, detail="Brand Already Exists")
        logo_url = UploadService.upload_image(logo)
        new_brand = Brand(
            name=brand.name,
            logo=logo_url,
            description=brand.description,
        )

        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand

    @staticmethod
    def get_brand_by_id(db: Session, id: UUID):
        return db.query(Brand).filter(Brand.id == id).first()

    @staticmethod
    def update_brand_by_id(db: Session, id: UUID, new_brand: UpdateBrandRequest, file: UploadFile):
        brand = db.query(Brand).filter(Brand.id == id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand Not Found")
        brand.name = new_brand.name
        brand.description = new_brand.description
        result = cloudinary.uploader.upload(
            file.file
        )
        brand.logo = result["secure_url"]
        db.commit()
        db.refresh(brand)
        return brand

    @staticmethod
    def delete_brand_by_id(db: Session, id: UUID):
        brand = db.query(Brand).filter(Brand.id == id).first()
        if not brand:
            raise HTTPException(status_code=404, detail="Brand Not Found")
        db.delete(brand)
        db.commit()
        return null
