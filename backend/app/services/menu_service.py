"""
Menu Service - Unit 2: Customer Order Domain

메뉴 조회 비즈?�스 로직???�당?�니??
"""

from typing import List, Optional
from app.models.menu import Menu
from app.repositories.menu_repository import MenuRepository


class MenuService:
    """메뉴 조회 ?�비??""
    
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository
    
    def get_available_menus(
        self, 
        store_id: int, 
        category: Optional[str] = None
    ) -> List[Menu]:
        """
        ?�매 가?�한 메뉴 조회
        
        Args:
            store_id: 매장 ID
            category: 카테고리 ?�터 (?�택?�항)
        
        Returns:
            ?�매 가?�한 메뉴 목록
        """
        menus = self.menu_repository.find_by_store(store_id)
        
        # ?�매 가?�한 메뉴�??�터�?
        available_menus = [menu for menu in menus if menu.is_available]
        
        # 카테고리 ?�터�?
        if category:
            available_menus = [
                menu for menu in available_menus
                if menu.category_level1 == category or menu.category_level2 == category
            ]
        
        return available_menus
    
    def get_menu_by_id(self, menu_id: int) -> Optional[Menu]:
        """
        메뉴 ?�세 조회
        
        Args:
            menu_id: 메뉴 ID
        
        Returns:
            메뉴 객체 ?�는 None
        """
        return self.menu_repository.get_by_id(menu_id)
    
    def get_categories(self, store_id: int) -> List[str]:
        """
        카테고리 목록 조회
        
        Args:
            store_id: 매장 ID
        
        Returns:
            카테고리 목록 (중복 ?�거)
        """
        menus = self.menu_repository.find_by_store(store_id)
        categories = set()
        
        for menu in menus:
            if menu.category_level1:
                categories.add(menu.category_level1)
            if menu.category_level2:
                categories.add(menu.category_level2)
        
        return sorted(list(categories))
