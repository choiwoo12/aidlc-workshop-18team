# Unit Test Execution

## Overview

Backend 유닛의 단위 테스트 실행 가이드입니다. Standard 코드 생성 방식을 사용했으므로, 테스트 코드를 먼저 작성한 후 실행합니다.

**Note**: TDD 방식을 사용하지 않았으므로, 테스트 코드는 implementation-guide.md와 testing-guide.md를 참고하여 작성해야 합니다.

---

## Prerequisites

### Required
- ✅ Build 성공 (`build-instructions.md` 참고)
- ✅ JDK 17 설치
- ✅ Maven 3.6+ 설치

### Test Dependencies
`pom.xml`에 이미 포함된 테스트 의존성:
- `spring-boot-starter-test` (JUnit 5, Mockito, AssertJ)
- `spring-security-test` (Security 테스트)
- `h2` (In-Memory Database)

---

## Test Structure

### Test Directory Structure
```
backend/src/test/java/com/tableorder/
├── controller/                    # Controller 테스트
│   ├── admin/
│   │   ├── AdminOrderControllerTest.java
│   │   ├── AdminMenuControllerTest.java
│   │   └── AdminTableControllerTest.java
│   ├── auth/
│   │   └── AuthControllerTest.java
│   └── customer/
│       ├── CustomerOrderControllerTest.java
│       ├── CustomerMenuControllerTest.java
│       └── CustomerSSEControllerTest.java
├── service/                       # Service 테스트
│   ├── OrderServiceTest.java
│   ├── MenuServiceTest.java
│   ├── TableServiceTest.java
│   ├── AuthServiceTest.java
│   └── StoreServiceTest.java
├── util/                          # Utility 테스트
│   ├── OrderNumberGeneratorTest.java
│   ├── HashUtilTest.java
│   └── DateTimeUtilTest.java
├── infrastructure/                # Infrastructure 테스트
│   ├── SSEServiceTest.java
│   └── FileServiceTest.java
└── security/                      # Security 테스트
    ├── JwtTokenProviderTest.java
    └── JwtAuthenticationFilterTest.java
```

---

## Test Writing Guidelines

### 1. Service Layer Tests

**Example**: `OrderServiceTest.java`
```java
@SpringBootTest
@Transactional
class OrderServiceTest {
    
    @Autowired
    private OrderService orderService;
    
    @MockBean
    private OrderMapper orderMapper;
    
    @MockBean
    private SSEService sseService;
    
    @Test
    @DisplayName("주문 생성 성공")
    void createOrder_Success() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        // ... setup request
        
        // When
        OrderResponse response = orderService.createOrder(request);
        
        // Then
        assertThat(response).isNotNull();
        assertThat(response.getOrderNumber()).startsWith("ORD-");
    }
    
    @Test
    @DisplayName("주문 생성 실패 - 유효하지 않은 세션")
    void createOrder_InvalidSession() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        request.setSessionId("invalid-session");
        
        // When & Then
        assertThatThrownBy(() -> orderService.createOrder(request))
            .isInstanceOf(InvalidSessionException.class);
    }
}
```

### 2. Controller Layer Tests

**Example**: `CustomerOrderControllerTest.java`
```java
@WebMvcTest(CustomerOrderController.class)
class CustomerOrderControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private OrderService orderService;
    
    @Test
    @DisplayName("주문 생성 API 성공")
    void createOrder_Success() throws Exception {
        // Given
        CreateOrderRequest request = new CreateOrderRequest();
        // ... setup request
        
        OrderResponse response = new OrderResponse();
        // ... setup response
        
        when(orderService.createOrder(any())).thenReturn(response);
        
        // When & Then
        mockMvc.perform(post("/api/customer/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.success").value(true))
            .andExpect(jsonPath("$.data.orderNumber").exists());
    }
}
```

### 3. Utility Tests

**Example**: `OrderNumberGeneratorTest.java`
```java
class OrderNumberGeneratorTest {
    
    private OrderNumberGenerator generator;
    
    @BeforeEach
    void setUp() {
        generator = new OrderNumberGenerator();
    }
    
    @Test
    @DisplayName("주문 번호 생성 - 형식 검증")
    void generate_ValidFormat() {
        // When
        String orderNumber = generator.generate();
        
        // Then
        assertThat(orderNumber).matches("ORD-\\d{8}-\\d{4}");
    }
    
    @Test
    @DisplayName("주문 번호 생성 - 유니크 검증")
    void generate_Unique() {
        // When
        String orderNumber1 = generator.generate();
        String orderNumber2 = generator.generate();
        
        // Then
        assertThat(orderNumber1).isNotEqualTo(orderNumber2);
    }
}
```

---

## Run Unit Tests

### 1. Run All Unit Tests
```bash
cd backend
mvn test
```

**Expected Output**:
```
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.tableorder.service.OrderServiceTest
[INFO] Tests run: 10, Failures: 0, Errors: 0, Skipped: 0
[INFO] Running com.tableorder.controller.CustomerOrderControllerTest
[INFO] Tests run: 8, Failures: 0, Errors: 0, Skipped: 0
...
[INFO] 
[INFO] Results:
[INFO] 
[INFO] Tests run: XX, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

### 2. Run Specific Test Class
```bash
mvn test -Dtest=OrderServiceTest
```

### 3. Run Specific Test Method
```bash
mvn test -Dtest=OrderServiceTest#createOrder_Success
```

### 4. Run Tests by Package
```bash
# Service 테스트만 실행
mvn test -Dtest=com.tableorder.service.*Test

# Controller 테스트만 실행
mvn test -Dtest=com.tableorder.controller.*Test
```

---

## Test Coverage

### 1. Generate Coverage Report
```bash
mvn test jacoco:report
```

**Coverage Report Location**: `target/site/jacoco/index.html`

### 2. View Coverage Report
```bash
# Linux/Mac
open target/site/jacoco/index.html

# Windows
start target/site/jacoco/index.html
```

### 3. Expected Coverage
- **Overall**: 70-80%
- **Service Layer**: 80-90% (핵심 비즈니스 로직)
- **Controller Layer**: 70-80%
- **Utility Layer**: 90-100% (단순 유틸리티)
- **Domain Layer**: 50-60% (주로 getter/setter)

---

## Test Categories

### 1. Service Layer Tests (Priority: High)

**Test Scenarios**:
- ✅ **OrderService**: 주문 생성, 조회, 상태 변경, 삭제, 검증
- ✅ **MenuService**: 메뉴 생성, 조회, 수정, 삭제, 이미지 업로드
- ✅ **TableService**: 세션 시작, 종료, 조회, 검증
- ✅ **AuthService**: 로그인, JWT 생성, 검증
- ✅ **StoreService**: 매장 조회, 데이터 격리

**Expected Tests**: ~50-60 tests

### 2. Controller Layer Tests (Priority: High)

**Test Scenarios**:
- ✅ **Request Validation**: 입력 검증 (형식, 필수 필드)
- ✅ **Success Cases**: 정상 응답 (200 OK)
- ✅ **Error Cases**: 에러 응답 (400, 404, 500)
- ✅ **Security**: JWT 인증, 권한 검증

**Expected Tests**: ~40-50 tests

### 3. Utility Layer Tests (Priority: Medium)

**Test Scenarios**:
- ✅ **OrderNumberGenerator**: 주문 번호 생성, 형식 검증
- ✅ **HashUtil**: SHA-256 해싱, 검증
- ✅ **DateTimeUtil**: 날짜/시간 변환, 포맷팅

**Expected Tests**: ~10-15 tests

### 4. Infrastructure Layer Tests (Priority: Medium)

**Test Scenarios**:
- ✅ **SSEService**: 연결 관리, 이벤트 전송, 타임아웃
- ✅ **FileService**: 파일 업로드, 저장, 삭제, 검증

**Expected Tests**: ~10-15 tests

### 5. Security Layer Tests (Priority: High)

**Test Scenarios**:
- ✅ **JwtTokenProvider**: 토큰 생성, 검증, 만료
- ✅ **JwtAuthenticationFilter**: 필터 동작, 인증 처리

**Expected Tests**: ~10-15 tests

---

## Test Execution Strategy

### Phase 1: Utility & Domain Tests
```bash
mvn test -Dtest=com.tableorder.util.*Test
```
**Duration**: ~5초
**Expected**: 10-15 tests pass

### Phase 2: Service Tests
```bash
mvn test -Dtest=com.tableorder.service.*Test
```
**Duration**: ~10-15초
**Expected**: 50-60 tests pass

### Phase 3: Controller Tests
```bash
mvn test -Dtest=com.tableorder.controller.*Test
```
**Duration**: ~15-20초
**Expected**: 40-50 tests pass

### Phase 4: Infrastructure & Security Tests
```bash
mvn test -Dtest=com.tableorder.infrastructure.*Test,com.tableorder.security.*Test
```
**Duration**: ~10초
**Expected**: 20-30 tests pass

### Phase 5: All Tests
```bash
mvn test
```
**Duration**: ~30-40초
**Expected**: 120-150 tests pass

---

## Troubleshooting

### Issue 1: Tests Fail with "Cannot find bean"
**Symptoms**:
```
NoSuchBeanDefinitionException: No qualifying bean of type 'XXX'
```

**Solutions**:
1. `@SpringBootTest` 또는 `@WebMvcTest` 어노테이션 확인
2. `@MockBean` 또는 `@Autowired` 사용 확인
3. Configuration 클래스 확인

### Issue 2: H2 Database Connection Error
**Symptoms**:
```
JdbcSQLException: Database not found
```

**Solutions**:
1. `application.yml` 설정 확인
2. `schema.sql` 파일 존재 확인
3. H2 의존성 확인 (`pom.xml`)

### Issue 3: Test Timeout
**Symptoms**:
```
Test timed out after 60 seconds
```

**Solutions**:
1. `@Timeout` 어노테이션 추가: `@Timeout(value = 10, unit = TimeUnit.SECONDS)`
2. 무한 루프 확인
3. Mock 설정 확인

### Issue 4: Flaky Tests (간헐적 실패)
**Symptoms**:
- 테스트가 때때로 실패함

**Solutions**:
1. 시간 의존성 제거 (고정된 시간 사용)
2. 비동기 처리 확인 (`@Async` 테스트)
3. 테스트 격리 확인 (`@Transactional`)

---

## Test Best Practices

### 1. Test Naming Convention
```java
// Pattern: methodName_scenario_expectedResult
@Test
void createOrder_ValidRequest_ReturnsOrderResponse() { }

@Test
void createOrder_InvalidSession_ThrowsException() { }
```

### 2. AAA Pattern (Arrange-Act-Assert)
```java
@Test
void testExample() {
    // Arrange (Given)
    // ... setup test data
    
    // Act (When)
    // ... execute method
    
    // Assert (Then)
    // ... verify results
}
```

### 3. Use AssertJ for Fluent Assertions
```java
// Good
assertThat(result).isNotNull();
assertThat(result.getOrderNumber()).startsWith("ORD-");

// Avoid
assertTrue(result != null);
assertTrue(result.getOrderNumber().startsWith("ORD-"));
```

### 4. Mock External Dependencies
```java
@MockBean
private OrderMapper orderMapper;

@MockBean
private SSEService sseService;

// Mock behavior
when(orderMapper.findById(anyLong())).thenReturn(order);
```

### 5. Test Edge Cases
- ✅ Null values
- ✅ Empty collections
- ✅ Boundary values
- ✅ Invalid inputs
- ✅ Exception scenarios

---

## Test Report

### 1. Surefire Report
```bash
mvn surefire-report:report
```

**Report Location**: `target/site/surefire-report.html`

### 2. Test Results Summary
```
Tests run: XXX
Failures: 0
Errors: 0
Skipped: 0
Success rate: 100%
Time elapsed: XX.XXX sec
```

---

## Requirements Coverage

### User Story Coverage
모든 32개 User Stories는 다음 테스트로 검증됩니다:

#### Feature 1: 테이블 세션 관리 (5 stories)
- `TableServiceTest`: 세션 시작, 종료, 조회, 검증
- `AdminTableControllerTest`: API 테스트

#### Feature 2: 메뉴 조회 (1 story)
- `MenuServiceTest`: 메뉴 조회
- `CustomerMenuControllerTest`: API 테스트

#### Feature 4: 주문 생성 및 조회 (3 stories)
- `OrderServiceTest`: 주문 생성, 조회, 검증
- `CustomerOrderControllerTest`: API 테스트
- `SSEServiceTest`: 실시간 알림

#### Feature 5: 주문 모니터링 (3 stories)
- `OrderServiceTest`: 주문 목록 조회
- `AdminOrderControllerTest`: API 테스트
- `SSEServiceTest`: 실시간 업데이트

#### Feature 6: 주문 상태 관리 (3 stories)
- `OrderServiceTest`: 상태 변경, 삭제, 이력 저장
- `AdminOrderControllerTest`: API 테스트

#### Feature 7: 메뉴 관리 (5 stories)
- `MenuServiceTest`: CRUD, 이미지 업로드
- `AdminMenuControllerTest`: API 테스트
- `FileServiceTest`: 파일 처리

#### Feature 8: 테이블 관리 (4 stories)
- `TableServiceTest`: CRUD
- `AdminTableControllerTest`: API 테스트

#### Feature 9: 주문 이력 조회 (2 stories)
- `OrderServiceTest`: 이력 조회
- `AdminOrderControllerTest`: API 테스트

#### Feature 10: 관리자 인증 (3 stories)
- `AuthServiceTest`: 로그인, JWT 생성
- `AuthControllerTest`: API 테스트
- `JwtTokenProviderTest`: JWT 검증

---

## Next Steps

Unit 테스트 성공 후:
1. ✅ **Integration Tests**: `integration-test-instructions.md` 참고
2. ✅ **Performance Tests**: `performance-test-instructions.md` 참고 (optional)
3. ✅ **Test Summary**: `build-and-test-summary.md` 참고

---

## References

- **Testing Guide**: `aidlc-docs/construction/backend/code/testing-guide.md`
- **Implementation Guide**: `aidlc-docs/construction/backend/code/implementation-guide.md`
- **JUnit 5 Documentation**: https://junit.org/junit5/docs/current/user-guide/
- **Spring Boot Testing**: https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing
- **AssertJ Documentation**: https://assertj.github.io/doc/
