from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, session: Session):
        self.db = session

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_login(self, login: str) -> User | None:
        return self.db.query(User).filter(User.login == login).first()

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int, limit: int, city: str = None) -> list[User]:
        query = self.db.query(User)
        if city:
            query = query.filter(User.city.ilike(f"%{city}%"))
        return query.offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(
            login=user.login,
            email=user.email,
            city=user.city,
            password_hash=hashed_password,
            is_admin=False
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_update: UserUpdate):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            update_data = user_update.dict(exclude_unset=True)
            if "password" in update_data and update_data["password"]:
                update_data["password_hash"] = pwd_context.hash(update_data.pop("password"))
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user