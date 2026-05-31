from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.category_service import CategoryService
from app.getDatabase.getAllDatabase import get_db
from app.response.ApiResponse import ApiResponse
from app.schemas.category_schema import CategoryResponse, CategoryCreateRequest

router = APIRouter(
    prefix="/api",
    tags=["Category"],
    responses={404: {"description": "Not found"}}
)


@router.get("/category", response_model=ApiResponse[list[CategoryResponse]])
def get_all_category(db: Session = Depends(get_db)):
    category = CategoryService.get_all_category(db)
    return {
        "status": 200,
        "message": "Get All Categories Successfully",
        "data": category
    }


@router.post("/category")
def create_category(request: CategoryCreateRequest, db: Session = Depends(get_db)):
    return {
        "status": 200,
        "message": "Create Category Successfully",
        "data": CategoryService.create_category(
            db,
            request
        )
    }
