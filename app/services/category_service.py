import datetime

from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category_schema import CategoryCreateRequest


class CategoryService:
    @staticmethod
    def get_all_category(db: Session):
        return db.query(Category).order_by(asc(Category.id)).all()

    @staticmethod
    def create_category(db: Session, new_category: CategoryCreateRequest):
        new_category = Category(
            name=new_category.name,
            description=new_category.description,
            slug=new_category.slug,
            created_at=datetime.datetime.utcnow(),
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category
