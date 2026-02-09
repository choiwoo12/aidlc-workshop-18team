# Code Summary - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)는 고객의 메뉴 조회, 장바구니 관리, 주문 생성 및 주문 내역 조회 기능을 제공합니다. Backend는 REST API와 SSE를 통해 실시간 주문 상태 업데이트를 지원하며, Frontend는 React 기반의 SPA로 구현되었습니다.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
├─────────────────────────────────────────────────────────────┤
│  Pages:                                                      │
│  - MenuPage (메뉴 목록)                                      │
│  - CartPage (장바구니)                                       │
│  - OrderHistoryPage (주문 내역)                             │
│                                                              │
│  Context:                                                    │
│  - CartContext (장바구니 상태)                               │
│  - OrderContext (주문 상태 + SSE)                           │
│                                                              │
│  Services:                                                   │
│  - MenuService, OrderService, SSEService                    │
│  - CartService, ValidationService                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP / SSE
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
├─────────────────────────────────────────────────────────────┤
│  Controllers:                                                │
│  - MenuController (GET /api/menus)                          │
│  - OrderController (POST /api/orders, GET /api/orders)      │
│  - SSEController (GET /api/sse/orders/{table_id})          │
│                                                              │
│  Services:                                                   │
│  - MenuService (메뉴 조회)                                   │
│  - OrderService (주문 생성/관리)                             │
│  - SSEService (SSE 이벤트 브로드캐스트)                      │
│  - OrderValidationService (서버 검증)                        │
│                                                              │
│  Utilities:                                                  │
│  - OrderNumberGenerator (주문 번호 생성)                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Repository Pattern
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database (SQLite)                         │
│  - orders, order_items, menus, tables (Unit 1 재사용)       │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Implementation

### Generated Files (10 files)

#### Services (5 files)
1. **MenuService** (`backend/app/services/menu_service.py`)
   - 메뉴 조회 비즈니스 로직
   - 판매 가능한 메뉴 필터링
   - 카테고리별 필터링

2. **OrderService** (`backend/app/services/order_service.py`)
   - 주문 생성 및 관리
   - 주문 번호 생성 (OrderNumberGenerator 사용)
   - 주문 항목 생성 (OrderItem)
   - 메뉴 스냅샷 저장

3. **SSEService** (`backend/app/services/sse_service.py`)
   - SSE 이벤트 생성 및 브로드캐스트
   - 테이블별 연결 관리 (Queue 기반)
   - Keep-alive 메시지 (30초 간격)
   - 주문 상태 변경 이벤트 브로드캐스트

4. **OrderValidationService** (`backend/app/services/order_validation_service.py`)
   - 서버 측 주문 데이터 검증
   - 메뉴 존재 여부 확인
   - 판매 가능 여부 확인
   - 가격 일치 확인

5. **OrderNumberGenerator** (`backend/app/utils/order_number_generator.py`)
   - 주문 번호 생성 (T{테이블번호}-{순차번호})
   - AUTO_INCREMENT 활용

#### Controllers (3 files)
1. **MenuController** (`backend/app/api/menu_controller.py`)
   - `GET /api/menus`: 메뉴 목록 조회
   - `GET /api/menus/{menu_id}`: 메뉴 상세 조회
   - `GET /api/menus/categories`: 카테고리 목록 조회

2. **OrderController** (`backend/app/api/order_controller.py`)
   - `POST /api/orders`: 주문 생성
   - `GET /api/orders`: 주문 내역 조회
   - `GET /api/orders/{order_id}`: 주문 상세 조회

3. **SSEController** (`backend/app/api/sse_controller.py`)
   - `GET /api/sse/orders/{table_id}`: SSE 연결

#### Integration (1 file)
1. **Main App** (`backend/app/main.py`)
   - 라우터 추가 (menu, order, sse)

#### Documentation (1 file)
1. **Backend Summary** (`aidlc-docs/construction/unit-2-customer-order-domain/code/backend-summary.md`)

### Key Features
- **주문 번호 생성**: T{테이블번호}-{순차번호} (예: T01-001)
- **메뉴 스냅샷**: 주문 시점의 메뉴 정보 저장 (가격 변경 대응)
- **SSE 실시간 업데이트**: 주문 상태 변경 시 자동 알림
- **서버 측 검증**: 메뉴 존재, 판매 가능, 가격 일치 확인

---

## Frontend Implementation

### Generated Files (12 files)

#### Services (5 files)
1. **MenuService** (`frontend/src/services/MenuService.js`)
   - 메뉴 API 호출

2. **OrderService** (`frontend/src/services/OrderService.js`)
   - 주문 API 호출

3. **SSEService** (`frontend/src/services/SSEService.js`)
   - SSE 연결 관리
   - 자동 재연결 (최대 3회)

4. **CartService** (`frontend/src/services/CartService.js`)
   - 장바구니 관리 (SessionStorage)
   - 옵션 순서 무관 비교

5. **ValidationService** (`frontend/src/services/ValidationService.js`)
   - 클라이언트 검증

#### Context (2 files)
1. **CartContext** (`frontend/src/context/CartContext.jsx`)
   - 장바구니 전역 상태 관리

2. **OrderContext** (`frontend/src/context/OrderContext.jsx`)
   - 주문 전역 상태 관리
   - SSE 연결 초기화

#### Pages (3 files)
1. **MenuPage** (`frontend/src/pages/MenuPage.jsx`)
   - 메뉴 목록 및 장바구니 추가

2. **CartPage** (`frontend/src/pages/CartPage.jsx`)
   - 장바구니 화면

3. **OrderHistoryPage** (`frontend/src/pages/OrderHistoryPage.jsx`)
   - 주문 내역 화면 (실시간 업데이트)

#### Integration (1 file)
1. **App** (`frontend/src/App.jsx`)
   - CartProvider, OrderProvider 추가
   - 라우트 추가

#### Documentation (1 file)
1. **Frontend Summary** (`aidlc-docs/construction/unit-2-customer-order-domain/code/frontend-summary.md`)

### Key Features
- **SessionStorage 장바구니**: 페이지 새로고침 시 유지
- **SSE 실시간 업데이트**: 주문 상태 변경 자동 반영
- **옵션 순서 무관 비교**: 중복 항목 자동 수량 증가
- **Context 기반 상태 관리**: CartContext, OrderContext

---

## Integration with Unit 1

### Backend Reuse
- **Repository**: OrderRepository, OrderItemRepository, MenuRepository, TableRepository
- **Middleware**: AuthMiddleware, ErrorMiddleware
- **Database**: SQLite (orders, order_items, menus, tables)
- **Models**: Order, OrderItem, Menu, Table

### Frontend Reuse
- **Components**: Button, Loading, ErrorMessage, Modal
- **Context**: AuthContext
- **Services**: axios 설정, StorageService
- **Utils**: axios interceptor

---

## API Endpoints

### Menu API
- `GET /api/menus`: 메뉴 목록 조회
  - Query: `store_id`, `category` (optional)
- `GET /api/menus/{menu_id}`: 메뉴 상세 조회
- `GET /api/menus/categories`: 카테고리 목록 조회
  - Query: `store_id`

### Order API
- `POST /api/orders`: 주문 생성
  - Body: `{ table_id, cart_items }`
- `GET /api/orders`: 주문 내역 조회
  - Query: `table_id`
- `GET /api/orders/{order_id}`: 주문 상세 조회

### SSE API
- `GET /api/sse/orders/{table_id}`: SSE 연결
  - Event: `order_status_changed`

---

## Data Flow

### 1. 메뉴 조회 Flow
```
MenuPage → MenuService.getMenus()
  → GET /api/menus
    → MenuController.get_menus()
      → MenuService.get_available_menus()
        → MenuRepository.find_available_menus()
          → Database
```

### 2. 장바구니 추가 Flow
```
MenuPage → CartContext.addItem()
  → CartService.addItem()
    → SessionStorage.setItem()
```

### 3. 주문 생성 Flow
```
CartPage → OrderContext.createOrder()
  → OrderService.createOrder()
    → POST /api/orders
      → OrderController.create_order()
        → OrderValidationService.validate_order_items()
        → OrderService.create_order()
          → OrderNumberGenerator.generate()
          → OrderRepository.save()
          → OrderItemRepository.save()
          → SSEService.broadcast_order_status_change()
            → Database
```

### 4. 실시간 업데이트 Flow
```
OrderHistoryPage → OrderContext (SSE 연결)
  → SSEService.connect()
    → GET /api/sse/orders/{table_id}
      → SSEController.stream_orders()
        → SSEService.event_generator()
          → Queue (Keep-alive 30초)

Admin 주문 상태 변경
  → SSEService.broadcast_order_status_change()
    → Queue.put(event)
      → SSEService.event_generator()
        → Frontend SSEService.onmessage
          → OrderContext.handleSSEMessage()
            → orders 상태 업데이트
              → OrderHistoryPage 리렌더링
```

---

## Key Design Decisions

### 1. 주문 번호 생성
- **Format**: T{테이블번호}-{순차번호}
- **Example**: T01-001, T01-002, T02-001
- **Implementation**: AUTO_INCREMENT 활용

### 2. 메뉴 스냅샷
- 주문 시점의 메뉴 정보 저장 (name, price)
- 가격 변경 시에도 주문 내역 정확성 유지

### 3. SSE 실시간 업데이트
- 자동 재연결 (최대 3회: 즉시, 5초, 10초)
- Keep-alive 메시지 (30초 간격)
- 재연결 시 전체 주문 목록 다시 조회

### 4. 장바구니 관리
- SessionStorage 기반 (페이지 새로고침 시 유지)
- 옵션 순서 무관 비교 (정렬 후 비교)
- 중복 항목 시 수량 증가

### 5. 검증 전략
- **Client**: 최소 검증 (메뉴 필수, 수량 1 이상)
- **Server**: 상세 검증 (메뉴 존재, 판매 가능, 가격 일치)

---

## Testing Checklist

### Backend Testing
- [ ] 메뉴 목록 조회 (전체, 카테고리별)
- [ ] 주문 생성 (정상, 검증 실패)
- [ ] 주문 내역 조회
- [ ] SSE 연결 및 이벤트 수신
- [ ] 주문 번호 생성 (순차 증가)
- [ ] 메뉴 스냅샷 저장

### Frontend Testing
- [ ] 메뉴 목록 표시
- [ ] 카테고리 필터링
- [ ] 옵션 선택 모달
- [ ] 장바구니 추가 (중복 항목 수량 증가)
- [ ] 장바구니 수량 조절
- [ ] 주문 생성
- [ ] 주문 내역 표시
- [ ] SSE 실시간 업데이트
- [ ] 페이지 새로고침 시 장바구니 유지

### Integration Testing
- [ ] Backend + Frontend 통합
- [ ] SSE 실시간 업데이트 동작
- [ ] 장바구니 → 주문 생성 → 주문 내역 Flow
- [ ] 에러 처리 (네트워크 에러, 검증 실패)

---

## File Structure

### Backend
```
backend/app/
├── services/
│   ├── menu_service.py
│   ├── order_service.py
│   ├── sse_service.py
│   └── order_validation_service.py
├── utils/
│   └── order_number_generator.py
├── api/
│   ├── menu_controller.py
│   ├── order_controller.py
│   └── sse_controller.py
└── main.py
```

### Frontend
```
frontend/src/
├── services/
│   ├── MenuService.js
│   ├── OrderService.js
│   ├── SSEService.js
│   ├── CartService.js
│   └── ValidationService.js
├── context/
│   ├── CartContext.jsx
│   └── OrderContext.jsx
├── pages/
│   ├── MenuPage.jsx
│   ├── CartPage.jsx
│   └── OrderHistoryPage.jsx
└── App.jsx
```

---

## Dependencies

### Backend
- FastAPI (Unit 1)
- SQLAlchemy (Unit 1)
- asyncio (SSE)

### Frontend
- React (Unit 1)
- react-router-dom (Unit 1)
- axios (Unit 1)
- EventSource API (SSE)

---

## Performance Considerations

### Backend
- SSE 연결 관리 (Queue 기반)
- Keep-alive로 연결 유지 (30초)
- 비동기 처리 (asyncio)

### Frontend
- SessionStorage 사용 (서버 부하 최소화)
- Context 기반 상태 관리 (불필요한 리렌더링 방지)
- SSE 자동 재연결 (최대 3회)

---

## Security Considerations

### Backend
- AuthMiddleware 재사용 (JWT 검증)
- 서버 측 검증 (메뉴 존재, 판매 가능, 가격 일치)
- SSE 연결 시 테이블 ID 검증

### Frontend
- 클라이언트 검증 (최소)
- 서버 응답 신뢰
- SessionStorage (XSS 주의)

---

## Next Steps

1. **Unit 2 통합 테스트**
   - Backend + Frontend 통합
   - SSE 실시간 업데이트 동작 확인
   - 장바구니 SessionStorage 동작 확인

2. **Unit 3 개발 시작**
   - Admin Operations Domain
   - 주문 관리 (상태 변경)
   - 메뉴 관리 (CRUD)

3. **Build and Test**
   - 빌드 및 테스트 지침 문서 작성
   - 통합 테스트 실행

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: Unit 2 코드 생성 완료
