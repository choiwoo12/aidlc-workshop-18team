"""
Custom Exception Classes
"""


class AuthenticationError(Exception):
    """Authentication failed"""
    pass


class AuthorizationError(Exception):
    """Authorization failed (insufficient permissions)"""
    pass


class TokenExpiredError(Exception):
    """JWT token expired"""
    pass


class ValidationError(Exception):
    """Data validation failed"""
    pass


class BusinessRuleError(Exception):
    """Business rule violation"""
    pass


class ResourceNotFoundError(Exception):
    """Requested resource not found"""
    pass


class ConflictError(Exception):
    """Resource conflict (e.g., duplicate data)"""
    pass
