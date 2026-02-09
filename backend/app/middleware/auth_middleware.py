"""
Authentication Middleware
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from backend.app.utils.jwt_manager import decode_access_token, verify_token_type
from backend.app.utils.exceptions import AuthenticationError, AuthorizationError

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Get current user from JWT token
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


async def require_admin(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Require admin token
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Token payload
        
    Raises:
        HTTPException: If token is not admin type
    """
    payload = await get_current_user(credentials)
    
    if not verify_token_type(payload, "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    
    return payload


async def require_table(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Require table token
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Token payload
        
    Raises:
        HTTPException: If token is not table type
    """
    payload = await get_current_user(credentials)
    
    if not verify_token_type(payload, "table"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Table access required",
        )
    
    return payload
