/**
 * Order Context - Unit 2: Customer Order Domain
 * 
 * 주문 내역 전역 상태 관리 및 SSE 연결 관리
 */

import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import OrderService from '../services/OrderService';
import SSEService from '../services/SSEService';

const OrderContext = createContext();

export function OrderProvider({ children }) {
  const { user, isTable } = useAuth();
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [sseConnected, setSseConnected] = useState(false);

  /**
   * 주문 목록 조회
   */
  const fetchOrders = useCallback(async () => {
    if (!isTable || !user?.tableId) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const orderList = await OrderService.getOrders(user.tableId);
      setOrders(orderList);
    } catch (err) {
      console.error('Failed to fetch orders:', err);
      setError('주문 내역을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, [isTable, user?.tableId]);

  /**
   * SSE 메시지 수신 핸들러
   */
  const handleSSEMessage = useCallback((event) => {
    if (event.type === 'order_status_changed') {
      // 주문 상태 변경 이벤트 수신
      setOrders((prevOrders) => 
        prevOrders.map((order) => 
          order.id === event.order_id
            ? { ...order, status: event.new_status }
            : order
        )
      );
    }
  }, []);

  /**
   * SSE 에러 핸들러
   */
  const handleSSEError = useCallback((err) => {
    console.error('SSE connection error:', err);
    setSseConnected(false);
    setError(err.message);
  }, []);

  /**
   * SSE 연결 초기화
   */
  useEffect(() => {
    if (!isTable || !user?.tableId) {
      return;
    }

    // 초기 주문 목록 조회
    fetchOrders();

    // SSE 연결 설정
    SSEService.connect(user.tableId, handleSSEMessage, handleSSEError);
    setSseConnected(true);

    // Cleanup: 컴포넌트 언마운트 시 SSE 연결 종료
    return () => {
      SSEService.disconnect();
      setSseConnected(false);
    };
  }, [isTable, user?.tableId, fetchOrders, handleSSEMessage, handleSSEError]);

  /**
   * 주문 생성
   */
  const createOrder = async (cartItems) => {
    if (!isTable || !user?.tableId) {
      throw new Error('테이블 로그인이 필요합니다.');
    }

    setLoading(true);
    setError(null);

    try {
      const newOrder = await OrderService.createOrder(user.tableId, cartItems);
      
      // 주문 목록에 추가
      setOrders((prevOrders) => [newOrder, ...prevOrders]);
      
      return newOrder;
    } catch (err) {
      console.error('Failed to create order:', err);
      setError('주문 생성에 실패했습니다.');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  /**
   * 주문 목록 새로고침 (재연결 시 사용)
   */
  const refreshOrders = useCallback(() => {
    fetchOrders();
  }, [fetchOrders]);

  const value = {
    orders,
    loading,
    error,
    sseConnected,
    createOrder,
    refreshOrders
  };

  return (
    <OrderContext.Provider value={value}>
      {children}
    </OrderContext.Provider>
  );
}

export function useOrder() {
  const context = useContext(OrderContext);
  if (!context) {
    throw new Error('useOrder must be used within an OrderProvider');
  }
  return context;
}
