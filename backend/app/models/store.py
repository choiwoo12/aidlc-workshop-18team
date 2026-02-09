"""
Store Model
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.utils.database import Base


class Store(Base):
    """
    Store Entity
    
    매장 기본 정보 관리
    """
    __tablename__ = "stores"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Attributes
    name = Column(String(100), nullable=False, comment="매장명")
    admin_username = Column(String(50), unique=True, nullable=False, comment="관리자 계정 아이디")
    admin_password_hash = Column(String(255), nullable=False, comment="관리자 비밀번호 해시")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    tables = relationship("Table", back_populates="store", cascade="all, delete-orphan")
    menus = relationship("Menu", back_populates="store", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="store", cascade="all, delete-orphan")
    order_histories = relationship("OrderHistory", back_populates="store", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Store(id={self.id}, name='{self.name}', admin_username='{self.admin_username}')>"
