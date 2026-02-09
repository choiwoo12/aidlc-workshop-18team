# Code Generation Plan - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 코드 생성 계획입니다. 일반 방식(Standard)으로 진행하며, Unit 1의 기존 코드베이스에 Unit 2 기능을 추가합니다.

---

## Code Generation Strategy

### Approach
- **Method**: Standard (일반 방식)
- **Integration**: Unit 1 코드베이스에 Unit 2 기능 추가
- **Testing**: Build & Test 단계에서 작성

### Code Location
- **Backend**: `backend/app/` (Unit 1 구조 확장)
- **Frontend**: `frontend/src/` (Unit 1 구조 확장)
- **Documentation**: `aidlc-docs/construction/unit-2-customer-order-domain/code/`

---

## Execution Plan

### Phase 1: Backend Implementation (10 steps)
- [x] Step 1: Service Layer - Menu Service
- [x] Step 2: Utility - Order Number Generator
- [x] Step 3: Service Layer - Validation Service
- [x] Step 4: Service Layer - Order Service
- [x] Step 5: Service Layer - SSE Service
- [x] Step 6: API Controllers - Menu Controller
- [x] Step 7: API Controllers - Order Controller
- [x] Step 8: API Controllers - SSE Controller
- [x] Step 9: Main App Integration (SSE 라우트 추가)
- [x] Step 10: Backend Summary Documentation
- [ ] Step 6: API Controllers - Menu Controller
- [ ] Step 7: API Controllers - Order Controller
- [ ] Step 8: API Controllers - SSE Controller
- [ ] Step 9: Main App Integration (SSE 라우트 추가)
- [ ] Step 10: Backend Summary Documentation

### Phase 2: Frontend Implementation (12 steps)
- [x] Step 11: Services - Menu Service
- [x] Step 12: Services - Order Service
- [x] Step 13: Services - SSE Service
- [x] Step 14: Services - Cart Service
- [x] Step 15: Services - Validation Service
- [x] Step 16: Context - Cart Context
- [x] Step 17: Context - Order Context
- [x] Step 18: Pages - Menu Page
- [x] Step 19: Pages - Cart Page
- [x] Step 20: Pages - Order History Page
- [x] Step 21: App Integration (라우트 추가)
- [x] Step 22: Frontend Summary Documentation

### Phase 3: Documentation (1 step)
- [x] Step 23: Code Summary Documentation

**Total Steps**: 23 (모두 완료)

---

## Detailed Implementation Steps

### Backend Implementation

#### Step 1: Service Layer - Menu Service
**Purpose**: 메뉴 조회 비즈니스 로직

**Files to Create**:
- `backend/app/services/menu_service.py`

**Implementation**:
```python
from app.repositories.menu_repository import MenuRepository
from typing import List, Optional

class MenuService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository
    
    def get_available_menus(
        self, 
        store_id: int, 
        category: Optional[str] = None
    ) -> List[Menu]:
        """판매 가능한 메뉴 조회"""
        return self.menu_repository.find_available_menus(store_id, category)
    
    def get_menu_by_id(self, menu_id: int) -> Menu:
        """메뉴 상세 조회"""
        menu = self.menu_repository.get_by_id(menu_id)
        if not menu:
            raise ValueError("메뉴를 찾을 수 없습니다.")
        return menu
```

**Dependencies**: MenuRepository (Unit 1)

---

#### Step 2: Service Layer - Order Service
**Purpose**: 주문 생성 및 관리 비즈니스 로직

**Files to Create**:
- `backend/app/services/order_service.py`

**Implementation**:
```python
from app.repositories.order_repository import OrderRepository
from app.repositories.order_item_repository import OrderItemRepository
from app.services.order_number_generator import OrderNumberGenerator
from app.services.order_validation_service import OrderValidationService
from typing import List

class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
        order_item_repository: OrderItemRepository,
        order_number_generator: OrderNumberGenerator,
        validation_service: OrderValidationService
    ):
        self.order_repository = order_repository
        self.order_item_repository = order_item_repository
        self.order_number_generator = order_number_generator
        self.validation_service = validation_service
    
    def create_order(self, table_id: int, cart_items: List[dict]) -> Order:
        """주문 생성"""
        # 유효성 검증
        self.validation_service.validate_order_items(cart_items)
        
        # 주문 번호 생성
        table = self.table_repository.get_by_id(table_id)
        order_number = self.order_number_generator.generate(table.table_number)
        
        # Order 생성
        order = Order(
            table_id=table_id,
            order_number=order_number,
            status='PENDING',
            total_amount=sum(item['subtotal'] for item in cart_items)
        )
        order = self.order_repository.save(order)
        
        # OrderItem 생성
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                menu_id=item['menu_id'],
                menu_name_snapshot=item['menu_snapshot']['name'],
                menu_price_snapshot=item['menu_snapshot']['price'],
                selected_options=item['selected_options'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )
            self.order_item_repository.save(order_item)
        
        return order
    
    def get_orders_by_table(self, table_id: int) -> List[Order]:
        """테이블별 주문 내역 조회"""
        return self.order_repository.find_by_table(table_id)
```

**Dependencies**: OrderRepository, OrderItemRepository, OrderNumberGenerator, ValidationService (Unit 1)

---

#### Step 3: Service Layer - SSE Service
**Purpose**: SSE 이벤트 생성 및 브로드캐스트

**Files to Create**:
- `backend/app/services/sse_service.py`

**Implementation**:
```python
import asyncio
import json
from typing import AsyncGenerator

class SSEService:
    def __init__(self):
        self.connections = {}  # table_id -> list of queues
    
    async def event_generator(self, table_id: int) -> AsyncGenerator:
        """SSE 이벤트 생성기"""
        queue = asyncio.Queue()
        
        # 연결 등록
        if table_id not in self.connections:
            self.connections[table_id] = []
        self.connections[table_id].append(queue)
        
        try:
            while True:
                # Keep-alive (30초마다)
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(event)}\n\n"
                except asyncio.TimeoutError:
                    # Keep-alive 메시지
                    yield ":\n\n"
        finally:
            # 연결 해제
            self.connections[table_id].remove(queue)
    
    async def broadcast_order_status_change(
        self, 
        table_id: int, 
        order_id: int, 
        old_status: str, 
        new_status: str
    ):
        """주문 상태 변경 이벤트 브로드캐스트"""
        event = {
            "type": "order_status_changed",
            "order_id": order_id,
            "old_status": old_status,
            "new_status": new_status
        }
        
        if table_id in self.connections:
            for queue in self.connections[table_id]:
                await queue.put(event)
```

**Dependencies**: asyncio, json

---

#### Step 4: Service Layer - Validation Service
**Purpose**: 서버 측 데이터 유효성 검증

**Files to Create**:
- `backend/app/services/order_validation_service.py`

**Implementation**:
```python
from app.repositories.menu_repository import MenuRepository
from app.utils.exceptions import ValidationError

class OrderValidationService:
    def __init__(self, menu_repository: MenuRepository):
        self.menu_repository = menu_repository
    
    def validate_order_items(self, cart_items: list):
        """주문 항목 유효성 검증"""
        for item in cart_items:
            # 메뉴 존재 여부
            menu = self.menu_repository.get_by_id(item['menu_id'])
            if not menu:
                raise ValidationError("메뉴를 찾을 수 없습니다.")
            
            # 판매 가능 여부
            if not menu.is_available:
                raise ValidationError(
                    f"{menu.name}은(는) 현재 판매하지 않습니다."
                )
            
            # 가격 일치 확인
            if item['menu_snapshot']['price'] != menu.price:
                raise ValidationError(
                    "메뉴 가격이 변경되었습니다. 장바구니를 다시 확인해주세요."
                )
```

**Dependencies**: MenuRepository (Unit 1), ValidationError (Unit 1)

---

#### Step 5: Utility - Order Number Generator
**Purpose**: 주문 번호 생성

**Files to Create**:
- `backend/app/utils/order_number_generator.py`

**Implementation**:
```python
from app.repositories.order_repository import OrderRepository

class OrderNumberGenerator:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
    
    def generate(self, table_number: str) -> str:
        """주문 번호 생성: T{테이블번호}-{순차번호}"""
        last_order = self.order_repository.get_last_order_by_table(table_number)
        
        if last_order:
            last_seq = int(last_order.order_number.split('-')[1])
            next_seq = last_seq + 1
        else:
            next_seq = 1
        
        return f"T{table_number}-{next_seq:03d}"
```

**Dependencies**: OrderRepository (Unit 1)

---

#### Step 6-8: API Controllers
**Purpose**: REST API 엔드포인트

**Files to Create**:
- `backend/app/api/menu_controller.py`
- `backend/app/api/order_controller.py`
- `backend/app/api/sse_controller.py`

**Endpoints**:
- GET `/api/menus` - 메뉴 목록 조회
- GET `/api/menus/{menu_id}` - 메뉴 상세 조회
- POST `/api/orders` - 주문 생성
- GET `/api/orders` - 주문 내역 조회
- GET `/api/sse/orders/{table_id}` - SSE 연결

---

### Frontend Implementation

#### Step 11-15: Services
**Purpose**: API 호출 및 비즈니스 로직

**Files to Create**:
- `frontend/src/services/MenuService.js`
- `frontend/src/services/OrderService.js`
- `frontend/src/services/SSEService.js`
- `frontend/src/services/CartService.js`
- `frontend/src/services/ValidationService.js`

---

#### Step 16-17: Context
**Purpose**: 전역 상태 관리

**Files to Create**:
- `frontend/src/context/CartContext.jsx`
- `frontend/src/context/OrderContext.jsx`

---

#### Step 18-20: Pages
**Purpose**: 고객 화면

**Files to Create**:
- `frontend/src/pages/MenuPage.jsx`
- `frontend/src/pages/CartPage.jsx`
- `frontend/src/pages/OrderHistoryPage.jsx`

---

## Dependencies

### Backend Dependencies (추가)
```txt
# requirements.txt에 추가 없음 (Unit 1 의존성 재사용)
```

### Frontend Dependencies (추가)
```json
// package.json에 추가 없음 (Unit 1 의존성 재사용)
```

---

## Integration Points

### Backend Integration
- Unit 1 Repository 재사용 (Order, OrderItem, Menu, Table)
- Unit 1 Middleware 재사용 (Auth, Error)
- Unit 1 Database 재사용 (SQLite)

### Frontend Integration
- Unit 1 Axios 설정 재사용
- Unit 1 AuthContext 재사용
- Unit 1 공통 컴포넌트 재사용 (Button, Input, Loading, ErrorMessage, Modal)

---

## Validation Checklist

### Backend
- [ ] 모든 서비스 클래스 구현
- [ ] 모든 API 컨트롤러 구현
- [ ] SSE 이벤트 생성기 구현
- [ ] 유효성 검증 로직 구현
- [ ] 주문 번호 생성 로직 구현
- [ ] Main App에 라우트 추가

### Frontend
- [ ] 모든 서비스 클래스 구현
- [ ] 모든 Context 구현
- [ ] 모든 페이지 컴포넌트 구현
- [ ] SSE 연결 관리 구현
- [ ] 장바구니 관리 구현
- [ ] App.jsx에 라우트 추가

### Documentation
- [ ] Backend 코드 요약 문서
- [ ] Frontend 코드 요약 문서
- [ ] 통합 가이드 문서

---

## Next Steps

1. 계획 검토 및 승인
2. Part 2: Generation 실행 (23개 단계)
3. 코드 생성 완료 후 승인 요청

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 계획 수립 완료
