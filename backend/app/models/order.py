"""
Order Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.utils.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """주문 상태"""
    PENDING = "PENDING"  # 대기중 (주문 생성 직후)
    CONFIRMED = "CONFIRMED"  # 확인됨 (관리자가 확인)
    PREPARING = "PREPARING"  # 준비중 (조리 시작)
    READY = "READY"  # 서빙 대기 (조리 완료)
    COMPLETED = "COMPLETED"  # 완료 (서빙 완료)


class Order(Base):
    """
    Order Entity
    
    고객 주문 정보 및 상태 관리
    """
    __tablename__ = "orders"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    order_number = Column(String(10), nullable=False, comment="주문 번호")
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True, comment="주문 상태")
    total_amount = Column(Float, nullable=False, comment="총 금액")
    lock_version = Column(Integer, nullable=False, default=0, comment="비관적 잠금용 버전 번호")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}', total_amount={self.total_amount})>"
