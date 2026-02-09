# Backend Code Summary - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 Backend 구현 요약입니다. 고객 주문 프로세스를 지원하는 API 및 서비스를 구현했습니다.

---

## Generated Files (8개)

### Service Layer (4개)
1. `backend/app/services/menu_service.py` - 메뉴 조회 서비스
2. `backend/app/services/order_service.py` - 주문 생성/관리 서비스
3. `backend/app/services/order_validation_service.py` - 주문 검증 서비스
4. `backend/app/services/sse_service.py` - SSE 이벤트 서비스

### Utility (1개)
5. `backend/app/utils/order_number_generator.py` - 주문 번호 생성기

### API Controllers (3개)
6. `backend/app/api/menu_controller.py` - 메뉴 API
7. `backend/app/api/order_controller.py` - 주문 API
8. `backend/app/api/sse_controller.py` - SSE API

### Modified Files (1개)
- `backend/app/main.py` - Unit 2 라우터 추가

---

## API Endpoints

### Menu API (`/api/menus`)
- `GET /api/menus` - 판매 가능한 메뉴 목록 조회
  - Query: `store_id`, `category` (선택)
  - Response: 메뉴 목록 (is_available=true만)
  
- `GET /api/menus/{menu_id}` - 메뉴 상세 조회
  - Response: 메뉴 상세 정보
  
- `GET /api/menus/categories` - 카테고리 목록 조회
  - Query: `store_id`
  - Response: 카테고리 목록

### Order API (`/api/orders`)
- `POST /api/orders` - 주문 생성
  - Body: `{ table_id, cart_items[] }`
  - Response: 생성된 주문 정보
  - SSE 이벤트 브로드캐스트
  
- `GET /api/orders` - 주문 내역 조회
  - Query: `table_id`
  - Response: 주문 목록 (시간 역순)
  
- `GET /api/orders/{order_id}` - 주문 상세 조회
  - Response: 주문 상세 정보 (OrderItem 포함)

### SSE API (`/api/sse`)
- `GET /api/sse/orders/{table_id}` - SSE 연결
  - Response: text/event-stream
  - Keep-alive: 30초마다
  - Events: `order_created`, `order_status_changed`

---

## Service Layer

### MenuService
**Purpose**: 메뉴 조회 비즈니스 로직

**Methods**:
- `get_available_menus(store_id, category)` - 판매 가능한 메뉴 조회
- `get_menu_by_id(menu_id)` - 메뉴 상세 조회
- `get_categories(store_id)` - 카테고리 목록 조회

**Dependencies**: MenuRepository (Unit 1)

---

### OrderService
**Purpose**: 주문 생성 및 관리 비즈니스 로직

**Methods**:
- `create_order(table_id, cart_items)` - 주문 생성
  - 유효성 검증
  - 주문 번호 생성
  - Order + OrderItem 생성
  - SSE 이벤트 브로드캐스트
  
- `get_orders_by_table(table_id)` - 테이블별 주문 내역 조회
- `get_order_by_id(order_id)` - 주문 상세 조회

**Dependencies**: 
- OrderRepository, OrderItemRepository, TableRepository (Unit 1)
- OrderNumberGenerator, OrderValidationService (Unit 2)

---

### OrderValidationService
**Purpose**: 서버 측 주문 데이터 유효성 검증

**Methods**:
- `validate_order_items(cart_items)` - 주문 항목 검증
  - 장바구니 비어있지 않음
  - 메뉴 존재 여부
  - 판매 가능 여부
  - 가격 일치 확인
  - 수량 확인

**Dependencies**: MenuRepository (Unit 1)

---

### SSEService
**Purpose**: SSE 이벤트 생성 및 브로드캐스트

**Methods**:
- `event_generator(table_id)` - SSE 이벤트 생성기
  - Keep-alive 30초마다
  - 비동기 큐 기반
  
- `broadcast_order_status_change(...)` - 주문 상태 변경 이벤트
- `broadcast_order_created(...)` - 주문 생성 이벤트
- `get_connection_count(table_id)` - 연결 수 조회

**Implementation**: 
- 싱글톤 패턴
- 테이블별 연결 관리 (Dict[int, List[Queue]])
- asyncio.Queue 기반

---

## Utility

### OrderNumberGenerator
**Purpose**: 주문 번호 생성

**Method**:
- `generate(table_number)` - 주문 번호 생성
  - 형식: `T{테이블번호}-{순차번호}`
  - 예시: T01-001, T01-002
  - 테이블별 순차 번호 관리

**Dependencies**: OrderRepository (Unit 1)

---

## Data Flow

### 주문 생성 플로우
```
[Client] → POST /api/orders
    ↓
[OrderController]
    ↓
[OrderService.create_order()]
    ↓
[OrderValidationService.validate_order_items()]
    ↓
[OrderNumberGenerator.generate()]
    ↓
[OrderRepository.save()] + [OrderItemRepository.save()]
    ↓
[SSEService.broadcast_order_created()]
    ↓
[Response: Order]
```

### 메뉴 조회 플로우
```
[Client] → GET /api/menus?category=음료
    ↓
[MenuController]
    ↓
[MenuService.get_available_menus()]
    ↓
[MenuRepository.find_by_store()]
    ↓
[Filter: is_available=true, category match]
    ↓
[Response: Menu[]]
```

### SSE 연결 플로우
```
[Client] → GET /api/sse/orders/1
    ↓
[SSEController]
    ↓
[SSEService.event_generator()]
    ↓
[StreamingResponse]
    ↓
[Keep-alive every 30s]
    ↓
[Events when order status changes]
```

---

## Integration with Unit 1

### Reused Components
- **Repositories**: OrderRepository, OrderItemRepository, MenuRepository, TableRepository
- **Models**: Order, OrderItem, Menu, Table
- **Database**: SQLite connection, session management
- **Middleware**: Auth middleware, Error middleware
- **Utilities**: Database utils, Exceptions

### New Components
- **Services**: MenuService, OrderService, OrderValidationService, SSEService
- **Utility**: OrderNumberGenerator
- **Controllers**: MenuController, OrderController, SSEController

---

## Error Handling

### Validation Errors (400)
- 장바구니 비어있음
- 메뉴 판매 불가
- 가격 불일치
- 수량 오류

### Not Found Errors (404)
- 메뉴를 찾을 수 없음
- 테이블을 찾을 수 없음
- 주문을 찾을 수 없음

### Server Errors (500)
- 주문 생성 실패
- 주문 조회 실패
- 메뉴 조회 실패

---

## Testing Considerations

### Unit Tests (Build & Test 단계에서 작성)
- MenuService: 메뉴 조회, 카테고리 필터링
- OrderService: 주문 생성, 주문 내역 조회
- OrderValidationService: 유효성 검증 로직
- OrderNumberGenerator: 주문 번호 생성 로직

### Integration Tests (Build & Test 단계에서 작성)
- POST /api/orders: 주문 생성 플로우
- GET /api/orders: 주문 내역 조회
- GET /api/menus: 메뉴 조회
- SSE 연결 및 이벤트 수신

---

## Performance Considerations

### Database Queries
- 메뉴 조회: 인덱스 활용 (store_id, is_available)
- 주문 조회: 테이블별 인덱스
- 주문 번호 생성: 마지막 주문 조회 (최적화 가능)

### SSE Connections
- 테이블별 연결 관리
- Keep-alive로 연결 유지
- 비동기 큐로 이벤트 전송

### Response Time Targets
- 메뉴 조회: < 1초
- 주문 생성: < 2초
- SSE 연결: < 1초
- SSE 이벤트 전송: < 2초

---

## Security Considerations

### Authentication
- JWT 토큰 검증 (Unit 1 Middleware 재사용)
- 테이블 세션 검증

### Validation
- 서버 측 상세 검증
- 메뉴 판매 가능 여부 확인
- 가격 일치 확인

### Data Protection
- 메뉴 정보 스냅샷 (가격 변경 대응)
- 주문 데이터 무결성 보장

---

## Next Steps

Frontend 구현:
- Services (5개)
- Context (2개)
- Pages (3개)
- App 통합

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: Backend 구현 완료
