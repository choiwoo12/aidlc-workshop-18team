# Frontend Code Summary - Unit 2: Customer Order Domain

## Overview

Unit 2 Frontend는 고객의 메뉴 조회, 장바구니 관리, 주문 생성 및 주문 내역 조회 기능을 제공합니다. SSE를 통한 실시간 주문 상태 업데이트를 지원합니다.

---

## Generated Files

### Services (5 files)

#### 1. MenuService.js
**Location**: `frontend/src/services/MenuService.js`

**Purpose**: 메뉴 조회 API 호출

**Key Methods**:
- `getMenus(storeId, category)`: 판매 가능한 메뉴 목록 조회
- `getMenuById(menuId)`: 메뉴 상세 조회
- `getCategories(storeId)`: 카테고리 목록 조회

**Dependencies**: axios

---

#### 2. OrderService.js
**Location**: `frontend/src/services/OrderService.js`

**Purpose**: 주문 생성 및 조회 API 호출

**Key Methods**:
- `createOrder(tableId, cartItems)`: 주문 생성
- `getOrders(tableId)`: 테이블별 주문 내역 조회
- `getOrderById(orderId)`: 주문 상세 조회

**Dependencies**: axios

---

#### 3. SSEService.js
**Location**: `frontend/src/services/SSEService.js`

**Purpose**: Server-Sent Events 연결 관리

**Key Features**:
- SSE 연결 설정 및 종료
- 자동 재연결 (최대 3회: 즉시, 5초, 10초)
- Keep-alive 메시지 처리 (30초 간격)
- 연결 상태 확인

**Key Methods**:
- `connect(tableId, onMessage, onError)`: SSE 연결 설정
- `disconnect()`: SSE 연결 종료
- `isConnected()`: 연결 상태 확인
- `handleConnectionError()`: 재연결 로직

**Dependencies**: EventSource API

---

#### 4. CartService.js
**Location**: `frontend/src/services/CartService.js`

**Purpose**: 장바구니 관리 (SessionStorage 기반)

**Key Features**:
- 장바구니 항목 추가 (중복 시 수량 증가)
- 옵션 순서 무관 비교 (정렬 후 비교)
- 수량 업데이트 및 항목 제거
- SessionStorage 자동 저장/로드

**Key Methods**:
- `addItem(cart, menu, selectedOptions, quantity)`: 항목 추가
- `updateQuantity(cart, cartItemId, quantity)`: 수량 업데이트
- `removeItem(cart, cartItemId)`: 항목 제거
- `clearCart()`: 장바구니 비우기
- `loadCart()`: SessionStorage에서 로드
- `saveCart(cart)`: SessionStorage에 저장

**Data Structure**:
```javascript
{
  items: [
    {
      id: "unique-id",
      menu_id: 1,
      menu_snapshot: { name, price, ... },
      selected_options: [{ name, price }],
      quantity: 2,
      subtotal: 15000
    }
  ],
  total_amount: 15000
}
```

---

#### 5. ValidationService.js
**Location**: `frontend/src/services/ValidationService.js`

**Purpose**: 클라이언트 측 데이터 유효성 검증

**Key Methods**:
- `validateCartItem(menu, selectedOptions, quantity)`: 장바구니 항목 검증
- `validateQuantity(quantity)`: 수량 검증 (1 이상)
- `validateOptions(options)`: 옵션 검증

**Validation Rules**:
- 메뉴 필수 (menu_id, name, price)
- 수량 1 이상
- 옵션 형식 검증 (name, price)

---

### Context (2 files)

#### 1. CartContext.jsx
**Location**: `frontend/src/context/CartContext.jsx`

**Purpose**: 장바구니 전역 상태 관리

**State**:
- `cart`: 장바구니 데이터 (items, total_amount)

**Methods**:
- `addItem(menu, selectedOptions, quantity)`: 항목 추가
- `updateQuantity(cartItemId, quantity)`: 수량 업데이트
- `removeItem(cartItemId)`: 항목 제거
- `clearCart()`: 장바구니 비우기
- `getItemCount()`: 총 항목 개수

**Features**:
- SessionStorage 자동 저장
- 초기 로드 시 SessionStorage에서 복원

---

#### 2. OrderContext.jsx
**Location**: `frontend/src/context/OrderContext.jsx`

**Purpose**: 주문 내역 전역 상태 관리 및 SSE 연결 관리

**State**:
- `orders`: 주문 목록
- `loading`: 로딩 상태
- `error`: 에러 메시지
- `sseConnected`: SSE 연결 상태

**Methods**:
- `createOrder(cartItems)`: 주문 생성
- `refreshOrders()`: 주문 목록 새로고침

**Features**:
- 테이블 로그인 시 SSE 자동 연결
- SSE 이벤트 수신 시 주문 상태 실시간 업데이트
- 컴포넌트 언마운트 시 SSE 자동 종료
- 재연결 시 전체 주문 목록 다시 조회

**SSE Event Handling**:
```javascript
{
  type: "order_status_changed",
  order_id: 1,
  old_status: "PENDING",
  new_status: "CONFIRMED"
}
```

---

### Pages (3 files)

#### 1. MenuPage.jsx
**Location**: `frontend/src/pages/MenuPage.jsx`

**Purpose**: 메뉴 목록 및 장바구니 추가 화면

**Features**:
- 메뉴 목록 표시 (카드 형식)
- 카테고리 필터링 (전체, 카테고리별)
- 메뉴 클릭 시 옵션 선택 모달
- 옵션 선택 (체크박스)
- 수량 선택 (증감 버튼)
- 장바구니에 추가
- 장바구니 버튼 (항목 개수 배지)

**UI Components**:
- Header (제목, 장바구니 버튼)
- 카테고리 필터 (가로 스크롤)
- 메뉴 카드 그리드 (이미지, 이름, 설명, 가격, 카테고리)
- 옵션 선택 모달 (옵션, 수량, 총 금액)

---

#### 2. CartPage.jsx
**Location**: `frontend/src/pages/CartPage.jsx`

**Purpose**: 장바구니 화면

**Features**:
- 장바구니 항목 목록
- 항목별 수량 조절 (증감 버튼)
- 항목 제거 (X 버튼)
- 전체 삭제
- 주문하기 (확인 모달)
- 총 금액 표시

**UI Components**:
- Header (뒤로가기, 제목)
- 장바구니 항목 카드 (메뉴명, 옵션, 수량, 소계)
- 총 금액 및 버튼 (전체 삭제, 주문하기)
- 주문 확인 모달

**Flow**:
1. 장바구니 항목 표시
2. 수량 조절 또는 항목 제거
3. 주문하기 클릭 → 확인 모달
4. 확인 → 주문 생성 → 장바구니 비우기 → 주문 내역 페이지 이동

---

#### 3. OrderHistoryPage.jsx
**Location**: `frontend/src/pages/OrderHistoryPage.jsx`

**Purpose**: 주문 내역 화면 (실시간 업데이트)

**Features**:
- 주문 내역 목록 (최신순)
- 주문 상태 표시 (색상 배지)
- 주문 항목 상세 (메뉴명, 옵션, 수량, 소계)
- 총 금액 표시
- SSE 연결 상태 표시
- 실시간 주문 상태 업데이트
- 주문 상태별 안내 메시지

**Order Status**:
- `PENDING`: 접수 대기 (노란색)
- `CONFIRMED`: 접수 완료 (파란색)
- `PREPARING`: 조리 중 (보라색)
- `READY`: 준비 완료 (초록색)
- `SERVED`: 서빙 완료 (회색)
- `CANCELLED`: 취소됨 (빨간색)

**UI Components**:
- Header (뒤로가기, 제목, SSE 연결 상태)
- 주문 카드 (주문번호, 시간, 상태, 항목, 총 금액)
- 상태별 안내 메시지 (READY, PREPARING)

---

### App Integration

#### App.jsx
**Location**: `frontend/src/App.jsx`

**Changes**:
- CartProvider 추가 (AuthProvider 내부)
- OrderProvider 추가 (CartProvider 내부)
- 라우트 추가:
  - `/customer/menu`: MenuPage
  - `/customer/cart`: CartPage
  - `/customer/orders`: OrderHistoryPage

**Provider Hierarchy**:
```
AuthProvider
  └─ CartProvider
      └─ OrderProvider
          └─ Router
```

---

## Integration with Unit 1

### Reused Components
- `Button`: 버튼 컴포넌트
- `Loading`: 로딩 스피너
- `ErrorMessage`: 에러 메시지
- `Modal`: 모달 컴포넌트
- `Input`: 입력 필드 (Unit 2에서는 미사용)

### Reused Services
- `axios`: HTTP 클라이언트 (Unit 1 설정 재사용)
- `StorageService`: SessionStorage 관리 (Unit 1)

### Reused Context
- `AuthContext`: 인증 상태 관리 (user, isTable)

---

## Key Design Decisions

### 1. SessionStorage for Cart
- 페이지 새로고침 시 장바구니 유지
- 브라우저 탭 닫으면 자동 삭제
- 서버 부하 최소화

### 2. SSE for Real-time Updates
- 주문 상태 변경 시 실시간 알림
- 자동 재연결 (최대 3회)
- Keep-alive로 연결 유지 (30초)

### 3. Option Comparison (Order-Independent)
- 옵션 순서 무관 비교 (정렬 후 비교)
- 중복 항목 시 수량 증가
- 사용자 편의성 향상

### 4. Context Hierarchy
- AuthProvider → CartProvider → OrderProvider
- 각 Context는 상위 Context에 의존
- OrderContext는 AuthContext의 user 정보 사용

### 5. Client-side Validation
- 최소한의 검증 (메뉴 필수, 수량 1 이상)
- 서버 측 상세 검증에 의존
- 사용자 경험 개선

---

## API Endpoints Used

### Menu API
- `GET /api/menus`: 메뉴 목록 조회
- `GET /api/menus/{menu_id}`: 메뉴 상세 조회
- `GET /api/menus/categories`: 카테고리 목록 조회

### Order API
- `POST /api/orders`: 주문 생성
- `GET /api/orders`: 주문 내역 조회
- `GET /api/orders/{order_id}`: 주문 상세 조회

### SSE API
- `GET /api/sse/orders/{table_id}`: SSE 연결

---

## Testing Considerations

### Manual Testing Checklist
- [ ] 메뉴 목록 조회 (전체, 카테고리별)
- [ ] 메뉴 클릭 → 옵션 선택 모달
- [ ] 옵션 선택 및 수량 조절
- [ ] 장바구니에 추가 (중복 항목 수량 증가 확인)
- [ ] 장바구니 페이지 이동
- [ ] 장바구니 항목 수량 조절
- [ ] 장바구니 항목 제거
- [ ] 주문하기 → 확인 모달 → 주문 생성
- [ ] 주문 내역 페이지 이동
- [ ] SSE 연결 상태 확인
- [ ] 주문 상태 실시간 업데이트 확인 (관리자가 상태 변경 시)
- [ ] 페이지 새로고침 시 장바구니 유지 확인
- [ ] 브라우저 탭 닫기 후 재접속 시 장바구니 초기화 확인

### Edge Cases
- 메뉴 목록이 비어있을 때
- 장바구니가 비어있을 때
- 주문 내역이 비어있을 때
- SSE 연결 실패 시
- 네트워크 에러 시
- 옵션 없는 메뉴
- 동일 메뉴 + 동일 옵션 중복 추가

---

## Dependencies

### External Libraries
- `react`: UI 라이브러리
- `react-router-dom`: 라우팅
- `axios`: HTTP 클라이언트

### Internal Dependencies
- Unit 1 공통 컴포넌트 (Button, Loading, ErrorMessage, Modal)
- Unit 1 AuthContext
- Unit 1 axios 설정

---

## File Structure

```
frontend/src/
├── services/
│   ├── MenuService.js          # 메뉴 API 호출
│   ├── OrderService.js         # 주문 API 호출
│   ├── SSEService.js           # SSE 연결 관리
│   ├── CartService.js          # 장바구니 관리
│   └── ValidationService.js    # 클라이언트 검증
├── context/
│   ├── CartContext.jsx         # 장바구니 전역 상태
│   └── OrderContext.jsx        # 주문 전역 상태 + SSE
├── pages/
│   ├── MenuPage.jsx            # 메뉴 목록 화면
│   ├── CartPage.jsx            # 장바구니 화면
│   └── OrderHistoryPage.jsx   # 주문 내역 화면
└── App.jsx                     # 라우트 통합
```

---

## Next Steps

1. Unit 2 Backend와 통합 테스트
2. SSE 실시간 업데이트 동작 확인
3. 장바구니 SessionStorage 동작 확인
4. Unit 3 (Admin Operations Domain) 개발 시작

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 코드 생성 완료
