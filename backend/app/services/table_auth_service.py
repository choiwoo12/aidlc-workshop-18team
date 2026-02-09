"""
Table Authentication Service
"""
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.repositories.table_repository import TableRepository
from backend.app.models.table import TableStatus
from backend.app.utils.jwt_manager import create_access_token
from backend.app.utils.exceptions import AuthenticationError


class TableAuthService:
    """Table authentication business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.table_repo = TableRepository(db)
    
    def login(self, store_id: int, table_number: str) -> dict:
        """
        Table auto-login
        
        Args:
            store_id: Store ID
            table_number: Table number
            
        Returns:
            Dict with access_token and table_id
            
        Raises:
            AuthenticationError: If table not found
        """
        # Get table by table_number
        table = self.table_repo.get_by_table_number(store_id, table_number)
        
        if not table:
            raise AuthenticationError("존재하지 않는 테이블 번호입니다")
        
        # Update table status to IN_USE if AVAILABLE
        if table.status == TableStatus.AVAILABLE:
            table.status = TableStatus.IN_USE
            table.status_changed_at = datetime.utcnow()
            table.current_session_started_at = datetime.utcnow()
            
            # Add to status history
            if table.status_history is None:
                table.status_history = []
            
            table.status_history.append({
                "status": TableStatus.IN_USE.value,
                "timestamp": datetime.utcnow().isoformat(),
                "changed_by": "customer"
            })
            
            self.table_repo.update(table)
        
        # Create JWT token
        token_data = {
            "store_id": store_id,
            "table_id": table.id,
            "table_number": table.table_number
        }
        access_token = create_access_token(token_data, "table")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "table_id": table.id
        }
