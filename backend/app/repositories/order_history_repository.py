"""
OrderHistory Repository
"""
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.order_history import OrderHistory
from app.repositories.base_repository import BaseRepository


class OrderHistoryRepository(BaseRepository[OrderHistory]):
    """OrderHistory data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(OrderHistory, db)
    
    def get_by_store(self, store_id: int) -> List[OrderHistory]:
        """Get all order histories by store_id"""
        return self.db.query(OrderHistory).filter(
            OrderHistory.store_id == store_id
        ).order_by(desc(OrderHistory.created_at)).all()
    
    def get_by_table(self, table_id: int) -> List[OrderHistory]:
        """Get all order histories by table_id"""
        return self.db.query(OrderHistory).filter(
            OrderHistory.table_id == table_id
        ).order_by(desc(OrderHistory.created_at)).all()
