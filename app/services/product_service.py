from sqlalchemy.orm import Session

from app.models.product import Product


class ProductService:
    @staticmethod
    def get_product(db: Session):
        return db.query(Product).all()
