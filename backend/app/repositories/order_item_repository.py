"""
OrderItem Repository
"""
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.order_item import OrderItem
from backend.app.repositories.base_repository import BaseRepository


class OrderItemRepository(BaseRepository[OrderItem]):
    """OrderItem data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(OrderItem, db)
    
    def get_by_order(self, order_id: int) -> List[OrderItem]:
        """Get all order items by order_id"""
        return self.db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
