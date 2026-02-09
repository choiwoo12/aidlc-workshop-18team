/**
 * Order Service - Unit 2: Customer Order Domain
 * 
 * 주문 생성 및 조회 API 호출 서비스
 */

import axios from '../utils/axios';

class OrderService {
  /**
   * 주문 생성
   * @param {number} tableId - 테이블 ID
   * @param {Array} cartItems - 장바구니 항목 목록
   * @returns {Promise<Object>} 생성된 주문 정보
   */
  async createOrder(tableId, cartItems) {
    try {
      const response = await axios.post('/api/orders', {
        table_id: tableId,
        cart_items: cartItems
      });
      return response.data;
    } catch (error) {
      console.error('Failed to create order:', error);
      throw error;
    }
  }

  /**
   * 테이블별 주문 내역 조회
   * @param {number} tableId - 테이블 ID
   * @returns {Promise<Array>} 주문 목록
   */
  async getOrders(tableId) {
    try {
      const response = await axios.get('/api/orders', {
        params: { table_id: tableId }
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch orders:', error);
      throw error;
    }
  }

  /**
   * 주문 상세 조회
   * @param {number} orderId - 주문 ID
   * @returns {Promise<Object>} 주문 상세 정보
   */
  async getOrderById(orderId) {
    try {
      const response = await axios.get(`/api/orders/${orderId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch order:', error);
      throw error;
    }
  }
}

export default new OrderService();
