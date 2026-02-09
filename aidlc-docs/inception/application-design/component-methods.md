# Component Methods

## Method Signatures Overview

이 문서는 각 컴포넌트의 주요 메서드 시그니처를 정의합니다. 상세한 비즈니스 로직은 Functional Design 단계에서 정의됩니다.

---

## Frontend Component Methods (React)

### Customer Interface

#### MenuPage
```typescript
interface MenuPageMethods {
  // 메뉴 목록 로드
  loadMenus(category?: string): Promise<Menu[]>
  
  // 장바구니에 메뉴 추가
  addToCart(menu: Menu, quantity: number): void
  
  // 카테고리 변경
  handleCategoryChange(category: string): void
}
```

#### CartPage
```typescript
interface CartPageMethods {
  // 장바구니 아이템 수량 증가
  increaseQuantity(itemId: string): void
  
  // 장바구니 아이템 수량 감소
  decreaseQuantity(itemId: string): void
  
  // 장바구니 아이템 제거
  removeItem(itemId: string): void
  
  // 주문 생성
  createOrder(): Promise<Order>
  
  // 총 금액 계산
  calculateTotal(): number
}
```

#### OrderHistoryPage
```typescript
interface OrderHistoryPageMethods {
  // 주문 내역 로드
  loadOrders(): Promise<Order[]>
  
  // 주문 상세 보기
  viewOrderDetail(orderId: string): void
}
```

---

### Admin Interface

#### DashboardPage
```typescript
interface DashboardPageMethods {
  // SSE 연결 초기화
  initializeSSE(): void
  
  // 주문 목록 로드
  loadOrders(): Promise<Order[]>
  
  // 주문 상태 변경
  updateOrderStatus(orderId: string, status: OrderStatus): Promise<void>
  
  // 주문 상세 보기
  viewOrderDetail(orderId: string): void
  
  // SSE 이벤트 처리
  handleOrderUpdate(event: OrderEvent): void
}
```

#### TableManagementPage
```typescript
interface TableManagementPageMethods {
  // 테이블 초기 설정
  setupTable(tableNumber: number, password: string): Promise<void>
  
  // 주문 삭제
  deleteOrder(orderId: string): Promise<void>
  
  // 테이블 세션 종료
  completeTableSession(tableId: string): Promise<void>
  
  // 과거 주문 내역 조회
  loadOrderHistory(tableId: string, dateFilter?: DateRange): Promise<OrderHistory[]>
}
```

#### MenuManagementPage
```typescript
interface MenuManagementPageMethods {
  // 메뉴 목록 로드
  loadMenus(): Promise<Menu[]>
  
  // 메뉴 생성
  createMenu(menuData: MenuInput): Promise<Menu>
  
  // 메뉴 수정
  updateMenu(menuId: string, menuData: MenuInput): Promise<Menu>
  
  // 메뉴 삭제
  deleteMenu(menuId: string): Promise<void>
  
  // 이미지 업로드
  uploadImage(file: File): Promise<string>
  
  // 메뉴 순서 변경
  reorderMenus(menuIds: string[]): Promise<void>
}
```

---

### Shared Components

#### LoginPage
```typescript
interface LoginPageMethods {
  // 관리자 로그인
  adminLogin(storeId: string, username: string, password: string): Promise<AuthToken>
  
  // 테이블 자동 로그인
  tableAutoLogin(): Promise<TableSession>
}
```

---

## Backend Component Methods (Python)

### Presentation Layer

#### CustomerController
```python
class CustomerController:
    # 메뉴 조회
    def get_menus(category: Optional[str] = None) -> List[Menu]:
        pass
    
    # 주문 생성
    def create_order(order_data: OrderInput) -> Order:
        pass
    
    # 주문 내역 조회
    def get_orders(table_id: str, session_id: str) -> List[Order]:
        pass
```

#### AdminController
```python
class AdminController:
    # 관리자 로그인
    def login(store_id: str, username: str, password: str) -> AuthToken:
        pass
    
    # 주문 목록 조회
    def get_orders(store_id: str) -> List[Order]:
        pass
    
    # 주문 상태 변경
    def update_order_status(order_id: str, status: OrderStatus) -> Order:
        pass
    
    # 주문 삭제
    def delete_order(order_id: str) -> None:
        pass
    
    # 테이블 세션 종료
    def complete_table_session(table_id: str) -> None:
        pass
    
    # 과거 주문 내역 조회
    def get_order_history(table_id: str, date_filter: Optional[DateRange]) -> List[OrderHistory]:
        pass
    
    # 메뉴 조회
    def get_menus(store_id: str) -> List[Menu]:
        pass
    
    # 메뉴 생성
    def create_menu(menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 수정
    def update_menu(menu_id: str, menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 삭제
    def delete_menu(menu_id: str) -> None:
        pass
```

#### SSEController
```python
class SSEController:
    # SSE 스트림 생성
    def create_stream(store_id: str) -> EventStream:
        pass
    
    # 주문 이벤트 브로드캐스트
    def broadcast_order_event(store_id: str, event: OrderEvent) -> None:
        pass
```

---

### Application Layer

#### MenuService
```python
class MenuService:
    # 카테고리별 메뉴 조회
    def get_menus_by_category(store_id: str, category: Optional[str]) -> List[Menu]:
        pass
    
    # 메뉴 상세 조회
    def get_menu_by_id(menu_id: str) -> Menu:
        pass
```

#### OrderService
```python
class OrderService:
    # 주문 생성
    def create_order(order_data: OrderInput) -> Order:
        pass
    
    # 주문 유효성 검증
    def validate_order(order_data: OrderInput) -> bool:
        pass
    
    # 주문 내역 조회
    def get_orders_by_session(table_id: str, session_id: str) -> List[Order]:
        pass
```

#### AdminAuthService
```python
class AdminAuthService:
    # 로그인 처리
    def login(store_id: str, username: str, password: str) -> AuthToken:
        pass
    
    # 비밀번호 검증
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        pass
    
    # JWT 토큰 생성
    def generate_token(store_id: str, username: str) -> str:
        pass
    
    # JWT 토큰 검증
    def verify_token(token: str) -> TokenPayload:
        pass
```

#### OrderManagementService
```python
class OrderManagementService:
    # 주문 상태 변경
    def update_order_status(order_id: str, status: OrderStatus) -> Order:
        pass
    
    # 주문 삭제
    def delete_order(order_id: str) -> None:
        pass
    
    # 실시간 주문 목록 조회
    def get_active_orders(store_id: str) -> List[Order]:
        pass
```

#### TableManagementService
```python
class TableManagementService:
    # 테이블 초기 설정
    def setup_table(store_id: str, table_number: int, password: str) -> Table:
        pass
    
    # 테이블 세션 종료
    def complete_session(table_id: str) -> None:
        pass
    
    # 과거 주문 내역 조회
    def get_order_history(table_id: str, date_filter: Optional[DateRange]) -> List[OrderHistory]:
        pass
```

#### MenuManagementService
```python
class MenuManagementService:
    # 메뉴 생성
    def create_menu(menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 수정
    def update_menu(menu_id: str, menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 삭제
    def delete_menu(menu_id: str) -> None:
        pass
    
    # 이미지 업로드 처리
    def upload_image(file: UploadFile) -> str:
        pass
    
    # 메뉴 순서 조정
    def reorder_menus(menu_ids: List[str]) -> None:
        pass
```

#### SSEService
```python
class SSEService:
    # SSE 연결 관리
    def add_connection(store_id: str, connection: SSEConnection) -> None:
        pass
    
    # SSE 연결 제거
    def remove_connection(store_id: str, connection: SSEConnection) -> None:
        pass
    
    # 주문 이벤트 브로드캐스트
    def broadcast_order_event(store_id: str, event: OrderEvent) -> None:
        pass
```

---

### Infrastructure Layer

#### StoreRepository
```python
class StoreRepository:
    # 매장 조회
    def get_by_id(store_id: str) -> Optional[Store]:
        pass
    
    # 매장 생성
    def create(store_data: StoreInput) -> Store:
        pass
```

#### TableRepository
```python
class TableRepository:
    # 테이블 조회
    def get_by_id(table_id: str) -> Optional[Table]:
        pass
    
    # 테이블 번호로 조회
    def get_by_number(store_id: str, table_number: int) -> Optional[Table]:
        pass
    
    # 테이블 생성
    def create(table_data: TableInput) -> Table:
        pass
    
    # 테이블 수정
    def update(table_id: str, table_data: TableInput) -> Table:
        pass
```

#### MenuRepository
```python
class MenuRepository:
    # 메뉴 조회
    def get_by_id(menu_id: str) -> Optional[Menu]:
        pass
    
    # 매장별 메뉴 조회
    def get_by_store(store_id: str, category: Optional[str]) -> List[Menu]:
        pass
    
    # 메뉴 생성
    def create(menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 수정
    def update(menu_id: str, menu_data: MenuInput) -> Menu:
        pass
    
    # 메뉴 삭제
    def delete(menu_id: str) -> None:
        pass
```

#### OrderRepository
```python
class OrderRepository:
    # 주문 조회
    def get_by_id(order_id: str) -> Optional[Order]:
        pass
    
    # 세션별 주문 조회
    def get_by_session(table_id: str, session_id: str) -> List[Order]:
        pass
    
    # 매장별 활성 주문 조회
    def get_active_orders(store_id: str) -> List[Order]:
        pass
    
    # 주문 생성
    def create(order_data: OrderInput) -> Order:
        pass
    
    # 주문 수정
    def update(order_id: str, order_data: OrderInput) -> Order:
        pass
    
    # 주문 삭제
    def delete(order_id: str) -> None:
        pass
```

#### OrderHistoryRepository
```python
class OrderHistoryRepository:
    # 이력 저장
    def create(history_data: OrderHistoryInput) -> OrderHistory:
        pass
    
    # 테이블별 이력 조회
    def get_by_table(table_id: str, date_filter: Optional[DateRange]) -> List[OrderHistory]:
        pass
```

#### FileStorage
```python
class FileStorage:
    # 파일 저장
    def save_file(file: UploadFile, directory: str) -> str:
        pass
    
    # 파일 삭제
    def delete_file(file_path: str) -> None:
        pass
    
    # 파일 경로 생성
    def generate_file_path(filename: str, directory: str) -> str:
        pass
```

---

## Type Definitions

### Common Types
```typescript
// Frontend Types
interface Menu {
  id: string
  name: string
  price: number
  description: string
  category: string
  imagePath: string
}

interface Order {
  id: string
  orderNumber: string
  tableId: string
  sessionId: string
  items: OrderItem[]
  totalAmount: number
  status: OrderStatus
  createdAt: Date
}

interface OrderItem {
  menuId: string
  menuName: string
  quantity: number
  unitPrice: number
}

enum OrderStatus {
  PENDING = 'pending',
  PREPARING = 'preparing',
  COMPLETED = 'completed'
}
```

```python
# Backend Types
from enum import Enum
from typing import Optional, List
from datetime import datetime

class OrderStatus(Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    COMPLETED = "completed"

class Menu:
    id: str
    store_id: str
    name: str
    price: float
    description: str
    category: str
    image_path: str

class Order:
    id: str
    store_id: str
    table_id: str
    session_id: str
    order_number: str
    total_amount: float
    status: OrderStatus
    created_at: datetime
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안

**Note**: 상세한 비즈니스 로직 및 알고리즘은 CONSTRUCTION 단계의 Functional Design에서 정의됩니다.
