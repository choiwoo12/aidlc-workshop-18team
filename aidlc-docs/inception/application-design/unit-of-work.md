# Unit of Work - 테이블오더 서비스

## Overview
테이블오더 서비스를 3개의 독립적인 유닛으로 분해합니다. 각 유닛은 명확한 책임과 경계를 가지며, REST API와 SSE를 통해 통신합니다.

---

## Unit Decomposition Strategy

### 선택된 전략
- **시스템 분해**: Multi-Frontend (고객용, 관리자용, 백엔드 분리)
- **프론트엔드 구성**: Separate Apps (완전히 별도 React 앱)
- **백엔드 모듈**: Logical Modules (패키지 구조로 모듈 분리)
- **유닛 크기**: Medium Units (도메인별 그룹화)
- **공통 컴포넌트**: Shared Module (별도 공통 모듈)
- **개발 순서**: User-Journey-First (사용자 여정 순서)
- **통합 테스트**: Incremental Integration
- **데이터베이스**: No Schema (In-Memory DB)
- **배포 전략**: Separate Deployments (프론트엔드/백엔드 별도)
- **디렉토리 구조**: Layered Structure (frontend/, backend/)

---

## Unit 1: Customer Frontend

### 책임
- 고객용 UI 제공
- 메뉴 탐색 및 주문 생성
- 장바구니 관리
- 주문 내역 조회
- 실시간 주문 상태 업데이트 수신

### 경계
- **포함**: 고객 관련 모든 UI 컴포넌트, 고객용 페이지, 장바구니 상태 관리
- **제외**: 관리자 기능, 백엔드 비즈니스 로직, 데이터 저장

### 기술 스택
- **Framework**: React 18+
- **State Management**: Zustand
- **HTTP Client**: Axios
- **SSE Client**: EventSource 기반 라이브러리
- **Styling**: CSS Modules 또는 Styled Components
- **Build Tool**: Vite 또는 Create React App

### 주요 컴포넌트
- **Pages**: MenuPage, CartPage, OrderHistoryPage
- **Organisms**: MenuList, Cart, OrderHistory, CategoryTabs
- **Molecules**: MenuCard, CartItem, OrderStatusBadge
- **Atoms**: Button, Input, Card, Badge, Image
- **Stores**: useCartStore, useOrderStore, useMenuStore
- **Services**: ApiClient, SSEClient

### 인터페이스
- **REST API 호출**:
  - `GET /api/customer/menus` - 메뉴 목록 조회
  - `POST /api/customer/orders` - 주문 생성
  - `GET /api/customer/orders` - 주문 내역 조회
- **SSE 수신**:
  - `ORDER_STATUS_CHANGED` - 주문 상태 변경 이벤트

### 배포
- **빌드 산출물**: 정적 파일 (HTML, CSS, JS)
- **배포 위치**: `frontend/customer/build/` 또는 `frontend/customer/dist/`
- **서빙 방식**: 정적 파일 서버 또는 CDN

---

## Unit 2: Admin Frontend

### 책임
- 관리자용 UI 제공
- 실시간 주문 모니터링
- 주문 상태 관리
- 메뉴 CRUD 관리
- 테이블 및 세션 관리
- 과거 주문 내역 조회

### 경계
- **포함**: 관리자 관련 모든 UI 컴포넌트, 관리자용 페이지, 인증 UI
- **제외**: 고객 기능, 백엔드 비즈니스 로직, 데이터 저장

### 기술 스택
- **Framework**: React 18+
- **State Management**: Zustand
- **HTTP Client**: Axios
- **SSE Client**: EventSource 기반 라이브러리
- **Styling**: CSS Modules 또는 Styled Components
- **Build Tool**: Vite 또는 Create React App

### 주요 컴포넌트
- **Pages**: LoginPage, DashboardPage, MenuManagementPage, TableManagementPage, HistoryPage
- **Organisms**: OrderDashboard, MenuManagement, TableManagement
- **Molecules**: TableCard, MenuForm, StatusDropdown
- **Atoms**: Button, Input, Modal, DataTable
- **Stores**: useAuthStore, useOrderStore, useMenuStore
- **Services**: ApiClient, SSEClient

### 인터페이스
- **REST API 호출**:
  - `POST /api/auth/login` - 관리자 로그인
  - `GET /api/admin/orders` - 주문 목록 조회
  - `PUT /api/admin/orders/{id}/status` - 주문 상태 변경
  - `GET /api/admin/menus` - 메뉴 목록 조회
  - `POST /api/admin/menus` - 메뉴 등록
  - `PUT /api/admin/menus/{id}` - 메뉴 수정
  - `DELETE /api/admin/menus/{id}` - 메뉴 삭제
  - `GET /api/admin/tables` - 테이블 목록 조회
  - `POST /api/admin/tables/{id}/end-session` - 세션 종료
  - `DELETE /api/admin/orders/{id}` - 주문 삭제
  - `GET /api/admin/history` - 과거 주문 내역 조회
- **SSE 수신**:
  - `NEW_ORDER` - 신규 주문 생성 이벤트
  - `ORDER_STATUS_CHANGED` - 주문 상태 변경 이벤트
  - `ORDER_DELETED` - 주문 삭제 이벤트

### 배포
- **빌드 산출물**: 정적 파일 (HTML, CSS, JS)
- **배포 위치**: `frontend/admin/build/` 또는 `frontend/admin/dist/`
- **서빙 방식**: 정적 파일 서버 또는 CDN

---

## Unit 3: Backend

### 책임
- 비즈니스 로직 처리
- 데이터 저장 및 조회
- 인증 및 권한 관리
- REST API 제공
- SSE 실시간 이벤트 전송
- 파일 업로드 처리

### 경계
- **포함**: 모든 비즈니스 로직, 데이터 액세스, API 엔드포인트, SSE 관리
- **제외**: UI 렌더링, 클라이언트 상태 관리

### 기술 스택
- **Framework**: Spring Boot 3.x
- **Data Access**: MyBatis
- **Database**: H2 (In-Memory)
- **Security**: Spring Security + JWT
- **SSE**: Spring WebFlux SseEmitter
- **File Upload**: Multipart Form Data
- **Build Tool**: Maven 또는 Gradle

### 주요 컴포넌트

#### Controller Layer
- `CustomerController` - 고객용 API
- `AdminController` - 관리자용 API
- `AuthController` - 인증 API
- `SSEController` - SSE 연결 관리

#### Service Layer
- `OrderService` - 주문 비즈니스 로직
- `MenuService` - 메뉴 비즈니스 로직
- `TableService` - 테이블 및 세션 비즈니스 로직
- `AuthService` - 인증 비즈니스 로직
- `SSEService` - SSE 이벤트 관리
- `FileService` - 파일 업로드 처리

#### Repository Layer (MyBatis Mapper)
- `OrderMapper` - 주문 데이터 액세스
- `MenuMapper` - 메뉴 데이터 액세스
- `TableMapper` - 테이블 데이터 액세스
- `UserMapper` - 사용자 데이터 액세스
- `OrderHistoryMapper` - 주문 이력 데이터 액세스

#### Common Components
- `GlobalExceptionHandler` - 전역 예외 처리
- `JwtTokenProvider` - JWT 토큰 생성/검증
- `JwtAuthenticationFilter` - JWT 인증 필터
- `FileStorageConfig` - 파일 저장소 설정

#### Domain Models
- `Store`, `Table`, `Menu`, `Order`, `OrderItem`, `OrderHistory`, `User`

### 논리적 모듈 구조 (패키지)
```
com.tableorder
├── controller/          # API 엔드포인트
│   ├── customer/
│   ├── admin/
│   ├── auth/
│   └── sse/
├── service/             # 비즈니스 로직
│   ├── order/
│   ├── menu/
│   ├── table/
│   ├── auth/
│   ├── sse/
│   └── file/
├── repository/          # MyBatis Mapper
│   ├── mapper/
│   └── xml/
├── domain/              # 도메인 모델
├── dto/                 # 데이터 전송 객체
├── config/              # 설정 클래스
├── security/            # 보안 관련
├── exception/           # 예외 클래스
└── util/                # 유틸리티
```

### 인터페이스
- **REST API 제공**: 위의 Customer Frontend 및 Admin Frontend 인터페이스 참조
- **SSE 이벤트 전송**: 
  - `NEW_ORDER` → Admin Frontend
  - `ORDER_STATUS_CHANGED` → Customer Frontend, Admin Frontend
  - `ORDER_DELETED` → Admin Frontend

### 배포
- **빌드 산출물**: JAR 파일 (Spring Boot Executable JAR)
- **배포 위치**: `backend/target/` 또는 `backend/build/`
- **실행 방식**: `java -jar table-order-backend.jar`

---

## Code Organization Strategy (Greenfield)

### 프로젝트 디렉토리 구조

```
aidlc-workshop-18team/                    # Workspace Root
├── frontend/                              # 프론트엔드 루트
│   ├── customer/                          # Unit 1: Customer Frontend
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── atoms/
│   │   │   ├── molecules/
│   │   │   ├── organisms/
│   │   │   ├── templates/
│   │   │   ├── pages/
│   │   │   ├── services/
│   │   │   ├── stores/
│   │   │   ├── utils/
│   │   │   ├── App.jsx
│   │   │   └── main.jsx
│   │   ├── package.json
│   │   └── vite.config.js
│   │
│   └── admin/                             # Unit 2: Admin Frontend
│       ├── public/
│       ├── src/
│       │   ├── atoms/
│       │   ├── molecules/
│       │   ├── organisms/
│       │   ├── templates/
│       │   ├── pages/
│       │   ├── services/
│       │   ├── stores/
│       │   ├── utils/
│       │   ├── App.jsx
│       │   └── main.jsx
│       ├── package.json
│       └── vite.config.js
│
├── backend/                               # Unit 3: Backend
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/
│   │   │   │   └── com/
│   │   │   │       └── tableorder/
│   │   │   │           ├── controller/
│   │   │   │           ├── service/
│   │   │   │           ├── repository/
│   │   │   │           ├── domain/
│   │   │   │           ├── dto/
│   │   │   │           ├── config/
│   │   │   │           ├── security/
│   │   │   │           ├── exception/
│   │   │   │           └── util/
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       ├── mybatis/
│   │   │       │   └── mapper/
│   │   │       └── static/
│   │   └── test/
│   ├── pom.xml (Maven) 또는 build.gradle (Gradle)
│   └── README.md
│
├── aidlc-docs/                            # 문서 전용 (코드 제외)
│   ├── inception/
│   ├── construction/
│   ├── aidlc-state.md
│   └── audit.md
│
└── README.md                              # 프로젝트 루트 README
```

### 빌드 및 패키징 전략

#### Customer Frontend
- **빌드 명령**: `npm run build` (in `frontend/customer/`)
- **산출물**: `frontend/customer/dist/` 또는 `frontend/customer/build/`
- **배포**: 정적 파일 서버 또는 CDN

#### Admin Frontend
- **빌드 명령**: `npm run build` (in `frontend/admin/`)
- **산출물**: `frontend/admin/dist/` 또는 `frontend/admin/build/`
- **배포**: 정적 파일 서버 또는 CDN

#### Backend
- **빌드 명령**: `mvn clean package` 또는 `gradle build` (in `backend/`)
- **산출물**: `backend/target/table-order-backend.jar` 또는 `backend/build/libs/table-order-backend.jar`
- **배포**: Java 실행 환경에서 JAR 실행

### 공통 모듈 처리
- **프론트엔드 공통**: 각 프론트엔드 앱에 공통 컴포넌트 복사 또는 npm 패키지로 분리 (향후 고려)
- **백엔드 공통**: 패키지 구조로 공통 기능 분리 (`config/`, `security/`, `exception/`, `util/`)

---

## Unit Boundaries and Interfaces

### Customer Frontend ↔ Backend
- **통신 방식**: REST API (Axios), SSE (EventSource)
- **데이터 형식**: JSON
- **인증**: 테이블 세션 ID (자동 로그인)

### Admin Frontend ↔ Backend
- **통신 방식**: REST API (Axios), SSE (EventSource)
- **데이터 형식**: JSON
- **인증**: JWT 토큰 (Authorization 헤더)

### Backend ↔ Database
- **통신 방식**: MyBatis SQL Mapper
- **데이터베이스**: H2 In-Memory
- **트랜잭션**: Spring `@Transactional`

---

## Development Sequence

### 권장 개발 순서 (User-Journey-First)

1. **Backend (Unit 3)** - 먼저 개발
   - 이유: 프론트엔드가 의존하는 API 제공
   - 우선순위: 인증 → 메뉴 조회 → 주문 생성 → 주문 상태 관리 → SSE → 메뉴 관리 → 테이블 관리

2. **Customer Frontend (Unit 1)** - 두 번째 개발
   - 이유: 고객 여정이 핵심 비즈니스 가치
   - 우선순위: 메뉴 조회 → 장바구니 → 주문 생성 → 주문 내역 → 실시간 업데이트

3. **Admin Frontend (Unit 2)** - 마지막 개발
   - 이유: 관리 기능은 고객 기능 이후 필요
   - 우선순위: 로그인 → 주문 모니터링 → 주문 상태 변경 → 메뉴 관리 → 테이블 관리

### 통합 테스트 전략 (Incremental Integration)
- **Phase 1**: Backend 단독 테스트 (Postman, curl)
- **Phase 2**: Backend + Customer Frontend 통합 테스트
- **Phase 3**: Backend + Admin Frontend 통합 테스트
- **Phase 4**: 전체 시스템 통합 테스트 (고객 주문 → 관리자 처리)

---

## Unit Validation

### 검증 항목
- [x] 모든 유닛의 책임이 명확히 정의됨
- [x] 유닛 간 경계가 명확함
- [x] 유닛 간 인터페이스가 정의됨
- [x] 각 유닛의 기술 스택이 결정됨
- [x] 코드 조직 전략이 정의됨 (Greenfield)
- [x] 배포 전략이 정의됨
- [x] 개발 순서가 결정됨
- [x] 통합 테스트 전략이 정의됨

### 유닛 크기 검증
- **Customer Frontend**: 적정 (8개 페이지/컴포넌트 그룹)
- **Admin Frontend**: 적정 (5개 페이지/컴포넌트 그룹)
- **Backend**: 적정 (6개 서비스, 5개 Mapper)

### 순환 의존성 확인
- **Customer Frontend → Backend**: 단방향 (API 호출)
- **Admin Frontend → Backend**: 단방향 (API 호출)
- **Backend → Frontend**: 단방향 (SSE 이벤트 전송)
- **순환 의존성**: 없음 ✅

---

## Notes

- 각 유닛은 독립적으로 개발 및 테스트 가능
- 프론트엔드 유닛은 완전히 별도 React 앱으로 분리
- 백엔드는 단일 Spring Boot 애플리케이션이지만 논리적 모듈로 구성
- 공통 컴포넌트는 패키지 구조로 분리
- 배포는 프론트엔드(정적 파일)와 백엔드(JAR)로 분리
- 개발 순서는 Backend → Customer Frontend → Admin Frontend
- 통합 테스트는 점진적으로 진행

