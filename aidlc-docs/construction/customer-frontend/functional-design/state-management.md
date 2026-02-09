# Customer Frontend - State Management

## Overview
Zustand를 사용한 전역 상태 관리. 간단하고 직관적인 API로 React Context보다 효율적.

---

## Store Architecture

```
src/stores/
├── useCartStore.ts      # 장바구니 상태
├── useOrderStore.ts     # 주문 상태
└── useMenuStore.ts      # 메뉴 상태
```

---

## CartStore (장바구니)

### State Structure
```typescript
interface CartState {
  items: CartItem[];
  addItem: (menu: Menu, quantity: number) => void;
  removeItem: (menuId: number) => void;
  updateQuantity: (menuId: number, quantity: number) => void;
  clearCart: () => void;
  getTotalAmount: () => number;
  getTotalItems: () => number;
}
```

---

### Implementation
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (menu, quantity) => {
        const existingItem = get().items.find(item => item.menuId === menu.id);
        
        if (existingItem) {
          // 기존 항목 수량 증가
          set({
            items: get().items.map(item =>
              item.menuId === menu.id
                ? { ...item, quantity: item.quantity + quantity }
                : item
            ),
          });
        } else {
          // 새 항목 추가
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
      name: 'cart-storage', // localStorage key
    }
  )
);
```

---

### Usage Example
```typescript
import { useCartStore } from '@/stores/useCartStore';

function MenuCard({ menu }: MenuCardProps) {
  const addItem = useCartStore(state => state.addItem);
  const [quantity, setQuantity] = useState(1);

  const handleAddToCart = () => {
    addItem(menu, quantity);
    toast.success('장바구니에 담았습니다');
  };

  return (
    <div>
      <h3>{menu.name}</h3>
      <p>{menu.price}원</p>
      <input
        type="number"
        value={quantity}
        onChange={(e) => setQuantity(Number(e.target.value))}
      />
      <button onClick={handleAddToCart}>담기</button>
    </div>
  );
}
```

---

## OrderStore (주문)

### State Structure
```typescript
interface OrderState {
  orders: Order[];
  currentOrder: Order | null;
  isLoading: boolean;
  error: string | null;
  eventSource: EventSource | null;
  
  fetchOrders: (sessionId: string) => Promise<void>;
  createOrder: (request: CreateOrderRequest) => Promise<Order>;
  updateOrderStatus: (orderId: number, status: OrderStatus) => void;
  subscribeToOrderUpdates: (sessionId: string) => void;
  unsubscribeFromOrderUpdates: () => void;
}
```

---

### Implementation
```typescript
import { create } from 'zustand';
import { apiClient } from '@/services/apiClient';

export const useOrderStore = create<OrderState>((set, get) => ({
  orders: [],
  currentOrder: null,
  isLoading: false,
  error: null,
  eventSource: null,

  fetchOrders: async (sessionId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get<ApiResponse<Order[]>>(
        `/api/customer/orders?sessionId=${sessionId}`
      );
      set({ orders: response.data.data || [], isLoading: false });
    } catch (error) {
      set({ error: '주문 내역을 불러오지 못했습니다', isLoading: false });
    }
  },

  createOrder: async (request) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.post<ApiResponse<Order>>(
        '/api/customer/orders',
        request
      );
      const newOrder = response.data.data!;
      set({
        orders: [newOrder, ...get().orders],
        currentOrder: newOrder,
        isLoading: false,
      });
      return newOrder;
    } catch (error) {
      set({ error: '주문 생성에 실패했습니다', isLoading: false });
      throw error;
    }
  },

  updateOrderStatus: (orderId, status) => {
    set({
      orders: get().orders.map(order =>
        order.id === orderId ? { ...order, status } : order
      ),
    });
  },

  subscribeToOrderUpdates: (sessionId) => {
    const eventSource = new EventSource(
      `${import.meta.env.VITE_API_URL}/api/sse/subscribe?sessionId=${sessionId}`
    );

    eventSource.addEventListener('ORDER_STATUS_CHANGED', (event) => {
      const data: OrderStatusChangedEvent = JSON.parse(event.data);
      get().updateOrderStatus(data.orderId, data.status);
    });

    eventSource.onerror = () => {
      console.error('SSE connection error');
      eventSource.close();
    };

    set({ eventSource });
  },

  unsubscribeFromOrderUpdates: () => {
    const { eventSource } = get();
    if (eventSource) {
      eventSource.close();
      set({ eventSource: null });
    }
  },
}));
```

---

### Usage Example
```typescript
import { useOrderStore } from '@/stores/useOrderStore';
import { useEffect } from 'react';

function OrderHistoryPage() {
  const { orders, isLoading, fetchOrders, subscribeToOrderUpdates, unsubscribeFromOrderUpdates } = useOrderStore();
  const sessionId = getSessionId();

  useEffect(() => {
    fetchOrders(sessionId);
    subscribeToOrderUpdates(sessionId);

    return () => {
      unsubscribeFromOrderUpdates();
    };
  }, []);

  if (isLoading) return <div>로딩 중...</div>;

  return (
    <div>
      {orders.map(order => (
        <OrderCard key={order.id} order={order} />
      ))}
    </div>
  );
}
```

---

## MenuStore (메뉴)

### State Structure
```typescript
interface MenuState {
  menus: Menu[];
  isLoading: boolean;
  error: string | null;
  fetchMenus: (storeId: number) => Promise<void>;
}
```

---

### Implementation
```typescript
import { create } from 'zustand';
import { apiClient } from '@/services/apiClient';

export const useMenuStore = create<MenuState>((set) => ({
  menus: [],
  isLoading: false,
  error: null,

  fetchMenus: async (storeId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get<ApiResponse<Menu[]>>(
        `/api/customer/menus?storeId=${storeId}`
      );
      set({ menus: response.data.data || [], isLoading: false });
    } catch (error) {
      set({ error: '메뉴를 불러오지 못했습니다', isLoading: false });
    }
  },
}));
```

---

### Usage Example
```typescript
import { useMenuStore } from '@/stores/useMenuStore';
import { useEffect } from 'react';

function MenuPage() {
  const { menus, isLoading, fetchMenus } = useMenuStore();

  useEffect(() => {
    fetchMenus(1); // storeId = 1
  }, []);

  if (isLoading) return <div>로딩 중...</div>;

  return (
    <div>
      {menus.map(menu => (
        <MenuCard key={menu.id} menu={menu} />
      ))}
    </div>
  );
}
```

---

## State Persistence

### CartStore Persistence
- **Storage**: localStorage
- **Key**: `cart-storage`
- **이유**: 페이지 새로고침 시에도 장바구니 유지

### OrderStore Persistence
- **Storage**: 없음 (메모리만)
- **이유**: 항상 최신 데이터를 서버에서 가져옴

### MenuStore Persistence
- **Storage**: 없음 (메모리만)
- **이유**: 메뉴는 변경 가능하므로 항상 서버에서 가져옴

---

## Performance Optimization

### Selector Pattern
```typescript
// ❌ Bad: 전체 상태 구독
const cartStore = useCartStore();

// ✅ Good: 필요한 부분만 구독
const totalItems = useCartStore(state => state.getTotalItems());
const addItem = useCartStore(state => state.addItem);
```

**이유**: 불필요한 리렌더링 방지

---

### Shallow Comparison
```typescript
import { shallow } from 'zustand/shallow';

const { items, totalAmount } = useCartStore(
  state => ({ items: state.items, totalAmount: state.getTotalAmount() }),
  shallow
);
```

**이유**: 객체 비교 시 얕은 비교로 성능 향상

---

## Error Handling

### API Error
```typescript
try {
  await createOrder(request);
  toast.success('주문이 완료되었습니다');
  navigate('/orders');
} catch (error) {
  toast.error('주문에 실패했습니다');
}
```

### SSE Error
```typescript
eventSource.onerror = () => {
  console.error('실시간 업데이트 연결 실패');
  // 자동 재연결 로직 (선택)
  setTimeout(() => {
    subscribeToOrderUpdates(sessionId);
  }, 5000);
};
```

---

## Testing Strategy

### Unit Tests
```typescript
import { renderHook, act } from '@testing-library/react';
import { useCartStore } from '@/stores/useCartStore';

test('장바구니에 아이템 추가', () => {
  const { result } = renderHook(() => useCartStore());

  act(() => {
    result.current.addItem(mockMenu, 2);
  });

  expect(result.current.items).toHaveLength(1);
  expect(result.current.getTotalItems()).toBe(2);
});
```

---

## Notes

- Zustand는 Redux보다 간단하고 보일러플레이트 적음
- persist 미들웨어로 localStorage 자동 동기화
- SSE 연결은 컴포넌트 언마운트 시 정리 필수
- Selector 패턴으로 성능 최적화
