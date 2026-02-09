# Customer Frontend - Implementation Guide

## Overview
Customer Frontend Core MVP 구현 가이드. TDD 방식으로 테스트 먼저 작성 후 구현.

---

## 구현 완료 항목

### ✅ 프로젝트 설정
- [x] package.json
- [x] vite.config.ts
- [x] tsconfig.json
- [x] .env.development
- [x] index.html

### ✅ Core Infrastructure
- [x] src/types/index.ts - TypeScript 타입 정의
- [x] src/utils/storage.ts - localStorage 래퍼 (TDD)
- [x] src/stores/useCartStore.ts - 장바구니 상태 관리 (TDD)
- [x] src/services/apiClient.ts - Axios 클라이언트
- [x] src/App.tsx - 기본 라우팅 구조
- [x] src/main.tsx - 엔트리 포인트

---

## 구현 필요 항목

### 1. API Services (High Priority)

#### src/services/api/menuApi.ts
```typescript
import { apiClient } from '../apiClient';
import type { ApiResponse, Menu } from '@/types';

export const menuApi = {
  getMenus: async (storeId: number): Promise<Menu[]> => {
    const response = await apiClient.get<ApiResponse<Menu[]>>(
      `/api/customer/menus?storeId=${storeId}`
    );
    return response.data.data || [];
  },
};
```

#### src/services/api/orderApi.ts
```typescript
import { apiClient } from '../apiClient';
import type { ApiResponse, Order, CreateOrderRequest } from '@/types';

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
```

---

### 2. Stores (High Priority)

#### src/stores/useMenuStore.ts
```typescript
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
```

#### src/stores/useOrderStore.ts
```typescript
import { create } from 'zustand';
import { orderApi } from '@/services/api/orderApi';
import type { Order, CreateOrderRequest } from '@/types';

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
```

---

### 3. Pages (High Priority)

#### src/pages/MenuPage.tsx
```typescript
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMenuStore } from '@/stores/useMenuStore';
import { useCartStore } from '@/stores/useCartStore';
import { toast } from 'react-toastify';

export function MenuPage() {
  const navigate = useNavigate();
  const { menus, isLoading, fetchMenus } = useMenuStore();
  const { addItem, getTotalItems } = useCartStore();

  useEffect(() => {
    fetchMenus(1); // storeId = 1
  }, []);

  const handleAddToCart = (menu: any, quantity: number) => {
    addItem(menu, quantity);
    toast.success('장바구니에 담았습니다');
  };

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  return (
    <div className="menu-page">
      <h1>메뉴</h1>
      <div className="menu-grid">
        {menus.map(menu => (
          <div key={menu.id} className="menu-card">
            <h3>{menu.name}</h3>
            <p>{menu.price}원</p>
            <button onClick={() => handleAddToCart(menu, 1)}>
              담기
            </button>
          </div>
        ))}
      </div>
      <button onClick={() => navigate('/cart')}>
        장바구니 ({getTotalItems()})
      </button>
    </div>
  );
}
```

#### src/pages/CartPage.tsx
```typescript
import { useNavigate } from 'react-router-dom';
import { useCartStore } from '@/stores/useCartStore';
import { useOrderStore } from '@/stores/useOrderStore';
import { getSessionId } from '@/utils/storage';
import { toast } from 'react-toastify';

export function CartPage() {
  const navigate = useNavigate();
  const { items, getTotalAmount, clearCart, removeItem } = useCartStore();
  const { createOrder } = useOrderStore();

  const handleCheckout = async () => {
    try {
      await createOrder({
        storeId: 1,
        tableId: 1,
        sessionId: getSessionId(),
        items: items.map(item => ({
          menuId: item.menuId,
          quantity: item.quantity,
        })),
      });
      
      clearCart();
      toast.success('주문이 완료되었습니다');
      navigate('/orders');
    } catch (error) {
      toast.error('주문 생성에 실패했습니다');
    }
  };

  if (items.length === 0) {
    return (
      <div className="empty-cart">
        <p>장바구니가 비어있습니다</p>
        <button onClick={() => navigate('/')}>
          메뉴 보러가기
        </button>
      </div>
    );
  }

  return (
    <div className="cart-page">
      <h1>장바구니</h1>
      <div className="cart-items">
        {items.map(item => (
          <div key={item.menuId} className="cart-item">
            <h3>{item.menuName}</h3>
            <p>{item.price}원 x {item.quantity}</p>
            <button onClick={() => removeItem(item.menuId)}>
              삭제
            </button>
          </div>
        ))}
      </div>
      <div className="cart-summary">
        <p>총액: {getTotalAmount()}원</p>
        <button onClick={handleCheckout}>주문하기</button>
      </div>
    </div>
  );
}
```

#### src/pages/OrderHistoryPage.tsx
```typescript
import { useEffect } from 'react';
import { useOrderStore } from '@/stores/useOrderStore';
import { getSessionId } from '@/utils/storage';

export function OrderHistoryPage() {
  const { orders, isLoading, fetchOrders } = useOrderStore();

  useEffect(() => {
    fetchOrders(getSessionId());
  }, []);

  if (isLoading) {
    return <div>로딩 중...</div>;
  }

  if (orders.length === 0) {
    return <div>주문 내역이 없습니다</div>;
  }

  return (
    <div className="order-history-page">
      <h1>주문 내역</h1>
      <div className="order-list">
        {orders.map(order => (
          <div key={order.id} className="order-card">
            <h3>{order.orderNumber}</h3>
            <p>상태: {order.status}</p>
            <p>총액: {order.totalAmount}원</p>
            <p>{new Date(order.createdAt).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

### 4. App.tsx 업데이트

```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import { MenuPage } from './pages/MenuPage';
import { CartPage } from './pages/CartPage';
import { OrderHistoryPage } from './pages/OrderHistoryPage';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Routes>
          <Route path="/" element={<MenuPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/orders" element={<OrderHistoryPage />} />
        </Routes>
        <ToastContainer position="top-center" autoClose={3000} />
      </div>
    </BrowserRouter>
  );
}

export default App;
```

---

## 실행 방법

### 1. 의존성 설치
```bash
cd frontend/customer
npm install
```

### 2. Backend 서버 실행 (별도 터미널)
```bash
cd backend
java -jar target/table-order-backend-1.0.0.jar
```

### 3. Frontend 개발 서버 실행
```bash
npm run dev
```

### 4. 브라우저에서 확인
```
http://localhost:5173
```

---

## 테스트 실행

```bash
# 모든 테스트
npm test

# Watch 모드
npm test -- --watch

# Coverage
npm test -- --coverage
```

---

## 다음 단계

### Medium Priority
- SSE 실시간 업데이트
- 에러 처리 개선
- 로딩 스켈레톤 UI

### Low Priority
- 애니메이션
- 이미지 최적화
- 성능 최적화

---

## Notes

- 현재 구현은 Core MVP (핵심 기능만)
- 스타일링은 최소한으로 구현
- 실제 프로덕션에서는 CSS Modules 또는 Tailwind 사용 권장
- 테스트 커버리지 목표: 80% 이상
