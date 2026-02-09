# Units of Work

## Overview

테이블오더 서비스는 Monolithic 아키텍처로 Monorepo 구조를 사용하며, 도메인 경계(Bounded Context)를 기준으로 3개의 Unit of Work로 분해됩니다.

**배포 모델**: Monolithic (단일 애플리케이션)  
**저장소 구조**: Monorepo (프론트엔드와 백엔드 함께)  
**개발 순서**: Sequential (순차적 개발)

---

## Unit of Work Definitions

### Unit 1: Shared Foundation (공통 기반)

**Purpose**: 공통 인프라, 엔티티, 유틸리티 제공

**Bounded Context**: Infrastructure & Shared Domain

**Responsibilities**:
- 데이터베이스 연결 및 관리
- 도메인 엔티티 정의 (Store, Table, Menu, Order, OrderItem, OrderHistory)
- 공통 유틸리티 (인증, 유효성 검증, 로깅)
- 공통 UI 컴포넌트 (Button, Input, Modal, Loading, ErrorMessage)
- 인증 서비스 (테이블 자동 로그인, 관리자 로그인)
- 파일 저장소 (이미지 업로드)

**Components**:

**Backend**:
- Domain Layer:
  - `Store` (매장 엔티티)
  - `Table` (테이블 엔티티)
  - `Menu` (메뉴 엔티티)
  - `Order` (주문 엔티티)
  - `OrderItem` (주문 항목 엔티티)
  - `OrderHistory` (주문 이력 엔티티)
- Infrastructure Layer:
  - `Database` (데이터베이스 연결)
  - `StoreRepository`
  - `TableRepository`
  - `FileStorage`
- Application Layer:
  - `AdminAuthService` (관리자 인증)
- Presentation Layer:
  - `AuthMiddleware`
  - `ErrorMiddleware`

**Frontend**:
- Shared Components:
  - `Button`, `Input`, `Modal`, `Loading`, `ErrorMessage`, `ConfirmDialog`
  - `LoginPage`
- Services:
  - `AuthService` (API)
  - `StorageService` (Utility)
  - `ValidationService` (Utility)
- Context:
  - `AuthContext` (전역 인증 상태)

**User Stories**: 
- US-A-001 (관리자 로그인)
- US-NFR-002 (보안 요구사항)

**Development Priority**: 1 (최우선 - 다른 유닛의 기반)

---

### Unit 2: Customer Order Domain (고객 주문 도메인)

**Purpose**: 고객의 주문 프로세스 관리

**Bounded Context**: Customer Order Management

**Responsibilities**:
- 메뉴 조회 및 탐색
- 장바구니 관리
- 주문 생성 및 조회
- 고객 UI 제공

**Components**:

**Backend**:
- Infrastructure Layer:
  - `MenuRepository`
  - `OrderRepository`
- Application Layer:
  - `MenuService` (메뉴 조회)
  - `OrderService` (주문 생성/조회)
  - `SSEService` (실시간 통신)
- Presentation Layer:
  - `CustomerController` (고객 API)
  - `SSEController` (SSE 엔드포인트)

**Frontend**:
- Customer Interface:
  - `CustomerLayout`
  - `MenuPage` (메뉴 조회)
  - `CartPage` (장바구니)
  - `OrderHistoryPage` (주문 내역)
- Services:
  - `MenuService` (API)
  - `OrderService` (API)
  - `SSEService` (Real-time)
- Context:
  - `CartContext` (장바구니 상태)

**User Stories**:
- US-C-001 (테이블 태블릿 자동 로그인)
- US-C-002 (메뉴 카테고리별 조회)
- US-C-003 (장바구니에 메뉴 추가)
- US-C-004 (장바구니 수량 조절)
- US-C-005 (주문 생성)
- US-C-006 (주문 내역 조회)
- US-C-007 (주문 실패 처리)
- US-C-008 (빈 장바구니 주문 방지)

**Development Priority**: 2 (Unit 1 이후)

**Dependencies**:
- Unit 1 (Shared Foundation): 엔티티, 인증, 데이터베이스

---

### Unit 3: Admin Operations Domain (관리자 운영 도메인)

**Purpose**: 관리자의 매장 운영 관리

**Bounded Context**: Admin Operations Management

**Responsibilities**:
- 실시간 주문 모니터링
- 주문 상태 관리
- 테이블 관리 (초기 설정, 세션 종료, 과거 내역)
- 메뉴 관리 (CRUD)
- 관리자 UI 제공

**Components**:

**Backend**:
- Infrastructure Layer:
  - `OrderHistoryRepository`
- Application Layer:
  - `OrderManagementService` (주문 관리)
  - `TableManagementService` (테이블 관리)
  - `MenuManagementService` (메뉴 관리)
- Presentation Layer:
  - `AdminController` (관리자 API)

**Frontend**:
- Admin Interface:
  - `AdminLayout`
  - `DashboardPage` (실시간 주문 모니터링)
  - `TableManagementPage` (테이블 관리)
  - `MenuManagementPage` (메뉴 관리)
- Services:
  - `TableService` (API)

**User Stories**:
- US-A-002 (실시간 주문 모니터링)
- US-A-003 (주문 상세 보기)
- US-A-004 (주문 상태 변경)
- US-A-005 (주문 삭제)
- US-A-006 (테이블 세션 종료)
- US-A-007 (과거 주문 내역 조회)
- US-A-008 (메뉴 관리 CRUD)
- US-A-009 (테이블 태블릿 초기 설정)
- US-NFR-001 (성능 요구사항)
- US-NFR-003 (사용성 및 신뢰성)

**Development Priority**: 3 (Unit 1, 2 이후)

**Dependencies**:
- Unit 1 (Shared Foundation): 엔티티, 인증, 데이터베이스, 파일 저장소
- Unit 2 (Customer Order Domain): SSEService (실시간 주문 업데이트 수신)

---

## Code Organization (Monorepo Structure)

```
table-order-service/
├── backend/                          # Python 백엔드
│   ├── src/
│   │   ├── domain/                   # Unit 1: Domain Entities
│   │   │   ├── __init__.py
│   │   │   ├── store.py
│   │   │   ├── table.py
│   │   │   ├── menu.py
│   │   │   ├── order.py
│   │   │   └── order_history.py
│   │   ├── infrastructure/           # Unit 1: Infrastructure
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── repositories/
│   │   │   │   ├── store_repository.py
│   │   │   │   ├── table_repository.py
│   │   │   │   ├── menu_repository.py
│   │   │   │   ├── order_repository.py
│   │   │   │   └── order_history_repository.py
│   │   │   └── file_storage.py
│   │   ├── application/              # Application Services
│   │   │   ├── __init__.py
│   │   │   ├── auth/                 # Unit 1: Auth Services
│   │   │   │   └── admin_auth_service.py
│   │   │   ├── customer/             # Unit 2: Customer Services
│   │   │   │   ├── menu_service.py
│   │   │   │   └── order_service.py
│   │   │   ├── admin/                # Unit 3: Admin Services
│   │   │   │   ├── order_management_service.py
│   │   │   │   ├── table_management_service.py
│   │   │   │   └── menu_management_service.py
│   │   │   └── realtime/             # Unit 2: Real-time
│   │   │       └── sse_service.py
│   │   ├── presentation/             # API Controllers
│   │   │   ├── __init__.py
│   │   │   ├── middleware/           # Unit 1: Middleware
│   │   │   │   ├── auth_middleware.py
│   │   │   │   └── error_middleware.py
│   │   │   ├── customer_controller.py    # Unit 2
│   │   │   ├── admin_controller.py       # Unit 3
│   │   │   └── sse_controller.py         # Unit 2
│   │   └── main.py                   # Application Entry Point
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
├── frontend/                         # React 프론트엔드
│   ├── src/
│   │   ├── shared/                   # Unit 1: Shared Components
│   │   │   ├── components/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   ├── Loading.tsx
│   │   │   │   ├── ErrorMessage.tsx
│   │   │   │   └── ConfirmDialog.tsx
│   │   │   ├── services/
│   │   │   │   ├── AuthService.ts
│   │   │   │   ├── StorageService.ts
│   │   │   │   └── ValidationService.ts
│   │   │   ├── context/
│   │   │   │   └── AuthContext.tsx
│   │   │   └── pages/
│   │   │       └── LoginPage.tsx
│   │   ├── customer/                 # Unit 2: Customer Features
│   │   │   ├── components/
│   │   │   │   ├── MenuPage.tsx
│   │   │   │   ├── CartPage.tsx
│   │   │   │   └── OrderHistoryPage.tsx
│   │   │   ├── services/
│   │   │   │   ├── MenuService.ts
│   │   │   │   ├── OrderService.ts
│   │   │   │   └── SSEService.ts
│   │   │   ├── context/
│   │   │   │   └── CartContext.tsx
│   │   │   └── layout/
│   │   │       └── CustomerLayout.tsx
│   │   ├── admin/                    # Unit 3: Admin Features
│   │   │   ├── components/
│   │   │   │   ├── DashboardPage.tsx
│   │   │   │   ├── TableManagementPage.tsx
│   │   │   │   └── MenuManagementPage.tsx
│   │   │   ├── services/
│   │   │   │   └── TableService.ts
│   │   │   └── layout/
│   │   │       └── AdminLayout.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   └── README.md
├── docker-compose.yml                # Docker Compose 설정
├── .gitignore
└── README.md
```

---

## Development Sequence

### Phase 1: Unit 1 - Shared Foundation
**Duration**: 예상 2-3일

**Tasks**:
1. 데이터베이스 스키마 및 연결 설정
2. 도메인 엔티티 정의
3. Repository 패턴 구현
4. 관리자 인증 서비스 구현
5. 공통 UI 컴포넌트 구현
6. 인증 Context 구현

**Deliverables**:
- 작동하는 데이터베이스 연결
- 모든 엔티티 및 Repository
- 관리자 로그인 기능
- 공통 컴포넌트 라이브러리

---

### Phase 2: Unit 2 - Customer Order Domain
**Duration**: 예상 3-4일

**Tasks**:
1. 메뉴 조회 API 및 UI 구현
2. 장바구니 기능 구현 (Context + SessionStorage)
3. 주문 생성 API 및 UI 구현
4. 주문 내역 조회 API 및 UI 구현
5. SSE 실시간 통신 구현
6. 에러 처리 및 유효성 검증

**Deliverables**:
- 완전한 고객 주문 플로우
- 실시간 주문 업데이트 (SSE)
- 장바구니 영속성

---

### Phase 3: Unit 3 - Admin Operations Domain
**Duration**: 예상 3-4일

**Tasks**:
1. 실시간 주문 모니터링 대시보드 구현
2. 주문 관리 기능 구현 (상태 변경, 삭제)
3. 테이블 관리 기능 구현 (초기 설정, 세션 종료, 과거 내역)
4. 메뉴 관리 CRUD 구현
5. 이미지 업로드 기능 구현
6. 관리자 UI 통합

**Deliverables**:
- 완전한 관리자 운영 기능
- 실시간 주문 모니터링
- 테이블 및 메뉴 관리

---

## Integration Points

### Unit 1 → Unit 2
- **Entities**: Order, Menu, Table 엔티티 사용
- **Repositories**: MenuRepository, OrderRepository 사용
- **Auth**: 테이블 자동 로그인 사용
- **Database**: 데이터베이스 연결 사용

### Unit 1 → Unit 3
- **Entities**: 모든 엔티티 사용
- **Repositories**: 모든 Repository 사용
- **Auth**: 관리자 인증 사용
- **FileStorage**: 이미지 업로드 사용

### Unit 2 → Unit 3
- **SSEService**: 실시간 주문 업데이트 수신
- **OrderService**: 주문 데이터 공유

---

## Shared Code Strategy

### Shared Library/Package
- **Domain Entities**: 모든 유닛에서 공유
- **Repositories**: Infrastructure Layer에서 공유
- **Common UI Components**: 모든 프론트엔드 기능에서 공유
- **Services**: AuthService, StorageService, ValidationService 공유

### No Duplication
- 엔티티, Repository, 공통 컴포넌트는 중복 없이 Unit 1에서 정의
- 다른 유닛은 import하여 사용

---

## Testing Strategy

### Unit 1 Testing
- 엔티티 유효성 검증 테스트
- Repository CRUD 테스트
- 인증 서비스 테스트
- 공통 컴포넌트 테스트

### Unit 2 Testing
- 메뉴 조회 API 테스트
- 주문 생성/조회 API 테스트
- 장바구니 로직 테스트
- SSE 연결 테스트
- 고객 UI E2E 테스트

### Unit 3 Testing
- 주문 관리 API 테스트
- 테이블 관리 API 테스트
- 메뉴 관리 API 테스트
- 이미지 업로드 테스트
- 관리자 UI E2E 테스트

### Integration Testing
- Unit 2 + Unit 3: 실시간 주문 업데이트 통합 테스트
- 전체 시스템: 고객 주문 → 관리자 확인 플로우 테스트

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
