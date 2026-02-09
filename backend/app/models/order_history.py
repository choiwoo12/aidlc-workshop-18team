"""
OrderHistory Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.app.utils.database import Base


class OrderHistory(Base):
    """
    OrderHistory Entity
    
    완료된 주문의 이력 보관 및 분석
    """
    __tablename__ = "order_histories"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    original_order_id = Column(Integer, nullable=True, comment="원본 주문 ID")
    order_number = Column(String(10), nullable=False, comment="주문 번호")
    order_items_snapshot = Column(JSON, nullable=False, comment="주문 항목 스냅샷 JSON")
    total_amount = Column(Float, nullable=False, comment="총 금액")
    status_transitions = Column(JSON, nullable=False, comment="상태 변경 이력 JSON")
    session_started_at = Column(DateTime(timezone=True), nullable=False, comment="테이블 세션 시작 일시")
    session_ended_at = Column(DateTime(timezone=True), nullable=False, comment="테이블 세션 종료 일시")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="order_histories")
    table = relationship("Table", back_populates="order_histories")
    
    def __repr__(self):
        return f"<OrderHistory(id={self.id}, order_number='{self.order_number}', total_amount={self.total_amount})>"
