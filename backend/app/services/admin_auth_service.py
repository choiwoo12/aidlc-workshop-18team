"""
Admin Authentication Service
"""
from sqlalchemy.orm import Session
from backend.app.repositories.store_repository import StoreRepository
from backend.app.utils.auth import verify_password
from backend.app.utils.jwt_manager import create_access_token
from backend.app.utils.exceptions import AuthenticationError


class AdminAuthService:
    """Admin authentication business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.store_repo = StoreRepository(db)
    
    def login(self, username: str, password: str) -> dict:
        """
        Admin login
        
        Args:
            username: Admin username
            password: Plain text password
            
        Returns:
            Dict with access_token and store_id
            
        Raises:
            AuthenticationError: If authentication fails
        """
        # Get store by admin username
        store = self.store_repo.get_by_admin_username(username)
        
        if not store:
            raise AuthenticationError("아이디 또는 비밀번호가 일치하지 않습니다")
        
        # Verify password
        if not verify_password(password, store.admin_password_hash):
            raise AuthenticationError("아이디 또는 비밀번호가 일치하지 않습니다")
        
        # Create JWT token
        token_data = {
            "store_id": store.id,
            "username": store.admin_username
        }
        access_token = create_access_token(token_data, "admin")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "store_id": store.id
        }
