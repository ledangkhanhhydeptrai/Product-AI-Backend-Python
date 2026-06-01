from uuid import UUID

from fastapi import Depends, APIRouter, Form, UploadFile, File
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db

from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreateRequest
from app.schemas.product_schema import ProductResponse, ProductListResponse
from app.response.ApiResponse import ApiResponse
from app.core.permissions import require_admin

router = APIRouter(
    prefix="/api",
    tags=["Product"]
)


@router.get("/product",
            response_model=ApiResponse[list[ProductResponse]],
            dependencies=[Depends(require_admin)])
def get_product(
        db: Session = Depends(get_db)
):
    products = ProductService.get_product(db)

    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.get("/product/public", response_model=ApiResponse[list[ProductListResponse]])
def get_product_public(
        db: Session = Depends(get_db)
):
    products = ProductService.get_product(db)

    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.post("/create-product", dependencies=[Depends(require_admin)])
def create_product(
        name: str = Form(...),
        slug: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        stock: int = Form(...),
        thumbnail: str = Form(...),
        category_id: UUID = Form(...),
        brand_id: UUID = Form(...),
        is_active: bool = Form(...),
        db: Session = Depends(get_db),
        file: UploadFile = File(...)
):
    new_product = ProductCreateRequest(
        name=name,
        slug=slug,
        description=description,
        price=price,
        stock=stock,
        thumbnail=thumbnail,
        category_id=category_id,
        brand_id=brand_id,
        is_active=is_active,

    )
    product = ProductService.create_product(db, new_product, file)
    return {
        "status": 201,
        "message": "Create Product Successfully",
        "data": product
    }
