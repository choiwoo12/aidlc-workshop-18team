# Component Methods - 테이블오더 서비스

## Overview
각 컴포넌트의 주요 메서드 시그니처를 정의합니다. 상세한 비즈니스 규칙은 Functional Design 단계에서 정의됩니다.

---

## 1. Frontend Component Methods (React)

### 1.1 Customer Pages

#### MenuPage
```typescript
// 메뉴 목록 조회
fetchMenus(): Promise<Menu[]>

// 카테고리 변경
handleCategoryChange(category: string): void

// 메뉴 클릭 (상세 보기)
handleMenuClick(menuId: string): void

// 장바구니에 추가
handleAddToCart(menu: Menu, quantity: number): void
```

#### CartPage
```typescript
// 장바구니 조회
getCartItems(): CartItem[]

// 수량 증가
handleIncreaseQuantity(menuId: string): void

// 수량 감소
handleDecreaseQuantity(menuId: string): void

// 아이템 삭제
handleRemoveItem(menuId: string): void

// 장바구니 비우기
handleClearCart(): void

// 주문 생성
handleCheckout(): Promise<Order>
```

#### OrderHistoryPage
```typescript
// 주문 내역 조회
fetchOrders(): Promise<Order[]>

// SSE 연결 (실시간 업데이트)
connectSSE(): void

// SSE 연결 해제
disconnectSSE(): void

// 주문 상태 업데이트 처리
handleOrderStatusUpdate(order: Order): void
```

---

### 1.2 Admin Pages

#### LoginPage
```typescript
// 로그인
handleLogin(credentials: LoginCredentials): Promise<AuthResponse>

// 로그인 실패 처리
handleLoginError(error: Error): void
```

#### DashboardPage
```typescript
// 테이블별 주문 현황 조회
fetchTableOrders(): Promise<TableOrder[]>

// SSE 연결 (실시간 주문 수신)
connectSSE(): void

// SSE 연결 해제
disconnectSSE(): void

// 신규 주문 수신 처리
handleNewOrder(order: Order): void

// 테이블 카드 클릭 (상세 보기)
handleTableClick(tableId: string): void

// 주문 상태 변경
handleStatusChange(orderId: string, newStatus: OrderStatus): Promise<void>

// 테이블 필터링
handleTableFilter(tableNumber: string): void
```

#### MenuManagementPage
```typescript
// 메뉴 목록 조회
fetchMenus(): Promise<Menu[]>

// 메뉴 등록
handleAddMenu(menu: MenuInput): Promise<Menu>

// 메뉴 수정
handleEditMenu(menuId: string, menu: MenuInput): Promise<Menu>

// 메뉴 삭제
handleDeleteMenu(menuId: string): Promise<void>

// 이미지 업로드
handleImageUpload(file: File): Promise<string>

// 메뉴 순서 변경
handleReorderMenu(menuId: string, newOrder: number): Promise<void>
```

#### TableManagementPage
```typescript
// 테이블 목록 조회
fetchTables(): Promise<Table[]>

// 테이블 초기 설정
handleTableSetup(tableSetup: TableSetup): Promise<Table>

// 세션 종료
handleSessionEnd(tableId: string): Promise<void>

// 주문 삭제
handleDeleteOrder(orderId: string): Promise<void>

// 과거 주문 내역 조회
fetchOrderHistory(tableId: string, dateRange?: DateRange): Promise<OrderHistory[]>
```

---

### 1.3 Shared Services

#### ApiClient
```typescript
// GET 요청
get<T>(url: string, config?: AxiosRequestConfig): Promise<T>

// POST 요청
post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>

// PUT 요청
put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>

// DELETE 요청
delete<T>(url: string, config?: AxiosRequestConfig): Promise<T>

// 요청 인터셉터 (토큰 추가)
requestInterceptor(config: AxiosRequestConfig): AxiosRequestConfig

// 응답 인터셉터 (에러 처리)
responseInterceptor(response: AxiosResponse): AxiosResponse

// 에러 인터셉터
errorInterceptor(error: AxiosError): Promise<never>
```

#### SSEClient
```typescript
// SSE 연결
connect(url: string, options?: SSEOptions): EventSource

// SSE 연결 해제
disconnect(): void

// 이벤트 리스너 등록
addEventListener(eventType: string, handler: (event: MessageEvent) => void): void

// 이벤트 리스너 제거
removeEventListener(eventType: string, handler: (event: MessageEvent) => void): void

// 재연결 처리
handleReconnect(): void

// 연결 상태 확인
isConnected(): boolean
```

---

### 1.4 Zustand Stores

#### useAuthStore
```typescript
// 로그인
login(credentials: LoginCredentials): Promise<void>

// 로그아웃
logout(): void

// 토큰 갱신
refreshToken(): Promise<void>

// 인증 상태 확인
isAuthenticated(): boolean

// 사용자 정보 조회
getUser(): User | null
```

#### useCartStore
```typescript
// 아이템 추가
addItem(menu: Menu, quantity: number): void

// 아이템 제거
removeItem(menuId: string): void

// 수량 업데이트
updateQuantity(menuId: string, quantity: number): void

// 장바구니 비우기
clearCart(): void

// 총 금액 계산
getTotalAmount(): number

// 아이템 개수 조회
getItemCount(): number

// localStorage 동기화
syncToLocalStorage(): void

// localStorage에서 로드
loadFromLocalStorage(): void
```

#### useOrderStore
```typescript
// 주문 생성
createOrder(orderInput: OrderInput): Promise<Order>

// 주문 목록 조회
fetchOrders(): Promise<Order[]>

// 주문 상태 업데이트
updateOrderStatus(orderId: string, status: OrderStatus): void

// 현재 주문 설정
setCurrentOrder(order: Order): void

// 현재 주문 조회
getCurrentOrder(): Order | null
```

#### useMenuStore
```typescript
// 메뉴 목록 조회
fetchMenus(): Promise<Menu[]>

// 메뉴 추가
addMenu(menu: MenuInput): Promise<Menu>

// 메뉴 수정
updateMenu(menuId: string, menu: MenuInput): Promise<Menu>

// 메뉴 삭제
deleteMenu(menuId: string): Promise<void>

// 카테고리별 메뉴 조회
getMenusByCategory(category: string): Menu[]

// 메뉴 검색
searchMenus(keyword: string): Menu[]
```

---

## 2. Backend Component Methods (Spring Boot)

### 2.1 Controller Layer

#### CustomerController
```java
// 메뉴 목록 조회
@GetMapping("/menus")
ResponseEntity<List<MenuDTO>> getMenus(@RequestParam String storeId)

// 메뉴 상세 조회
@GetMapping("/menus/{menuId}")
ResponseEntity<MenuDTO> getMenu(@PathVariable String menuId)

// 주문 생성
@PostMapping("/orders")
ResponseEntity<OrderDTO> createOrder(@RequestBody OrderRequest request)

// 주문 내역 조회
@GetMapping("/orders")
ResponseEntity<List<OrderDTO>> getOrders(
    @RequestParam String tableId,
    @RequestParam String sessionId
)
```

#### AdminController
```java
// 로그인
@PostMapping("/login")
ResponseEntity<AuthResponse> login(@RequestBody LoginRequest request)

// 테이블별 주문 현황 조회
@GetMapping("/tables/orders")
ResponseEntity<List<TableOrderDTO>> getTableOrders(@RequestParam String storeId)

// 주문 상태 변경
@PutMapping("/orders/{orderId}/status")
ResponseEntity<OrderDTO> updateOrderStatus(
    @PathVariable String orderId,
    @RequestBody StatusUpdateRequest request
)

// 주문 삭제
@DeleteMapping("/orders/{orderId}")
ResponseEntity<Void> deleteOrder(@PathVariable String orderId)

// 메뉴 등록
@PostMapping("/menus")
ResponseEntity<MenuDTO> createMenu(@RequestBody MenuRequest request)

// 메뉴 수정
@PutMapping("/menus/{menuId}")
ResponseEntity<MenuDTO> updateMenu(
    @PathVariable String menuId,
    @RequestBody MenuRequest request
)

// 메뉴 삭제
@DeleteMapping("/menus/{menuId}")
ResponseEntity<Void> deleteMenu(@PathVariable String menuId)

// 이미지 업로드
@PostMapping("/menus/images")
ResponseEntity<ImageUploadResponse> uploadImage(@RequestParam("file") MultipartFile file)

// 테이블 초기 설정
@PostMapping("/tables/setup")
ResponseEntity<TableDTO> setupTable(@RequestBody TableSetupRequest request)

// 세션 종료
@PostMapping("/tables/{tableId}/session/end")
ResponseEntity<Void> endSession(@PathVariable String tableId)

// 과거 주문 내역 조회
@GetMapping("/orders/history")
ResponseEntity<List<OrderHistoryDTO>> getOrderHistory(
    @RequestParam String tableId,
    @RequestParam(required = false) LocalDate startDate,
    @RequestParam(required = false) LocalDate endDate
)
```

#### SSEController
```java
// SSE 연결 (고객용)
@GetMapping("/customer/subscribe")
SseEmitter subscribeCustomer(
    @RequestParam String tableId,
    @RequestParam String sessionId
)

// SSE 연결 (관리자용)
@GetMapping("/admin/subscribe")
SseEmitter subscribeAdmin(@RequestParam String storeId)
```

---

### 2.2 Service Layer

#### OrderService
```java
// 주문 생성
Order createOrder(OrderRequest request)

// 주문 조회 (ID)
Order getOrderById(String orderId)

// 주문 목록 조회 (테이블, 세션)
List<Order> getOrdersByTableAndSession(String tableId, String sessionId)

// 주문 상태 변경
Order updateOrderStatus(String orderId, OrderStatus newStatus)

// 주문 삭제
void deleteOrder(String orderId)

// 테이블별 주문 현황 조회
List<TableOrder> getTableOrders(String storeId)

// 주문 총액 계산
BigDecimal calculateTotalAmount(List<OrderItem> items)

// 주문 검증
void validateOrder(OrderRequest request)
```

#### MenuService
```java
// 메뉴 목록 조회
List<Menu> getMenusByStore(String storeId)

// 메뉴 조회 (ID)
Menu getMenuById(String menuId)

// 메뉴 등록
Menu createMenu(MenuRequest request)

// 메뉴 수정
Menu updateMenu(String menuId, MenuRequest request)

// 메뉴 삭제
void deleteMenu(String menuId)

// 메뉴 순서 변경
void reorderMenu(String menuId, int newOrder)

// 카테고리별 메뉴 조회
List<Menu> getMenusByCategory(String storeId, String category)

// 메뉴 검증
void validateMenu(MenuRequest request)
```

#### TableService
```java
// 테이블 목록 조회
List<Table> getTablesByStore(String storeId)

// 테이블 조회 (ID)
Table getTableById(String tableId)

// 테이블 초기 설정
Table setupTable(TableSetupRequest request)

// 세션 시작
String startSession(String tableId)

// 세션 종료
void endSession(String tableId)

// 세션 검증
boolean validateSession(String tableId, String sessionId)

// 테이블 PIN 검증
boolean validateTablePin(String tableId, String pin)
```

#### AuthService
```java
// 로그인 검증
User authenticate(String username, String password)

// JWT 토큰 생성
String generateToken(User user)

// JWT 토큰 검증
boolean validateToken(String token)

// 토큰에서 사용자 정보 추출
User getUserFromToken(String token)

// 비밀번호 해싱
String hashPassword(String password)

// 비밀번호 검증
boolean verifyPassword(String rawPassword, String hashedPassword)
```

#### SSEService
```java
// 클라이언트 연결 등록
void registerClient(String clientId, SseEmitter emitter)

// 클라이언트 연결 해제
void unregisterClient(String clientId)

// 이벤트 전송 (특정 클라이언트)
void sendEvent(String clientId, String eventType, Object data)

// 이벤트 브로드캐스트 (모든 클라이언트)
void broadcastEvent(String eventType, Object data)

// 이벤트 브로드캐스트 (매장별)
void broadcastEventToStore(String storeId, String eventType, Object data)

// 연결 상태 확인
boolean isClientConnected(String clientId)

// 타임아웃 처리
void handleTimeout(String clientId)
```

#### FileService
```java
// 파일 저장
String saveFile(MultipartFile file, String directory)

// 파일 삭제
void deleteFile(String filePath)

// 파일 검증 (형식, 크기)
void validateFile(MultipartFile file)

// 파일 경로 생성
String generateFilePath(String fileName, String directory)

// 파일 존재 확인
boolean fileExists(String filePath)
```

---

### 2.3 Repository Layer (MyBatis Mapper)

#### OrderMapper
```java
// 주문 생성
void insertOrder(Order order)

// 주문 항목 생성
void insertOrderItems(List<OrderItem> items)

// 주문 조회 (ID)
Order selectOrderById(String orderId)

// 주문 목록 조회 (테이블, 세션)
List<Order> selectOrdersByTableAndSession(String tableId, String sessionId)

// 주문 상태 업데이트
void updateOrderStatus(String orderId, OrderStatus status)

// 주문 삭제
void deleteOrder(String orderId)

// 주문 항목 삭제
void deleteOrderItems(String orderId)

// 테이블별 주문 조회
List<Order> selectOrdersByTable(String tableId)

// 매장별 주문 조회
List<Order> selectOrdersByStore(String storeId)
```

#### MenuMapper
```java
// 메뉴 생성
void insertMenu(Menu menu)

// 메뉴 조회 (ID)
Menu selectMenuById(String menuId)

// 메뉴 목록 조회 (매장)
List<Menu> selectMenusByStore(String storeId)

// 메뉴 목록 조회 (카테고리)
List<Menu> selectMenusByCategory(String storeId, String category)

// 메뉴 업데이트
void updateMenu(Menu menu)

// 메뉴 삭제
void deleteMenu(String menuId)

// 메뉴 순서 업데이트
void updateMenuOrder(String menuId, int displayOrder)
```

#### TableMapper
```java
// 테이블 생성
void insertTable(Table table)

// 테이블 조회 (ID)
Table selectTableById(String tableId)

// 테이블 목록 조회 (매장)
List<Table> selectTablesByStore(String storeId)

// 테이블 업데이트
void updateTable(Table table)

// 세션 ID 업데이트
void updateSessionId(String tableId, String sessionId)

// 세션 상태 업데이트
void updateSessionStatus(String tableId, String status)
```

#### UserMapper
```java
// 사용자 조회 (사용자명)
User selectUserByUsername(String username)

// 사용자 조회 (ID)
User selectUserById(String userId)

// 사용자 생성
void insertUser(User user)

// 사용자 업데이트
void updateUser(User user)
```

#### OrderHistoryMapper
```java
// 주문 이력 생성
void insertOrderHistory(OrderHistory history)

// 주문 이력 조회 (테이블)
List<OrderHistory> selectOrderHistoryByTable(String tableId)

// 주문 이력 조회 (날짜 범위)
List<OrderHistory> selectOrderHistoryByDateRange(
    String tableId,
    LocalDate startDate,
    LocalDate endDate
)

// 1년 이상 된 이력 삭제
void deleteOldHistory(LocalDate cutoffDate)
```

---

### 2.4 Common Components

#### GlobalExceptionHandler
```java
// 일반 예외 처리
@ExceptionHandler(Exception.class)
ResponseEntity<ErrorResponse> handleException(Exception ex)

// 검증 예외 처리
@ExceptionHandler(ValidationException.class)
ResponseEntity<ErrorResponse> handleValidationException(ValidationException ex)

// 인증 예외 처리
@ExceptionHandler(AuthenticationException.class)
ResponseEntity<ErrorResponse> handleAuthenticationException(AuthenticationException ex)

// 리소스 없음 예외 처리
@ExceptionHandler(ResourceNotFoundException.class)
ResponseEntity<ErrorResponse> handleResourceNotFoundException(ResourceNotFoundException ex)

// 에러 응답 생성
ErrorResponse createErrorResponse(Exception ex, HttpStatus status)
```

#### JwtTokenProvider
```java
// 토큰 생성
String generateToken(User user)

// 토큰 파싱
Claims parseToken(String token)

// 토큰 검증
boolean validateToken(String token)

// 토큰에서 사용자 ID 추출
String getUserIdFromToken(String token)

// 토큰 만료 확인
boolean isTokenExpired(String token)
```

#### JwtAuthenticationFilter
```java
// 필터 실행
void doFilterInternal(
    HttpServletRequest request,
    HttpServletResponse response,
    FilterChain filterChain
)

// 토큰 추출
String extractToken(HttpServletRequest request)

// 인증 정보 설정
void setAuthentication(String token)
```

---

## Method Signature Conventions

### Frontend (TypeScript)
- **비동기 메서드**: `Promise<T>` 반환
- **이벤트 핸들러**: `handle` 접두사 사용
- **데이터 조회**: `fetch` 또는 `get` 접두사
- **상태 변경**: `set` 또는 `update` 접두사

### Backend (Java)
- **조회 메서드**: `get`, `select`, `find` 접두사
- **생성 메서드**: `create`, `insert`, `add` 접두사
- **수정 메서드**: `update`, `modify` 접두사
- **삭제 메서드**: `delete`, `remove` 접두사
- **검증 메서드**: `validate`, `verify`, `check` 접두사

---

## Notes

- 상세한 비즈니스 규칙은 Functional Design 단계에서 정의됩니다
- 메서드 시그니처는 구현 시 필요에 따라 조정될 수 있습니다
- 에러 처리 및 예외 상황은 각 메서드 구현 시 상세화됩니다
- 트랜잭션 경계는 Service 레이어에서 정의됩니다
