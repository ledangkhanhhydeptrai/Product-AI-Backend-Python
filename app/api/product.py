from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db

from app.services.product_service import ProductService

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
