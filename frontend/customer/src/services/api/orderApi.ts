import { apiClient } from '../apiClient';
import type { Order } from '@/types';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

interface CreateOrderRequest {
  storeId: number;
  tableId: number;
  sessionId: string;
  items: Array<{
    menuId: number;
    quantity: number;
  }>;
}

export const orderApi = {
  createOrder: async (request: CreateOrderRequest): Promise<Order> => {
    const response = await apiClient.post<ApiResponse<Order>>(
      '/api/customer/orders',
      request
    );
    return response.data.data!;
  },

  getOrders: async (sessionId: string): Promise<Order[]> => {
    const response = await apiClient.get<ApiResponse<Order[]>>(
      `/api/customer/orders?sessionId=${sessionId}`
    );
    return response.data.data || [];
  },
};
