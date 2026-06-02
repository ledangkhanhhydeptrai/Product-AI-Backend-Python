from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.category_service import CategoryService
from app.getDatabase.getAllDatabase import get_db
from app.response.ApiResponse import ApiResponse
from app.schemas.category_schema import CategoryResponse, CategoryCreateRequest
from app.core.permissions import require_admin

router = APIRouter(
    prefix="/api",
    tags=["Category"],
    responses={404: {"description": "Not found"}}
)


@router.get("/public/category",
            response_model=ApiResponse[list[CategoryResponse]],
            dependencies=[Depends(require_admin)])
def get_all_category(db: Session = Depends(get_db)):
    category = CategoryService.get_all_category(db)
    return {
        "status": 200,
        "message": "Get All Categories Successfully",
        "data": category
    }


@router.post("/category",
             response_model=ApiResponse[CategoryResponse],
             dependencies=[Depends(require_admin)])
def create_category(request: CategoryCreateRequest, db: Session = Depends(get_db)):
    return {
        "status": 200,
        "message": "Create Category Successfully",
        "data": CategoryService.create_category(
            db,
            request
        )
    }


@router.get("/public/category/{id}",
            response_model=ApiResponse[CategoryResponse],
            dependencies=[Depends(require_admin)])
def get_category(id: UUID, db: Session = Depends(get_db)):
    category = CategoryService.get_category_by_id(db, id)
    return {
        "status": 200,
        "message": "Get Category Successfully",
        "data": category
    }


@router.put("/category/{id}",
            response_model=ApiResponse[CategoryResponse],
            dependencies=[Depends(require_admin)])
def update_category(id: UUID, request: CategoryCreateRequest, db: Session = Depends(get_db)):
    category = CategoryService.update_category_by_id(db, id, request)
    return {
        "status": 200,
        "message": "Update Category Successfully",
        "data": category
    }


@router.delete("/category/{id}",
               dependencies=[Depends(require_admin)])
def delete_category(id: UUID, db: Session = Depends(get_db)):
    CategoryService.delete_category_by_id(db, id)
    return {
        "status": 200,
        "message": "Delete Category Successfully",
        "data": None
    }
