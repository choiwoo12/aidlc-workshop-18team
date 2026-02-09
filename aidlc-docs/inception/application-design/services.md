# Service Layer Design

## Service Layer Overview

서비스 레이어는 비즈니스 로직을 캡슐화하고 컴포넌트 간 오케스트레이션을 담당합니다.

---

## Frontend Services (React)

### 1. API Service Layer

#### AuthService
**Purpose**: 인증 관련 API 호출 추상화

**Responsibilities**:
- 관리자 로그인 API 호출
- 테이블 자동 로그인 API 호출
- JWT 토큰 저장 및 관리
- 인증 상태 확인

**Methods**:
```typescript
class AuthService {
  // 관리자 로그인
  async adminLogin(storeId: string, username: string, password: string): Promise<AuthToken>
  
  // 테이블 자동 로그인
  async tableAutoLogin(storeId: string, tableNumber: number, password: string): Promise<TableSession>
  
  // 토큰 저장
  saveToken(token: string): void
  
  // 토큰 조회
  getToken(): string | null
  
  // 로그아웃
  logout(): void
  
  // 인증 상태 확인
  isAuthenticated(): boolean
}
```

---

#### MenuService
**Purpose**: 메뉴 관련 API 호출 추상화

**Responsibilities**:
- 메뉴 조회 API 호출
- 메뉴 관리 API 호출 (관리자)

**Methods**:
```typescript
class MenuService {
  // 메뉴 목록 조회
  async getMenus(category?: string): Promise<Menu[]>
  
  // 메뉴 상세 조회
  async getMenuById(menuId: string): Promise<Menu>
  
  // 메뉴 생성 (관리자)
  async createMenu(menuData: MenuInput): Promise<Menu>
  
  // 메뉴 수정 (관리자)
  async updateMenu(menuId: string, menuData: MenuInput): Promise<Menu>
  
  // 메뉴 삭제 (관리자)
  async deleteMenu(menuId: string): Promise<void>
  
  // 이미지 업로드 (관리자)
  async uploadImage(file: File): Promise<string>
}
```

---

#### OrderService
**Purpose**: 주문 관련 API 호출 추상화

**Responsibilities**:
- 주문 생성 API 호출
- 주문 조회 API 호출
- 주문 관리 API 호출 (관리자)

**Methods**:
```typescript
class OrderService {
  // 주문 생성
  async createOrder(orderData: OrderInput): Promise<Order>
  
  // 주문 내역 조회
  async getOrders(tableId: string, sessionId: string): Promise<Order[]>
  
  // 주문 목록 조회 (관리자)
  async getActiveOrders(storeId: string): Promise<Order[]>
  
  // 주문 상태 변경 (관리자)
  async updateOrderStatus(orderId: string, status: OrderStatus): Promise<Order>
  
  // 주문 삭제 (관리자)
  async deleteOrder(orderId: string): Promise<void>
}
```

---

#### TableService
**Purpose**: 테이블 관련 API 호출 추상화

**Responsibilities**:
- 테이블 관리 API 호출 (관리자)

**Methods**:
```typescript
class TableService {
  // 테이블 초기 설정
  async setupTable(storeId: string, tableNumber: number, password: string): Promise<Table>
  
  // 테이블 세션 종료
  async completeTableSession(tableId: string): Promise<void>
  
  // 과거 주문 내역 조회
  async getOrderHistory(tableId: string, dateFilter?: DateRange): Promise<OrderHistory[]>
}
```

---

#### SSEService
**Purpose**: 실시간 통신 (SSE) 관리

**Responsibilities**:
- SSE 연결 생성 및 관리
- 실시간 이벤트 수신 및 처리
- 연결 상태 관리

**Methods**:
```typescript
class SSEService {
  // SSE 연결 초기화
  connect(storeId: string, onMessage: (event: OrderEvent) => void): void
  
  // SSE 연결 종료
  disconnect(): void
  
  // 연결 상태 확인
  isConnected(): boolean
  
  // 재연결
  reconnect(): void
}
```

---

### 2. State Management Services (Context API)

#### AuthContext
**Purpose**: 전역 인증 상태 관리

**State**:
```typescript
interface AuthState {
  isAuthenticated: boolean
  user: User | null
  token: string | null
}
```

**Actions**:
- `login(user, token)`: 로그인 처리
- `logout()`: 로그아웃 처리
- `updateUser(user)`: 사용자 정보 업데이트

---

#### CartContext
**Purpose**: 장바구니 상태 관리 (고객 UI)

**State**:
```typescript
interface CartState {
  items: CartItem[]
  totalAmount: number
}
```

**Actions**:
- `addItem(menu, quantity)`: 아이템 추가
- `removeItem(itemId)`: 아이템 제거
- `updateQuantity(itemId, quantity)`: 수량 변경
- `clearCart()`: 장바구니 비우기
- `loadFromStorage()`: SessionStorage에서 로드
- `saveToStorage()`: SessionStorage에 저장

---

### 3. Utility Services

#### StorageService
**Purpose**: 로컬 저장소 관리

**Methods**:
```typescript
class StorageService {
  // SessionStorage 저장
  setSessionItem(key: string, value: any): void
  
  // SessionStorage 조회
  getSessionItem(key: string): any
  
  // SessionStorage 삭제
  removeSessionItem(key: string): void
  
  // LocalStorage 저장
  setLocalItem(key: string, value: any): void
  
  // LocalStorage 조회
  getLocalItem(key: string): any
  
  // LocalStorage 삭제
  removeLocalItem(key: string): void
}
```

---

#### ValidationService
**Purpose**: 데이터 유효성 검증

**Methods**:
```typescript
class ValidationService {
  // 주문 데이터 검증
  validateOrder(orderData: OrderInput): ValidationResult
  
  // 메뉴 데이터 검증
  validateMenu(menuData: MenuInput): ValidationResult
  
  // 테이블 설정 검증
  validateTableSetup(tableNumber: number, password: string): ValidationResult
}
```

---

## Backend Services (Python - Application Layer)

### 1. Customer Services

#### MenuService
**Purpose**: 메뉴 조회 비즈니스 로직

**Orchestration**:
- MenuRepository와 상호작용
- 메뉴 데이터 변환 및 포맷팅

**Dependencies**:
- `MenuRepository`: 데이터 접근

---

#### OrderService
**Purpose**: 주문 관리 비즈니스 로직

**Orchestration**:
- OrderRepository, MenuRepository와 상호작용
- 주문 유효성 검증
- 주문 번호 생성
- SSEService를 통한 실시간 알림

**Dependencies**:
- `OrderRepository`: 주문 데이터 접근
- `MenuRepository`: 메뉴 정보 조회
- `TableRepository`: 테이블 세션 확인
- `SSEService`: 실시간 알림

---

### 2. Admin Services

#### AdminAuthService
**Purpose**: 관리자 인증 비즈니스 로직

**Orchestration**:
- StoreRepository와 상호작용
- 비밀번호 검증 (bcrypt)
- JWT 토큰 생성 및 검증

**Dependencies**:
- `StoreRepository`: 매장 정보 조회
- `bcrypt`: 비밀번호 해싱
- `jwt`: 토큰 생성/검증

---

#### OrderManagementService
**Purpose**: 주문 관리 비즈니스 로직

**Orchestration**:
- OrderRepository와 상호작용
- 주문 상태 변경
- 주문 삭제 및 총 주문액 재계산
- SSEService를 통한 실시간 업데이트

**Dependencies**:
- `OrderRepository`: 주문 데이터 접근
- `SSEService`: 실시간 알림

---

#### TableManagementService
**Purpose**: 테이블 관리 비즈니스 로직

**Orchestration**:
- TableRepository, OrderRepository, OrderHistoryRepository와 상호작용
- 테이블 초기 설정
- 세션 종료 및 이력 저장
- 과거 주문 내역 조회

**Dependencies**:
- `TableRepository`: 테이블 데이터 접근
- `OrderRepository`: 주문 데이터 접근
- `OrderHistoryRepository`: 이력 데이터 접근

---

#### MenuManagementService
**Purpose**: 메뉴 관리 비즈니스 로직

**Orchestration**:
- MenuRepository, FileStorage와 상호작용
- 메뉴 CRUD
- 이미지 업로드 처리
- 메뉴 순서 조정

**Dependencies**:
- `MenuRepository`: 메뉴 데이터 접근
- `FileStorage`: 이미지 파일 저장

---

### 3. Real-time Communication Service

#### SSEService
**Purpose**: 실시간 통신 관리

**Orchestration**:
- SSE 연결 관리
- 주문 이벤트 브로드캐스트
- 클라이언트 연결 추적

**Dependencies**:
- None (독립적인 서비스)

**Event Types**:
- `ORDER_CREATED`: 새 주문 생성
- `ORDER_UPDATED`: 주문 상태 변경
- `ORDER_DELETED`: 주문 삭제

---

## Service Interaction Patterns

### 1. Customer Order Flow
```
Customer UI → OrderService (Frontend)
  → API Call → CustomerController
    → OrderService (Backend)
      → OrderRepository (데이터 저장)
      → SSEService (실시간 알림)
        → Admin UI (실시간 업데이트)
```

### 2. Admin Order Management Flow
```
Admin UI → OrderService (Frontend)
  → API Call → AdminController
    → OrderManagementService
      → OrderRepository (데이터 수정)
      → SSEService (실시간 알림)
        → Admin UI (실시간 업데이트)
```

### 3. Real-time Communication Flow
```
SSEService (Backend)
  → SSE Stream → SSEService (Frontend)
    → Event Handler → Admin UI Component
      → State Update → UI Re-render
```

---

## Service Design Principles

### 1. Single Responsibility
각 서비스는 하나의 명확한 책임을 가집니다.

### 2. Dependency Injection
서비스 간 의존성은 생성자 주입을 통해 관리합니다.

### 3. Interface Segregation
서비스는 필요한 메서드만 노출합니다.

### 4. Error Handling
모든 서비스는 일관된 에러 처리 패턴을 따릅니다.

### 5. Logging
중요한 비즈니스 로직 실행 시 로깅을 수행합니다.

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
