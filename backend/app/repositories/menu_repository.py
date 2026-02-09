"""
Menu Repository
"""
from typing import List
from sqlalchemy.orm import Session
from backend.app.models.menu import Menu
from backend.app.repositories.base_repository import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    """Menu data access layer"""
    
    def __init__(self, db: Session):
        super().__init__(Menu, db)
    
    def get_by_store(self, store_id: int) -> List[Menu]:
        """Get all menus by store_id"""
        return self.db.query(Menu).filter(Menu.store_id == store_id).all()
    
    def get_available_by_store(self, store_id: int) -> List[Menu]:
        """Get available menus by store_id"""
        return self.db.query(Menu).filter(
            Menu.store_id == store_id,
            Menu.is_available == True
        ).all()
    
    def get_by_category(self, store_id: int, category_level1: str) -> List[Menu]:
        """Get menus by store_id and category_level1"""
        return self.db.query(Menu).filter(
            Menu.store_id == store_id,
            Menu.category_level1 == category_level1
        ).all()
