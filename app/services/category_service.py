from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models import Category


class CategoryService:
    @staticmethod
    def get_all_category(db: Session):
        return db.query(Category).order_by(asc(Category.id)).all()
