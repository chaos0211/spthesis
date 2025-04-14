# backend/models/order.py
from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from product import Product

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(Enum('pending', 'completed', 'cancelled'), default='pending')
    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="orders")

    @staticmethod
    def get_orders(db_session, seller_id):
        return db_session.query(Order).join(Product).filter(Product.seller_id == seller_id).all()