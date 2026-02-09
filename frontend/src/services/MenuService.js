/**
 * Menu Service - Unit 2: Customer Order Domain
 * 
 * 메뉴 조회 API 호출 서비스
 */

import axios from '../utils/axios';

class MenuService {
  /**
   * 판매 가능한 메뉴 목록 조회
   * @param {number} storeId - 매장 ID
   * @param {string} category - 카테고리 필터 (선택)
   * @returns {Promise<Array>} 메뉴 목록
   */
  async getMenus(storeId = 1, category = null) {
    try {
      const params = { store_id: storeId };
      if (category) {
        params.category = category;
      }
      
      const response = await axios.get('/api/menus', { params });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch menus:', error);
      throw error;
    }
  }

  /**
   * 메뉴 상세 조회
   * @param {number} menuId - 메뉴 ID
   * @returns {Promise<Object>} 메뉴 상세 정보
   */
  async getMenuById(menuId) {
    try {
      const response = await axios.get(`/api/menus/${menuId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch menu:', error);
      throw error;
    }
  }

  /**
   * 카테고리 목록 조회
   * @param {number} storeId - 매장 ID
   * @returns {Promise<Array>} 카테고리 목록
   */
  async getCategories(storeId = 1) {
    try {
      const response = await axios.get('/api/menus/categories', {
        params: { store_id: storeId }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch categories:', error);
      throw error;
    }
  }
}

export default new MenuService();
