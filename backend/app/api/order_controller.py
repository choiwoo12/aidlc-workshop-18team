"""
Order Controller - Unit 2: Customer Order Domain

주문 생성 및 조회 API 엔드포인트입니다.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from app.services.order_service import OrderService
from app.services.order_validation_service import OrderValidationService
from app.services.sse_service import sse_service
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.repositories.table_repository import TableRepository
from app.repositories.menu_repository import MenuRepository
from app.utils.order_number_generator import OrderNumberGenerator
from app.utils.database import get_db
from app.utils.exceptions import ValidationError
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/orders", tags=["orders"])


class CartItemRequest(BaseModel):
    """장바구니 아이템 요청 모델"""
    menu_id: int
    menu_snapshot: dict
    selected_options: List[dict] = []
    quantity: int
    subtotal: float


class OrderCreateRequest(BaseModel):
    """주문 생성 요청 모델"""
    table_id: int
    cart_items: List[CartItemRequest]


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    """OrderService 의존성 주입"""
    order_repository = OrderRepository(db)
    order_item_repository = OrderItemRepository(db)
    table_repository = TableRepository(db)
    menu_repository = MenuRepository(db)

    order_number_generator = OrderNumberGenerator(order_repository)
    validation_service = OrderValidationService(menu_repository)

    return OrderService(
        order_repository,
        order_item_repository,
        table_repository,
        order_number_generator,
        validation_service
    )


@router.post("", response_model=dict)
async def create_order(
    request: OrderCreateRequest,
    order_service: OrderService = Depends(get_order_service)
):
    """
    주문 생성

    Args:
        request: 주문 생성 요청

    Returns:
        생성된 주문 정보
    """
    try:
        # 장바구니 아이템을 dict로 변환
        cart_items = [item.dict() for item in request.cart_items]

        # 주문 생성
        order = order_service.create_order(request.table_id, cart_items)

        # SSE 이벤트 브로드캐스트
        await sse_service.broadcast_order_created(
            request.table_id,
            order.id,
            order.order_number
        )

        return {
            "id": order.id,
            "order_number": order.order_number,
            "table_id": order.table_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at.isoformat()
        }

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="주문 생성에 실패했습니다.")


@router.get("", response_model=List[dict])
async def get_orders(
    table_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    """
    테이블별 주문 이력 조회

    Args:
        table_id: 테이블 ID

    Returns:
        주문 목록
    """
    try:
        orders = order_service.get_orders_by_table(table_id)

        return [
            {
                "id": order.id,
                "order_number": order.order_number,
                "table_id": order.table_id,
                "status": order.status,
                "total_amount": order.total_amount,
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "id": item.id,
                        "menu_name": item.menu_name_snapshot,
                        "menu_price": item.menu_price_snapshot,
                        "selected_options": item.selected_options,
                        "quantity": item.quantity,
                        "subtotal": item.subtotal
                    }
                    for item in order.items
                ]
            }
            for order in orders
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail="주문 이력 조회에 실패했습니다.")


@router.get("/{order_id}", response_model=dict)
async def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    """
    주문 상세 조회

    Args:
        order_id: 주문 ID

    Returns:
        주문 상세 정보
    """
    try:
        order = order_service.get_order_by_id(order_id)

        return {
            "id": order.id,
            "order_number": order.order_number,
            "table_id": order.table_id,
            "status": order.status,
            "total_amount": order.total_amount,
            "created_at": order.created_at.isoformat(),
            "items": [
                {
                    "id": item.id,
                    "menu_name": item.menu_name_snapshot,
                    "menu_price": item.menu_price_snapshot,
                    "selected_options": item.selected_options,
                    "quantity": item.quantity,
                    "subtotal": item.subtotal
                }
                for item in order.items
            ]
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="주문 조회에 실패했습니다.")
