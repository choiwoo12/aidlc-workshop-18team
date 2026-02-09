"""
Order Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """Order status"""
    PENDING = "PENDING"  # Waiting (just created)
    CONFIRMED = "CONFIRMED"  # Confirmed (by admin)
    PREPARING = "PREPARING"  # Preparing (cooking started)
    READY = "READY"  # Ready for serving (cooking done)
    COMPLETED = "COMPLETED"  # Completed (served)


class Order(Base):
    """
    Order Entity
    
    Customer order information and status management
    """
    __tablename__ = "orders"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    order_number = Column(String(10), nullable=False, comment="Order number")
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True, comment="Order status")
    total_amount = Column(Float, nullable=False, comment="Total amount")
    lock_version = Column(Integer, nullable=False, default=0, comment="Optimistic lock version")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}', total_amount={self.total_amount})>"
