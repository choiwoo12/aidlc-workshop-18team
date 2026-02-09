# Application Components

## Component Overview

테이블오더 서비스는 Feature-based 구조로 조직화되며, Clean Architecture 원칙을 따릅니다.

---

## Frontend Components (React)

### 1. Customer Interface Components

#### 1.1 Menu Feature
**Component**: `MenuPage`
- **Purpose**: 메뉴 조회 및 탐색 기능 제공
- **Responsibilities**:
  - 카테고리별 메뉴 목록 표시
  - 메뉴 상세 정보 표시
  - 장바구니에 메뉴 추가
- **Key Sub-components**:
  - `CategoryTabs`: 카테고리 탭 네비게이션
  - `MenuCard`: 개별 메뉴 카드
  - `MenuDetail`: 메뉴 상세 정보 모달

#### 1.2 Cart Feature
**Component**: `CartPage`
- **Purpose**: 장바구니 관리 기능 제공
- **Responsibilities**:
  - 장바구니 아이템 목록 표시
  - 수량 조절 (증가/감소)
  - 총 금액 계산
  - 주문 확정
- **Key Sub-components**:
  - `CartItem`: 개별 장바구니 아이템
  - `CartSummary`: 총 금액 및 주문 버튼

#### 1.3 Order Feature
**Component**: `OrderHistoryPage`
- **Purpose**: 주문 내역 조회 기능 제공
- **Responsibilities**:
  - 현재 세션 주문 목록 표시
  - 주문 상태 표시
  - 주문 상세 정보 표시
- **Key Sub-components**:
  - `OrderCard`: 개별 주문 카드
  - `OrderDetail`: 주문 상세 정보

#### 1.4 Customer Layout
**Component**: `CustomerLayout`
- **Purpose**: 고객 UI 공통 레이아웃
- **Responsibilities**:
  - 네비게이션 바
  - 장바구니 아이콘 (아이템 수 표시)
  - 페이지 라우팅

---

### 2. Admin Interface Components

#### 2.1 Dashboard Feature
**Component**: `DashboardPage`
- **Purpose**: 실시간 주문 모니터링 대시보드
- **Responsibilities**:
  - 테이블별 주문 카드 그리드 표시
  - 실시간 주문 업데이트 (SSE)
  - 신규 주문 강조 표시
- **Key Sub-components**:
  - `TableCard`: 테이블별 주문 카드
  - `OrderPreview`: 주문 미리보기
  - `OrderDetailModal`: 주문 상세 모달

#### 2.2 Table Management Feature
**Component**: `TableManagementPage`
- **Purpose**: 테이블 관리 기능 제공
- **Responsibilities**:
  - 테이블 초기 설정
  - 주문 삭제
  - 테이블 세션 종료 (이용 완료)
  - 과거 주문 내역 조회
- **Key Sub-components**:
  - `TableSetupForm`: 테이블 설정 폼
  - `OrderList`: 주문 목록
  - `HistoryModal`: 과거 내역 모달

#### 2.3 Menu Management Feature
**Component**: `MenuManagementPage`
- **Purpose**: 메뉴 관리 기능 제공
- **Responsibilities**:
  - 메뉴 CRUD (생성, 조회, 수정, 삭제)
  - 메뉴 순서 조정
  - 이미지 업로드
- **Key Sub-components**:
  - `MenuForm`: 메뉴 등록/수정 폼
  - `MenuList`: 메뉴 목록
  - `ImageUpload`: 이미지 업로드 컴포넌트

#### 2.4 Admin Layout
**Component**: `AdminLayout`
- **Purpose**: 관리자 UI 공통 레이아웃
- **Responsibilities**:
  - 사이드바 네비게이션
  - 로그아웃 버튼
  - 페이지 라우팅

---

### 3. Shared Components

#### 3.1 Authentication
**Component**: `LoginPage`
- **Purpose**: 인증 기능 제공
- **Responsibilities**:
  - 테이블 자동 로그인 (고객)
  - 관리자 로그인 폼
  - 인증 상태 관리

#### 3.2 Common UI Components
- `Button`: 공통 버튼 컴포넌트
- `Input`: 공통 입력 컴포넌트
- `Modal`: 공통 모달 컴포넌트
- `Loading`: 로딩 스피너
- `ErrorMessage`: 에러 메시지 표시
- `ConfirmDialog`: 확인 다이얼로그

---

## Backend Components (Python - Clean Architecture)

### 1. Presentation Layer (Adapters)

#### 1.1 API Controllers
**Component**: `CustomerController`
- **Purpose**: 고객용 API 엔드포인트
- **Responsibilities**:
  - 메뉴 조회 API
  - 주문 생성 API
  - 주문 내역 조회 API
- **Routes**:
  - `GET /api/customer/menus`
  - `POST /api/customer/orders`
  - `GET /api/customer/orders`

**Component**: `AdminController`
- **Purpose**: 관리자용 API 엔드포인트
- **Responsibilities**:
  - 인증 API
  - 주문 관리 API
  - 테이블 관리 API
  - 메뉴 관리 API
- **Routes**:
  - `POST /api/admin/login`
  - `GET /api/admin/orders`
  - `PUT /api/admin/orders/:id/status`
  - `DELETE /api/admin/orders/:id`
  - `POST /api/admin/tables/:id/complete`
  - `GET /api/admin/tables/:id/history`
  - `GET /api/admin/menus`
  - `POST /api/admin/menus`
  - `PUT /api/admin/menus/:id`
  - `DELETE /api/admin/menus/:id`

**Component**: `SSEController`
- **Purpose**: 실시간 통신 엔드포인트
- **Responsibilities**:
  - SSE 연결 관리
  - 실시간 주문 업데이트 전송
- **Routes**:
  - `GET /api/admin/orders/stream`

#### 1.2 Middleware
**Component**: `AuthMiddleware`
- **Purpose**: 인증 검증
- **Responsibilities**:
  - JWT 토큰 검증
  - 테이블 세션 검증
  - 권한 확인

**Component**: `ErrorMiddleware`
- **Purpose**: 에러 처리
- **Responsibilities**:
  - 예외 처리
  - 에러 응답 포맷팅
  - 로깅

---

### 2. Application Layer (Use Cases)

#### 2.1 Customer Use Cases
**Component**: `MenuService`
- **Purpose**: 메뉴 조회 비즈니스 로직
- **Responsibilities**:
  - 카테고리별 메뉴 조회
  - 메뉴 상세 조회

**Component**: `OrderService`
- **Purpose**: 주문 관리 비즈니스 로직
- **Responsibilities**:
  - 주문 생성
  - 주문 내역 조회
  - 주문 유효성 검증

#### 2.2 Admin Use Cases
**Component**: `AdminAuthService`
- **Purpose**: 관리자 인증 비즈니스 로직
- **Responsibilities**:
  - 로그인 처리
  - JWT 토큰 생성
  - 비밀번호 검증

**Component**: `OrderManagementService`
- **Purpose**: 주문 관리 비즈니스 로직
- **Responsibilities**:
  - 주문 상태 변경
  - 주문 삭제
  - 실시간 주문 목록 조회

**Component**: `TableManagementService`
- **Purpose**: 테이블 관리 비즈니스 로직
- **Responsibilities**:
  - 테이블 초기 설정
  - 테이블 세션 종료
  - 과거 주문 내역 조회

**Component**: `MenuManagementService`
- **Purpose**: 메뉴 관리 비즈니스 로직
- **Responsibilities**:
  - 메뉴 CRUD
  - 이미지 업로드 처리
  - 메뉴 순서 조정

#### 2.3 Real-time Communication
**Component**: `SSEService`
- **Purpose**: 실시간 통신 관리
- **Responsibilities**:
  - SSE 연결 관리
  - 주문 이벤트 브로드캐스트
  - 클라이언트 연결 추적

---

### 3. Domain Layer (Entities & Business Rules)

#### 3.1 Domain Entities
**Component**: `Store`
- **Purpose**: 매장 엔티티
- **Attributes**: store_id, store_name, admin_username, admin_password_hash

**Component**: `Table`
- **Purpose**: 테이블 엔티티
- **Attributes**: table_id, store_id, table_number, table_password_hash, session_id

**Component**: `Menu`
- **Purpose**: 메뉴 엔티티
- **Attributes**: menu_id, store_id, menu_name, price, description, category, image_path

**Component**: `Order`
- **Purpose**: 주문 엔티티
- **Attributes**: order_id, store_id, table_id, session_id, order_number, total_amount, status

**Component**: `OrderItem`
- **Purpose**: 주문 항목 엔티티
- **Attributes**: order_item_id, order_id, menu_id, menu_name, quantity, unit_price

**Component**: `OrderHistory`
- **Purpose**: 주문 이력 엔티티
- **Attributes**: history_id, store_id, table_id, session_id, order_data, completed_at

---

### 4. Infrastructure Layer (Data Access)

#### 4.1 Database Access
**Component**: `Database`
- **Purpose**: 데이터베이스 연결 관리
- **Responsibilities**:
  - 인메모리 데이터베이스 초기화
  - 연결 관리
  - 트랜잭션 관리

**Component**: `StoreRepository`
- **Purpose**: 매장 데이터 접근
- **Responsibilities**:
  - 매장 조회
  - 매장 생성

**Component**: `TableRepository`
- **Purpose**: 테이블 데이터 접근
- **Responsibilities**:
  - 테이블 조회
  - 테이블 생성/수정

**Component**: `MenuRepository`
- **Purpose**: 메뉴 데이터 접근
- **Responsibilities**:
  - 메뉴 CRUD

**Component**: `OrderRepository`
- **Purpose**: 주문 데이터 접근
- **Responsibilities**:
  - 주문 CRUD
  - 주문 조회 (테이블별, 세션별)

**Component**: `OrderHistoryRepository`
- **Purpose**: 주문 이력 데이터 접근
- **Responsibilities**:
  - 이력 저장
  - 이력 조회

#### 4.2 File Storage
**Component**: `FileStorage`
- **Purpose**: 파일 저장소 관리
- **Responsibilities**:
  - 이미지 파일 저장
  - 파일 경로 생성
  - 파일 삭제

---

## Component Summary

**Frontend Components**: 15개
- Customer Interface: 4개 주요 컴포넌트
- Admin Interface: 4개 주요 컴포넌트
- Shared Components: 7개 공통 컴포넌트

**Backend Components**: 20개
- Presentation Layer: 5개 (Controllers + Middleware)
- Application Layer: 6개 (Services)
- Domain Layer: 6개 (Entities)
- Infrastructure Layer: 3개 (Repositories + Storage)

**Total**: 35개 컴포넌트

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
