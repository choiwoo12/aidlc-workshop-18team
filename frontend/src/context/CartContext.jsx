/**
 * Cart Context - Unit 2: Customer Order Domain
 * 
 * 장바구니 전역 상태 관리
 */

import React, { createContext, useState, useEffect, useContext } from 'react';
import CartService from '../services/CartService';

const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState(() => CartService.loadCart());

  // SessionStorage에 자동 저장
  useEffect(() => {
    CartService.saveCart(cart);
  }, [cart]);

  /**
   * 장바구니에 항목 추가
   */
  const addItem = (menu, selectedOptions = [], quantity = 1) => {
    const updatedCart = CartService.addItem(cart, menu, selectedOptions, quantity);
    setCart({ ...updatedCart });
  };

  /**
   * 항목 수량 업데이트
   */
  const updateQuantity = (cartItemId, quantity) => {
    const updatedCart = CartService.updateQuantity(cart, cartItemId, quantity);
    setCart({ ...updatedCart });
  };

  /**
   * 항목 제거
   */
  const removeItem = (cartItemId) => {
    const updatedCart = CartService.removeItem(cart, cartItemId);
    setCart({ ...updatedCart });
  };

  /**
   * 장바구니 비우기
   */
  const clearCart = () => {
    const emptyCart = CartService.clearCart();
    setCart(emptyCart);
  };

  /**
   * 장바구니 항목 개수
   */
  const getItemCount = () => {
    return cart.items.reduce((sum, item) => sum + item.quantity, 0);
  };

  const value = {
    cart,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
    getItemCount
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}
