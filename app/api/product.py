from uuid import UUID

from fastapi import Depends, APIRouter, Form, UploadFile, File, Path
from sqlalchemy.orm import Session

from app.getDatabase.getAllDatabase import get_db

from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreateRequest, ProductUpdateRequest
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


@router.get("/product/{id}",
            response_model=ApiResponse[ProductResponse],
            dependencies=[Depends(require_admin)])
def get_product_by_id(
        db: Session = Depends(get_db),
        id: UUID = Path(...)
):
    products = ProductService.get_product_by_id(db, id)

    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.get("/public/product", response_model=ApiResponse[list[ProductListResponse]])
def get_product_public(
        db: Session = Depends(get_db)
):
    products = ProductService.get_product_public(db)
    print("PUBLIC API CALLED")
    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.get("/public/product/{id}", response_model=ApiResponse[ProductListResponse])
def get_product_public_by_id(
        db: Session = Depends(get_db),
        id: UUID = Path(...)
):
    products = ProductService.get_product_public_by_id(db, id)

    return {
        "status": 200,
        "message": "Get All Products Successfully",
        "data": products
    }


@router.post("/create-product", dependencies=[Depends(require_admin)], response_model=ApiResponse[ProductResponse])
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


@router.put("/product/{id}", response_model=ApiResponse[ProductResponse], dependencies=[Depends(require_admin)])
def update_product(request: ProductUpdateRequest, db: Session = Depends(get_db), id: UUID = Path(...)):
    update_product_admin = ProductService.update_product_by_id(db, id, request)
    return {
        "status": 200,
        "message": "Update Product Successfully",
        "data": update_product_admin
    }


@router.delete("/product/{id}", dependencies=[Depends(require_admin)])
def delete_product(db: Session = Depends(get_db), id: UUID = Path(...)):
    ProductService.delete_product_by_id(db, id)
    return {
        "status": 200,
        "message": "Delete Product Successfully",
        "data": None
    }
