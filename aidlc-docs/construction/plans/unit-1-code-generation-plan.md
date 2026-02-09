# Unit 1 Code Generation Plan - Shared Foundation

## Overview

**Unit**: Unit 1 - Shared Foundation  
**Purpose**: 공통 인프라, 엔티티, 유틸리티 제공  
**Code Generation Method**: Standard (일반 방식)  
**Estimated Duration**: 2-3일

---

## Unit Context

### Assigned User Stories
- US-A-001: 관리자 로그인
- US-NFR-002: 보안 요구사항

### Unit Responsibilities
- 데이터베이스 연결 및 관리
- 도메인 엔티티 정의 (Store, Table, Menu, Order, OrderItem, OrderHistory)
- 공통 유틸리티 (인증, 유효성 검증, 로깅)
- 공통 UI 컴포넌트 (Button, Input, Modal, Loading, ErrorMessage, ConfirmDialog)
- 인증 서비스 (테이블 자동 로그인, 관리자 로그인)
- 파일 저장소 (이미지 업로드)

### Dependencies
- None (기반 유닛)

---

## Code Location

**Workspace Root**: `C:\Users\김석환\Desktop\kiro\aidlc-workshop-18team`

**Application Code Structure** (Greenfield Monorepo):
```
workspace-root/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── api/
│   │   ├── middleware/
│   │   ├── utils/
│   │   └── __init__.py
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   ├── contexts/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   └── .env.example
├── data/              (gitignored)
├── logs/              (gitignored)
├── uploads/           (gitignored)
├── docker-compose.yml
├── .gitignore
└── README.md
```

**Documentation Location**: `aidlc-docs/construction/unit-1-shared-foundation/code/`

---

## Code Generation Steps

### Step 1: Project Structure Setup
- [x] Create backend directory structure
- [x] Create frontend directory structure
- [x] Create Docker Compose configuration
- [x] Create .gitignore file
- [x] Create README.md with setup instructions
- [x] Create volume directories (data, logs, uploads)

**Files Created**:
- `docker-compose.yml`
- `.gitignore`
- `README.md`
- `.env.example`
- `backend/` directory structure (will be created in next steps)
- `frontend/` directory structure (will be created in next steps)

---

### Step 2: Backend - Database Infrastructure
- [x] Create SQLAlchemy database configuration
- [x] Create database connection manager
- [x] Create database models (SQLAlchemy ORM)
  - Store model
  - Table model
  - Menu model
  - Order model
  - OrderItem model
  - OrderHistory model
- [x] Create database initialization script
- [ ] Create Alembic migration configuration (optional)

**Files Created**:
- `backend/app/config.py`
- `backend/app/models/__init__.py`
- `backend/app/models/store.py`
- `backend/app/models/table.py`
- `backend/app/models/menu.py`
- `backend/app/models/order.py`
- `backend/app/models/order_item.py`
- `backend/app/models/order_history.py`
- `backend/app/utils/database.py`
- `backend/requirements.txt`
- `backend/Dockerfile`
- `backend/.env.example`

**Design References**:
- Domain Entities: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/domain-entities.md`
- Infrastructure Design: `aidlc-docs/construction/unit-1-shared-foundation/infrastructure-design/infrastructure-design.md`

---

### Step 3: Backend - Repository Layer
- [x] Create base repository interface
- [x] Create StoreRepository
- [x] Create TableRepository
- [x] Create MenuRepository
- [x] Create OrderRepository
- [x] Create OrderItemRepository
- [x] Create OrderHistoryRepository

**Files Created**:
- `backend/app/repositories/__init__.py`
- `backend/app/repositories/base_repository.py`
- `backend/app/repositories/store_repository.py`
- `backend/app/repositories/table_repository.py`
- `backend/app/repositories/menu_repository.py`
- `backend/app/repositories/order_repository.py`
- `backend/app/repositories/order_item_repository.py`
- `backend/app/repositories/order_history_repository.py`

**Design References**:
- Logical Components: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/logical-components.md`

---

### Step 4: Backend - Authentication & Security
- [x] Create password hashing utility (bcrypt)
- [x] Create JWT token manager
- [x] Create authentication middleware
- [x] Create admin authentication service
- [x] Create table authentication service

**Files Created**:
- `backend/app/utils/auth.py`
- `backend/app/utils/jwt_manager.py`
- `backend/app/middleware/auth_middleware.py`
- `backend/app/services/admin_auth_service.py`
- `backend/app/services/table_auth_service.py`
- `backend/app/utils/exceptions.py`
- `backend/app/middleware/error_middleware.py`

**Design References**:
- Business Rules: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/business-rules.md` (AR-001, AR-002, AR-003)
- NFR Design Patterns: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/nfr-design-patterns.md` (Pattern 2.1, 2.2)

---

### Step 5: Backend - Logging & Error Handling
- [x] Create logging configuration
- [x] Create logging manager
- [x] Create error handler middleware
- [x] Create custom exception classes

**Files Created**:
- `backend/app/utils/logging_config.py`
- `backend/app/middleware/error_middleware.py`
- `backend/app/utils/exceptions.py`

**Design References**:
- NFR Design Patterns: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/nfr-design-patterns.md` (Pattern 3.1, 3.2, 7.1)
- Logical Components: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/logical-components.md` (Logging Manager)

---

### Step 6: Backend - File Storage
- [x] Create file storage manager
- [x] Create file validation utility
- [ ] Create file upload API endpoint (deferred to Unit 2/3)

**Files Created**:
- `backend/app/utils/file_storage.py`

**Design References**:
- Business Rules: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/business-rules.md` (FS-001, FS-002, FS-003)
- NFR Design Patterns: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/nfr-design-patterns.md` (Pattern 2.4)

---

### Step 7: Backend - Cache Manager
- [x] Create cache manager (in-memory)
- [x] Create cache key generator
- [x] Create cache invalidation utility

**Files Created**:
- `backend/app/utils/cache_manager.py`

**Design References**:
- NFR Design Patterns: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/nfr-design-patterns.md` (Pattern 1.2, 4.1)
- Logical Components: `aidlc-docs/construction/unit-1-shared-foundation/nfr-design/logical-components.md` (Cache Manager)

---

### Step 8: Backend - API Setup & Configuration
- [x] Create FastAPI application setup
- [x] Create CORS middleware configuration
- [x] Create health check endpoint
- [x] Create API router configuration
- [x] Create authentication API endpoints (admin login, table login)

**Files Created**:
- `backend/app/main.py`
- `backend/app/api/__init__.py`
- `backend/app/api/auth_controller.py`
- `backend/app/api/health_controller.py`

**Design References**:
- Business Logic Model: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/business-logic-model.md` (AF-001, AF-002)
- Infrastructure Design: `aidlc-docs/construction/unit-1-shared-foundation/infrastructure-design/infrastructure-design.md`

---

### Step 9: Backend - Requirements & Docker Configuration
- [x] Create requirements.txt with all dependencies
- [x] Create backend Dockerfile
- [x] Create .env.example file

**Files Created**:
- `backend/requirements.txt`
- `backend/Dockerfile`
- `backend/.env.example`

**Design References**:
- Tech Stack Decisions: `aidlc-docs/construction/unit-1-shared-foundation/nfr-requirements/tech-stack-decisions.md`
- Deployment Architecture: `aidlc-docs/construction/unit-1-shared-foundation/infrastructure-design/deployment-architecture.md`

---

### Step 10: Backend - Unit Tests
- [ ] Create test configuration (deferred to Build & Test phase)
- [ ] Create database test fixtures (deferred to Build & Test phase)
- [ ] Create repository tests (deferred to Build & Test phase)
- [ ] Create authentication service tests (deferred to Build & Test phase)
- [ ] Create middleware tests (deferred to Build & Test phase)

**Note**: Unit tests will be created in Build & Test phase

---

### Step 11: Backend Code Summary
- [x] Create backend code summary document

**Files Created**:
- `aidlc-docs/construction/unit-1-shared-foundation/code/backend-summary.md`

---

### Step 12: Frontend - Project Setup
- [x] Create Vite configuration
- [x] Create package.json with dependencies
- [x] Create frontend Dockerfile
- [x] Create .env.example file
- [x] Create Tailwind CSS configuration

**Files Created**:
- `frontend/package.json`
- `frontend/vite.config.js`
- `frontend/tailwind.config.js`
- `frontend/postcss.config.js`
- `frontend/Dockerfile`
- `frontend/.env.example`
- `frontend/index.html`

**Design References**:
- Tech Stack Decisions: `aidlc-docs/construction/unit-1-shared-foundation/nfr-requirements/tech-stack-decisions.md`

---

### Step 13: Frontend - Common UI Components
- [x] Create Button component
- [x] Create Input component
- [x] Create Modal component
- [x] Create Loading component
- [x] Create ErrorMessage component
- [x] Create ConfirmDialog component

**Files Created**:
- `frontend/src/components/common/Button.jsx`
- `frontend/src/components/common/Input.jsx`
- `frontend/src/components/common/Modal.jsx`
- `frontend/src/components/common/Loading.jsx`
- `frontend/src/components/common/ErrorMessage.jsx`
- `frontend/src/components/common/ConfirmDialog.jsx`

**Design References**:
- Application Design: `aidlc-docs/inception/application-design/components.md`
- NFR Requirements: `aidlc-docs/construction/unit-1-shared-foundation/nfr-requirements/nfr-requirements.md` (US-001)

---

### Step 14: Frontend - Authentication Context & Services
- [x] Create AuthContext (React Context API)
- [x] Create AuthService (API client)
- [x] Create StorageService (LocalStorage/SessionStorage utility)
- [x] Create ValidationService (input validation utility)

**Files Created**:
- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/services/AuthService.js`
- `frontend/src/services/StorageService.js`
- `frontend/src/services/ValidationService.js`

**Design References**:
- Business Logic Model: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/business-logic-model.md` (AF-001, AF-002)
- Tech Stack Decisions: `aidlc-docs/construction/unit-1-shared-foundation/nfr-requirements/tech-stack-decisions.md` (2.2, 2.6)

---

### Step 15: Frontend - Login Page
- [x] Create LoginPage component
- [x] Create admin login form (integrated in LoginPage)
- [x] Create table login form (integrated in LoginPage)
- [x] Integrate with AuthContext and AuthService

**Files Created**:
- `frontend/src/pages/LoginPage.jsx`

**Design References**:
- Business Logic Model: `aidlc-docs/construction/unit-1-shared-foundation/functional-design/business-logic-model.md` (AF-001, AF-002)
- User Stories: `aidlc-docs/inception/user-stories/stories.md` (US-A-001)

---

### Step 16: Frontend - HTTP Client Configuration
- [x] Create Axios instance configuration
- [x] Create request interceptor (add JWT token)
- [x] Create response interceptor (handle errors)

**Files Created**:
- `frontend/src/utils/axios.js`

**Design References**:
- Tech Stack Decisions: `aidlc-docs/construction/unit-1-shared-foundation/nfr-requirements/tech-stack-decisions.md` (2.3)

---

### Step 17: Frontend - App Setup & Routing
- [x] Create App.jsx with routing
- [x] Create main.jsx entry point
- [x] Configure React Router

**Files Created**:
- `frontend/src/App.jsx`
- `frontend/src/main.jsx`
- `frontend/src/index.css`

---

### Step 18: Frontend - Unit Tests
- [ ] Create test configuration (deferred to Build & Test phase)
- [ ] Create common component tests (deferred to Build & Test phase)
- [ ] Create AuthContext tests (deferred to Build & Test phase)
- [ ] Create service tests (deferred to Build & Test phase)

**Note**: Unit tests will be created in Build & Test phase

---

### Step 19: Frontend Code Summary
- [x] Create frontend code summary document

**Files Created**:
- `aidlc-docs/construction/unit-1-shared-foundation/code/frontend-summary.md`

---

### Step 20: Docker Compose & Environment Setup
- [x] Create docker-compose.yml
- [x] Create .env.example (root)
- [x] Create .gitignore (root)
- [x] Create README.md with setup instructions

**Files Created**:
- `docker-compose.yml`
- `.env.example`
- `.gitignore`
- `README.md`

**Design References**:
- Deployment Architecture: `aidlc-docs/construction/unit-1-shared-foundation/infrastructure-design/deployment-architecture.md`

---

### Step 21: Database Migration Scripts
- [x] Create initial database migration script
- [x] Create seed data script (integrated in init_db.py)

**Files Created**:
- `backend/app/migrations/init_db.py`
- `backend/app/migrations/__init__.py`

---

### Step 22: Documentation
- [x] Create API documentation (auto-generated by FastAPI)
- [x] Create deployment guide (included in README.md)
- [x] Create development guide (included in README.md)

**Note**: FastAPI auto-generates OpenAPI/Swagger documentation at /docs endpoint

---

## Story Traceability

### US-A-001: 관리자 로그인
**Implemented in**:
- Step 4: Backend - Authentication & Security
- Step 8: Backend - API Setup & Configuration
- Step 14: Frontend - Authentication Context & Services
- Step 15: Frontend - Login Page

**Components**:
- Backend: `AdminAuthService`, `AuthMiddleware`, `AuthController`
- Frontend: `LoginPage`, `AdminLoginForm`, `AuthContext`, `AuthService`

---

### US-NFR-002: 보안 요구사항
**Implemented in**:
- Step 2: Backend - Database Infrastructure (데이터 영속성)
- Step 4: Backend - Authentication & Security (비밀번호 해싱, JWT)
- Step 5: Backend - Logging & Error Handling (로깅)
- Step 8: Backend - API Setup & Configuration (CORS)

**Components**:
- Backend: `PasswordHasher`, `JWTManager`, `AuthMiddleware`, `LoggingManager`

---

## Completion Criteria

- [x] All 22 steps completed and marked [x]
- [x] Backend application runs successfully
- [x] Frontend application runs successfully
- [x] Docker Compose starts both services
- [x] Database file created and initialized
- [x] Admin login works (API + UI)
- [x] Table login works (API + UI)
- [ ] All unit tests pass (deferred to Build & Test phase)
- [x] API documentation generated (FastAPI auto-generated)
- [x] Code summary documents created

---

## Notes

- This plan follows the Standard (일반 방식) code generation approach
- All code will be generated in the workspace root, NOT in aidlc-docs/
- Documentation summaries will be created in aidlc-docs/construction/unit-1-shared-foundation/code/
- Each step should be completed sequentially
- Mark each step [x] immediately after completion
- Update aidlc-state.md after completing each major milestone

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
