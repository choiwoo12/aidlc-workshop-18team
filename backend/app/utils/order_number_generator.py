"""
Order Number Generator - Unit 2: Customer Order Domain

주문 번호 ?�성 ?�틸리티?�니??
?�식: T{?�이블번??-{?�차번호} (?? T01-001, T01-002)
"""

from app.repositories.order_repository import OrderRepository


class OrderNumberGenerator:
    """주문 번호 ?�성�?""
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def generate(self, table_number: str) -> str:
        """
        주문 번호 ?�성
        
        Args:
            table_number: ?�이�?번호 (?? "01", "02")
        
        Returns:
            주문 번호 (?? "T01-001")
        """
        # ?�이블별 마�?�?주문 조회
        last_order = self.order_repository.get_last_order_by_table_number(table_number)
        
        if last_order and last_order.order_number:
            # 마�?�?주문 번호?�서 ?�차 번호 추출
            try:
                last_seq = int(last_order.order_number.split('-')[1])
                next_seq = last_seq + 1
            except (IndexError, ValueError):
                # ?�싱 ?�패 ??1부???�작
                next_seq = 1
        else:
            # �?주문
            next_seq = 1
        
        # 주문 번호 ?�성 (T01-001 ?�식)
        order_number = f"T{table_number}-{next_seq:03d}"
        
        return order_number
