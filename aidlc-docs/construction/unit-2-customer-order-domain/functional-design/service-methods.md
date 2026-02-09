# Service Methods - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 서비스 메서드 정의입니다. 각 서비스의 책임과 메서드 시그니처를 명시합니다.

---

## 1. MenuService (메뉴 조회 서비스)

### Purpose
메뉴 조회 및 필터링 비즈니스 로직 처리

### Dependencies
- MenuRepository (Unit 1)

---

### Method: getMenus()

**Purpose**: 메뉴 목록 조회 (카테고리 필터링 선택사항)

**Signature**:
```python
def get_menus(
    store_id: int,
    category_level1: Optional[str] = None,
    category_level2: Optional[str] = None
) -> List[Menu]:
```

**Parameters**:
- `store_id`: 매장 ID (필수)
- `category_level1`: Level 1 카테고리 (선택사항)
- `category_level2`: Level 2 카테고리 (선택사항)

**Returns**:
- `List[Menu]`: 판매 가능한 메뉴 목록

**Business Logic**:
1. MenuRepository를 통해 메뉴 조회
2. `is_available = true`인 메뉴만 필터링
3. 카테고리가 지정된 경우 해당 카테고리 메뉴만 반환
4. 메뉴 ID 순서로 정렬

**Error Handling**:
- 매장 ID가 존재하지 않으면: `StoreNotFoundError`
- 데이터베이스 에러: `DatabaseError`

---

### Method: getMenuById()

**Purpose**: 특정 메뉴 상세 조회

**Signature**:
```python
def get_menu_by_id(
    menu_id: int
) -> Menu:
```

**Parameters**:
- `menu_id`: 메뉴 ID (필수)

**Returns**:
- `Menu`: 메뉴 상세 정보

**Business Logic**:
1. MenuRepository를 통해 메뉴 조회
2. 메뉴가 존재하지 않으면 에러
3. 판매 불가 메뉴도 조회 가능 (주문 생성 시 검증용)

**Error Handling**:
- 메뉴가 존재하지 않으면: `MenuNotFoundError`

---

## 2. OrderService (주문 생성 및 조회 서비스)

### Purpose
주문 생성, 조회 비즈니스 로직 처리

### Dependencies
- OrderRepository (Unit 1)
- OrderItemRepository (Unit 1)
- MenuRepository (Unit 1)
- TableRepository (Unit 1)

---

### Method: createOrder()

**Purpose**: 주문 생성

**Signature**:
```python
def create_order(
    store_id: int,
    table_id: int,
    cart_items: List[CartItem]
) -> Order:
```

**Parameters**:
- `store_id`: 매장 ID (필수)
- `table_id`: 테이블 ID (필수)
- `cart_items`: 장바구니 항목 목록 (필수)

**CartItem Structure**:
```python
class CartItem:
    menu_id: int
    menu_snapshot: MenuSnapshot
    selected_options: List[SelectedOption]
    quantity: int
    subtotal: Decimal
```

**Returns**:
- `Order`: 생성된 주문 정보

**Business Logic**:
1. 장바구니 비어있지 않음 검증
2. 주문 번호 생성 (테이블별 순차)
3. Order 엔티티 생성 (status: PENDING)
4. CartItem을 OrderItem으로 변환
5. 총액 계산
6. 데이터베이스에 저장 (트랜잭션)
7. 생성된 주문 반환

**Order Number Generation**:
```python
def generate_order_number(table_id: int) -> str:
    table = get_table(table_id)
    last_order = get_last_order_by_table(table_id)
    
    if last_order is None:
        sequence = 1
    else:
        sequence = extract_sequence(last_order.order_number) + 1
    
    return f"T{table.table_number:02d}-{sequence:03d}"
```

**Error Handling**:
- 장바구니 비어있음: `EmptyCartError`
- 테이블이 존재하지 않음: `TableNotFoundError`
- 데이터베이스 에러: `DatabaseError`

---

### Method: getOrderHistory()

**Purpose**: 주문 내역 조회 (현재 세션)

**Signature**:
```python
def get_order_history(
    table_id: int,
    session_started_at: datetime
) -> List[Order]:
```

**Parameters**:
- `table_id`: 테이블 ID (필수)
- `session_started_at`: 세션 시작 시각 (필수)

**Returns**:
- `List[Order]`: 주문 목록 (시간 역순)

**Business Logic**:
1. OrderRepository를 통해 주문 조회
2. 현재 세션의 주문만 필터링 (created_at >= session_started_at)
3. 시간 역순으로 정렬
4. OrderItem 포함하여 반환

**Error Handling**:
- 테이블이 존재하지 않음: `TableNotFoundError`

---

### Method: getOrderById()

**Purpose**: 특정 주문 상세 조회

**Signature**:
```python
def get_order_by_id(
    order_id: int
) -> Order:
```

**Parameters**:
- `order_id`: 주문 ID (필수)

**Returns**:
- `Order`: 주문 상세 정보 (OrderItem 포함)

**Business Logic**:
1. OrderRepository를 통해 주문 조회
2. OrderItem 포함하여 반환

**Error Handling**:
- 주문이 존재하지 않음: `OrderNotFoundError`

---

## 3. SSEService (실시간 통신 서비스)

### Purpose
Server-Sent Events를 통한 실시간 주문 상태 업데이트

### Dependencies
- None (독립적인 서비스)

---

### Method: connect()

**Purpose**: SSE 연결 설정

**Signature**:
```python
async def connect(
    table_id: int
) -> EventSourceResponse:
```

**Parameters**:
- `table_id`: 테이블 ID (필수)

**Returns**:
- `EventSourceResponse`: SSE 연결 응답

**Business Logic**:
1. 테이블 ID로 SSE 연결 생성
2. Keep-alive 메시지 전송 (30초마다)
3. 연결 유지

**Error Handling**:
- 테이블이 존재하지 않음: `TableNotFoundError`
- 연결 실패: 자동 재연결 시도 (클라이언트 측)

---

### Method: sendOrderStatusUpdate()

**Purpose**: 주문 상태 변경 이벤트 전송

**Signature**:
```python
async def send_order_status_update(
    table_id: int,
    order_id: int,
    order_number: str,
    old_status: str,
    new_status: str
) -> None:
```

**Parameters**:
- `table_id`: 테이블 ID (필수)
- `order_id`: 주문 ID (필수)
- `order_number`: 주문 번호 (필수)
- `old_status`: 이전 상태 (필수)
- `new_status`: 새로운 상태 (필수)

**Returns**:
- None

**Business Logic**:
1. 해당 테이블의 SSE 연결 확인
2. 이벤트 데이터 생성
3. 이벤트 전송

**Event Data**:
```json
{
  "event": "order_status_changed",
  "data": {
    "order_id": 123,
    "order_number": "T01-001",
    "old_status": "PENDING",
    "new_status": "CONFIRMED"
  }
}
```

**Error Handling**:
- 연결이 존재하지 않음: 무시 (에러 발생 안 함)

---

## 4. CartService (장바구니 관리 서비스 - Frontend)

### Purpose
장바구니 상태 관리 (클라이언트 측)

### Dependencies
- SessionStorage

---

### Method: addToCart()

**Purpose**: 장바구니에 메뉴 추가

**Signature**:
```javascript
function addToCart(
  menu: Menu,
  selectedOptions: SelectedOption[],
  quantity: number = 1
): void
```

**Parameters**:
- `menu`: 메뉴 정보 (필수)
- `selectedOptions`: 선택된 옵션 목록 (필수)
- `quantity`: 수량 (기본값: 1)

**Returns**:
- None

**Business Logic**:
1. 필수 옵션 검증
2. 중복 항목 확인 (같은 메뉴 + 같은 옵션)
3. 중복이면 수량 증가, 아니면 새 항목 추가
4. 소계 계산
5. SessionStorage에 저장
6. 장바구니 아이콘 배지 업데이트

**Error Handling**:
- 필수 옵션 미선택: `RequiredOptionError`

---

### Method: updateQuantity()

**Purpose**: 장바구니 항목 수량 변경

**Signature**:
```javascript
function updateQuantity(
  cartItemId: string,
  newQuantity: number
): void
```

**Parameters**:
- `cartItemId`: 장바구니 항목 ID (필수)
- `newQuantity`: 새로운 수량 (필수)

**Returns**:
- None

**Business Logic**:
1. 수량이 0이면 항목 제거
2. 수량이 1 이상이면 수량 업데이트
3. 소계 재계산
4. 총액 재계산
5. SessionStorage에 저장

**Error Handling**:
- 항목이 존재하지 않음: `CartItemNotFoundError`
- 수량이 음수: `InvalidQuantityError`

---

### Method: removeFromCart()

**Purpose**: 장바구니에서 항목 제거

**Signature**:
```javascript
function removeFromCart(
  cartItemId: string
): void
```

**Parameters**:
- `cartItemId`: 장바구니 항목 ID (필수)

**Returns**:
- None

**Business Logic**:
1. 장바구니에서 항목 제거
2. 총액 재계산
3. SessionStorage에 저장

**Error Handling**:
- 항목이 존재하지 않음: `CartItemNotFoundError`

---

### Method: clearCart()

**Purpose**: 장바구니 비우기

**Signature**:
```javascript
function clearCart(): void
```

**Parameters**:
- None

**Returns**:
- None

**Business Logic**:
1. 장바구니 모든 항목 제거
2. SessionStorage에서 삭제

---

### Method: getCart()

**Purpose**: 장바구니 조회

**Signature**:
```javascript
function getCart(): Cart
```

**Parameters**:
- None

**Returns**:
- `Cart`: 장바구니 정보 (항목 목록, 총액)

**Business Logic**:
1. SessionStorage에서 장바구니 조회
2. 장바구니가 없으면 빈 장바구니 반환

---

### Method: getCartItemCount()

**Purpose**: 장바구니 항목 개수 조회

**Signature**:
```javascript
function getCartItemCount(): number
```

**Parameters**:
- None

**Returns**:
- `number`: 장바구니 항목 개수

**Business Logic**:
1. SessionStorage에서 장바구니 조회
2. 항목 개수 반환

---

## 5. ValidationService (유효성 검증 서비스 - Frontend)

### Purpose
클라이언트 측 유효성 검증

### Dependencies
- None

---

### Method: validateRequiredOptions()

**Purpose**: 필수 옵션 선택 검증

**Signature**:
```javascript
function validateRequiredOptions(
  menu: Menu,
  selectedOptions: SelectedOption[]
): ValidationResult
```

**Parameters**:
- `menu`: 메뉴 정보 (필수)
- `selectedOptions`: 선택된 옵션 목록 (필수)

**Returns**:
- `ValidationResult`: 검증 결과 (valid: boolean, errors: string[])

**Business Logic**:
1. 메뉴의 옵션 그룹 순회
2. `required = true`인 옵션 그룹 확인
3. 해당 옵션 그룹에서 선택된 항목이 있는지 확인
4. 없으면 에러 메시지 추가

---

### Method: validateCart()

**Purpose**: 장바구니 유효성 검증

**Signature**:
```javascript
function validateCart(
  cart: Cart
): ValidationResult
```

**Parameters**:
- `cart`: 장바구니 정보 (필수)

**Returns**:
- `ValidationResult`: 검증 결과 (valid: boolean, errors: string[])

**Business Logic**:
1. 장바구니가 비어있는지 확인
2. 각 항목의 수량이 1 이상인지 확인

---

## 6. Service Integration

### Integration Flow: 주문 생성

```
[CartService] → getCart()
    ↓
[ValidationService] → validateCart()
    ↓
[OrderService] → createOrder()
    ↓
[OrderRepository] → save()
    ↓
[SSEService] → sendOrderStatusUpdate() (관리자에게)
    ↓
[CartService] → clearCart()
```

---

### Integration Flow: 실시간 상태 업데이트

```
[관리자 UI] → 주문 상태 변경
    ↓
[OrderManagementService] → updateOrderStatus()
    ↓
[OrderRepository] → update()
    ↓
[SSEService] → sendOrderStatusUpdate()
    ↓
[고객 UI] → 주문 상태 업데이트
```

---

## 7. Error Handling Strategy

### Service-Level Errors

**MenuService**:
- `StoreNotFoundError`: 매장이 존재하지 않음
- `MenuNotFoundError`: 메뉴가 존재하지 않음
- `DatabaseError`: 데이터베이스 에러

**OrderService**:
- `EmptyCartError`: 장바구니가 비어있음
- `TableNotFoundError`: 테이블이 존재하지 않음
- `OrderNotFoundError`: 주문이 존재하지 않음
- `DatabaseError`: 데이터베이스 에러

**CartService** (Frontend):
- `RequiredOptionError`: 필수 옵션 미선택
- `CartItemNotFoundError`: 장바구니 항목이 존재하지 않음
- `InvalidQuantityError`: 수량이 유효하지 않음

**SSEService**:
- `TableNotFoundError`: 테이블이 존재하지 않음
- `ConnectionError`: 연결 실패 (자동 재연결)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
