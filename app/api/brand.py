from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File, Form, Path
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db
from app.services.brand_service import BrandService
from app.schemas.brand_schema import CreateBrandRequest, UpdateBrandRequest
from app.schemas.brand_schema import BrandResponse
from app.response.ApiResponse import ApiResponse

router = APIRouter(
    prefix="/api",
    tags=["Brands"],
)


@router.get("/brands", response_model=ApiResponse[list[BrandResponse]])
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


@router.get("/brands/{id}")
def get_brand(db: Session = Depends(get_db), id: UUID = Path(...)):
    branded = BrandService.get_brand_by_id(db, id)
    return {
        "status": 200,
        "message": "Get Brand Successfully",
        "data": branded
    }


@router.put("/brands/{id}")
def update_brand(id: UUID = Path(...),
                 name: str = Form(...),
                 description: str = Form(...),
                 logo: UploadFile = File(...),
                 db: Session = Depends(get_db)):
    new_brand = UpdateBrandRequest(
        name=name,
        description=description,
    )
    brand = BrandService.update_brand_by_id(db, id, new_brand, logo)
    return {
        "status": 200,
        "message": "Update Brand Successfully",
        "data": brand
    }


@router.delete("/brands/{id}")
def delete_brand(db: Session = Depends(get_db), id: UUID = Path(...)):
    BrandService.delete_brand_by_id(db, id)
    return {
        "status": 200,
        "message": "Delete Brand Successfully",
        "data": None
    }
