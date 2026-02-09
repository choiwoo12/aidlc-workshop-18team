"""
Menu Controller - Unit 2: Customer Order Domain

메뉴 조회 API 엔드포인트입니다.
"""

from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.models.menu import Menu
from app.services.menu_service import MenuService
from app.repositories.menu_repository import MenuRepository
from app.utils.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/menus", tags=["menus"])


def get_menu_service(db: Session = Depends(get_db)) -> MenuService:
    """MenuService 의존성 주입"""
    menu_repository = MenuRepository(db)
    return MenuService(menu_repository)


@router.get("", response_model=List[dict])
async def get_menus(
    store_id: int = Query(1, description="매장 ID"),
    category: Optional[str] = Query(None, description="카테고리 필터"),
    menu_service: MenuService = Depends(get_menu_service)
):
    """
    판매 가능한 메뉴 목록 조회
    
    Args:
        store_id: 매장 ID (기본값: 1)
        category: 카테고리 필터 (선택사항)
    
    Returns:
        메뉴 목록
    """
    menus = menu_service.get_available_menus(store_id, category)
    
    return [
        {
            "id": menu.id,
            "name": menu.name,
            "description": menu.description,
            "price": menu.price,
            "category_level1": menu.category_level1,
            "category_level2": menu.category_level2,
            "image_url": menu.image_url,
            "options": menu.options,
            "is_available": menu.is_available
        }
        for menu in menus
    ]


@router.get("/{menu_id}", response_model=dict)
async def get_menu(
    menu_id: int,
    menu_service: MenuService = Depends(get_menu_service)
):
    """
    메뉴 상세 조회
    
    Args:
        menu_id: 메뉴 ID
    
    Returns:
        메뉴 상세 정보
    """
    menu = menu_service.get_menu_by_id(menu_id)
    
    if not menu:
        return {"error": "메뉴를 찾을 수 없습니다."}, 404
    
    return {
        "id": menu.id,
        "name": menu.name,
        "description": menu.description,
        "price": menu.price,
        "category_level1": menu.category_level1,
        "category_level2": menu.category_level2,
        "image_url": menu.image_url,
        "options": menu.options,
        "is_available": menu.is_available
    }


@router.get("/categories", response_model=List[str])
async def get_categories(
    store_id: int = Query(1, description="매장 ID"),
    menu_service: MenuService = Depends(get_menu_service)
):
    """
    카테고리 목록 조회
    
    Args:
        store_id: 매장 ID (기본값: 1)
    
    Returns:
        카테고리 목록
    """
    return menu_service.get_categories(store_id)
