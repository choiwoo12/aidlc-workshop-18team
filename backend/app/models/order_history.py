"""
OrderHistory Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base


class OrderHistory(Base):
    """
    OrderHistory Entity
    
    ?„ë£Œ??ì£¼ë¬¸???´ë ¥ ë³´ê? ë°?ë¶„ì„
    """
    __tablename__ = "order_histories"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    store_id = Column(Integer, ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    table_id = Column(Integer, ForeignKey("tables.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Attributes
    original_order_id = Column(Integer, nullable=True, comment="?ë³¸ ì£¼ë¬¸ ID")
    order_number = Column(String(10), nullable=False, comment="ì£¼ë¬¸ ë²ˆí˜¸")
    order_items_snapshot = Column(JSON, nullable=False, comment="ì£¼ë¬¸ ??ª© ?¤ëƒ…??JSON")
    total_amount = Column(Float, nullable=False, comment="ì´?ê¸ˆì•¡")
    status_transitions = Column(JSON, nullable=False, comment="?íƒœ ë³€ê²??´ë ¥ JSON")
    session_started_at = Column(DateTime(timezone=True), nullable=False, comment="?Œì´ë¸??¸ì…˜ ?œì‘ ?¼ì‹œ")
    session_ended_at = Column(DateTime(timezone=True), nullable=False, comment="?Œì´ë¸??¸ì…˜ ì¢…ë£Œ ?¼ì‹œ")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    store = relationship("Store", back_populates="order_histories")
    table = relationship("Table", back_populates="order_histories")
    
    def __repr__(self):
        return f"<OrderHistory(id={self.id}, order_number='{self.order_number}', total_amount={self.total_amount})>"
