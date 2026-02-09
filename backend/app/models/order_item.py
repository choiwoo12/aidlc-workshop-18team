"""
OrderItem Model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.utils.database import Base


class OrderItem(Base):
    """
    OrderItem Entity
    
    주문 ??개별 메뉴 ??�� ?�보
    """
    __tablename__ = "order_items"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign Keys
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id", ondelete="SET NULL"), nullable=True, comment="메뉴 ID (참조??")
    
    # Snapshot Attributes
    menu_name_snapshot = Column(String(100), nullable=False, comment="주문 ?�점 메뉴�?)
    menu_price_snapshot = Column(Float, nullable=False, comment="주문 ?�점 기본 가�?)
    selected_options = Column(JSON, nullable=True, comment="?�택???�션 JSON")
    
    # Attributes
    quantity = Column(Integer, nullable=False, comment="?�량")
    subtotal = Column(Float, nullable=False, comment="?�계")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu = relationship("Menu", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, menu_name='{self.menu_name_snapshot}', quantity={self.quantity}, subtotal={self.subtotal})>"
