import { create } from 'zustand';
import { orderApi } from '@/services/api/orderApi';
import type { Order } from '@/types';

interface CreateOrderRequest {
  storeId: number;
  tableId: number;
  sessionId: string;
  items: Array<{
    menuId: number;
    quantity: number;
  }>;
}

interface OrderState {
  orders: Order[];
  isLoading: boolean;
  error: string | null;
  fetchOrders: (sessionId: string) => Promise<void>;
  createOrder: (request: CreateOrderRequest) => Promise<Order>;
}

export const useOrderStore = create<OrderState>((set, get) => ({
  orders: [],
  isLoading: false,
  error: null,

  fetchOrders: async (sessionId) => {
    set({ isLoading: true, error: null });
    try {
      const orders = await orderApi.getOrders(sessionId);
      set({ orders, isLoading: false });
    } catch (error) {
      set({ error: '주문 내역을 불러오지 못했습니다', isLoading: false });
    }
  },

  createOrder: async (request) => {
    set({ isLoading: true, error: null });
    try {
      const newOrder = await orderApi.createOrder(request);
      set({
        orders: [newOrder, ...get().orders],
        isLoading: false,
      });
      return newOrder;
    } catch (error) {
      set({ error: '주문 생성에 실패했습니다', isLoading: false });
      throw error;
    }
  },
}));
