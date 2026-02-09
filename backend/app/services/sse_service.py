"""
SSE Service - Unit 2: Customer Order Domain

Server-Sent Events를 통한 실시간 주문 상태 업데이트 서비스입니다.
"""

import asyncio
import json
from typing import Dict, List, AsyncGenerator
from collections import defaultdict


class SSEService:
    """SSE 이벤트 생성 및 브로드캐스트 서비스"""

    def __init__(self):
        # table_id -> list of queues
        self.connections: Dict[int, List[asyncio.Queue]] = defaultdict(list)

    async def event_generator(self, table_id: int) -> AsyncGenerator[str, None]:
        """
        SSE 이벤트 생성기

        Args:
            table_id: 테이블 ID

        Yields:
            SSE 형식의 이벤트 문자열
        """
        queue = asyncio.Queue()

        # 연결 등록
        self.connections[table_id].append(queue)

        try:
            while True:
                # Keep-alive 메시지 (30초마다)
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    # 이벤트 전송
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive 메시지 (빈 메시지)
                    yield ":\n\n"
        except asyncio.CancelledError:
            # 연결 종료 처리
            pass
        finally:
            # 연결 제거
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
        주문 상태 변경 이벤트 브로드캐스트

        Args:
            table_id: 테이블 ID
            order_id: 주문 ID
            order_number: 주문 번호
            old_status: 이전 상태
            new_status: 새로운 상태
        """
        event = {
            "type": "order_status_changed",
            "order_id": order_id,
            "order_number": order_number,
            "old_status": old_status,
            "new_status": new_status
        }

        # 해당 테이블의 모든 연결에 이벤트 전송
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
        주문 생성 이벤트 브로드캐스트

        Args:
            table_id: 테이블 ID
            order_id: 주문 ID
            order_number: 주문 번호
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
        테이블별 연결 수 조회

        Args:
            table_id: 테이블 ID

        Returns:
            연결 수
        """
        return len(self.connections.get(table_id, []))


# 싱글톤 인스턴스
sse_service = SSEService()
