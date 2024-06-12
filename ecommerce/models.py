from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class UserRole(PyEnum):
    USER = "User"
    ADMIN = "Admin"

class OrderStatus(PyEnum):
    PENDING = "Pending"
    PROCESSED = "Processed"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"

class User(Base):
    _tablename_ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    cart_items = relationship('CartItem', back_populates='user')
    orders = relationship('Order', back_populates='user')
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

class Product(Base):
    _tablename_ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    cart_items = relationship('CartItem', back_populates='product')

