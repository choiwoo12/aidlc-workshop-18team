"""
Menu Service - Unit 2: Customer Order Domain

Menu query business logic
"""

from typing import List, Optional
from app.models.menu import Menu
from app.repositories.menu_repository import MenuRepository


class MenuService:
    """Menu service"""

    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository

    def get_available_menus(
        self,
        store_id: int,
        category: Optional[str] = None
    ) -> List[Menu]:
        """
        Get available menus

        Args:
            store_id: Store ID
            category: Category filter (optional)

        Returns:
            List of available menus
        """
        menus = self.menu_repository.get_by_store(store_id)

        # Filter available menus only
        available_menus = [menu for menu in menus if menu.is_available]

        # Filter by category
        if category:
            available_menus = [
                menu for menu in available_menus
                if menu.category_level1 == category or menu.category_level2 == category
            ]

        return available_menus

    def get_menu_by_id(self, menu_id: int) -> Optional[Menu]:
        """
        Get menu by ID

        Args:
            menu_id: Menu ID

        Returns:
            Menu object or None
        """
        return self.menu_repository.get_by_id(menu_id)

    def get_categories(self, store_id: int) -> List[str]:
        """
        Get category list

        Args:
            store_id: Store ID

        Returns:
            List of categories (deduplicated)
        """
        menus = self.menu_repository.get_by_store(store_id)
        categories = set()

        for menu in menus:
            if menu.category_level1:
                categories.add(menu.category_level1)
            if menu.category_level2:
                categories.add(menu.category_level2)

        return sorted(list(categories))
