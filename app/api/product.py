from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db

from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreateRequest

router = APIRouter(
    prefix="/api",
    tags=["Product"]
)


@router.get("/product")
def get_product(
        db: Session = Depends(get_db)
):
    products = ProductService.get_product(db)

    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.post("/create-product")
def create_product(
        product: ProductCreateRequest, db: Session = Depends(get_db),
):
    product = ProductService.create_product(db, product)
    return {
        "status": 201,
        "message": "Create Product Successfully",
        "data": product
    }
