"""
Table Repository
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.table import Table, TableStatus
from app.repositories.base_repository import BaseRepository


class TableRepository(BaseRepository[Table]):
    """Table data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Table, db)
    
    def get_by_table_number(self, store_id: int, table_number: str) -> Optional[Table]:
        """Get table by store_id and table_number"""
        return self.db.query(Table).filter(
            Table.store_id == store_id,
            Table.table_number == table_number
        ).first()
    
    def get_by_store(self, store_id: int) -> List[Table]:
        """Get all tables by store_id"""
        return self.db.query(Table).filter(Table.store_id == store_id).all()
    
    def get_by_status(self, store_id: int, status: TableStatus) -> List[Table]:
        """Get tables by store_id and status"""
        return self.db.query(Table).filter(
            Table.store_id == store_id,
            Table.status == status
        ).all()
