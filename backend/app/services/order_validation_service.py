"""
Order Validation Service - Unit 2: Customer Order Domain

ì£¼ë¬¸ ?°ì´??? íš¨??ê²€ì¦??œë¹„?¤ì…?ˆë‹¤.
"""

from typing import List, Dict, Any
from app.repositories.menu_repository import MenuRepository
from app.utils.exceptions import ValidationError


class OrderValidationService:
    """ì£¼ë¬¸ ? íš¨??ê²€ì¦??œë¹„??""
    
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository
    
    def validate_order_items(self, cart_items: List[Dict[str, Any]]):
        """
        ì£¼ë¬¸ ??ª© ? íš¨??ê²€ì¦?
        
        Args:
            cart_items: ?¥ë°”êµ¬ë‹ˆ ??ª© ëª©ë¡
        
        Raises:
            ValidationError: ê²€ì¦??¤íŒ¨ ??
        """
        if not cart_items:
            raise ValidationError("?¥ë°”êµ¬ë‹ˆê°€ ë¹„ì–´?ˆìŠµ?ˆë‹¤.")
        
        for item in cart_items:
            self._validate_cart_item(item)
    
    def _validate_cart_item(self, item: Dict[str, Any]):
        """
        ê°œë³„ ?¥ë°”êµ¬ë‹ˆ ??ª© ê²€ì¦?
        
        Args:
            item: ?¥ë°”êµ¬ë‹ˆ ??ª©
        
        Raises:
            ValidationError: ê²€ì¦??¤íŒ¨ ??
        """
        # ?„ìˆ˜ ?„ë“œ ?•ì¸
        required_fields = ['menu_id', 'menu_snapshot', 'quantity', 'subtotal']
        for field in required_fields:
            if field not in item:
                raise ValidationError(f"?„ìˆ˜ ?„ë“œê°€ ?„ë½?˜ì—ˆ?µë‹ˆ?? {field}")
        
        # ë©”ë‰´ ì¡´ì¬ ?¬ë? ?•ì¸
        menu = self.menu_repository.get_by_id(item['menu_id'])
        if not menu:
            raise ValidationError("ë©”ë‰´ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤.")
        
        # ?ë§¤ ê°€???¬ë? ?•ì¸
        if not menu.is_available:
            raise ValidationError(
                f"{menu.name}?€(?? ?„ì¬ ?ë§¤?˜ì? ?ŠìŠµ?ˆë‹¤."
            )
        
        # ê°€ê²??¼ì¹˜ ?•ì¸
        menu_snapshot = item.get('menu_snapshot', {})
        snapshot_price = menu_snapshot.get('price')
        
        if snapshot_price is not None and snapshot_price != menu.price:
            raise ValidationError(
                "ë©”ë‰´ ê°€ê²©ì´ ë³€ê²½ë˜?ˆìŠµ?ˆë‹¤. ?¥ë°”êµ¬ë‹ˆë¥??¤ì‹œ ?•ì¸?´ì£¼?¸ìš”."
            )
        
        # ?˜ëŸ‰ ?•ì¸
        quantity = item.get('quantity', 0)
        if quantity < 1:
            raise ValidationError("?˜ëŸ‰?€ 1 ?´ìƒ?´ì–´???©ë‹ˆ??")
