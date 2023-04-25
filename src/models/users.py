# -*- coding:utf-8 -*-
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, text

from src.models import db
from src.schemas.user import User
from src.libs.exceptions import UserNotFound, UserEmailExisted


class Users(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(32), unique=True, index=True)
    hashed_password = Column(String(64))
    is_active = Column(Boolean, default=True)
    created_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )
    updated_at = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新时间",
    )

    @classmethod
    def get_user(cls, user_id: int):
        result = db.session.query(cls).get(user_id)
        if not result:
            raise UserNotFound(message=f"User not found, user_id: {user_id}")
        return result

    @classmethod
    def get_user_by_email(cls, email: str):
        return db.session.query(cls).filter_by(email=email).one_or_none()

    @classmethod
    def create(cls, user: User):
        result = cls.get_user_by_email(email=user.email)
        if result:
            raise UserEmailExisted(message=f"Email have registed, email: {user.email}")

        fake_hashed_password = user.password + "notreallyhashed"
        obj = cls(
            email=user.email,
            hashed_password=fake_hashed_password,
        )
        with db.auto_commit():
            db.session.add(obj)
        return obj

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
