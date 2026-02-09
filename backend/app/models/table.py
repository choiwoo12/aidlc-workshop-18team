"""
Table Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
import enum


class TableStatus(str, enum.Enum):
    """테이블 상태"""
    AVAILABLE = "AVAILABLE"  # 비어?�음 (?�용 가??
    IN_USE = "IN_USE"  # ?�용�?(고객??착석)


class Table(Base):
    """
    Table Entity
    
    ?�이�??�보 �??�태 관�?
    """
    __tablename__ = "tables"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    table_number = Column(String(10), nullable=False, index=True, comment="?�이�?번호")
    status = Column(SQLEnum(TableStatus), nullable=False, default=TableStatus.AVAILABLE, index=True, comment="?�재 ?�태")
    status_changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="?�태 변�??�시")
    status_history = Column(JSON, nullable=False, default=list, comment="?�태 변�??�력")
    current_session_started_at = Column(DateTime(timezone=True), nullable=True, comment="?�재 ?�션 ?�작 ?�시")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="tables")
    orders = relationship("Order", back_populates="table", cascade="all, delete-orphan")
    order_histories = relationship("OrderHistory", back_populates="table", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Table(id={self.id}, table_number='{self.table_number}', status='{self.status}')>"
