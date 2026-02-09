import { apiClient } from '../apiClient';
import type { Menu } from '@/types';

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export const menuApi = {
  getMenus: async (storeId: number): Promise<Menu[]> => {
    const response = await apiClient.get<ApiResponse<Menu[]>>(
      `/api/customer/menus?storeId=${storeId}`
    );
    return response.data.data || [];
  },
};
