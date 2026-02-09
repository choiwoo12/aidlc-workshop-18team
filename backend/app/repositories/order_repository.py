"""
Order Repository
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.models.order import Order, OrderStatus
from backend.app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    """Order data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Order, db)
    
    def get_by_store(self, store_id: int) -> List[Order]:
        """Get all orders by store_id"""
        return self.db.query(Order).filter(Order.store_id == store_id).order_by(desc(Order.created_at)).all()
    
    def get_by_table(self, table_id: int) -> List[Order]:
        """Get all orders by table_id"""
        return self.db.query(Order).filter(Order.table_id == table_id).order_by(desc(Order.created_at)).all()
    
    def get_by_status(self, store_id: int, status: OrderStatus) -> List[Order]:
        """Get orders by store_id and status"""
        return self.db.query(Order).filter(
            Order.store_id == store_id,
            Order.status == status
        ).order_by(desc(Order.created_at)).all()
    
    def get_last_order_number(self, store_id: int) -> Optional[str]:
        """Get last order number for store"""
        last_order = self.db.query(Order).filter(
            Order.store_id == store_id
        ).order_by(desc(Order.created_at)).first()
        
        return last_order.order_number if last_order else None
