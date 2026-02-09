# Unit of Work Dependencies

## Dependency Matrix

| Unit | Depends On | Provides To | Dependency Type |
|------|------------|-------------|-----------------|
| Unit 1: Shared Foundation | None | Unit 2, Unit 3 | Foundation (Entities, Auth, DB) |
| Unit 2: Customer Order Domain | Unit 1 | Unit 3 | SSE Service |
| Unit 3: Admin Operations Domain | Unit 1, Unit 2 | None | Consumer |

---

## Detailed Dependencies

### Unit 1: Shared Foundation

**Dependencies**: None (기반 유닛)

**Provides**:
- **To Unit 2**:
  - Domain Entities (Store, Table, Menu, Order, OrderItem)
  - Repositories (MenuRepository, OrderRepository, TableRepository)
  - Database connection
  - AuthContext
  - Common UI Components
  - StorageService, ValidationService
  
- **To Unit 3**:
  - All Domain Entities (including OrderHistory)
  - All Repositories
  - Database connection
  - AdminAuthService
  - AuthMiddleware
  - FileStorage
  - AuthContext
  - Common UI Components

**Interface**:
```python
# Backend Exports
from domain import Store, Table, Menu, Order, OrderItem, OrderHistory
from infrastructure.repositories import (
    StoreRepository,
    TableRepository,
    MenuRepository,
    OrderRepository,
    OrderHistoryRepository
)
from infrastructure import Database, FileStorage
from application.auth import AdminAuthService
from presentation.middleware import AuthMiddleware, ErrorMiddleware
```

```typescript
// Frontend Exports
export { Button, Input, Modal, Loading, ErrorMessage, ConfirmDialog } from './shared/components'
export { AuthService, StorageService, ValidationService } from './shared/services'
export { AuthContext, useAuth } from './shared/context'
export { LoginPage } from './shared/pages'
```

---

### Unit 2: Customer Order Domain

**Dependencies**:
- **Unit 1**:
  - Menu, Order, OrderItem, Table entities
  - MenuRepository, OrderRepository, TableRepository
  - Database connection
  - AuthContext (테이블 자동 로그인)
  - Common UI Components
  - StorageService (장바구니 영속성)
  - ValidationService (주문 유효성 검증)

**Provides**:
- **To Unit 3**:
  - SSEService (실시간 주문 업데이트 브로드캐스트)
  - OrderService (주문 데이터 접근)

**Interface**:
```python
# Backend Exports
from application.customer import MenuService, OrderService
from application.realtime import SSEService
from presentation import CustomerController, SSEController
```

```typescript
// Frontend Exports
export { MenuPage, CartPage, OrderHistoryPage } from './customer/components'
export { CustomerLayout } from './customer/layout'
export { MenuService, OrderService, SSEService } from './customer/services'
export { CartContext, useCart } from './customer/context'
```

---

### Unit 3: Admin Operations Domain

**Dependencies**:
- **Unit 1**:
  - All Domain Entities
  - All Repositories
  - Database connection
  - AdminAuthService (관리자 인증)
  - AuthMiddleware (API 보호)
  - FileStorage (이미지 업로드)
  - AuthContext
  - Common UI Components
  
- **Unit 2**:
  - SSEService (실시간 주문 업데이트 수신)
  - OrderService (주문 데이터 조회)

**Provides**: None (최종 소비자)

**Interface**:
```python
# Backend Exports
from application.admin import (
    OrderManagementService,
    TableManagementService,
    MenuManagementService
)
from presentation import AdminController
```

```typescript
// Frontend Exports
export { DashboardPage, TableManagementPage, MenuManagementPage } from './admin/components'
export { AdminLayout } from './admin/layout'
export { TableService } from './admin/services'
```

---

## Dependency Graph

```
Unit 1: Shared Foundation
    |
    |-- Provides Entities, Repositories, Auth, DB
    |
    +----> Unit 2: Customer Order Domain
    |          |
    |          |-- Uses: Menu, Order, Table entities
    |          |-- Uses: MenuRepository, OrderRepository
    |          |-- Provides: SSEService
    |          |
    |          +----> Unit 3: Admin Operations Domain
    |                     |
    +---------------------|-- Uses: All Entities, All Repositories
                          |-- Uses: AdminAuthService, FileStorage
                          |-- Uses: SSEService (from Unit 2)
```

---

## Communication Patterns

### Unit 1 → Unit 2
**Pattern**: Direct Import (Shared Library)

```python
# Unit 2 imports from Unit 1
from domain import Menu, Order, OrderItem, Table
from infrastructure.repositories import MenuRepository, OrderRepository, TableRepository
from infrastructure import Database
```

```typescript
// Unit 2 imports from Unit 1
import { AuthContext } from '@/shared/context'
import { Button, Modal } from '@/shared/components'
import { StorageService } from '@/shared/services'
```

---

### Unit 1 → Unit 3
**Pattern**: Direct Import (Shared Library)

```python
# Unit 3 imports from Unit 1
from domain import Store, Table, Menu, Order, OrderHistory
from infrastructure.repositories import (
    StoreRepository,
    TableRepository,
    MenuRepository,
    OrderRepository,
    OrderHistoryRepository
)
from infrastructure import FileStorage
from application.auth import AdminAuthService
from presentation.middleware import AuthMiddleware
```

```typescript
// Unit 3 imports from Unit 1
import { AuthContext } from '@/shared/context'
import { Button, Modal, ConfirmDialog } from '@/shared/components'
import { ValidationService } from '@/shared/services'
```

---

### Unit 2 → Unit 3
**Pattern**: Event-Driven (SSE) + Direct Import

**SSE Event Flow**:
```
Customer creates order (Unit 2)
    → OrderService.create_order()
        → SSEService.broadcast_order_event()
            → Admin Dashboard (Unit 3) receives event
                → Updates UI in real-time
```

**Direct Import**:
```python
# Unit 3 imports SSEService from Unit 2
from application.realtime import SSEService

# AdminController uses SSEService
class AdminController:
    def __init__(self, sse_service: SSEService):
        self.sse_service = sse_service
```

```typescript
// Unit 3 imports SSEService from Unit 2
import { SSEService } from '@/customer/services'

// DashboardPage uses SSEService
const sseService = new SSEService()
sseService.connect(storeId, handleOrderUpdate)
```

---

## Dependency Management

### Build Order
1. **Unit 1**: Build first (no dependencies)
2. **Unit 2**: Build after Unit 1 (depends on Unit 1)
3. **Unit 3**: Build after Unit 1 and Unit 2 (depends on both)

### Import Rules
- **Unit 1**: Cannot import from Unit 2 or Unit 3
- **Unit 2**: Can import from Unit 1 only
- **Unit 3**: Can import from Unit 1 and Unit 2

### Circular Dependency Prevention
- **Rule**: Lower-numbered units cannot depend on higher-numbered units
- **Enforcement**: Import path validation in build process
- **Example**: Unit 1 cannot import from Unit 2 or Unit 3

---

## Integration Testing Strategy

### Unit 1 Integration Tests
- Database connection and Repository CRUD
- Auth service with database
- File storage operations

### Unit 2 Integration Tests
- Menu service with MenuRepository
- Order service with OrderRepository and SSEService
- Customer UI with backend API

### Unit 3 Integration Tests
- Order management with OrderRepository and SSEService
- Table management with TableRepository and OrderHistoryRepository
- Menu management with MenuRepository and FileStorage
- Admin UI with backend API

### Cross-Unit Integration Tests
- **Unit 2 + Unit 3**: 
  - Customer creates order → Admin receives real-time update
  - Admin changes order status → Customer sees updated status
- **Unit 1 + Unit 2 + Unit 3**:
  - End-to-end flow: Login → Order → Manage → Complete

---

## Deployment Dependencies

### Docker Compose Services
```yaml
services:
  backend:
    build: ./backend
    depends_on:
      - database
    # Unit 1, 2, 3 all in one service (Monolithic)
  
  frontend:
    build: ./frontend
    depends_on:
      - backend
    # Unit 1, 2, 3 all in one service (Single Page App)
  
  database:
    image: redis:latest
    # Or SQLite (file-based, no separate service needed)
```

### Startup Order
1. Database service
2. Backend service (includes all units)
3. Frontend service (includes all units)

---

## Dependency Injection

### Backend (Python)
```python
# Dependency injection container
class Container:
    def __init__(self):
        # Unit 1
        self.database = Database()
        self.store_repository = StoreRepository(self.database)
        self.table_repository = TableRepository(self.database)
        self.menu_repository = MenuRepository(self.database)
        self.order_repository = OrderRepository(self.database)
        self.order_history_repository = OrderHistoryRepository(self.database)
        self.file_storage = FileStorage()
        self.admin_auth_service = AdminAuthService(self.store_repository)
        
        # Unit 2
        self.menu_service = MenuService(self.menu_repository)
        self.sse_service = SSEService()
        self.order_service = OrderService(
            self.order_repository,
            self.menu_repository,
            self.table_repository,
            self.sse_service
        )
        
        # Unit 3
        self.order_management_service = OrderManagementService(
            self.order_repository,
            self.sse_service
        )
        self.table_management_service = TableManagementService(
            self.table_repository,
            self.order_repository,
            self.order_history_repository
        )
        self.menu_management_service = MenuManagementService(
            self.menu_repository,
            self.file_storage
        )
```

### Frontend (React)
```typescript
// Service provider
const ServiceContext = createContext({
  // Unit 1
  authService: new AuthService(),
  storageService: new StorageService(),
  validationService: new ValidationService(),
  
  // Unit 2
  menuService: new MenuService(),
  orderService: new OrderService(),
  sseService: new SSEService(),
  
  // Unit 3
  tableService: new TableService(),
})

// App.tsx
<ServiceContext.Provider value={services}>
  <AuthContext.Provider>
    <CartContext.Provider>
      <App />
    </CartContext.Provider>
  </AuthContext.Provider>
</ServiceContext.Provider>
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
