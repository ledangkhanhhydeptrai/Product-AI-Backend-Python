from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import asc, null
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review_schema import CreateReviewRequest


class ReviewService:
    @staticmethod
    def get_reviews(db: Session):
        return db.query(Review).order_by(asc(Review.id)).all()

    @staticmethod
    def create_review(db: Session, request: CreateReviewRequest, user_id: UUID):
        new_review = Review(
            user_id=user_id,
            product_id=request.product_id,
            comment=request.comment,
            rating=request.rating,
        )
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review

    @staticmethod
    def update_review(db: Session, request: CreateReviewRequest, user_id: UUID, id: UUID):
        update_review_by_user = db.query(Review).filter(Review.id == id).first()
        if not update_review_by_user:
            raise HTTPException(status_code=404, detail="Review not found")
        update_review_by_user.user_id = user_id
        update_review_by_user.product_id = request.product_id
        update_review_by_user.rating = request.rating
        update_review_by_user.comment = request.comment
        db.commit()
        db.refresh(update_review_by_user)
        return update_review_by_user

    @staticmethod
    def delete_review(db: Session, user_id: UUID, id: UUID):
        delete_review_by_user = db.query(Review).filter(Review.id == id, Review.user_id == user_id).first()
        if not delete_review_by_user:
            raise HTTPException(status_code=404, detail="Review not found")
        db.delete(delete_review_by_user)
        db.commit()
        return null
