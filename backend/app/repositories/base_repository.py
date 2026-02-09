"""
Base Repository
"""
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session
from backend.app.utils.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base Repository with common CRUD operations
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get entity by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all entities with pagination"""
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def create(self, entity: ModelType) -> ModelType:
        """Create new entity"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity: ModelType) -> ModelType:
        """Update existing entity"""
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity: ModelType) -> None:
        """Delete entity"""
        self.db.delete(entity)
        self.db.commit()
    
    def count(self) -> int:
        """Count total entities"""
        return self.db.query(self.model).count()
