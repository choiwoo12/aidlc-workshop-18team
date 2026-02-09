"""
Table Model
"""
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base
import enum


class TableStatus(str, enum.Enum):
    """?Œì´ë¸??íƒœ"""
    AVAILABLE = "AVAILABLE"  # ë¹„ì–´?ˆìŒ (?¬ìš© ê°€??
    IN_USE = "IN_USE"  # ?¬ìš©ì¤?(ê³ ê°??ì°©ì„)


class Table(Base):
    """
    Table Entity
    
    ?Œì´ë¸??•ë³´ ë°??íƒœ ê´€ë¦?
    """
    __tablename__ = "tables"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    table_number = Column(String(10), nullable=False, index=True, comment="?Œì´ë¸?ë²ˆí˜¸")
    status = Column(SQLEnum(TableStatus), nullable=False, default=TableStatus.AVAILABLE, index=True, comment="?„ì¬ ?íƒœ")
    status_changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="?íƒœ ë³€ê²??¼ì‹œ")
    status_history = Column(JSON, nullable=False, default=list, comment="?íƒœ ë³€ê²??´ë ¥")
    current_session_started_at = Column(DateTime(timezone=True), nullable=True, comment="?„ì¬ ?¸ì…˜ ?œì‘ ?¼ì‹œ")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="tables")
    orders = relationship("Order", back_populates="table", cascade="all, delete-orphan")
    order_histories = relationship("OrderHistory", back_populates="table", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Table(id={self.id}, table_number='{self.table_number}', status='{self.status}')>"
