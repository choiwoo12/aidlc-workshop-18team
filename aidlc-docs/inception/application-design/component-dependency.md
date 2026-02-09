# Component Dependencies - 테이블오더 서비스

## Overview
컴포넌트 간 의존성 관계, 통신 패턴, 데이터 흐름을 정의합니다.

---

## 1. Dependency Matrix

### 1.1 Backend Dependencies

| Component | Depends On | Depended By |
|-----------|------------|-------------|
| **CustomerController** | OrderService, MenuService | - |
| **AdminController** | OrderService, MenuService, TableService, AuthService, FileService | - |
| **AuthController** | AuthService | - |
| **SSEController** | SSEService | - |
| **OrderService** | OrderMapper, MenuService, TableService, SSEService | CustomerController, AdminController |
| **MenuService** | MenuMapper, FileService | CustomerController, AdminController, OrderService |
| **TableService** | TableMapper, OrderMapper, OrderHistoryMapper | AdminController, OrderService |
| **AuthService** | UserMapper, JwtTokenProvider | AuthController, JwtAuthenticationFilter |
| **SSEService** | - | OrderService, MenuService, TableService, SSEController |
| **FileService** | FileStorageConfig | MenuService |
| **OrderMapper** | - | OrderService, TableService |
| **MenuMapper** | - | MenuService |
| **TableMapper** | - | TableService |
| **UserMapper** | - | AuthService |
| **OrderHistoryMapper** | - | TableService |
| **JwtTokenProvider** | - | AuthService, JwtAuthenticationFilter |
| **JwtAuthenticationFilter** | JwtTokenProvider, AuthService | - |
| **GlobalExceptionHandler** | - | All Controllers |

---

### 1.2 Frontend Dependencies

| Component | Depends On | Depended By |
|-----------|------------|-------------|
| **MenuPage** | ApiClient, useMenuStore, useCartStore | - |
| **CartPage** | ApiClient, useCartStore, useOrderStore | - |
| **OrderHistoryPage** | ApiClient, SSEClient, useOrderStore | - |
| **DashboardPage** | ApiClient, SSEClient, useOrderStore | - |
| **MenuManagementPage** | ApiClient, useMenuStore | - |
| **TableManagementPage** | ApiClient | - |
| **useAuthStore** | ApiClient, storage | All Pages |
| **useCartStore** | storage | MenuPage, CartPage |
| **useOrderStore** | ApiClient | CartPage, OrderHistoryPage, DashboardPage |
| **useMenuStore** | ApiClient | MenuPage, MenuManagementPage |
| **ApiClient** | useAuthStore | All Pages, All Stores |
| **SSEClient** | - | OrderHistoryPage, DashboardPage |

---

## 2. Communication Patterns

### 2.1 REST API Communication

#### Customer API
```
Frontend (Customer) → Backend
  GET  /api/customer/menus?storeId={storeId}
  GET  /api/customer/menus/{menuId}
  POST /api/customer/orders
  GET  /api/customer/orders?tableId={tableId}&sessionId={sessionId}
```

#### Admin API
```
Frontend (Admin) → Backend
  POST /api/admin/login
  GET  /api/admin/tables/orders?storeId={storeId}
  PUT  /api/admin/orders/{orderId}/status
  DELETE /api/admin/orders/{orderId}
  POST /api/admin/menus
  PUT  /api/admin/menus/{menuId}
  DELETE /api/admin/menus/{menuId}
  POST /api/admin/menus/images
  POST /api/admin/tables/setup
  POST /api/admin/tables/{tableId}/session/end
  GET  /api/admin/orders/history
```

---

### 2.2 SSE Communication

#### Customer SSE
```
Frontend (Customer) ← Backend
  GET /api/sse/customer/subscribe?tableId={tableId}&sessionId={sessionId}
  
  Events:
    - ORDER_STATUS_CHANGED: 주문 상태 변경 알림
    - SESSION_ENDED: 세션 종료 알림
```

#### Admin SSE
```
Frontend (Admin) ← Backend
  GET /api/sse/admin/subscribe?storeId={storeId}
  
  Events:
    - NEW_ORDER: 신규 주문 알림
    - ORDER_STATUS_CHANGED: 주문 상태 변경 알림
    - ORDER_DELETED: 주문 삭제 알림
```

---

### 2.3 Local Storage Communication

```
Frontend (React) ↔ Browser localStorage
  - auth_token: JWT 토큰
  - cart_items: 장바구니 아이템
  - table_info: 테이블 정보 (고객용)
```

---

## 3. Data Flow Diagrams

### 3.1 주문 생성 플로우

```
[Customer Frontend]
  ↓ 1. 장바구니에 메뉴 추가
[useCartStore]
  ↓ 2. localStorage에 저장
[Browser localStorage]

[Customer Frontend]
  ↓ 3. 주문하기 버튼 클릭
[ApiClient]
  ↓ 4. POST /api/customer/orders
[CustomerController]
  ↓ 5. createOrder()
[OrderService]
  ├─ 6. validateMenu() → [MenuService]
  ├─ 7. validateSession() → [TableService]
  ├─ 8. insertOrder() → [OrderMapper]
  ├─ 9. insertOrderItems() → [OrderMapper]
  └─ 10. broadcastEventToStore() → [SSEService]
[SSEService]
  ↓ 11. NEW_ORDER 이벤트 전송
[Admin Frontend]
  ↓ 12. 신규 주문 표시
[DashboardPage]
```

---

### 3.2 주문 상태 변경 플로우

```
[Admin Frontend]
  ↓ 1. 주문 상태 변경 버튼 클릭
[ApiClient]
  ↓ 2. PUT /api/admin/orders/{orderId}/status
[AdminController]
  ↓ 3. updateOrderStatus()
[OrderService]
  ├─ 4. selectOrderById() → [OrderMapper]
  ├─ 5. updateOrderStatus() → [OrderMapper]
  └─ 6. sendEvent() → [SSEService]
[SSEService]
  ↓ 7. ORDER_STATUS_CHANGED 이벤트 전송
[Customer Frontend]
  ↓ 8. 주문 상태 업데이트
[OrderHistoryPage]
```

---

### 3.3 메뉴 등록 플로우

```
[Admin Frontend]
  ↓ 1. 메뉴 정보 입력 및 이미지 선택
[MenuManagementPage]
  ↓ 2. 이미지 업로드
[ApiClient]
  ↓ 3. POST /api/admin/menus/images (MultipartFile)
[AdminController]
  ↓ 4. uploadImage()
[FileService]
  ├─ 5. validateFile()
  └─ 6. saveFile() → [File System]
[File System]
  ↑ 7. 파일 경로 반환
[AdminController]
  ↑ 8. 이미지 경로 응답
[MenuManagementPage]
  ↓ 9. 메뉴 등록 (이미지 경로 포함)
[ApiClient]
  ↓ 10. POST /api/admin/menus
[AdminController]
  ↓ 11. createMenu()
[MenuService]
  └─ 12. insertMenu() → [MenuMapper]
[MenuMapper]
  ↓ 13. 메뉴 저장
[Database]
```

---

### 3.4 세션 종료 플로우

```
[Admin Frontend]
  ↓ 1. 세션 종료 버튼 클릭
[ApiClient]
  ↓ 2. POST /api/admin/tables/{tableId}/session/end
[AdminController]
  ↓ 3. endSession()
[TableService]
  ├─ 4. selectOrdersByTableAndSession() → [OrderMapper]
  ├─ 5. insertOrderHistory() → [OrderHistoryMapper]
  ├─ 6. updateSessionStatus() → [TableMapper]
  └─ 7. sendEvent() → [SSEService] (선택적)
[Database]
  ↑ 8. 세션 종료 완료
[AdminController]
  ↑ 9. 성공 응답
[Admin Frontend]
```

---

## 4. Dependency Injection (Spring Boot)

### 4.1 Service Layer DI

```java
@Service
public class OrderService {
    private final OrderMapper orderMapper;
    private final MenuService menuService;
    private final TableService tableService;
    private final SSEService sseService;
    
    @Autowired
    public OrderService(
        OrderMapper orderMapper,
        MenuService menuService,
        TableService tableService,
        SSEService sseService
    ) {
        this.orderMapper = orderMapper;
        this.menuService = menuService;
        this.tableService = tableService;
        this.sseService = sseService;
    }
}
```

### 4.2 Controller Layer DI

```java
@RestController
@RequestMapping("/api/customer")
public class CustomerController {
    private final OrderService orderService;
    private final MenuService menuService;
    
    @Autowired
    public CustomerController(
        OrderService orderService,
        MenuService menuService
    ) {
        this.orderService = orderService;
        this.menuService = menuService;
    }
}
```

---

## 5. State Management (Zustand)

### 5.1 Store Dependencies

```typescript
// useCartStore
import { create } from 'zustand';
import { storage } from '@/utils/storage';

// useOrderStore
import { create } from 'zustand';
import { apiClient } from '@/services/apiClient';

// useMenuStore
import { create } from 'zustand';
import { apiClient } from '@/services/apiClient';

// useAuthStore
import { create } from 'zustand';
import { apiClient } from '@/services/apiClient';
import { storage } from '@/utils/storage';
```

### 5.2 Store Communication

```
useAuthStore
  ↓ 토큰 제공
ApiClient
  ↓ 인증된 요청
Backend API

useCartStore
  ↔ localStorage 동기화
Browser localStorage

useOrderStore
  ↓ API 호출
ApiClient
  ↓ 주문 데이터
Backend API
```

---

## 6. Component Interaction Patterns

### 6.1 Frontend Component Hierarchy

```
App
├─ CustomerLayout
│  ├─ MenuPage
│  │  ├─ CategoryTabs
│  │  └─ MenuList
│  │     └─ MenuCard (multiple)
│  ├─ CartPage
│  │  └─ Cart
│  │     └─ CartItem (multiple)
│  └─ OrderHistoryPage
│     └─ OrderHistory
│        └─ OrderCard (multiple)
└─ AdminLayout
   ├─ DashboardPage
   │  └─ OrderDashboard
   │     └─ TableCard (multiple)
   ├─ MenuManagementPage
   │  └─ MenuManagement
   │     ├─ DataTable
   │     └─ MenuForm
   └─ TableManagementPage
      └─ TableManagement
         └─ DataTable
```

### 6.2 Props Flow

```
MenuPage
  ↓ menus, onMenuClick
MenuList
  ↓ menu, onClick
MenuCard
  ↓ onClick event
MenuPage
  ↓ addToCart
useCartStore
```

### 6.3 Context API Usage

```
AuthContext
  ↓ user, token, isAuthenticated
All Pages (Consumer)

ThemeContext (선택적)
  ↓ theme, toggleTheme
All Components (Consumer)
```

---

## 7. Database Dependencies

### 7.1 Table Relationships

```
Store (매장)
  ↓ 1:N
Table (테이블)
  ↓ 1:N
Order (주문)
  ↓ 1:N
OrderItem (주문 항목)
  ↓ N:1
Menu (메뉴)
  ↑ N:1
Store (매장)

Order (주문)
  ↓ 1:1
OrderHistory (주문 이력)

Store (매장)
  ↓ 1:N
User (사용자)
```

### 7.2 MyBatis Mapper Dependencies

```
OrderMapper
  ↓ JOIN
MenuMapper (메뉴 정보 조회)

OrderMapper
  ↓ JOIN
TableMapper (테이블 정보 조회)

OrderHistoryMapper
  ↓ JOIN
OrderMapper (주문 정보 조회)
```

---

## 8. External Dependencies

### 8.1 Frontend Libraries

```
React
  ↓ UI 렌더링
React DOM

Zustand
  ↓ 상태 관리
React Components

Axios
  ↓ HTTP 통신
Backend API

SSE Library
  ↓ 실시간 통신
Backend SSE Endpoint

React Router
  ↓ 라우팅
React Components
```

### 8.2 Backend Libraries

```
Spring Boot
  ↓ 프레임워크
All Components

MyBatis
  ↓ ORM
Database (H2)

JWT Library
  ↓ 토큰 생성/검증
AuthService

BCrypt
  ↓ 비밀번호 해싱
AuthService

H2 Database
  ↓ 데이터 저장
All Mappers
```

---

## 9. Circular Dependency Prevention

### 9.1 금지된 의존성

```
❌ OrderService → MenuService → OrderService
❌ TableService → OrderService → TableService
❌ useCartStore → useOrderStore → useCartStore
```

### 9.2 의존성 방향 규칙

```
✅ Controller → Service → Repository
✅ Service → Service (단방향)
✅ Service → Common Components
✅ Pages → Stores → Services
```

---

## 10. Dependency Summary

### 10.1 High-Level Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (React)                │
│  ┌─────────────────────────────────┐   │
│  │  Pages → Stores → Services      │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
              ↓ HTTP/SSE
┌─────────────────────────────────────────┐
│         Backend (Spring Boot)           │
│  ┌─────────────────────────────────┐   │
│  │  Controller → Service → Mapper  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
              ↓ SQL
┌─────────────────────────────────────────┐
│         Database (H2)                   │
└─────────────────────────────────────────┘
```

### 10.2 Key Dependency Principles

1. **Layered Architecture**: 각 레이어는 바로 아래 레이어에만 의존
2. **Dependency Inversion**: 고수준 모듈은 저수준 모듈에 의존하지 않음
3. **Single Direction**: 의존성은 단방향으로 흐름
4. **Loose Coupling**: 컴포넌트 간 결합도 최소화
5. **High Cohesion**: 관련 기능은 같은 컴포넌트에 응집

---

## Notes

- 순환 의존성은 엄격히 금지
- 의존성 방향은 항상 상위 레이어 → 하위 레이어
- 공통 컴포넌트는 어디서든 의존 가능
- 상세한 데이터 흐름은 Functional Design에서 정의
