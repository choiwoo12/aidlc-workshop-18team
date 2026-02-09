"""
SSE Controller - Unit 2: Customer Order Domain

Server-Sent Events API 엔드포인트입니다.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.sse_service import sse_service


router = APIRouter(prefix="/api/sse", tags=["sse"])


@router.get("/orders/{table_id}")
async def sse_orders(table_id: int):
    """
    주문 상태 실시간 업데이트 SSE 연결
    
    Args:
        table_id: 테이블 ID
    
    Returns:
        SSE 스트림
    """
    return StreamingResponse(
        sse_service.event_generator(table_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Nginx 버퍼링 비활성화
        }
    )
