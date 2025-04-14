# backend/models/user.py
from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum('user', 'seller'), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    @staticmethod
    def register(db_session, username, password, email, role):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(
            username=username,
            password=hashed.decode('utf-8'),
            email=email,
            role=role
        )
        try:
            db_session.add(user)
            db_session.commit()
            return True
        except:
            db_session.rollback()
            return False

    @staticmethod
    def login(db_session, username, password):
        user = db_session.query(User).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return user
        return None