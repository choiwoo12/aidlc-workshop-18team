"""
SSE Controller - Unit 2: Customer Order Domain

Server-Sent Events API ?”ë“œ?¬ì¸?¸ì…?ˆë‹¤.
"""

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.sse_service import sse_service


router = APIRouter(prefix="/api/sse", tags=["sse"])


@router.get("/orders/{table_id}")
async def sse_orders(table_id: int):
    """
    ì£¼ë¬¸ ?íƒœ ?¤ì‹œê°??…ë°?´íŠ¸ SSE ?°ê²°
    
    Args:
        table_id: ?Œì´ë¸?ID
    
    Returns:
        SSE ?¤íŠ¸ë¦?
    """
    return StreamingResponse(
        sse_service.event_generator(table_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Nginx ë²„í¼ë§?ë¹„í™œ?±í™”
        }
    )
