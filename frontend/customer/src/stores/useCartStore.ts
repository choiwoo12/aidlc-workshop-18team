import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CartItem, Menu } from '@/types';

interface CartState {
  items: CartItem[];
  addItem: (menu: Menu, quantity: number) => void;
  removeItem: (menuId: number) => void;
  updateQuantity: (menuId: number, quantity: number) => void;
  clearCart: () => void;
  getTotalAmount: () => number;
  getTotalItems: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (menu, quantity) => {
        const existingItem = get().items.find(item => item.menuId === menu.id);
        
        if (existingItem) {
          set({
            items: get().items.map(item =>
              item.menuId === menu.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          });
        } else {
          set({
            items: [
              ...get().items,
              {
                menuId: menu.id,
                menuName: menu.name,
                price: menu.price,
                quantity,
                imageUrl: menu.imageUrl,
              },
            ],
          });
        }
      },

      removeItem: (menuId) => {
        set({
          items: get().items.filter(item => item.menuId !== menuId),
        });
      },

      updateQuantity: (menuId, quantity) => {
        if (quantity <= 0) {
          get().removeItem(menuId);
          return;
        }

        set({
          items: get().items.map(item =>
            item.menuId === menuId ? { ...item, quantity } : item
          ),
        });
      },

      clearCart: () => {
        set({ items: [] });
      },

      getTotalAmount: () => {
        return get().items.reduce(
          (total, item) => total + item.price * item.quantity,
          0
        );
      },

      getTotalItems: () => {
        return get().items.reduce((total, item) => total + item.quantity, 0);
      },
    }),
    {
      name: 'cart-storage',
    }
  )
);
