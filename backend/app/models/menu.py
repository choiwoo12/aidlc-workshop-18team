"""
Menu Model
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base


class Menu(Base):
    """
    Menu Entity
    
    메뉴 ?�보 �??�션 관�?
    """
    __tablename__ = "menus"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    name = Column(String(100), nullable=False, comment="메뉴�?)
    description = Column(Text, nullable=True, comment="메뉴 ?�명")
    price = Column(Float, nullable=False, comment="기본 가�?)
    category_level1 = Column(String(50), nullable=False, index=True, comment="1?�계 카테고리")
    category_level2 = Column(String(50), nullable=True, comment="2?�계 카테고리")
    image_url = Column(String(500), nullable=True, comment="메뉴 ?��?지 URL")
    is_available = Column(Boolean, nullable=False, default=True, comment="?�매 가???��?")
    options = Column(JSON, nullable=True, comment="메뉴 ?�션 JSON")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="menus")
    order_items = relationship("OrderItem", back_populates="menu")
    
    def __repr__(self):
        return f"<Menu(id={self.id}, name='{self.name}', price={self.price}, is_available={self.is_available})>"
