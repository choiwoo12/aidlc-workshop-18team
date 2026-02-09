/**
 * Cart Service - Unit 2: Customer Order Domain
 * 
 * 장바구니 관리 서비스 (SessionStorage 기반)
 */

import { v4 as uuidv4 } from 'uuid';

class CartService {
  constructor() {
    this.storageKey = 'cart';
  }

  /**
   * SessionStorage에서 장바구니 로드
   * @returns {Object} 장바구니 데이터
   */
  loadCart() {
    try {
      const saved = sessionStorage.getItem(this.storageKey);
      return saved ? JSON.parse(saved) : { items: [], total: 0 };
    } catch (error) {
      console.error('Failed to load cart from storage:', error);
      // JSON.parse 실패 시 빈 장바구니로 초기화
      return { items: [], total: 0 };
    }
  }

  /**
   * SessionStorage에 장바구니 저장
   * @param {Object} cart - 장바구니 데이터
   */
  saveCart(cart) {
    try {
      sessionStorage.setItem(this.storageKey, JSON.stringify(cart));
    } catch (error) {
      console.error('Failed to save cart to storage:', error);
      // JSON.stringify 실패 시 빈 장바구니로 초기화
      const emptyCart = { items: [], total: 0 };
      sessionStorage.setItem(this.storageKey, JSON.stringify(emptyCart));
    }
  }

  /**
   * 장바구니에 항목 추가
   * @param {Object} cart - 현재 장바구니
   * @param {Object} menu - 메뉴 정보
   * @param {Array} selectedOptions - 선택된 옵션
   * @param {number} quantity - 수량
   * @returns {Object} 업데이트된 장바구니
   */
  addItem(cart, menu, selectedOptions = [], quantity = 1) {
    // 중복 항목 확인 (옵션 순서 무관)
    const existingItem = this.findDuplicateItem(cart.items, menu.id, selectedOptions);

    if (existingItem) {
      // 수량 증가
      existingItem.quantity += quantity;
      existingItem.subtotal = this.calculateSubtotal(
        existingItem.menu_snapshot.price,
        existingItem.selected_options,
        existingItem.quantity
      );
    } else {
      // 새 항목 추가
      const newItem = {
        cart_item_id: uuidv4(),
        menu_id: menu.id,
        menu_snapshot: {
          name: menu.name,
          price: menu.price,
          image_url: menu.image_url
        },
        selected_options: selectedOptions,
        quantity: quantity,
        subtotal: this.calculateSubtotal(menu.price, selectedOptions, quantity)
      };
      cart.items.push(newItem);
    }

    // 총액 업데이트
    cart.total = this.calculateTotal(cart.items);
    
    // 저장
    this.saveCart(cart);
    
    return cart;
  }

  /**
   * 장바구니 항목 수량 업데이트
   * @param {Object} cart - 현재 장바구니
   * @param {string} cartItemId - 장바구니 항목 ID
   * @param {number} quantity - 새로운 수량
   * @returns {Object} 업데이트된 장바구니
   */
  updateQuantity(cart, cartItemId, quantity) {
    if (quantity <= 0) {
      // 수량이 0 이하면 항목 제거
      return this.removeItem(cart, cartItemId);
    }

    const item = cart.items.find(i => i.cart_item_id === cartItemId);
    if (item) {
      item.quantity = quantity;
      item.subtotal = this.calculateSubtotal(
        item.menu_snapshot.price,
        item.selected_options,
        item.quantity
      );
      
      // 총액 업데이트
      cart.total = this.calculateTotal(cart.items);
      
      // 저장
      this.saveCart(cart);
    }

    return cart;
  }

  /**
   * 장바구니 항목 제거
   * @param {Object} cart - 현재 장바구니
   * @param {string} cartItemId - 장바구니 항목 ID
   * @returns {Object} 업데이트된 장바구니
   */
  removeItem(cart, cartItemId) {
    cart.items = cart.items.filter(item => item.cart_item_id !== cartItemId);
    
    // 총액 업데이트
    cart.total = this.calculateTotal(cart.items);
    
    // 저장
    this.saveCart(cart);
    
    return cart;
  }

  /**
   * 장바구니 비우기
   * @returns {Object} 빈 장바구니
   */
  clearCart() {
    const emptyCart = { items: [], total: 0 };
    this.saveCart(emptyCart);
    return emptyCart;
  }

  /**
   * 중복 항목 찾기 (옵션 순서 무관)
   * @param {Array} items - 장바구니 항목 목록
   * @param {number} menuId - 메뉴 ID
   * @param {Array} selectedOptions - 선택된 옵션
   * @returns {Object|null} 중복 항목 또는 null
   */
  findDuplicateItem(items, menuId, selectedOptions) {
    return items.find(item => 
      item.menu_id === menuId && 
      this.isSameOptions(item.selected_options, selectedOptions)
    );
  }

  /**
   * 옵션 비교 (순서 무관)
   * @param {Array} options1 - 옵션 1
   * @param {Array} options2 - 옵션 2
   * @returns {boolean} 같은 옵션 여부
   */
  isSameOptions(options1, options2) {
    if (options1.length !== options2.length) {
      return false;
    }

    // 옵션 정렬 후 비교
    const sorted1 = this.sortOptions(options1);
    const sorted2 = this.sortOptions(options2);

    return JSON.stringify(sorted1) === JSON.stringify(sorted2);
  }

  /**
   * 옵션 정렬 (그룹 ID, 선택 ID 순)
   * @param {Array} options - 옵션 목록
   * @returns {Array} 정렬된 옵션
   */
  sortOptions(options) {
    return options.slice().sort((a, b) => {
      if (a.group_id !== b.group_id) {
        return a.group_id.localeCompare(b.group_id);
      }
      return a.choice_id.localeCompare(b.choice_id);
    });
  }

  /**
   * 항목 소계 계산
   * @param {number} menuPrice - 메뉴 가격
   * @param {Array} selectedOptions - 선택된 옵션
   * @param {number} quantity - 수량
   * @returns {number} 소계
   */
  calculateSubtotal(menuPrice, selectedOptions, quantity) {
    const optionPrice = selectedOptions.reduce(
      (sum, opt) => sum + (opt.price_adjustment || 0),
      0
    );
    return (menuPrice + optionPrice) * quantity;
  }

  /**
   * 장바구니 총액 계산
   * @param {Array} items - 장바구니 항목 목록
   * @returns {number} 총액
   */
  calculateTotal(items) {
    return items.reduce((sum, item) => sum + item.subtotal, 0);
  }
}

export default new CartService();
