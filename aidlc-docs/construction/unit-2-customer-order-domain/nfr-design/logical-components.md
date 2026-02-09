# Logical Components - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 논리적 컴포넌트 정의입니다. NFR 설계 패턴을 논리적 컴포넌트로 통합하여 인프라 독립적인 설계를 제공합니다.

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ SSE Manager  │  │ Cart Manager │  │ Order Manager│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Menu Manager │  │ Validation   │  │ Error Handler│     │
│  └──────────────┘  │ Service      │  └──────────────┘     │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────────┐
│                     Backend Layer                           │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ SSE Service  │  │ Order Service│  │ Menu Service │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Validation   │  │ Order Number │                        │
│  │ Service      │  │ Generator    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  Data Layer (Unit 1)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Order Repo   │  │ Menu Repo    │  │ OrderItem    │     │
│  │              │  │              │  │ Repo         │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Frontend Components

### Component 1: SSE Connection Manager

**Purpose**: SSE 연결 생명주기 관리 및 자동 재연결

**Responsibilities**:
- SSE 연결 설정 및 종료
- 자동 재연결 (최대 3회)
- Keep-alive 메시지 수신
- 연결 상태 모니터링

**Interface**:
```typescript
interface ISSEConnectionManager {
  // 연결 설정
  connect(
    onMessage: (event: MessageEvent) => void,
    onError: (error: Error) => void
  ): void;
  
  // 연결 종료
  disconnect(): void;
  
  // 연결 상태 확인
  isConnected(): boolean;
  
  // 재연결 시도 횟수
  getReconnectAttempts(): number;
}
```

**Dependencies**:
- Browser EventSource API
- Error Handler

**Configuration**:
```javascript
{
  maxReconnectAttempts: 3,
  reconnectDelays: [0, 5000, 10000], // ms
  keepAliveInterval: 30000 // ms
}
```

---

### Component 2: Cart Manager

**Purpose**: 장바구니 상태 관리 및 영속성

**Responsibilities**:
- 장바구니 항목 추가/수정/삭제
- 중복 항목 처리 (옵션 순서 무관 비교)
- SessionStorage 저장/복원
- 가격 계산 (소계, 총액)

**Interface**:
```typescript
interface ICartManager {
  // 항목 추가
  addItem(
    menu: Menu,
    selectedOptions: SelectedOption[],
    quantity: number
  ): void;
  
  // 항목 수정
  updateQuantity(cartItemId: string, quantity: number): void;
  
  // 항목 삭제
  removeItem(cartItemId: string): void;
  
  // 장바구니 비우기
  clear(): void;
  
  // 장바구니 조회
  getCart(): Cart;
  
  // 총액 계산
  calculateTotal(): number;
}
```

**Dependencies**:
- SessionStorage
- Validation Service
- Error Handler

**Data Structure**:
```typescript
interface Cart {
  items: CartItem[];
  total: number;
}

interface CartItem {
  cart_item_id: string;
  menu_id: number;
  menu_snapshot: {
    name: string;
    price: number;
    image_url: string;
  };
  selected_options: SelectedOption[];
  quantity: number;
  subtotal: number;
}
```

---

### Component 3: Order Manager

**Purpose**: 주문 생성 및 주문 내역 관리

**Responsibilities**:
- 주문 생성 (장바구니 → 주문)
- 주문 내역 조회
- SSE를 통한 주문 상태 실시간 업데이트
- 주문 상태 동기화

**Interface**:
```typescript
interface IOrderManager {
  // 주문 생성
  createOrder(cart: Cart): Promise<Order>;
  
  // 주문 내역 조회
  fetchOrders(): Promise<Order[]>;
  
  // 주문 상태 업데이트 (SSE 이벤트)
  updateOrderStatus(orderId: number, newStatus: string): void;
  
  // SSE 연결 초기화
  initializeSSE(): void;
  
  // SSE 연결 종료
  disconnectSSE(): void;
}
```

**Dependencies**:
- SSE Connection Manager
- Cart Manager
- HTTP Client (Axios)
- Error Handler

---

### Component 4: Menu Manager

**Purpose**: 메뉴 조회 및 필터링

**Responsibilities**:
- 메뉴 목록 조회
- 카테고리 필터링
- 메뉴 상세 조회
- 에러 처리 및 재시도

**Interface**:
```typescript
interface IMenuManager {
  // 메뉴 목록 조회
  fetchMenus(category?: string): Promise<Menu[]>;
  
  // 메뉴 상세 조회
  getMenuById(menuId: number): Promise<Menu>;
  
  // 카테고리 목록 조회
  getCategories(): Promise<string[]>;
  
  // 재시도
  retry(): Promise<Menu[]>;
}
```

**Dependencies**:
- HTTP Client (Axios)
- Error Handler

---

### Component 5: Validation Service

**Purpose**: 클라이언트 측 데이터 유효성 검증

**Responsibilities**:
- 필수 옵션 검증
- 장바구니 비어있지 않음 검증
- 수량 검증
- 입력 데이터 검증

**Interface**:
```typescript
interface IValidationService {
  // 필수 옵션 검증
  validateRequiredOptions(
    menu: Menu,
    selectedOptions: SelectedOption[]
  ): ValidationResult;
  
  // 장바구니 검증
  validateCart(cart: Cart): ValidationResult;
  
  // 수량 검증
  validateQuantity(quantity: number): ValidationResult;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
}
```

**Dependencies**: None (Pure function)

---

### Component 6: Error Handler

**Purpose**: 에러 처리 및 사용자 피드백

**Responsibilities**:
- API 에러 처리
- 에러 메시지 표시
- 재시도 전략 제공
- 에러 로깅

**Interface**:
```typescript
interface IErrorHandler {
  // API 에러 처리
  handleAPIError(error: Error, context: string): ErrorResult;
  
  // 메뉴 조회 에러 처리
  handleMenuFetchError(error: Error): ErrorResult;
  
  // 장바구니 에러 처리
  handleCartError(error: Error): Cart;
}

interface ErrorResult {
  success: boolean;
  message: string;
  showRetryButton?: boolean;
}
```

**Dependencies**:
- Toast/Modal UI Component

---

## Backend Components

### Component 7: SSE Service

**Purpose**: SSE 이벤트 생성 및 브로드캐스트

**Responsibilities**:
- SSE 연결 관리
- Keep-alive 메시지 전송 (30초마다)
- 주문 상태 변경 이벤트 브로드캐스트
- 연결 종료 처리

**Interface**:
```python
class ISSEService:
    def generate_events(self, table_id: int) -> AsyncGenerator:
        """SSE 이벤트 생성기"""
        pass
    
    def broadcast_order_status_change(
        self, 
        table_id: int, 
        order_id: int, 
        old_status: str, 
        new_status: str
    ):
        """주문 상태 변경 이벤트 브로드캐스트"""
        pass
    
    def send_keep_alive(self, table_id: int):
        """Keep-alive 메시지 전송"""
        pass
```

**Dependencies**:
- FastAPI StreamingResponse
- asyncio

**Configuration**:
```python
{
    'keep_alive_interval': 30,  # seconds
    'connection_timeout': 60,   # seconds
}
```

---

### Component 8: Order Service

**Purpose**: 주문 생성 및 관리 비즈니스 로직

**Responsibilities**:
- 주문 생성 (장바구니 → Order + OrderItem)
- 주문 내역 조회
- 주문 상태 변경
- 주문 번호 생성

**Interface**:
```python
class IOrderService:
    def create_order(
        self, 
        table_id: int, 
        cart_items: List[CartItemRequest]
    ) -> Order:
        """주문 생성"""
        pass
    
    def get_orders_by_table(
        self, 
        table_id: int, 
        session_id: str
    ) -> List[Order]:
        """테이블별 주문 내역 조회"""
        pass
    
    def update_order_status(
        self, 
        order_id: int, 
        new_status: str
    ) -> Order:
        """주문 상태 변경"""
        pass
```

**Dependencies**:
- Order Repository (Unit 1)
- OrderItem Repository (Unit 1)
- Order Number Generator
- Validation Service
- SSE Service

---

### Component 9: Menu Service

**Purpose**: 메뉴 조회 비즈니스 로직

**Responsibilities**:
- 판매 가능한 메뉴 조회
- 카테고리 필터링
- 메뉴 상세 조회

**Interface**:
```python
class IMenuService:
    def get_available_menus(
        self, 
        store_id: int, 
        category: str = None
    ) -> List[Menu]:
        """판매 가능한 메뉴 조회"""
        pass
    
    def get_menu_by_id(self, menu_id: int) -> Menu:
        """메뉴 상세 조회"""
        pass
    
    def get_categories(self, store_id: int) -> List[str]:
        """카테고리 목록 조회"""
        pass
```

**Dependencies**:
- Menu Repository (Unit 1)

---

### Component 10: Validation Service

**Purpose**: 서버 측 데이터 유효성 검증

**Responsibilities**:
- 주문 항목 유효성 검증
- 메뉴 판매 가능 여부 확인
- 가격 일치 확인
- 옵션 유효성 확인

**Interface**:
```python
class IValidationService:
    def validate_order_items(
        self, 
        cart_items: List[CartItemRequest]
    ):
        """주문 항목 유효성 검증"""
        pass
    
    def validate_menu_availability(self, menu_id: int) -> bool:
        """메뉴 판매 가능 여부 확인"""
        pass
    
    def validate_price_match(
        self, 
        menu_id: int, 
        snapshot_price: float
    ) -> bool:
        """가격 일치 확인"""
        pass
    
    def validate_options(
        self, 
        menu: Menu, 
        selected_options: List[SelectedOption]
    ):
        """옵션 유효성 확인"""
        pass
```

**Dependencies**:
- Menu Repository (Unit 1)

---

### Component 11: Order Number Generator

**Purpose**: 주문 번호 생성

**Responsibilities**:
- 테이블별 순차 번호 생성
- 주문 번호 형식 생성 (T{테이블번호}-{순차번호})
- AUTO_INCREMENT 활용

**Interface**:
```python
class IOrderNumberGenerator:
    def generate(self, table_number: str) -> str:
        """주문 번호 생성"""
        pass
    
    def get_next_sequence(self, table_number: str) -> int:
        """다음 순차 번호 조회"""
        pass
```

**Dependencies**:
- Order Repository (Unit 1)

---

## Component Dependencies

### Frontend Component Dependencies

```
SSE Connection Manager
  └─> Error Handler

Cart Manager
  ├─> Validation Service
  ├─> Error Handler
  └─> SessionStorage

Order Manager
  ├─> SSE Connection Manager
  ├─> Cart Manager
  ├─> HTTP Client
  └─> Error Handler

Menu Manager
  ├─> HTTP Client
  └─> Error Handler

Validation Service
  └─> (No dependencies)

Error Handler
  └─> Toast/Modal UI
```

### Backend Component Dependencies

```
SSE Service
  └─> FastAPI StreamingResponse

Order Service
  ├─> Order Repository (Unit 1)
  ├─> OrderItem Repository (Unit 1)
  ├─> Order Number Generator
  ├─> Validation Service
  └─> SSE Service

Menu Service
  └─> Menu Repository (Unit 1)

Validation Service
  └─> Menu Repository (Unit 1)

Order Number Generator
  └─> Order Repository (Unit 1)
```

---

## Component Interaction Flows

### Flow 1: 주문 생성 플로우

```
[고객 UI]
    ↓ (주문하기 버튼 클릭)
[Cart Manager] → validateCart()
    ↓ (장바구니 데이터)
[Order Manager] → createOrder()
    ↓ (HTTP POST /api/orders)
[Order Service] → validate_order_items()
    ↓
[Validation Service] → 메뉴/가격/옵션 검증
    ↓
[Order Number Generator] → generate()
    ↓
[Order Service] → Order + OrderItem 생성
    ↓
[Order Repository] → save()
    ↓
[SSE Service] → broadcast_order_created()
    ↓
[고객 UI] → 주문 번호 표시
    ↓
[Cart Manager] → clear()
```

### Flow 2: 실시간 주문 상태 업데이트 플로우

```
[관리자 UI]
    ↓ (주문 상태 변경)
[Admin Order Service] → update_order_status()
    ↓
[Order Repository] → update()
    ↓
[SSE Service] → broadcast_order_status_change()
    ↓ (SSE Event)
[SSE Connection Manager] → onMessage()
    ↓
[Order Manager] → updateOrderStatus()
    ↓
[고객 UI] → 주문 상태 업데이트
```

### Flow 3: 메뉴 조회 플로우

```
[고객 UI]
    ↓ (메뉴 페이지 접속)
[Menu Manager] → fetchMenus(category)
    ↓ (HTTP GET /api/menus)
[Menu Service] → get_available_menus()
    ↓
[Menu Repository] → find_by_category()
    ↓ (판매 가능 메뉴 필터링)
[Menu Service] → Menu[]
    ↓
[고객 UI] → 메뉴 카드 표시
```

---

## Configuration Management

### Frontend Configuration

```javascript
// config.js
export const config = {
  sse: {
    maxReconnectAttempts: 3,
    reconnectDelays: [0, 5000, 10000],
    keepAliveInterval: 30000,
  },
  cart: {
    storageKey: 'cart',
    maxItems: null, // 제한 없음
  },
  api: {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
    timeout: 10000,
  },
  error: {
    defaultMessage: '주문 생성에 실패했습니다. 다시 시도해주세요.',
  },
};
```

### Backend Configuration

```python
# config.py
class Settings(BaseSettings):
    # SSE Configuration
    SSE_KEEP_ALIVE_INTERVAL: int = 30
    SSE_CONNECTION_TIMEOUT: int = 60
    
    # Order Configuration
    ORDER_NUMBER_FORMAT: str = "T{table_number}-{sequence:03d}"
    
    # Performance Configuration
    MENU_QUERY_TIMEOUT: int = 1  # seconds
    ORDER_CREATE_TIMEOUT: int = 2  # seconds
    
    # Validation Configuration
    VALIDATE_MENU_AVAILABILITY: bool = True
    VALIDATE_PRICE_MATCH: bool = True
    VALIDATE_OPTIONS: bool = True
```

---

## Component Summary

| Component | Layer | Purpose | Complexity |
|-----------|-------|---------|------------|
| SSE Connection Manager | Frontend | SSE 연결 관리 | Medium |
| Cart Manager | Frontend | 장바구니 관리 | Medium |
| Order Manager | Frontend | 주문 관리 | Medium |
| Menu Manager | Frontend | 메뉴 조회 | Low |
| Validation Service (FE) | Frontend | 클라이언트 검증 | Low |
| Error Handler | Frontend | 에러 처리 | Low |
| SSE Service | Backend | SSE 이벤트 | Medium |
| Order Service | Backend | 주문 비즈니스 로직 | High |
| Menu Service | Backend | 메뉴 비즈니스 로직 | Low |
| Validation Service (BE) | Backend | 서버 검증 | Medium |
| Order Number Generator | Backend | 주문 번호 생성 | Low |

---

## Design Principles

1. **Single Responsibility**: 각 컴포넌트는 하나의 책임만 가짐
2. **Dependency Injection**: 의존성 주입으로 테스트 용이성 향상
3. **Interface Segregation**: 명확한 인터페이스 정의
4. **Infrastructure Independence**: 인프라 독립적인 설계
5. **Error Handling**: 모든 컴포넌트에서 에러 처리

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
