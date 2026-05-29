from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.brand import Brand
from app.schemas.brand_schema import CreateBrandRequest
from app.services.upload_service import UploadService


class BrandService:
    @staticmethod
    def get_brand(db: Session):
        return db.query(Brand).all()

    @staticmethod
    def create_brand(db: Session, brand: CreateBrandRequest, file: UploadFile):
        logo_url = UploadService.upload_image(file)
        new_brand = Brand(
            name=brand.name,
            logo=logo_url,
            description=brand.description,
        )

        db.add(new_brand)
        db.commit()
        db.refresh(new_brand)
        return new_brand
