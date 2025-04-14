# backend/models/product.py
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    @staticmethod
    def add_product(db_session, seller_id, name, description, price, stock):
        product = Product(
            seller_id=seller_id,
            name=name,
            description=description,
            price=price,
            stock=stock
        )
        try:
            db_session.add(product)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            return False

    @staticmethod
    def get_products(db_session, seller_id):
        return db_session.query(Product).filter_by(seller_id=seller_id).all()

    @staticmethod
    def update_product(db_session, product_id, name, description, price, stock):
        product = db_session.query(Product).filter_by(id=product_id).first()
        if product:
            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            try:
                db_session.commit()
                return True
            except:
                db_session.rollback()
        return False

    @staticmethod
    def delete_product(db_session, product_id):
        product = db_session.query(Product).filter_by(id=product_id).first()
        if product:
            try:
                db_session.delete(product)
                db_session.commit()
                return True
            except:
                db_session.rollback()
        return False