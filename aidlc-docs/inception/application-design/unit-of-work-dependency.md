# Unit of Work Dependency - 테이블오더 서비스

## Overview
3개 유닛 간의 의존성 관계, 통합 포인트, 개발 순서를 정의합니다.

---

## Unit Dependency Matrix

| From \ To | Customer Frontend | Admin Frontend | Backend |
|-----------|-------------------|----------------|---------|
| **Customer Frontend** | - | ❌ No | ✅ Yes (API, SSE) |
| **Admin Frontend** | ❌ No | - | ✅ Yes (API, SSE) |
| **Backend** | ✅ Yes (SSE) | ✅ Yes (SSE) | - |

### 의존성 설명

#### Customer Frontend → Backend
- **의존 타입**: REST API 호출, SSE 수신
- **의존 이유**: 메뉴 조회, 주문 생성, 주문 내역 조회, 실시간 상태 업데이트
- **결합도**: Loose (REST API, JSON)
- **통신 방향**: 양방향 (요청/응답 + SSE 이벤트)

#### Admin Frontend → Backend
- **의존 타입**: REST API 호출, SSE 수신
- **의존 이유**: 인증, 주문 관리, 메뉴 관리, 테이블 관리, 실시간 주문 알림
- **결합도**: Loose (REST API, JSON)
- **통신 방향**: 양방향 (요청/응답 + SSE 이벤트)

#### Backend → Customer Frontend
- **의존 타입**: SSE 이벤트 전송
- **의존 이유**: 주문 상태 변경 알림
- **결합도**: Loose (SSE, JSON)
- **통신 방향**: 단방향 (이벤트 푸시)

#### Backend → Admin Frontend
- **의존 타입**: SSE 이벤트 전송
- **의존 이유**: 신규 주문 알림, 주문 상태 변경 알림, 주문 삭제 알림
- **결합도**: Loose (SSE, JSON)
- **통신 방향**: 단방향 (이벤트 푸시)

#### Customer Frontend ↔ Admin Frontend
- **의존 타입**: 없음
- **의존 이유**: 완전히 독립적인 애플리케이션
- **결합도**: None
- **통신 방향**: 없음

---

## Integration Points

### 1. REST API Integration

#### Customer Frontend → Backend

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/api/customer/menus` | GET | 메뉴 목록 조회 | Query: `storeId`, `category` | `Menu[]` |
| `/api/customer/orders` | POST | 주문 생성 | Body: `CreateOrderRequest` | `Order` |
| `/api/customer/orders` | GET | 주문 내역 조회 | Query: `tableId`, `sessionId` | `Order[]` |

**CreateOrderRequest**:
```json
{
  "storeId": "string",
  "tableId": "string",
  "sessionId": "string",
  "items": [
    {
      "menuId": "string",
      "quantity": "number"
    }
  ]
}
```

**Menu**:
```json
{
  "id": "string",
  "storeId": "string",
  "name": "string",
  "price": "number",
  "description": "string",
  "category": "string",
  "imagePath": "string",
  "displayOrder": "number"
}
```

**Order**:
```json
{
  "id": "string",
  "storeId": "string",
  "tableId": "string",
  "sessionId": "string",
  "orderTime": "string (ISO 8601)",
  "totalAmount": "number",
  "status": "string (대기중|준비중|완료|취소)",
  "items": [
    {
      "id": "string",
      "menuId": "string",
      "menuName": "string",
      "quantity": "number",
      "unitPrice": "number"
    }
  ]
}
```

---

#### Admin Frontend → Backend

| Endpoint | Method | Purpose | Request | Response |
|----------|--------|---------|---------|----------|
| `/api/auth/login` | POST | 관리자 로그인 | Body: `LoginRequest` | `LoginResponse` |
| `/api/admin/orders` | GET | 주문 목록 조회 | Query: `storeId`, `tableId` | `Order[]` |
| `/api/admin/orders/{id}/status` | PUT | 주문 상태 변경 | Body: `UpdateStatusRequest` | `Order` |
| `/api/admin/orders/{id}` | DELETE | 주문 삭제 | - | `204 No Content` |
| `/api/admin/menus` | GET | 메뉴 목록 조회 | Query: `storeId` | `Menu[]` |
| `/api/admin/menus` | POST | 메뉴 등록 | Body: `CreateMenuRequest` (Multipart) | `Menu` |
| `/api/admin/menus/{id}` | PUT | 메뉴 수정 | Body: `UpdateMenuRequest` (Multipart) | `Menu` |
| `/api/admin/menus/{id}` | DELETE | 메뉴 삭제 | - | `204 No Content` |
| `/api/admin/tables` | GET | 테이블 목록 조회 | Query: `storeId` | `Table[]` |
| `/api/admin/tables/{id}/end-session` | POST | 세션 종료 | - | `Table` |
| `/api/admin/history` | GET | 과거 주문 내역 | Query: `storeId`, `startDate`, `endDate` | `OrderHistory[]` |

**LoginRequest**:
```json
{
  "storeId": "string",
  "username": "string",
  "password": "string"
}
```

**LoginResponse**:
```json
{
  "token": "string (JWT)",
  "user": {
    "id": "string",
    "username": "string",
    "storeId": "string",
    "role": "string"
  }
}
```

**UpdateStatusRequest**:
```json
{
  "status": "string (대기중|준비중|완료|취소)"
}
```

**CreateMenuRequest** (Multipart Form Data):
- `name`: string
- `price`: number
- `description`: string
- `category`: string
- `image`: file (JPG/PNG, max 5MB)

**Table**:
```json
{
  "id": "string",
  "storeId": "string",
  "tableNumber": "number",
  "sessionId": "string",
  "sessionStatus": "string (active|inactive)"
}
```

---

### 2. SSE Integration

#### Backend → Customer Frontend

| Event Type | Purpose | Payload |
|------------|---------|---------|
| `ORDER_STATUS_CHANGED` | 주문 상태 변경 알림 | `{ orderId, status, timestamp }` |

**연결 엔드포인트**: `/api/sse/customer?tableId={tableId}&sessionId={sessionId}`

**이벤트 예시**:
```
event: ORDER_STATUS_CHANGED
data: {"orderId":"order-123","status":"준비중","timestamp":"2026-02-09T10:30:00Z"}
```

---

#### Backend → Admin Frontend

| Event Type | Purpose | Payload |
|------------|---------|---------|
| `NEW_ORDER` | 신규 주문 생성 알림 | `{ orderId, tableId, totalAmount, timestamp }` |
| `ORDER_STATUS_CHANGED` | 주문 상태 변경 알림 | `{ orderId, status, timestamp }` |
| `ORDER_DELETED` | 주문 삭제 알림 | `{ orderId, timestamp }` |

**연결 엔드포인트**: `/api/sse/admin?storeId={storeId}&token={jwtToken}`

**이벤트 예시**:
```
event: NEW_ORDER
data: {"orderId":"order-123","tableId":"table-5","totalAmount":25000,"timestamp":"2026-02-09T10:30:00Z"}

event: ORDER_STATUS_CHANGED
data: {"orderId":"order-123","status":"준비중","timestamp":"2026-02-09T10:35:00Z"}

event: ORDER_DELETED
data: {"orderId":"order-123","timestamp":"2026-02-09T10:40:00Z"}
```

---

## Data Flow Diagrams

### 주문 생성 플로우

```
Customer Frontend
  |
  | 1. POST /api/customer/orders
  v
Backend (OrderService)
  |
  | 2. Validate & Save Order
  v
Database (H2)
  |
  | 3. SSE Event: NEW_ORDER
  v
Admin Frontend (실시간 알림)
```

### 주문 상태 변경 플로우

```
Admin Frontend
  |
  | 1. PUT /api/admin/orders/{id}/status
  v
Backend (OrderService)
  |
  | 2. Update Order Status
  v
Database (H2)
  |
  | 3. SSE Event: ORDER_STATUS_CHANGED
  v
Customer Frontend (실시간 업데이트)
Admin Frontend (실시간 업데이트)
```

### 메뉴 조회 플로우

```
Customer Frontend
  |
  | 1. GET /api/customer/menus
  v
Backend (MenuService)
  |
  | 2. Query Menus
  v
Database (H2)
  |
  | 3. Return Menu[]
  v
Customer Frontend (메뉴 표시)
```

---

## Development Order Recommendation

### Phase 1: Backend Foundation (Unit 3)
**Duration**: 2-3 weeks

**Priority 1 - Core Infrastructure**:
1. 프로젝트 설정 (Spring Boot, MyBatis, H2)
2. 도메인 모델 정의 (Store, Table, Menu, Order, OrderItem, User)
3. 데이터베이스 스키마 및 초기 데이터
4. 공통 컴포넌트 (GlobalExceptionHandler, JwtTokenProvider)

**Priority 2 - Authentication**:
5. AuthService, AuthController
6. JWT 인증 필터
7. 로그인 API 구현

**Priority 3 - Menu & Order APIs**:
8. MenuService, MenuMapper, MenuController
9. OrderService, OrderMapper, OrderController (Customer)
10. 메뉴 조회, 주문 생성, 주문 조회 API

**Priority 4 - Admin APIs**:
11. AdminController (주문 관리, 메뉴 관리)
12. TableService, TableMapper
13. 주문 상태 변경, 메뉴 CRUD, 테이블 관리 API

**Priority 5 - Real-time Features**:
14. SSEService, SSEController
15. 실시간 이벤트 전송 구현

**Priority 6 - File Upload**:
16. FileService, FileStorageConfig
17. 이미지 업로드 API

**Validation**: Postman 또는 curl로 모든 API 테스트

---

### Phase 2: Customer Frontend (Unit 1)
**Duration**: 2-3 weeks

**Dependency**: Backend Phase 1 완료 필요

**Priority 1 - Project Setup**:
1. React 프로젝트 생성 (Vite)
2. 디렉토리 구조 설정 (Atomic Design)
3. Zustand 스토어 설정
4. Axios 클라이언트 설정

**Priority 2 - Menu Browsing**:
5. Atoms (Button, Card, Image, Badge)
6. Molecules (MenuCard)
7. Organisms (MenuList, CategoryTabs)
8. MenuPage
9. useMenuStore

**Priority 3 - Cart Management**:
10. Molecules (CartItem)
11. Organisms (Cart)
12. CartPage
13. useCartStore (localStorage 동기화)

**Priority 4 - Order Creation**:
14. 주문 생성 API 연동
15. 주문 성공 처리

**Priority 5 - Order History**:
16. Molecules (OrderStatusBadge)
17. Organisms (OrderHistory)
18. OrderHistoryPage
19. useOrderStore

**Priority 6 - Real-time Updates**:
20. SSEClient 구현
21. 주문 상태 실시간 업데이트

**Validation**: Backend와 통합 테스트 (고객 주문 플로우)

---

### Phase 3: Admin Frontend (Unit 2)
**Duration**: 2-3 weeks

**Dependency**: Backend Phase 1 완료, Customer Frontend Phase 2 완료 권장

**Priority 1 - Project Setup**:
1. React 프로젝트 생성 (Vite)
2. 디렉토리 구조 설정
3. Zustand 스토어 설정
4. Axios 클라이언트 설정

**Priority 2 - Authentication**:
5. LoginPage
6. useAuthStore
7. JWT 토큰 관리

**Priority 3 - Order Monitoring**:
8. Molecules (TableCard, StatusDropdown)
9. Organisms (OrderDashboard)
10. DashboardPage
11. SSEClient 구현 (신규 주문 알림)

**Priority 4 - Order Management**:
12. 주문 상태 변경 기능
13. 주문 삭제 기능
14. 실시간 업데이트 (SSE)

**Priority 5 - Menu Management**:
15. Molecules (MenuForm)
16. Organisms (MenuManagement)
17. MenuManagementPage
18. 이미지 업로드 기능

**Priority 6 - Table Management**:
19. Organisms (TableManagement)
20. TableManagementPage
21. 세션 종료 기능

**Priority 7 - History**:
22. HistoryPage
23. 과거 주문 내역 조회

**Validation**: Backend와 통합 테스트 (전체 주문 플로우)

---

### Phase 4: Integration Testing
**Duration**: 1 week

**Scope**: 전체 시스템 통합 테스트

**Test Scenarios**:
1. 고객 주문 생성 → 관리자 실시간 알림 확인
2. 관리자 주문 상태 변경 → 고객 실시간 업데이트 확인
3. 관리자 메뉴 등록/수정/삭제 → 고객 화면 반영 확인
4. 관리자 세션 종료 → 주문 이력 이동 확인
5. 동시 접속 테스트 (여러 테이블, 여러 관리자)
6. SSE 재연결 테스트
7. 에러 처리 테스트 (네트워크 오류, 서버 오류)

---

## Dependency Management

### Backend Dependencies
- Spring Boot Starter Web
- Spring Boot Starter Security
- Spring Boot Starter WebFlux (SSE)
- MyBatis Spring Boot Starter
- H2 Database
- JWT Library (jjwt)
- Lombok
- Spring Boot Starter Test

### Customer Frontend Dependencies
- React
- React Router DOM
- Zustand
- Axios
- EventSource Polyfill (SSE)
- CSS Modules 또는 Styled Components

### Admin Frontend Dependencies
- React
- React Router DOM
- Zustand
- Axios
- EventSource Polyfill (SSE)
- CSS Modules 또는 Styled Components

---

## Risk Assessment

### High Risk Dependencies
1. **Backend → Customer Frontend (SSE)**
   - **Risk**: SSE 연결 불안정
   - **Mitigation**: 재연결 로직 구현, 폴백 메커니즘 (폴링)

2. **Backend → Admin Frontend (SSE)**
   - **Risk**: SSE 연결 불안정
   - **Mitigation**: 재연결 로직 구현, 폴백 메커니즘 (폴링)

### Medium Risk Dependencies
3. **Customer Frontend → Backend (REST API)**
   - **Risk**: 네트워크 오류, 서버 오류
   - **Mitigation**: 에러 처리, 재시도 로직, 사용자 피드백

4. **Admin Frontend → Backend (REST API)**
   - **Risk**: 네트워크 오류, 서버 오류
   - **Mitigation**: 에러 처리, 재시도 로직, 사용자 피드백

### Low Risk Dependencies
5. **Backend → Database (MyBatis)**
   - **Risk**: In-Memory DB 데이터 손실
   - **Mitigation**: 초기 데이터 스크립트, 데이터 백업 (선택적)

---

## Integration Testing Strategy

### Incremental Integration Approach

**Step 1: Backend Standalone**
- 모든 API 엔드포인트 테스트 (Postman, curl)
- SSE 연결 테스트 (curl, EventSource)
- 데이터베이스 CRUD 테스트

**Step 2: Backend + Customer Frontend**
- 메뉴 조회 통합 테스트
- 장바구니 기능 테스트
- 주문 생성 통합 테스트
- 주문 내역 조회 통합 테스트
- SSE 실시간 업데이트 테스트

**Step 3: Backend + Admin Frontend**
- 로그인 통합 테스트
- 주문 모니터링 통합 테스트
- 주문 상태 변경 통합 테스트
- 메뉴 관리 통합 테스트
- 테이블 관리 통합 테스트
- SSE 실시간 알림 테스트

**Step 4: Full System Integration**
- 고객 주문 → 관리자 처리 전체 플로우
- 다중 테이블 동시 주문 테스트
- 다중 관리자 동시 작업 테스트
- 세션 종료 및 이력 이동 테스트
- 에러 시나리오 테스트

---

## Notes

- 모든 유닛 간 통신은 REST API 또는 SSE를 통해 이루어짐
- 프론트엔드 유닛 간 직접 통신 없음 (완전히 독립적)
- Backend가 모든 비즈니스 로직과 데이터를 관리
- SSE는 실시간 업데이트를 위한 단방향 통신
- 개발 순서는 Backend → Customer Frontend → Admin Frontend 권장
- 통합 테스트는 점진적으로 진행 (Incremental Integration)

