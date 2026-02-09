"""
SSE Service - Unit 2: Customer Order Domain

Server-Sent Eventsë¥??µí•œ ?¤ì‹œê°?ì£¼ë¬¸ ?íƒœ ?…ë°?´íŠ¸ ?œë¹„?¤ì…?ˆë‹¤.
"""

import asyncio
import json
from typing import Dict, List, AsyncGenerator
from collections import defaultdict


class SSEService:
    """SSE ?´ë²¤???ì„± ë°?ë¸Œë¡œ?œìº?¤íŠ¸ ?œë¹„??""
    
    def __init__(self):
        # table_id -> list of queues
        self.connections: Dict[int, List[asyncio.Queue]] = defaultdict(list)
    
    async def event_generator(self, table_id: int) -> AsyncGenerator[str, None]:
        """
        SSE ?´ë²¤???ì„±ê¸?
        
        Args:
            table_id: ?Œì´ë¸?ID
        
        Yields:
            SSE ?•ì‹???´ë²¤??ë¬¸ì??
        """
        queue = asyncio.Queue()
        
        # ?°ê²° ?±ë¡
        self.connections[table_id].append(queue)
        
        try:
            while True:
                # Keep-alive ë©”ì‹œì§€ (30ì´ˆë§ˆ??
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    # ?´ë²¤???„ì†¡
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive ë©”ì‹œì§€ (ë¹?ë©”ì‹œì§€)
                    yield ":\n\n"
        except asyncio.CancelledError:
            # ?°ê²° ì¢…ë£Œ ???•ë¦¬
            pass
        finally:
            # ?°ê²° ?´ì œ
            if queue in self.connections[table_id]:
                self.connections[table_id].remove(queue)
            if not self.connections[table_id]:
                del self.connections[table_id]
    
    async def broadcast_order_status_change(
        self, 
        table_id: int, 
        order_id: int, 
        order_number: str,
        old_status: str, 
        new_status: str
    ):
        """
        ì£¼ë¬¸ ?íƒœ ë³€ê²??´ë²¤??ë¸Œë¡œ?œìº?¤íŠ¸
        
        Args:
            table_id: ?Œì´ë¸?ID
            order_id: ì£¼ë¬¸ ID
            order_number: ì£¼ë¬¸ ë²ˆí˜¸
            old_status: ?´ì „ ?íƒœ
            new_status: ?ˆë¡œ???íƒœ
        """
        event = {
            "type": "order_status_changed",
            "order_id": order_id,
            "order_number": order_number,
            "old_status": old_status,
            "new_status": new_status
        }
        
        # ?´ë‹¹ ?Œì´ë¸”ì˜ ëª¨ë“  ?°ê²°???´ë²¤???„ì†¡
        if table_id in self.connections:
            for queue in self.connections[table_id]:
                await queue.put(event)
    
    async def broadcast_order_created(
        self, 
        table_id: int, 
        order_id: int, 
        order_number: str
    ):
        """
        ì£¼ë¬¸ ?ì„± ?´ë²¤??ë¸Œë¡œ?œìº?¤íŠ¸
        
        Args:
            table_id: ?Œì´ë¸?ID
            order_id: ì£¼ë¬¸ ID
            order_number: ì£¼ë¬¸ ë²ˆí˜¸
        """
        event = {
            "type": "order_created",
            "order_id": order_id,
            "order_number": order_number
        }
        
        if table_id in self.connections:
            for queue in self.connections[table_id]:
                await queue.put(event)
    
    def get_connection_count(self, table_id: int) -> int:
        """
        ?Œì´ë¸”ë³„ ?°ê²° ??ì¡°íšŒ
        
        Args:
            table_id: ?Œì´ë¸?ID
        
        Returns:
            ?°ê²° ??
        """
        return len(self.connections.get(table_id, []))


# ?±ê????¸ìŠ¤?´ìŠ¤
sse_service = SSEService()
