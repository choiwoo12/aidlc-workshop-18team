"""
Order Service - Unit 2: Customer Order Domain

주문 ?�성 �?관�?비즈?�스 로직???�당?�니??
"""

from typing import List, Dict, Any
from datetime import datetime
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.table_repository import TableRepository
from app.utils.order_number_generator import OrderNumberGenerator
from app.services.order_validation_service import OrderValidationService
from app.utils.database import get_db


class OrderService:
    """주문 ?�비??""
    
    def __init__(
        self,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        table_repository: TableRepository,
        order_number_generator: OrderNumberGenerator,
        validation_service: OrderValidationService
    ):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository
        self.table_repository = table_repository
        self.order_number_generator = order_number_generator
        self.validation_service = validation_service
    
    def create_order(
        self, 
        table_id: int, 
        cart_items: List[Dict[str, Any]]
    ) -> Order:
        """
        주문 ?�성
        
        Args:
            table_id: ?�이�?ID
            cart_items: ?�바구니 ??�� 목록
        
        Returns:
            ?�성??주문 객체
        
        Raises:
            ValidationError: ?�효??검�??�패 ??
            ValueError: ?�이블을 찾을 ???�을 ??
        """
        # ?�효??검�?
        self.validation_service.validate_order_items(cart_items)
        
        # ?�이�?조회
        table = self.table_repository.get_by_id(table_id)
        if not table:
            raise ValueError("?�이블을 찾을 ???�습?�다.")
        
        # 주문 번호 ?�성
        order_number = self.order_number_generator.generate(table.table_number)
        
        # 총액 계산
        total_amount = sum(item['subtotal'] for item in cart_items)
        
        # Order ?�성
        order = Order(
            table_id=table_id,
            order_number=order_number,
            status='PENDING',
            total_amount=total_amount,
            created_at=datetime.utcnow()
        )
        order = self.order_repository.save(order)
        
        # OrderItem ?�성
        for item in cart_items:
            menu_snapshot = item.get('menu_snapshot', {})
            selected_options = item.get('selected_options', [])
            
            order_item = OrderItem(
                order_id=order.id,
                menu_id=item['menu_id'],
                menu_name_snapshot=menu_snapshot.get('name', ''),
                menu_price_snapshot=menu_snapshot.get('price', 0),
                selected_options=selected_options,
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            self.order_item_repository.save(order_item)
        
        return order
    
    def get_orders_by_table(self, table_id: int) -> List[Order]:
        """
        ?�이블별 주문 ?�역 조회
        
        Args:
            table_id: ?�이�?ID
        
        Returns:
            주문 목록 (?�간 ??��)
        """
        orders = self.order_repository.find_by_table(table_id)
        
        # ?�간 ??�� ?�렬 (최신 주문????
        orders.sort(key=lambda x: x.created_at, reverse=True)
        
        return orders
    
    def get_order_by_id(self, order_id: int) -> Order:
        """
        주문 ?�세 조회
        
        Args:
            order_id: 주문 ID
        
        Returns:
            주문 객체
        
        Raises:
            ValueError: 주문??찾을 ???�을 ??
        """
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError("주문??찾을 ???�습?�다.")
        return order
