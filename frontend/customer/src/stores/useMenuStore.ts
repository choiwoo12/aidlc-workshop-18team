import { create } from 'zustand';
import { menuApi } from '@/services/api/menuApi';
import type { Menu } from '@/types';

interface MenuState {
  menus: Menu[];
  isLoading: boolean;
  error: string | null;
  fetchMenus: (storeId: number) => Promise<void>;
}

export const useMenuStore = create<MenuState>((set) => ({
  menus: [],
  isLoading: false,
  error: null,

  fetchMenus: async (storeId) => {
    set({ isLoading: true, error: null });
    try {
      const menus = await menuApi.getMenus(storeId);
      set({ menus, isLoading: false });
    } catch (error) {
      set({ error: '메뉴를 불러오지 못했습니다', isLoading: false });
    }
  },
}));
