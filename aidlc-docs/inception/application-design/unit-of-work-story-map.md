# Unit of Work Story Mapping

## Story Distribution Summary

**Total Stories**: 20
- **Unit 1 (Shared Foundation)**: 2 stories
- **Unit 2 (Customer Order Domain)**: 8 stories
- **Unit 3 (Admin Operations Domain)**: 10 stories

---

## Unit 1: Shared Foundation

### Assigned Stories (2)

#### US-A-001: 관리자 로그인
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 관리자 인증은 공통 기반 기능으로 Unit 1에서 구현

**Components**:
- Backend: AdminAuthService, AuthMiddleware
- Frontend: LoginPage, AuthContext, AuthService

---

#### US-NFR-002: 보안 요구사항
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 보안 요구사항은 전체 시스템의 기반이므로 Unit 1에서 구현

**Components**:
- Backend: AdminAuthService (bcrypt, JWT), AuthMiddleware
- Frontend: AuthService (token management)

---

## Unit 2: Customer Order Domain

### Assigned Stories (8)

#### US-C-001: 테이블 태블릿 자동 로그인
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 고객 인증 기능으로 고객 주문 도메인의 진입점

**Components**:
- Backend: CustomerController (table login endpoint)
- Frontend: LoginPage (table auto-login), AuthContext

**Dependencies**: Unit 1 (AuthContext, Table entity)

---

#### US-C-002: 메뉴 카테고리별 조회
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 고객 주문 프로세스의 첫 단계

**Components**:
- Backend: MenuService, MenuRepository, CustomerController
- Frontend: MenuPage, MenuService

**Dependencies**: Unit 1 (Menu entity, MenuRepository)

---

#### US-C-003: 장바구니에 메뉴 추가
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 고객 주문 프로세스의 핵심 기능

**Components**:
- Frontend: CartPage, CartContext, StorageService

**Dependencies**: Unit 1 (StorageService), US-C-002

---

#### US-C-004: 장바구니 수량 조절
**Priority**: MVP  
**Story Points**: 2

**Rationale**: 장바구니 관리 기능

**Components**:
- Frontend: CartPage, CartContext

**Dependencies**: US-C-003

---

#### US-C-005: 주문 생성
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 고객 주문 프로세스의 완료 단계

**Components**:
- Backend: OrderService, OrderRepository, SSEService, CustomerController
- Frontend: CartPage, OrderService

**Dependencies**: Unit 1 (Order entity, OrderRepository), US-C-003, US-C-004

---

#### US-C-006: 주문 내역 조회
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 고객이 자신의 주문을 확인하는 기능

**Components**:
- Backend: OrderService, OrderRepository, CustomerController
- Frontend: OrderHistoryPage, OrderService

**Dependencies**: Unit 1 (Order entity, OrderRepository), US-C-005

---

#### US-C-007: 주문 실패 처리
**Priority**: MVP  
**Story Points**: 2

**Rationale**: 에러 처리는 고객 경험의 중요한 부분

**Components**:
- Backend: ErrorMiddleware, CustomerController
- Frontend: CartPage, ErrorMessage component

**Dependencies**: Unit 1 (ErrorMiddleware, ErrorMessage), US-C-005

---

#### US-C-008: 빈 장바구니 주문 방지
**Priority**: MVP  
**Story Points**: 1

**Rationale**: 클라이언트 측 유효성 검증

**Components**:
- Frontend: CartPage, ValidationService

**Dependencies**: Unit 1 (ValidationService), US-C-003

---

## Unit 3: Admin Operations Domain

### Assigned Stories (10)

#### US-A-002: 실시간 주문 모니터링
**Priority**: MVP  
**Story Points**: 8

**Rationale**: 관리자 운영의 핵심 기능

**Components**:
- Backend: OrderManagementService, SSEController
- Frontend: DashboardPage, SSEService

**Dependencies**: 
- Unit 1 (Order entity, AuthContext)
- Unit 2 (SSEService)
- US-A-001

---

#### US-A-003: 주문 상세 보기
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 주문 모니터링의 상세 기능

**Components**:
- Frontend: DashboardPage (OrderDetailModal)

**Dependencies**: US-A-002

---

#### US-A-004: 주문 상태 변경
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 주문 관리 기능

**Components**:
- Backend: OrderManagementService, AdminController
- Frontend: DashboardPage, OrderService

**Dependencies**: 
- Unit 1 (Order entity, OrderRepository)
- Unit 2 (SSEService for broadcast)
- US-A-002

---

#### US-A-005: 주문 삭제 (직권 수정)
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 주문 관리 기능

**Components**:
- Backend: OrderManagementService, AdminController
- Frontend: DashboardPage, ConfirmDialog

**Dependencies**: 
- Unit 1 (Order entity, OrderRepository, ConfirmDialog)
- US-A-002

---

#### US-A-006: 테이블 세션 종료 (이용 완료)
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 테이블 관리의 핵심 기능

**Components**:
- Backend: TableManagementService, OrderHistoryRepository, AdminController
- Frontend: TableManagementPage, TableService

**Dependencies**: 
- Unit 1 (Table, Order, OrderHistory entities, Repositories)
- US-A-001

---

#### US-A-007: 과거 주문 내역 조회
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 테이블 관리 및 이력 조회 기능

**Components**:
- Backend: TableManagementService, OrderHistoryRepository, AdminController
- Frontend: TableManagementPage, TableService

**Dependencies**: 
- Unit 1 (OrderHistory entity, OrderHistoryRepository)
- US-A-006

---

#### US-A-008: 메뉴 관리 (CRUD)
**Priority**: MVP  
**Story Points**: 8

**Rationale**: 메뉴 관리 기능

**Components**:
- Backend: MenuManagementService, MenuRepository, FileStorage, AdminController
- Frontend: MenuManagementPage, MenuService

**Dependencies**: 
- Unit 1 (Menu entity, MenuRepository, FileStorage)
- US-A-001

---

#### US-A-009: 테이블 태블릿 초기 설정
**Priority**: MVP  
**Story Points**: 3

**Rationale**: 테이블 관리 기능

**Components**:
- Backend: TableManagementService, TableRepository, AdminController
- Frontend: TableManagementPage, TableService

**Dependencies**: 
- Unit 1 (Table entity, TableRepository)
- US-A-001

---

#### US-NFR-001: 성능 요구사항
**Priority**: MVP  
**Story Points**: 5

**Rationale**: 전체 시스템의 성능 요구사항이지만 주로 관리자 기능에 영향

**Components**:
- Backend: All services (performance optimization)
- Frontend: All components (performance optimization)

**Dependencies**: All units

---

#### US-NFR-003: 사용성 및 신뢰성 요구사항
**Priority**: P1  
**Story Points**: 3

**Rationale**: 전체 시스템의 사용성 요구사항

**Components**:
- Backend: ErrorMiddleware, logging
- Frontend: All UI components (touch-friendly, feedback)

**Dependencies**: Unit 1 (ErrorMiddleware, Common UI components)

---

## Story Dependency Graph

```
Unit 1: Shared Foundation
├── US-A-001 (관리자 로그인)
└── US-NFR-002 (보안 요구사항)
    |
    v
Unit 2: Customer Order Domain
├── US-C-001 (테이블 자동 로그인) [depends on: US-A-001]
├── US-C-002 (메뉴 조회) [depends on: US-C-001]
├── US-C-003 (장바구니 추가) [depends on: US-C-002]
├── US-C-004 (수량 조절) [depends on: US-C-003]
├── US-C-005 (주문 생성) [depends on: US-C-003, US-C-004]
├── US-C-006 (주문 내역) [depends on: US-C-005]
├── US-C-007 (주문 실패) [depends on: US-C-005]
└── US-C-008 (빈 장바구니 방지) [depends on: US-C-003]
    |
    v
Unit 3: Admin Operations Domain
├── US-A-002 (실시간 모니터링) [depends on: US-A-001, Unit 2 SSE]
├── US-A-003 (주문 상세) [depends on: US-A-002]
├── US-A-004 (상태 변경) [depends on: US-A-002]
├── US-A-005 (주문 삭제) [depends on: US-A-002]
├── US-A-006 (세션 종료) [depends on: US-A-001]
├── US-A-007 (과거 내역) [depends on: US-A-006]
├── US-A-008 (메뉴 관리) [depends on: US-A-001]
├── US-A-009 (테이블 설정) [depends on: US-A-001]
├── US-NFR-001 (성능) [depends on: All units]
└── US-NFR-003 (사용성) [depends on: Unit 1]
```

---

## Development Sequence by Story

### Sprint 1: Unit 1 - Foundation (Week 1)
**Goal**: 공통 기반 구축

**Stories**:
1. US-A-001 (관리자 로그인) - 3 points
2. US-NFR-002 (보안 요구사항) - 5 points

**Total**: 8 points

**Deliverables**:
- 데이터베이스 스키마 및 연결
- 도메인 엔티티
- Repository 패턴
- 관리자 인증 (bcrypt, JWT)
- 공통 UI 컴포넌트
- AuthContext

---

### Sprint 2: Unit 2 - Customer Order (Week 2-3)
**Goal**: 고객 주문 플로우 구현

**Stories**:
1. US-C-001 (테이블 자동 로그인) - 3 points
2. US-C-002 (메뉴 조회) - 5 points
3. US-C-003 (장바구니 추가) - 3 points
4. US-C-004 (수량 조절) - 2 points
5. US-C-005 (주문 생성) - 5 points
6. US-C-006 (주문 내역) - 3 points
7. US-C-007 (주문 실패) - 2 points
8. US-C-008 (빈 장바구니 방지) - 1 point

**Total**: 24 points

**Deliverables**:
- 완전한 고객 주문 플로우
- 메뉴 조회 API 및 UI
- 장바구니 기능 (Context + SessionStorage)
- 주문 생성/조회 API 및 UI
- SSE 실시간 통신
- 에러 처리

---

### Sprint 3: Unit 3 - Admin Operations (Week 4-5)
**Goal**: 관리자 운영 기능 구현

**Stories**:
1. US-A-002 (실시간 모니터링) - 8 points
2. US-A-003 (주문 상세) - 3 points
3. US-A-004 (상태 변경) - 3 points
4. US-A-005 (주문 삭제) - 3 points
5. US-A-006 (세션 종료) - 5 points
6. US-A-007 (과거 내역) - 5 points
7. US-A-008 (메뉴 관리) - 8 points
8. US-A-009 (테이블 설정) - 3 points
9. US-NFR-001 (성능) - 5 points
10. US-NFR-003 (사용성) - 3 points

**Total**: 46 points

**Deliverables**:
- 실시간 주문 모니터링 대시보드
- 주문 관리 기능
- 테이블 관리 기능
- 메뉴 관리 CRUD
- 이미지 업로드
- 성능 최적화
- 사용성 개선

---

## Story Coverage Verification

### All Stories Assigned: ✓
- Unit 1: 2 stories
- Unit 2: 8 stories
- Unit 3: 10 stories
- **Total**: 20 stories (100% coverage)

### No Duplicate Assignments: ✓
- Each story assigned to exactly one unit

### Dependencies Resolved: ✓
- Unit 1 has no dependencies
- Unit 2 depends only on Unit 1
- Unit 3 depends on Unit 1 and Unit 2

---

## Story Priority Distribution

### MVP Stories (17)
- Unit 1: 2 stories (US-A-001, US-NFR-002)
- Unit 2: 8 stories (all customer stories)
- Unit 3: 7 stories (US-A-002 through US-A-009, US-NFR-001)

### P1 Stories (3)
- Unit 3: 1 story (US-NFR-003)

### Total Story Points
- Unit 1: 8 points
- Unit 2: 24 points
- Unit 3: 46 points
- **Total**: 78 points

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
