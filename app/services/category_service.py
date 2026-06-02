from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import asc, null
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category_schema import CategoryCreateRequest


class CategoryService:
    @staticmethod
    def get_all_category(db: Session):
        return db.query(Category).order_by(asc(Category.id)).all()

    @staticmethod
    def create_category(db: Session, new_category: CategoryCreateRequest):
        existing_category = db.query(Category).filter(Category.name == new_category.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category Already Exists")
        new_category = Category(
            name=new_category.name,
            description=new_category.description,
            slug=new_category.slug,
            created_at=datetime.now(),
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    @staticmethod
    def get_category_by_id(db: Session, id: UUID):
        return db.query(Category).filter(Category.id == id).first()

    @staticmethod
    def update_category_by_id(db: Session, id: UUID, new_category: CategoryCreateRequest):
        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category Not Found")
        category.name = new_category.name
        category.description = new_category.description
        category.slug = new_category.slug
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    @staticmethod
    def delete_category_by_id(db: Session, id: UUID):
        categories = db.query(Category).filter(Category.id == id).first()
        if not categories:
            raise HTTPException(status_code=404, detail="Category Not Found")
        db.delete(categories)
        db.commit()
        return null()
