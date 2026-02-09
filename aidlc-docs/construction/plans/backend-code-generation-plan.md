# Backend Code Generation Plan (Standard Approach)

## Overview
이 계획은 Backend 유닛의 코드를 생성하는 상세한 단계를 정의합니다. Standard 방식으로 코드를 먼저 생성하고, 이후 테스트를 작성합니다.

## Unit Context

### Unit Information
- **Unit Name**: Backend
- **Unit Type**: Spring Boot Application (Monolithic)
- **Priority**: 1 (First to implement)
- **Tech Stack**: Java 17, Spring Boot 3.x, MyBatis, H2 In-Memory, JWT, SSE

### Stories Implemented by This Unit
Backend 유닛은 모든 32개 User Stories를 구현합니다:
- Feature 1: 테이블 세션 관리 (5 stories)
- Feature 2: 메뉴 조회 (1 story)
- Feature 3: 장바구니 관리 (3 stories)
- Feature 4: 주문 생성 및 조회 (3 stories)
- Feature 5: 주문 모니터링 (관리자) (3 stories)
- Feature 6: 주문 상태 관리 (관리자) (3 stories)
- Feature 7: 메뉴 관리 (관리자) (5 stories)
- Feature 8: 테이블 관리 (관리자) (4 stories)
- Feature 9: 주문 이력 조회 (관리자) (2 stories)
- Feature 10: 관리자 인증 (3 stories)

### Dependencies
- **External**: None (standalone backend)
- **Internal**: None (monolithic architecture)
- **Database**: H2 In-Memory (self-contained)
- **Clients**: Customer Frontend, Admin Frontend (SSE + REST API)

### Code Location
- **Workspace Root**: `c:\AWS Kiro\AI-DLC Workshop-18\aidlc-workshop-18team`
- **Application Code**: `backend/` (new directory in workspace root)
- **Documentation**: `aidlc-docs/construction/backend/code/`

### Project Structure Pattern
Greenfield multi-unit (monolith with separate unit directories):
```
backend/
├── src/
│   └── main/
│       ├── java/
│       │   └── com/
│       │       └── tableorder/
│       │           ├── common/
│       │           ├── config/
│       │           ├── controller/
│       │           ├── domain/
│       │           ├── dto/
│       │           ├── exception/
│       │           ├── infrastructure/
│       │           ├── mapper/
│       │           ├── security/
│       │           ├── service/
│       │           └── util/
│       └── resources/
│           ├── mybatis/
│           │   └── mapper/
│           ├── application.yml
│           ├── application-dev.yml
│           └── logback-spring.xml
├── pom.xml
└── README.md
```

---

## Code Generation Steps


### Phase 1: Project Structure Setup

**Step 1: Create Maven Project Structure**
- [x] Create `backend/` directory in workspace root
- [x] Create `backend/pom.xml` with dependencies
- [x] Create `backend/src/main/java/com/tableorder/` package structure
- [x] Create `backend/src/main/resources/` directory
- [x] Create `backend/src/test/java/com/tableorder/` package structure
- [x] Create `backend/README.md`

**Dependencies to include in pom.xml**:
- spring-boot-starter-web
- spring-boot-starter-security
- spring-boot-starter-webflux (SSE)
- spring-boot-starter-cache
- mybatis-spring-boot-starter
- h2
- jjwt-api, jjwt-impl, jjwt-jackson
- caffeine
- springdoc-openapi-starter-webmvc-ui
- lombok
- spring-boot-starter-test

---

### Phase 2: Domain Layer Generation

**Step 2: Generate Store Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/Store.java`
- [ ] Implement all attributes from domain-entities.md
- [ ] Add Lombok annotations (@Data, @Builder, @NoArgsConstructor, @AllArgsConstructor)
- [ ] Add validation annotations

**Step 3: Generate Table Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/Table.java`
- [ ] Implement all attributes including sessionId, sessionStatus
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 4: Generate Menu Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/Menu.java`
- [ ] Implement all attributes including deleted flag
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 5: Generate Order Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/Order.java`
- [ ] Implement all attributes including version (optimistic locking)
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 6: Generate OrderItem Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/OrderItem.java`
- [ ] Implement all attributes including unitPrice snapshot
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 7: Generate OrderHistory Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/OrderHistory.java`
- [ ] Implement all attributes for archived orders
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 8: Generate OrderHistoryItem Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/OrderHistoryItem.java`
- [ ] Implement all attributes
- [ ] Add Lombok annotations
- [ ] Add validation annotations

**Step 9: Generate User Entity**
- [ ] Create `backend/src/main/java/com/tableorder/domain/User.java`
- [ ] Implement all attributes including loginAttempts, lockedUntil
- [ ] Add Lombok annotations
- [ ] Add validation annotations

---

### Phase 3: DTO Layer Generation

**Step 10: Generate Common DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/ApiResponse.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/ErrorResponse.java`

**Step 11: Generate Order DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/order/CreateOrderRequest.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/order/OrderItemRequest.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/order/OrderResponse.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/order/OrderItemResponse.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/order/UpdateOrderStatusRequest.java`

**Step 12: Generate Menu DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/menu/CreateMenuRequest.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/menu/UpdateMenuRequest.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/menu/MenuResponse.java`

**Step 13: Generate Table DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/table/TableResponse.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/table/StartSessionRequest.java`

**Step 14: Generate Auth DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/auth/LoginRequest.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/auth/LoginResponse.java`
- [ ] Create `backend/src/main/java/com/tableorder/dto/auth/UserResponse.java`

**Step 15: Generate SSE DTOs**
- [ ] Create `backend/src/main/java/com/tableorder/dto/sse/SseEvent.java`

---

### Phase 4: Exception Layer Generation

**Step 16: Generate Base Exception**
- [ ] Create `backend/src/main/java/com/tableorder/exception/BusinessException.java` (abstract)

**Step 17: Generate Specific Exceptions**
- [ ] Create `backend/src/main/java/com/tableorder/exception/OrderNotFoundException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/InvalidSessionException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/MenuNotFoundException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/InvalidStatusTransitionException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/OptimisticLockException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/AccountLockedException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/FileUploadException.java`
- [ ] Create `backend/src/main/java/com/tableorder/exception/TableNotFoundException.java`

**Step 18: Generate Global Exception Handler**
- [ ] Create `backend/src/main/java/com/tableorder/exception/GlobalExceptionHandler.java`
- [ ] Implement @RestControllerAdvice
- [ ] Handle all exception types with appropriate HTTP status codes

---

### Phase 5: Mapper Layer Generation

**Step 19: Generate Store Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/StoreMapper.java` (interface)
- [ ] Create `backend/src/main/resources/mybatis/mapper/StoreMapper.xml`
- [ ] Implement CRUD operations

**Step 20: Generate Table Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/TableMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/TableMapper.xml`
- [ ] Implement session management queries

**Step 21: Generate Menu Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/MenuMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/MenuMapper.xml`
- [ ] Implement CRUD with logical delete

**Step 22: Generate Order Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/OrderMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/OrderMapper.xml`
- [ ] Implement order queries with optimistic locking

**Step 23: Generate OrderItem Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/OrderItemMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/OrderItemMapper.xml`
- [ ] Implement order item operations

**Step 24: Generate OrderHistory Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/OrderHistoryMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/OrderHistoryMapper.xml`
- [ ] Implement history archival queries

**Step 25: Generate User Mapper**
- [ ] Create `backend/src/main/java/com/tableorder/mapper/UserMapper.java`
- [ ] Create `backend/src/main/resources/mybatis/mapper/UserMapper.xml`
- [ ] Implement user authentication queries

---

### Phase 6: Utility Layer Generation

**Step 26: Generate Utility Classes**
- [ ] Create `backend/src/main/java/com/tableorder/util/OrderNumberGenerator.java`
- [ ] Create `backend/src/main/java/com/tableorder/util/DateTimeUtil.java`
- [ ] Create `backend/src/main/java/com/tableorder/util/HashUtil.java` (SHA-256)

---

### Phase 7: Security Layer Generation

**Step 27: Generate JWT Components**
- [ ] Create `backend/src/main/java/com/tableorder/security/JwtTokenProvider.java`
- [ ] Create `backend/src/main/java/com/tableorder/security/JwtAuthenticationFilter.java`

**Step 28: Generate Security Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/security/SecurityConfig.java`
- [ ] Configure filter chain, CORS, password encoder

---

### Phase 8: Infrastructure Layer Generation

**Step 29: Generate SSE Service**
- [ ] Create `backend/src/main/java/com/tableorder/infrastructure/sse/SSEService.java`
- [ ] Implement connection management (ConcurrentHashMap)
- [ ] Implement event broadcasting

**Step 30: Generate File Service**
- [ ] Create `backend/src/main/java/com/tableorder/infrastructure/file/FileService.java`
- [ ] Implement file upload, validation, deletion
- [ ] Add @Retryable annotation

---

### Phase 9: Service Layer Generation

**Step 31: Generate Order Service**
- [ ] Create `backend/src/main/java/com/tableorder/service/OrderService.java`
- [ ] Implement createOrder() workflow
- [ ] Implement updateOrderStatus() with optimistic locking
- [ ] Implement deleteOrder()
- [ ] Implement getOrders() queries

**Step 32: Generate Menu Service**
- [ ] Create `backend/src/main/java/com/tableorder/service/MenuService.java`
- [ ] Implement createMenu() with file upload
- [ ] Implement updateMenu()
- [ ] Implement deleteMenu() (logical)
- [ ] Implement getMenus() with caching

**Step 33: Generate Table Service**
- [ ] Create `backend/src/main/java/com/tableorder/service/TableService.java`
- [ ] Implement startSession()
- [ ] Implement endSession() with order archival
- [ ] Implement getTables()

**Step 34: Generate Auth Service**
- [ ] Create `backend/src/main/java/com/tableorder/service/AuthService.java`
- [ ] Implement login() with account locking
- [ ] Implement JWT token generation

**Step 35: Generate Store Service**
- [ ] Create `backend/src/main/java/com/tableorder/service/StoreService.java`
- [ ] Implement getStore() with caching

---

### Phase 10: Controller Layer Generation

**Step 36: Generate Customer Order Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/customer/CustomerOrderController.java`
- [ ] Implement POST /api/customer/orders (create order)
- [ ] Implement GET /api/customer/orders (get orders by session)
- [ ] Add @Valid annotations for request validation

**Step 37: Generate Customer Menu Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/customer/CustomerMenuController.java`
- [ ] Implement GET /api/customer/menus (get menus by store)

**Step 38: Generate Customer SSE Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/customer/CustomerSSEController.java`
- [ ] Implement GET /api/customer/sse (SSE connection)

**Step 39: Generate Admin Order Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/admin/AdminOrderController.java`
- [ ] Implement GET /api/admin/orders (get all orders)
- [ ] Implement PUT /api/admin/orders/{id}/status (update status)
- [ ] Implement DELETE /api/admin/orders/{id} (delete order)

**Step 40: Generate Admin Menu Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/admin/AdminMenuController.java`
- [ ] Implement POST /api/admin/menus (create menu)
- [ ] Implement PUT /api/admin/menus/{id} (update menu)
- [ ] Implement DELETE /api/admin/menus/{id} (delete menu)
- [ ] Implement GET /api/admin/menus (get all menus)

**Step 41: Generate Admin Table Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/admin/AdminTableController.java`
- [ ] Implement POST /api/admin/tables/{id}/start-session (start session)
- [ ] Implement POST /api/admin/tables/{id}/end-session (end session)
- [ ] Implement GET /api/admin/tables (get all tables)

**Step 42: Generate Admin SSE Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/admin/AdminSSEController.java`
- [ ] Implement GET /api/admin/sse (SSE connection)

**Step 43: Generate Auth Controller**
- [ ] Create `backend/src/main/java/com/tableorder/controller/auth/AuthController.java`
- [ ] Implement POST /api/auth/login (admin login)

---

### Phase 11: Configuration Layer Generation

**Step 44: Generate Cache Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/config/CacheConfig.java`
- [ ] Configure Caffeine cache manager

**Step 45: Generate Async Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/config/AsyncConfig.java`
- [ ] Configure ThreadPoolTaskExecutor

**Step 46: Generate Retry Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/config/RetryConfig.java`
- [ ] Enable Spring Retry

**Step 47: Generate CORS Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/config/CorsConfig.java`
- [ ] Configure CORS filter

**Step 48: Generate Swagger Configuration**
- [ ] Create `backend/src/main/java/com/tableorder/config/SwaggerConfig.java`
- [ ] Configure OpenAPI documentation

---

### Phase 12: Application Configuration Files

**Step 49: Generate application.yml**
- [ ] Create `backend/src/main/resources/application.yml`
- [ ] Configure server port, datasource, H2 console, MyBatis, JWT, file upload, caching, logging

**Step 50: Generate application-dev.yml**
- [ ] Create `backend/src/main/resources/application-dev.yml`
- [ ] Configure development-specific settings

**Step 51: Generate logback-spring.xml**
- [ ] Create `backend/src/main/resources/logback-spring.xml`
- [ ] Configure console and file appenders

---

### Phase 13: Database Schema Generation

**Step 52: Generate H2 Schema SQL**
- [ ] Create `backend/src/main/resources/schema.sql`
- [ ] Define all tables with constraints and indexes
- [ ] Include CREATE TABLE statements for all 8 entities

**Step 53: Generate H2 Data SQL (Optional)**
- [ ] Create `backend/src/main/resources/data.sql`
- [ ] Insert sample data for development (stores, tables, menus, users)

---

### Phase 14: Main Application Class

**Step 54: Generate Spring Boot Application**
- [ ] Create `backend/src/main/java/com/tableorder/TableOrderApplication.java`
- [ ] Add @SpringBootApplication annotation
- [ ] Add main() method

---

### Phase 15: Unit Testing

**Step 55: Generate Service Layer Tests**
- [ ] Create `backend/src/test/java/com/tableorder/service/OrderServiceTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/service/MenuServiceTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/service/TableServiceTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/service/AuthServiceTest.java`
- [ ] Use @SpringBootTest, @MockBean for dependencies

**Step 56: Generate Controller Layer Tests**
- [ ] Create `backend/src/test/java/com/tableorder/controller/CustomerOrderControllerTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/controller/AdminOrderControllerTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/controller/AdminMenuControllerTest.java`
- [ ] Use @WebMvcTest, MockMvc

**Step 57: Generate Utility Tests**
- [ ] Create `backend/src/test/java/com/tableorder/util/OrderNumberGeneratorTest.java`
- [ ] Create `backend/src/test/java/com/tableorder/util/HashUtilTest.java`

---

### Phase 16: Documentation Generation

**Step 58: Generate Code Summary**
- [ ] Create `aidlc-docs/construction/backend/code/code-summary.md`
- [ ] Document all generated classes with package structure
- [ ] Include file count and line count estimates

**Step 59: Generate API Documentation Summary**
- [ ] Create `aidlc-docs/construction/backend/code/api-documentation.md`
- [ ] List all REST API endpoints with methods, paths, descriptions
- [ ] Reference Swagger UI for interactive documentation

**Step 60: Generate Testing Guide**
- [ ] Create `aidlc-docs/construction/backend/code/testing-guide.md`
- [ ] Document how to run unit tests
- [ ] Document how to run integration tests (Build & Test phase)

**Step 61: Update Backend README**
- [ ] Update `backend/README.md`
- [ ] Add project description, tech stack, setup instructions
- [ ] Add build and run instructions

---

### Phase 17: Deployment Artifacts

**Step 62: Generate Restart Script**
- [ ] Create `backend/restart.sh`
- [ ] Implement start, stop, restart, status functions
- [ ] Add executable permissions instructions

**Step 63: Generate Jenkinsfile**
- [ ] Create `backend/Jenkinsfile`
- [ ] Define pipeline stages: Checkout, Build, Test, Deploy, Verify

**Step 64: Generate .gitignore**
- [ ] Create `backend/.gitignore`
- [ ] Exclude target/, logs/, *.log, .env

---

## Story Traceability

### Feature 1: 테이블 세션 관리
- Story 1.1: 테이블 PIN 입력 → TableService.startSession()
- Story 1.2: 세션 ID 생성 → TableService.startSession()
- Story 1.3: 세션 유효성 확인 → OrderService validation
- Story 1.4: 세션 종료 → TableService.endSession()
- Story 1.5: 세션 만료 처리 → (Frontend timeout handling)

### Feature 2: 메뉴 조회
- Story 2.1: 메뉴 목록 조회 → MenuService.getMenus(), CustomerMenuController

### Feature 3: 장바구니 관리
- Story 3.1-3.3: 장바구니 → (Frontend state management, no backend)

### Feature 4: 주문 생성 및 조회
- Story 4.1: 주문 생성 → OrderService.createOrder(), CustomerOrderController
- Story 4.2: 주문 내역 조회 → OrderService.getOrders(), CustomerOrderController
- Story 4.3: 실시간 주문 상태 → SSEService, CustomerSSEController

### Feature 5: 주문 모니터링 (관리자)
- Story 5.1: 주문 목록 조회 → OrderService.getOrders(), AdminOrderController
- Story 5.2: 실시간 주문 알림 → SSEService, AdminSSEController
- Story 5.3: 주문 상세 조회 → OrderService.getOrder(), AdminOrderController

### Feature 6: 주문 상태 관리 (관리자)
- Story 6.1: 주문 상태 변경 → OrderService.updateOrderStatus(), AdminOrderController
- Story 6.2: 주문 이력 이동 → TableService.endSession() (OrderHistory)
- Story 6.3: 주문 삭제 → OrderService.deleteOrder(), AdminOrderController

### Feature 7: 메뉴 관리 (관리자)
- Story 7.1: 메뉴 목록 조회 → MenuService.getMenus(), AdminMenuController
- Story 7.2: 메뉴 등록 → MenuService.createMenu(), AdminMenuController
- Story 7.3: 메뉴 수정 → MenuService.updateMenu(), AdminMenuController
- Story 7.4: 메뉴 삭제 → MenuService.deleteMenu(), AdminMenuController
- Story 7.5: 메뉴 이미지 관리 → FileService, MenuService

### Feature 8: 테이블 관리 (관리자)
- Story 8.1: 테이블 목록 조회 → TableService.getTables(), AdminTableController
- Story 8.2: 테이블 세션 시작 → TableService.startSession(), AdminTableController
- Story 8.3: 테이블 세션 종료 → TableService.endSession(), AdminTableController
- Story 8.4: 테이블 상태 확인 → TableService.getTables(), AdminTableController

### Feature 9: 주문 이력 조회 (관리자)
- Story 9.1: 주문 이력 조회 → OrderHistoryService (future), AdminOrderController
- Story 9.2: 주문 이력 필터링 → OrderHistoryService (future)

### Feature 10: 관리자 인증
- Story 10.1: 관리자 로그인 → AuthService.login(), AuthController
- Story 10.2: JWT 토큰 발급 → JwtTokenProvider, AuthService
- Story 10.3: 계정 잠금 → AuthService.login() (loginAttempts)

---

## Completion Criteria

- [ ] All 64 steps completed and marked [x]
- [ ] All 32 user stories implemented
- [ ] All code generated in `backend/` directory (not aidlc-docs/)
- [ ] All tests generated in `backend/src/test/`
- [ ] All documentation generated in `aidlc-docs/construction/backend/code/`
- [ ] pom.xml with all dependencies
- [ ] application.yml with all configurations
- [ ] schema.sql with all tables
- [ ] README.md with setup instructions
- [ ] Deployment artifacts (restart.sh, Jenkinsfile)

---

## Notes

- This is a Standard (non-TDD) approach: code first, then tests
- All application code goes to `backend/` directory in workspace root
- Documentation goes to `aidlc-docs/construction/backend/code/`
- Tests will be executed in Build & Test phase
- Total estimated files: ~100+ Java files, ~10 XML files, ~10 config files
- Total estimated lines: ~15,000-20,000 lines of code

