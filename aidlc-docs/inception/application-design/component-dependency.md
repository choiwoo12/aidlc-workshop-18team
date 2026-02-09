# Component Dependencies

## Dependency Overview

이 문서는 컴포넌트 간 의존성 관계, 통신 패턴, 데이터 흐름을 정의합니다.

---

## Frontend Component Dependencies

### Customer Interface Dependencies

```
CustomerLayout
├── MenuPage
│   ├── MenuService (API)
│   ├── CartContext (State)
│   └── AuthContext (State)
├── CartPage
│   ├── OrderService (API)
│   ├── CartContext (State)
│   └── StorageService (Utility)
└── OrderHistoryPage
    ├── OrderService (API)
    └── AuthContext (State)
```

### Admin Interface Dependencies

```
AdminLayout
├── DashboardPage
│   ├── OrderService (API)
│   ├── SSEService (Real-time)
│   └── AuthContext (State)
├── TableManagementPage
│   ├── TableService (API)
│   ├── OrderService (API)
│   └── AuthContext (State)
└── MenuManagementPage
    ├── MenuService (API)
    └── AuthContext (State)
```

### Shared Component Dependencies

```
LoginPage
├── AuthService (API)
├── AuthContext (State)
└── StorageService (Utility)
```

---

## Backend Component Dependencies

### Clean Architecture Layers

```
Presentation Layer (Controllers)
    ↓ depends on
Application Layer (Services)
    ↓ depends on
Domain Layer (Entities)
    ↑ depends on
Infrastructure Layer (Repositories)
```

### Detailed Dependencies

#### CustomerController
```
CustomerController
├── MenuService
│   └── MenuRepository
├── OrderService
│   ├── OrderRepository
│   ├── MenuRepository
│   ├── TableRepository
│   └── SSEService
└── AuthMiddleware
```

#### AdminController
```
AdminController
├── AdminAuthService
│   └── StoreRepository
├── OrderManagementService
│   ├── OrderRepository
│   └── SSEService
├── TableManagementService
│   ├── TableRepository
│   ├── OrderRepository
│   └── OrderHistoryRepository
├── MenuManagementService
│   ├── MenuRepository
│   └── FileStorage
└── AuthMiddleware
```

#### SSEController
```
SSEController
└── SSEService
```

---

## Dependency Matrix

### Frontend Dependencies

| Component | MenuService | OrderService | TableService | AuthService | SSEService | CartContext | AuthContext |
|-----------|-------------|--------------|--------------|-------------|------------|-------------|-------------|
| MenuPage | ✓ | - | - | - | - | ✓ | ✓ |
| CartPage | - | ✓ | - | - | - | ✓ | - |
| OrderHistoryPage | - | ✓ | - | - | - | - | ✓ |
| DashboardPage | - | ✓ | - | - | ✓ | - | ✓ |
| TableManagementPage | - | ✓ | ✓ | - | - | - | ✓ |
| MenuManagementPage | ✓ | - | - | - | - | - | ✓ |
| LoginPage | - | - | - | ✓ | - | - | ✓ |

### Backend Dependencies

| Service | Repository | Other Services | External |
|---------|-----------|----------------|----------|
| MenuService | MenuRepository | - | - |
| OrderService | OrderRepository, MenuRepository, TableRepository | SSEService | - |
| AdminAuthService | StoreRepository | - | bcrypt, jwt |
| OrderManagementService | OrderRepository | SSEService | - |
| TableManagementService | TableRepository, OrderRepository, OrderHistoryRepository | - | - |
| MenuManagementService | MenuRepository | - | FileStorage |
| SSEService | - | - | - |

---

## Communication Patterns

### 1. REST API Communication

#### Customer → Backend
```
Customer UI Component
  → Frontend Service (MenuService, OrderService)
    → HTTP Request (Axios/Fetch)
      → Backend Controller (CustomerController)
        → Backend Service
          → Repository
            → Database
```

#### Admin → Backend
```
Admin UI Component
  → Frontend Service (OrderService, TableService, MenuService)
    → HTTP Request (Axios/Fetch)
      → Backend Controller (AdminController)
        → Backend Service
          → Repository
            → Database
```

### 2. Real-time Communication (SSE)

```
Backend SSEService
  → SSE Stream
    → Frontend SSEService
      → Event Handler
        → Admin UI Component
          → State Update
            → UI Re-render
```

### 3. State Management

#### Global State (Context API)
```
AuthContext Provider
  ├── Customer UI Components
  └── Admin UI Components

CartContext Provider
  └── Customer UI Components
```

#### Local State + SessionStorage
```
CartPage Component
  ├── Local State (React useState)
  └── SessionStorage (persistence)
```

---

## Data Flow Diagrams

### Customer Order Flow

```
[Customer UI]
    |
    | 1. Browse Menu
    v
[MenuService] → [GET /api/customer/menus] → [MenuService (Backend)]
    |                                              |
    |                                              v
    |                                        [MenuRepository]
    |                                              |
    | 2. Menu Data                                 v
    |<-----------------------------------------[Database]
    |
    | 3. Add to Cart
    v
[CartContext + SessionStorage]
    |
    | 4. Create Order
    v
[OrderService] → [POST /api/customer/orders] → [OrderService (Backend)]
    |                                                |
    |                                                v
    |                                          [OrderRepository]
    |                                                |
    |                                                v
    |                                          [Database]
    |                                                |
    |                                                v
    |                                          [SSEService]
    |                                                |
    | 5. Order Created                               v
    |<----------------------------------------[Admin UI (Real-time)]
    v
[Order Confirmation]
```

### Admin Order Management Flow

```
[Admin UI]
    |
    | 1. Connect SSE
    v
[SSEService] → [GET /api/admin/orders/stream] → [SSEController]
    |                                                  |
    |                                                  v
    |                                            [SSEService (Backend)]
    |                                                  |
    | 2. Real-time Updates                             |
    |<-------------------------------------------------|
    |
    | 3. Update Order Status
    v
[OrderService] → [PUT /api/admin/orders/:id/status] → [OrderManagementService]
    |                                                        |
    |                                                        v
    |                                                  [OrderRepository]
    |                                                        |
    |                                                        v
    |                                                  [Database]
    |                                                        |
    |                                                        v
    |                                                  [SSEService]
    |                                                        |
    | 4. Status Updated                                      v
    |<------------------------------------------------[All Admin Clients]
    v
[UI Update]
```

### Table Session Management Flow

```
[Admin UI]
    |
    | 1. Complete Table Session
    v
[TableService] → [POST /api/admin/tables/:id/complete] → [TableManagementService]
    |                                                           |
    |                                                           v
    |                                                     [OrderRepository]
    |                                                           |
    |                                                           v
    |                                                     [Get Session Orders]
    |                                                           |
    |                                                           v
    |                                                     [OrderHistoryRepository]
    |                                                           |
    |                                                           v
    |                                                     [Save to History]
    |                                                           |
    |                                                           v
    |                                                     [OrderRepository]
    |                                                           |
    |                                                           v
    |                                                     [Delete Session Orders]
    |                                                           |
    |                                                           v
    |                                                     [TableRepository]
    |                                                           |
    | 2. Session Completed                                      v
    |<------------------------------------------------[Reset Table Session]
    v
[UI Update]
```

---

## Dependency Injection Pattern

### Frontend (React)
```typescript
// Service instances created at app initialization
const authService = new AuthService()
const menuService = new MenuService()
const orderService = new OrderService()
const sseService = new SSEService()

// Provided via Context or props
<ServiceProvider services={{ authService, menuService, orderService, sseService }}>
  <App />
</ServiceProvider>
```

### Backend (Python)
```python
# Dependency injection via constructor
class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        menu_repository: MenuRepository,
        table_repository: TableRepository,
        sse_service: SSEService
    ):
        self.order_repository = order_repository
        self.menu_repository = menu_repository
        self.table_repository = table_repository
        self.sse_service = sse_service
```

---

## Circular Dependency Prevention

### Rules
1. **Presentation Layer** depends on **Application Layer** (not vice versa)
2. **Application Layer** depends on **Domain Layer** (not vice versa)
3. **Infrastructure Layer** implements interfaces defined in **Domain Layer**
4. **Services** do not depend on each other directly (use events or mediator pattern)

### Example: SSE Event Broadcasting
```
OrderService (creates order)
  → Emits OrderCreatedEvent
    → SSEService (listens to events)
      → Broadcasts to clients
```

---

## External Dependencies

### Frontend
- **React**: UI framework
- **React Router**: Routing
- **Axios**: HTTP client
- **Context API**: State management

### Backend
- **FastAPI/Django/Flask**: Web framework
- **bcrypt**: Password hashing
- **PyJWT**: JWT token handling
- **SQLite/Redis**: In-memory database

---

## Dependency Management Best Practices

### 1. Loose Coupling
- Components depend on interfaces, not concrete implementations
- Use dependency injection for flexibility

### 2. High Cohesion
- Related functionality grouped together
- Clear separation of concerns

### 3. Unidirectional Data Flow
- Data flows from parent to child components
- State updates propagate downward

### 4. Event-Driven Communication
- Use events for cross-cutting concerns (SSE, logging)
- Avoid tight coupling between services

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
