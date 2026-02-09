"""
Order Validation Service - Unit 2: Customer Order Domain

주문 아이템 유효성 검증 서비스입니다.
"""

from typing import List, Dict, Any
from app.repositories.menu_repository import MenuRepository
from app.utils.exceptions import ValidationError


class OrderValidationService:
    """주문 유효성 검증 서비스"""

    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def validate_order_items(self, cart_items: List[Dict[str, Any]]):
        """
        주문 아이템 유효성 검증

        Args:
            cart_items: 장바구니 아이템 목록

        Raises:
            ValidationError: 검증 실패 시
        """
        if not cart_items:
            raise ValidationError("장바구니가 비어있습니다.")

        for item in cart_items:
            self._validate_cart_item(item)

    def _validate_cart_item(self, item: Dict[str, Any]):
        """
        개별 장바구니 아이템 검증

        Args:
            item: 장바구니 아이템

        Raises:
            ValidationError: 검증 실패 시
        """
        # 필수 필드 확인
        required_fields = ['menu_id', 'menu_snapshot', 'quantity', 'subtotal']
        for field in required_fields:
            if field not in item:
                raise ValidationError(f"필수 필드가 누락되었습니다: {field}")

        # 메뉴 존재 여부 확인
        menu = self.menu_repository.get_by_id(item['menu_id'])
        if not menu:
            raise ValidationError("메뉴를 찾을 수 없습니다.")

        # 판매 가능 여부 확인
        if not menu.is_available:
            raise ValidationError(
                f"{menu.name}은(는) 현재 판매중이 아닙니다."
            )

        # 가격 일치 확인
        menu_snapshot = item.get('menu_snapshot', {})
        snapshot_price = menu_snapshot.get('price')

        if snapshot_price is not None and snapshot_price != menu.price:
            raise ValidationError(
                "메뉴 가격이 변경되었습니다. 장바구니를 다시 확인해주세요."
            )

        # 수량 확인
        quantity = item.get('quantity', 0)
        if quantity < 1:
            raise ValidationError("수량은 1 이상이어야 합니다.")
