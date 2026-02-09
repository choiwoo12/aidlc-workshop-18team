"""
Order Number Generator - Unit 2: Customer Order Domain

주문 번호 생성 유틸리티입니다.
형식: T{테이블번호}-{순차번호} (예: T01-001, T01-002)
"""

from app.repositories.order_repository import OrderRepository


class OrderNumberGenerator:
    """주문 번호 생성기"""
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def generate(self, table_number: str) -> str:
        """
        주문 번호 생성
        
        Args:
            table_number: 테이블 번호 (예: "01", "02")
        
        Returns:
            주문 번호 (예: "T01-001")
        """
        # 테이블별 마지막 주문 조회
        last_order = self.order_repository.get_last_order_by_table_number(table_number)
        
        if last_order and last_order.order_number:
            # 마지막 주문 번호에서 순차 번호 추출
            try:
                last_seq = int(last_order.order_number.split('-')[1])
                next_seq = last_seq + 1
            except (IndexError, ValueError):
                # 파싱 실패 시 1부터 시작
                next_seq = 1
        else:
            # 첫 주문
            next_seq = 1
        
        # 주문 번호 생성 (T01-001 형식)
        order_number = f"T{table_number}-{next_seq:03d}"
        
        return order_number
