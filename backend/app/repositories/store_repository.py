"""
Store Repository
"""
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.models.store import Store
from backend.app.repositories.base_repository import BaseRepository


class StoreRepository(BaseRepository[Store]):
    """Store data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Store, db)
    
    def get_by_admin_username(self, username: str) -> Optional[Store]:
        """Get store by admin username"""
        return self.db.query(Store).filter(Store.admin_username == username).first()
