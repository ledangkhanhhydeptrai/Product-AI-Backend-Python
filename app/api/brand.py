from fastapi import APIRouter, Depends, UploadFile, File, Form

from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.services.brand_service import BrandService
from app.schemas.brand_schema import CreateBrandRequest

router = APIRouter(
    prefix="/api",
    tags=["Brands"],
)


@router.get("/brands")
def get_brand(db: Session = Depends(get_db)):
    brand = BrandService.get_brand(db)
    return {
        "status": 200,
        "message": "Get All Brands Successfully",
        "data": brand
    }


@router.post("/create-brands")
def create_brand(name: str = Form(...),
                 description: str = Form(...),
                 file: UploadFile = File(...),
                 db: Session = Depends(get_db)):
    brand = CreateBrandRequest(
        name=name,
        description=description,
    )

    return {
        "status": 200,
        "message": "Create Brand Successfully",
        "data": BrandService.create_brand(
            db=db,
            brand=brand,
            file=file
        )
    }
