from uuid import UUID

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from app.response.ApiResponse import ApiResponse
from app.schemas.review_schema import ReviewResponse, CreateReviewRequest
from app.getDatabase.getAllDatabase import get_db
from app.services.review_service import ReviewService
from app.core.deps import CurrentUser, get_current_user

router = APIRouter(
    prefix="/api",
    tags=["Review"],
    responses={404: {"description": "Not found"}},
)


@router.get("/review", response_model=ApiResponse[list[ReviewResponse]])
def get_all_review(db: Session = Depends(get_db)):
    review = ReviewService.get_reviews(db)
    return {
        "status": 200,
        "message": "Get All Reviews Successfully",
        "data": review
    }


@router.post("/review/create", response_model=ApiResponse[ReviewResponse])
def create_review(request: CreateReviewRequest, db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    review = ReviewService.create_review(db=db, request=request, user_id=current_user.id)
    return {
        "status": 200,
        "message": "Create Review Successfully",
        "data": review
    }


@router.put("/review/{id}", response_model=ApiResponse[ReviewResponse])
def update_review(request: CreateReviewRequest, id: UUID = Path(...), db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    review = ReviewService.update_review(db=db, request=request, id=id, user_id=current_user.id)
    return {
        "status": 200,
        "message": "Update Review Successfully",
        "data": review
    }


@router.delete("/review/{id}")
def delete_review(id: UUID = Path(...), db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    ReviewService.delete_review(db=db, id=id, user_id=current_user.id)
    return {
        "status": 200,
        "message": "Delete Review Successfully",
        "data": None
    }
