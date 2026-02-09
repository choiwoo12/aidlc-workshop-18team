# Customer Frontend - Data Models

## Overview
Customer Frontend의 데이터 모델 정의. TypeScript 인터페이스로 타입 안정성 확보.

---

## Domain Models

### Menu (메뉴)
```typescript
interface Menu {
  id: number;
  storeId: number;
  name: string;
  price: number;
  imageUrl: string | null;
  createdAt: string;
}
```

**설명**:
- Backend API 응답과 동일한 구조
- `imageUrl`은 nullable (이미지 없을 수 있음)
- `createdAt`은 ISO 8601 문자열

---

### CartItem (장바구니 항목)
```typescript
interface CartItem {
  menuId: number;
  menuName: string;
  price: number;
  quantity: number;
  imageUrl: string | null;
}
```

**설명**:
- 클라이언트 전용 모델 (로컬 상태)
- `menuName`, `price`, `imageUrl`은 Menu에서 복사
- `quantity`는 사용자가 선택한 수량

---

### Order (주문)
```typescript
interface Order {
  id: number;
  orderNumber: string;
  tableId: number;
  sessionId: string;
  status: OrderStatus;
  totalAmount: number;
  items: OrderItem[];
  createdAt: string;
}

type OrderStatus = 'PENDING' | 'CONFIRMED' | 'PREPARING' | 'READY' | 'COMPLETED' | 'CANCELLED';
```

**설명**:
- Backend API 응답과 동일한 구조
- `status`는 제한된 문자열 타입
- `items`는 OrderItem 배열

---

### OrderItem (주문 항목)
```typescript
interface OrderItem {
  id: number;
  menuId: number;
  menuName: string;
  quantity: number;
  unitPrice: number;
  subtotal: number;
}
```

**설명**:
- Backend API 응답과 동일한 구조
- `subtotal = unitPrice * quantity`

---

## API Request/Response Models

### CreateOrderRequest
```typescript
interface CreateOrderRequest {
  storeId: number;
  tableId: number;
  sessionId: string;
  items: OrderItemRequest[];
}

interface OrderItemRequest {
  menuId: number;
  quantity: number;
}
```

**설명**:
- POST /api/customer/orders 요청 바디
- CartItem을 OrderItemRequest로 변환 필요

---

### ApiResponse
```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  message: string | null;
  error: string | null;
  timestamp: string;
}
```

**설명**:
- Backend의 표준 응답 래퍼
- 제네릭 타입으로 다양한 데이터 타입 지원

---

## Store State Models

### CartStore State
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

**설명**:
- Zustand store 상태 및 액션
- 장바구니 CRUD 작업

---

### OrderStore State
```typescript
interface OrderState {
  orders: Order[];
  currentOrder: Order | null;
  isLoading: boolean;
  error: string | null;
  fetchOrders: (sessionId: string) => Promise<void>;
  createOrder: (request: CreateOrderRequest) => Promise<Order>;
  subscribeToOrderUpdates: (sessionId: string) => void;
  unsubscribeFromOrderUpdates: () => void;
}
```

**설명**:
- Zustand store 상태 및 액션
- 주문 조회, 생성, SSE 구독

---

### MenuStore State
```typescript
interface MenuState {
  menus: Menu[];
  isLoading: boolean;
  error: string | null;
  fetchMenus: (storeId: number) => Promise<void>;
}
```

**설명**:
- Zustand store 상태 및 액션
- 메뉴 조회

---

## SSE Event Models

### OrderStatusChangedEvent
```typescript
interface OrderStatusChangedEvent {
  orderId: number;
  orderNumber: string;
  status: OrderStatus;
  timestamp: string;
}
```

**설명**:
- SSE로 수신하는 주문 상태 변경 이벤트
- EventSource로 수신 후 파싱

---

## Validation Rules

### Menu
- `id`: 양수
- `price`: 0 이상
- `name`: 1자 이상

### CartItem
- `quantity`: 1 이상 99 이하

### CreateOrderRequest
- `items`: 최소 1개 이상
- `sessionId`: 빈 문자열 불가

---

## Notes

- 모든 날짜는 ISO 8601 문자열 형식
- 금액은 정수 (원 단위)
- nullable 필드는 `| null` 명시
- Backend API 응답 구조와 일치하도록 설계
