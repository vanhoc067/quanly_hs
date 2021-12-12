from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime,  ForeignKey, Enum
from quanly_hs import db
from flask_login import UserMixin
from enum import Enum as UserEnum
from datetime import datetime


class baseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class DanhSachHS(baseModel):
    __tablename__ = 'danhsachhs'
    name = Column(String(50), nullable=False)
    gender = Column(Enum('Nam','Nu'), nullable=False)
    date_of_birth = Column(DateTime)
    address = Column(String(50), nullable=False)
    phone = Column(Integer)
    email = Column(String(50))


class DanhSachLop(baseModel):
    __tablename__ = 'danhsachlop'
    class_name = Column(String(20), nullable=False)
    grade = Column(String(20), nullable=False)
    quantity = Column(Integer, nullable=False)


class UserRole(UserEnum):
    admin = 1
    user = 2


class User(baseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    avatar = Column(String(100), default='images/default.png')
    user_role = Column(Enum(UserRole), default=UserRole.user)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()