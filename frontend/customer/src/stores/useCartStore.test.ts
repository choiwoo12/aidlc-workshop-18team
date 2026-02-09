import { describe, it, expect, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useCartStore } from './useCartStore';
import type { Menu } from '@/types';

describe('useCartStore', () => {
  const mockMenu: Menu = {
    id: 1,
    storeId: 1,
    name: '김치찌개',
    price: 8000,
    imageUrl: null,
    createdAt: '2024-01-01T00:00:00Z',
  };

  beforeEach(() => {
    const { result } = renderHook(() => useCartStore());
    act(() => {
      result.current.clearCart();
    });
  });

  it('should add item to cart', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].menuId).toBe(1);
    expect(result.current.items[0].quantity).toBe(2);
  });

  it('should increase quantity when adding existing item', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.addItem(mockMenu, 1);
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.items[0].quantity).toBe(3);
  });

  it('should remove item from cart', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.removeItem(1);
    });

    expect(result.current.items).toHaveLength(0);
  });

  it('should update item quantity', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.updateQuantity(1, 5);
    });

    expect(result.current.items[0].quantity).toBe(5);
  });

  it('should remove item when quantity is 0', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.updateQuantity(1, 0);
    });

    expect(result.current.items).toHaveLength(0);
  });

  it('should calculate total amount', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
    });

    expect(result.current.getTotalAmount()).toBe(16000);
  });

  it('should calculate total items', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.addItem({ ...mockMenu, id: 2 }, 3);
    });

    expect(result.current.getTotalItems()).toBe(5);
  });

  it('should clear cart', () => {
    const { result } = renderHook(() => useCartStore());

    act(() => {
      result.current.addItem(mockMenu, 2);
      result.current.clearCart();
    });

    expect(result.current.items).toHaveLength(0);
  });
});
