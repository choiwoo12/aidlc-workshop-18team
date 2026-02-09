"""
JWT Token Manager
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.config import settings


def create_access_token(data: Dict[str, Any], token_type: str) -> str:
    """
    Create JWT access token
    
    Args:
        data: Token payload data
        token_type: Token type ("admin" or "table")
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    # Set expiry based on token type
    if token_type == "admin":
        expire = datetime.utcnow() + timedelta(seconds=settings.JWT_ADMIN_EXPIRY)
    elif token_type == "table":
        expire = datetime.utcnow() + timedelta(seconds=settings.JWT_TABLE_EXPIRY)
    else:
        raise ValueError(f"Invalid token type: {token_type}")
    
    to_encode.update({
        "type": token_type,
        "exp": expire,
        "iat": datetime.utcnow()
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode and verify JWT access token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def verify_token_type(token_payload: Dict[str, Any], expected_type: str) -> bool:
    """
    Verify token type matches expected type
    
    Args:
        token_payload: Decoded token payload
        expected_type: Expected token type ("admin" or "table")
        
    Returns:
        True if token type matches, False otherwise
    """
    return token_payload.get("type") == expected_type
