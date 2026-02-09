"""
Authentication API Controller
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.app.utils.database import get_db
from backend.app.services.admin_auth_service import AdminAuthService
from backend.app.services.table_auth_service import TableAuthService
from backend.app.utils.exceptions import AuthenticationError

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# Request/Response Models
class AdminLoginRequest(BaseModel):
    username: str
    password: str


class TableLoginRequest(BaseModel):
    store_id: int
    table_number: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/admin/login", response_model=LoginResponse)
async def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Admin login endpoint
    
    Args:
        request: Login credentials
        db: Database session
        
    Returns:
        Access token
    """
    try:
        service = AdminAuthService(db)
        result = service.login(request.username, request.password)
        return result
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/table/login", response_model=LoginResponse)
async def table_login(
    request: TableLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Table auto-login endpoint
    
    Args:
        request: Table credentials
        db: Database session
        
    Returns:
        Access token
    """
    try:
        service = TableAuthService(db)
        result = service.login(request.store_id, request.table_number)
        return result
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
