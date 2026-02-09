# Components - 테이블오더 서비스

## Overview
테이블오더 서비스의 주요 컴포넌트를 정의합니다. Atomic Design 패턴을 따르는 프론트엔드와 3-Layer 아키텍처를 따르는 백엔드로 구성됩니다.

---

## Frontend Components (React)

### Atomic Design 계층 구조

```
src/
├── atoms/              # 기본 UI 요소
├── molecules/          # atoms 조합
├── organisms/          # molecules 조합
├── templates/          # 페이지 레이아웃
├── pages/              # 실제 페이지
├── services/           # API 통신
├── stores/             # Zustand 상태 관리
└── utils/              # 유틸리티 함수
```

---

## 1. Customer Frontend Components (고객용)

### 1.1 Atoms (기본 UI 요소)

#### Button
- **책임**: 재사용 가능한 버튼 컴포넌트
- **Props**: `label`, `onClick`, `variant`, `disabled`, `size`
- **용도**: 모든 버튼 UI (최소 44x44px 터치 친화적)

#### Input
- **책임**: 입력 필드 컴포넌트
- **Props**: `value`, `onChange`, `placeholder`, `type`, `error`
- **용도**: 폼 입력

#### Card
- **책임**: 카드 형태 컨테이너
- **Props**: `children`, `onClick`, `className`
- **용도**: 메뉴 카드, 주문 카드 등

#### Badge
- **책임**: 상태 표시 배지
- **Props**: `count`, `variant`, `position`
- **용도**: 장바구니 아이템 개수, 주문 상태 표시

#### Image
- **책임**: 이미지 표시 및 로딩 처리
- **Props**: `src`, `alt`, `fallback`, `onError`
- **용도**: 메뉴 이미지 표시

---

### 1.2 Molecules (atoms 조합)

#### MenuCard
- **책임**: 메뉴 정보를 카드 형태로 표시
- **구성**: Image + Card + Button
- **Props**: `menu` (id, name, price, image, description)
- **용도**: 메뉴 목록 표시

#### CartItem
- **책임**: 장바구니 아이템 표시 및 수량 조절
- **구성**: Image + Button (증가/감소/삭제)
- **Props**: `item` (menuId, name, price, quantity)
- **용도**: 장바구니 화면

#### OrderStatusBadge
- **책임**: 주문 상태를 시각적으로 표시
- **구성**: Badge + 색상 변경
- **Props**: `status` (대기중/준비중/완료/취소)
- **용도**: 주문 내역 화면

---

### 1.3 Organisms (molecules 조합)

#### MenuList
- **책임**: 카테고리별 메뉴 목록 표시
- **구성**: MenuCard 배열
- **Props**: `menus`, `onMenuClick`, `category`
- **용도**: 메뉴 탐색 화면

#### Cart
- **책임**: 장바구니 전체 관리
- **구성**: CartItem 배열 + 총 금액 + 주문 버튼
- **Props**: `items`, `onQuantityChange`, `onRemove`, `onCheckout`
- **용도**: 장바구니 화면

#### OrderHistory
- **책임**: 주문 내역 목록 표시
- **구성**: OrderCard 배열
- **Props**: `orders`, `onOrderClick`
- **용도**: 주문 내역 화면

#### CategoryTabs
- **책임**: 메뉴 카테고리 탭 네비게이션
- **구성**: Button 배열
- **Props**: `categories`, `activeCategory`, `onCategoryChange`
- **용도**: 메뉴 화면 상단

---

### 1.4 Templates (페이지 레이아웃)

#### CustomerLayout
- **책임**: 고객용 페이지 공통 레이아웃
- **구성**: Header + Content + Navigation
- **Props**: `children`, `title`, `showCart`
- **용도**: 모든 고객 페이지

---

### 1.5 Pages (실제 페이지)

#### MenuPage
- **책임**: 메뉴 탐색 및 장바구니 추가
- **구성**: CustomerLayout + CategoryTabs + MenuList
- **경로**: `/menu`

#### CartPage
- **책임**: 장바구니 관리 및 주문 생성
- **구성**: CustomerLayout + Cart
- **경로**: `/cart`

#### OrderHistoryPage
- **책임**: 주문 내역 조회
- **구성**: CustomerLayout + OrderHistory
- **경로**: `/orders`

---

## 2. Admin Frontend Components (관리자용)

### 2.1 Atoms

#### DataTable
- **책임**: 테이블 형태 데이터 표시
- **Props**: `columns`, `data`, `onRowClick`
- **용도**: 주문 목록, 메뉴 목록

#### Modal
- **책임**: 모달 다이얼로그
- **Props**: `isOpen`, `onClose`, `title`, `children`
- **용도**: 확인 팝업, 상세 보기

#### StatusDropdown
- **책임**: 주문 상태 변경 드롭다운
- **Props**: `currentStatus`, `onStatusChange`, `options`
- **용도**: 주문 상태 변경

---

### 2.2 Molecules

#### TableCard
- **책임**: 테이블별 주문 현황 카드
- **구성**: Card + Badge + 주문 미리보기
- **Props**: `table` (tableNumber, orders, totalAmount)
- **용도**: 주문 모니터링 대시보드

#### MenuForm
- **책임**: 메뉴 등록/수정 폼
- **구성**: Input 배열 + 이미지 업로드 + Button
- **Props**: `menu`, `onSubmit`, `onCancel`
- **용도**: 메뉴 관리 화면

---

### 2.3 Organisms

#### OrderDashboard
- **책임**: 실시간 주문 모니터링 대시보드
- **구성**: TableCard 배열 + 필터
- **Props**: `tables`, `onTableClick`, `onStatusChange`
- **용도**: 주문 모니터링 화면

#### MenuManagement
- **책임**: 메뉴 관리 테이블 및 CRUD
- **구성**: DataTable + MenuForm + Modal
- **Props**: `menus`, `onAdd`, `onEdit`, `onDelete`
- **용도**: 메뉴 관리 화면

#### TableManagement
- **책임**: 테이블 관리 및 세션 처리
- **구성**: DataTable + Modal
- **Props**: `tables`, `onSessionEnd`, `onOrderDelete`
- **용도**: 테이블 관리 화면

---

### 2.4 Templates

#### AdminLayout
- **책임**: 관리자용 페이지 공통 레이아웃
- **구성**: Sidebar + Header + Content
- **Props**: `children`, `title`, `activeMenu`
- **용도**: 모든 관리자 페이지

---

### 2.5 Pages

#### LoginPage
- **책임**: 관리자 로그인
- **구성**: LoginForm
- **경로**: `/admin/login`

#### DashboardPage
- **책임**: 실시간 주문 모니터링
- **구성**: AdminLayout + OrderDashboard
- **경로**: `/admin/dashboard`

#### MenuManagementPage
- **책임**: 메뉴 CRUD 관리
- **구성**: AdminLayout + MenuManagement
- **경로**: `/admin/menus`

#### TableManagementPage
- **책임**: 테이블 및 세션 관리
- **구성**: AdminLayout + TableManagement
- **경로**: `/admin/tables`

#### HistoryPage
- **책임**: 과거 주문 내역 조회
- **구성**: AdminLayout + DataTable
- **경로**: `/admin/history`

---

## 3. Shared Frontend Components

### 3.1 Services (API 통신)

#### ApiClient
- **책임**: Axios 기반 HTTP 클라이언트
- **기능**: 요청/응답 인터셉터, 에러 처리, 토큰 관리
- **용도**: 모든 API 호출

#### SSEClient
- **책임**: SSE 라이브러리 기반 실시간 통신
- **기능**: 연결 관리, 재연결 로직, 이벤트 리스너
- **용도**: 실시간 주문 상태 업데이트

---

### 3.2 Stores (Zustand 상태 관리)

#### useAuthStore
- **책임**: 인증 상태 관리
- **State**: `user`, `token`, `isAuthenticated`
- **Actions**: `login`, `logout`, `refreshToken`

#### useCartStore
- **책임**: 장바구니 상태 관리 (localStorage 동기화)
- **State**: `items`, `totalAmount`
- **Actions**: `addItem`, `removeItem`, `updateQuantity`, `clearCart`

#### useOrderStore
- **책임**: 주문 상태 관리
- **State**: `orders`, `currentOrder`
- **Actions**: `createOrder`, `fetchOrders`, `updateOrderStatus`

#### useMenuStore
- **책임**: 메뉴 상태 관리
- **State**: `menus`, `categories`
- **Actions**: `fetchMenus`, `addMenu`, `updateMenu`, `deleteMenu`

---

### 3.3 Utils

#### storage
- **책임**: localStorage 래퍼
- **기능**: `get`, `set`, `remove`, `clear`

#### formatter
- **책임**: 데이터 포맷팅
- **기능**: `formatCurrency`, `formatDate`, `formatTime`

#### validator
- **책임**: 입력 검증
- **기능**: `validateEmail`, `validatePrice`, `validateImage`

---

## 4. Backend Components (Spring Boot)

### 4.1 Controller Layer

#### CustomerController
- **책임**: 고객용 API 엔드포인트
- **경로**: `/api/customer/*`
- **기능**: 메뉴 조회, 주문 생성, 주문 내역 조회

#### AdminController
- **책임**: 관리자용 API 엔드포인트
- **경로**: `/api/admin/*`
- **기능**: 주문 관리, 메뉴 관리, 테이블 관리

#### AuthController
- **책임**: 인증 관련 API 엔드포인트
- **경로**: `/api/auth/*`
- **기능**: 로그인, 로그아웃, 토큰 갱신

#### SSEController
- **책임**: SSE 실시간 통신 엔드포인트
- **경로**: `/api/sse/*`
- **기능**: SSE 연결 관리, 이벤트 전송

---

### 4.2 Service Layer

#### OrderService
- **책임**: 주문 비즈니스 로직
- **기능**: 주문 생성, 상태 변경, 주문 조회, 주문 삭제

#### MenuService
- **책임**: 메뉴 비즈니스 로직
- **기능**: 메뉴 CRUD, 이미지 업로드, 순서 조정

#### TableService
- **책임**: 테이블 및 세션 비즈니스 로직
- **기능**: 세션 생성/종료, 테이블 초기 설정

#### AuthService
- **책임**: 인증 및 권한 비즈니스 로직
- **기능**: 로그인 검증, JWT 토큰 생성/검증

#### SSEService
- **책임**: SSE 이벤트 관리
- **기능**: 클라이언트 연결 관리, 이벤트 브로드캐스트

#### FileService
- **책임**: 파일 업로드/다운로드 처리
- **기능**: 이미지 저장, 파일 검증, 경로 관리

---

### 4.3 Repository Layer (MyBatis)

#### OrderMapper
- **책임**: 주문 데이터 액세스
- **기능**: 주문 CRUD, 주문 조회 (테이블별, 세션별)

#### MenuMapper
- **책임**: 메뉴 데이터 액세스
- **기능**: 메뉴 CRUD, 카테고리별 조회

#### TableMapper
- **책임**: 테이블 데이터 액세스
- **기능**: 테이블 CRUD, 세션 관리

#### UserMapper
- **책임**: 사용자 데이터 액세스
- **기능**: 사용자 조회, 인증 정보 검증

#### OrderHistoryMapper
- **책임**: 주문 이력 데이터 액세스
- **기능**: 과거 주문 조회, 이력 저장

---

### 4.4 Common Components

#### GlobalExceptionHandler
- **책임**: 전역 예외 처리 (@ControllerAdvice)
- **기능**: 표준화된 에러 응답, 로깅

#### JwtTokenProvider
- **책임**: JWT 토큰 생성 및 검증
- **기능**: 토큰 생성, 토큰 파싱, 토큰 검증

#### JwtAuthenticationFilter
- **책임**: JWT 인증 필터
- **기능**: 요청 인터셉트, 토큰 검증, 인증 정보 설정

#### FileStorageConfig
- **책임**: 파일 저장소 설정
- **기능**: 업로드 경로 설정, 파일 크기 제한

---

## 5. Domain Models (공통)

### Store
- **책임**: 매장 정보
- **필드**: `id`, `name`, `address`, `phone`

### Table
- **책임**: 테이블 정보
- **필드**: `id`, `storeId`, `tableNumber`, `pin`, `sessionId`, `sessionStatus`

### Menu
- **책임**: 메뉴 정보
- **필드**: `id`, `storeId`, `name`, `price`, `description`, `category`, `imagePath`, `displayOrder`

### Order
- **책임**: 주문 정보
- **필드**: `id`, `storeId`, `tableId`, `sessionId`, `orderTime`, `totalAmount`, `status`

### OrderItem
- **책임**: 주문 항목 정보
- **필드**: `id`, `orderId`, `menuId`, `quantity`, `unitPrice`

### OrderHistory
- **책임**: 주문 이력 정보
- **필드**: `id`, `orderId`, `completedTime`, `archivedTime`

### User
- **책임**: 관리자 사용자 정보
- **필드**: `id`, `storeId`, `username`, `password`, `role`

---

## Component Responsibilities Summary

### Frontend (React)
- **Atoms**: 재사용 가능한 기본 UI 요소
- **Molecules**: Atoms 조합으로 특정 기능 제공
- **Organisms**: Molecules 조합으로 복잡한 UI 섹션 구성
- **Templates**: 페이지 레이아웃 정의
- **Pages**: 실제 라우팅되는 페이지
- **Services**: API 통신 및 외부 서비스 연동
- **Stores**: Zustand 기반 전역 상태 관리
- **Utils**: 공통 유틸리티 함수

### Backend (Spring Boot)
- **Controller**: HTTP 요청 처리 및 응답
- **Service**: 비즈니스 로직 구현
- **Repository (Mapper)**: 데이터베이스 액세스
- **Common**: 공통 기능 (인증, 예외 처리, 파일 관리)
- **Domain**: 도메인 모델 정의

---

## Design Principles Applied

1. **Single Responsibility**: 각 컴포넌트는 하나의 명확한 책임
2. **Separation of Concerns**: UI, 비즈니스 로직, 데이터 액세스 명확히 분리
3. **Reusability**: Atomic Design을 통한 컴포넌트 재사용성 극대화
4. **Testability**: 각 레이어를 독립적으로 테스트 가능
5. **Maintainability**: 명확한 구조로 유지보수 용이

---

## Notes

- 프론트엔드는 Atomic Design 패턴을 따라 계층적으로 구성
- 백엔드는 3-Layer 아키텍처 (Controller-Service-Repository)
- 상태 관리는 Zustand 사용
- API 통신은 Axios 사용
- SSE는 라이브러리 기반 구현
- 데이터 액세스는 MyBatis 사용
- 파일 업로드는 Multipart Form Data 방식
- 에러 처리는 Global Error Handler 패턴
- 컴포넌트 간 통신은 Context API 사용
