"""
Error Handler Middleware
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    BusinessRuleError,
    ResourceNotFoundError,
    ConflictError
)
import logging

logger = logging.getLogger(__name__)


async def error_handler_middleware(request: Request, call_next):
    """
    Global error handler middleware
    """
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        return handle_exception(exc)


def handle_exception(exc: Exception) -> JSONResponse:
    """
    Handle exception and return appropriate JSON response

    Args:
        exc: Exception instance

    Returns:
        JSONResponse with error details
    """
    # Log error
    logger.error(f"Exception occurred: {type(exc).__name__}: {str(exc)}")

    # Authentication errors
    if isinstance(exc, AuthenticationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": {"code": 401, "message": str(exc) or "인증에 실패했습니다"}}
        )

    # Authorization errors
    if isinstance(exc, AuthorizationError):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": {"code": 403, "message": str(exc) or "권한이 없습니다"}}
        )

    # Resource not found errors
    if isinstance(exc, ResourceNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": {"code": 404, "message": str(exc) or "리소스를 찾을 수 없습니다"}}
        )

    # Conflict errors
    if isinstance(exc, ConflictError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"error": {"code": 409, "message": str(exc) or "데이터 충돌이 발생했습니다"}}
        )

    # Validation errors
    if isinstance(exc, (ValidationError, RequestValidationError)):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": {"code": 400, "message": str(exc) or "입력 데이터가 올바르지 않습니다"}}
        )

    # Business rule errors
    if isinstance(exc, BusinessRuleError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": {"code": 400, "message": str(exc)}}
        )

    # Generic server errors
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": 500, "message": "서버 오류가 발생했습니다"}}
    )
