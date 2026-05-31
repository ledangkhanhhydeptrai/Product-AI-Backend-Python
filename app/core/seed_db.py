
from app.models.user import User
from app.core.security import hash_password
from app.core.database import SessionLocal
from app.core.enums import Role


def seed_users():
    db = SessionLocal()

    # check đã có admin chưa
    admin = db.query(User).filter(User.email == "admin@gmail.com").first()
    if not admin:
        admin_user = User(
            full_name="Admin",
            email="admin@gmail.com",
            password=hash_password("123456"),
            phone="0123456789",
            role=Role.ADMIN
        )
        db.add(admin_user)

    # staff
    staff = db.query(User).filter(User.email == "staff@gmail.com").first()
    if not staff:
        staff_user = User(
            full_name="Staff",
            email="staff@gmail.com",
            password=hash_password("123456"),
            phone="0123456789",
            role=Role.STAFF
        )
        db.add(staff_user)

    db.commit()
    db.close()

    print("Seed users done!")