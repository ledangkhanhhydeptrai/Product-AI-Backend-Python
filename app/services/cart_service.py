from uuid import UUID

from sqlalchemy import asc, null
from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product


class CartService:
    @staticmethod
    def get_cart(db: Session, user_id: UUID):
        return (db.query(Cart)
                .order_by(asc(Cart.id))
                .filter(Cart.user_id == user_id)
                .all())

    @staticmethod
    def add_to_cart(db: Session, user_id: UUID, product_id: UUID, quantity: int = 1):
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise Exception("Product not found")

        price = product.price  # 👈 lấy từ DB
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        item = (
            db.query(CartItem)
            .filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
            .first()
        )
        if item:
            item.quantity += quantity
        else:
            item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                price=price,
                quantity=quantity
            )
            db.add(item)

        db.commit()
        return cart

    @staticmethod
    def remove_from_cart(db: Session, user_id: UUID, product_id: UUID):
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        (db.query(CartItem)
         .filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id)
         .delete()
         )
        db.commit()
        return null()
