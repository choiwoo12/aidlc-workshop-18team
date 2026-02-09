# Integration Test Instructions

## Purpose

Backend 유닛의 통합 테스트 가이드입니다. 여러 컴포넌트 간의 상호작용과 전체 시스템 흐름을 검증합니다.

---

## Integration Test Scope

### What to Test
- ✅ **Controller → Service → Mapper → Database** 전체 흐름
- ✅ **SSE 이벤트 전송 및 수신**
- ✅ **JWT 인증 및 권한 검증**
- ✅ **파일 업로드 및 저장**
- ✅ **트랜잭션 및 롤백**
- ✅ **캐싱 동작**
- ✅ **예외 처리 및 에러 응답**

### What NOT to Test
- ❌ 외부 시스템 연동 (없음)
- ❌ Frontend 통합 (별도 E2E 테스트)
- ❌ 성능 테스트 (별도 performance-test-instructions.md)

---

## Test Environment Setup

### 1. Prerequisites
- ✅ Build 성공 (`build-instructions.md` 참고)
- ✅ Unit 테스트 성공 (`unit-test-instructions.md` 참고)
- ✅ JDK 17, Maven 3.6+

### 2. Test Configuration

**Create**: `src/test/resources/application-test.yml`
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
    driver-class-name: org.h2.Driver
    username: sa
    password:
  
  h2:
    console:
      enabled: false
  
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql
      data-locations: classpath:data.sql

jwt:
  secret: test-secret-key-for-integration-tests
  expiration: 3600000  # 1 hour

file:
  upload:
    path: /tmp/test-uploads/
    max-size: 5242880  # 5MB

logging:
  level:
    com.tableorder: DEBUG
```

### 3. Test Data Setup

**Create**: `src/test/resources/test-data.sql`
```sql
-- Test Stores
INSERT INTO store (id, name, created_at) VALUES 
(1, 'Test Store 1', CURRENT_TIMESTAMP),
(2, 'Test Store 2', CURRENT_TIMESTAMP);

-- Test Tables
INSERT INTO `table` (id, store_id, table_number, session_id, session_active, created_at) VALUES
(1, 1, 1, NULL, FALSE, CURRENT_TIMESTAMP),
(2, 1, 2, NULL, FALSE, CURRENT_TIMESTAMP);

-- Test Menus
INSERT INTO menu (id, store_id, name, price, image_url, deleted, created_at) VALUES
(1, 1, 'Test Menu 1', 10000, NULL, FALSE, CURRENT_TIMESTAMP),
(2, 1, 'Test Menu 2', 15000, NULL, FALSE, CURRENT_TIMESTAMP);

-- Test Admin User
INSERT INTO user (id, store_id, username, password, role, created_at) VALUES
(1, 1, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'ADMIN', CURRENT_TIMESTAMP);
-- Password: admin (SHA-256 hashed)
```

---

## Integration Test Structure

### Test Directory
```
backend/src/test/java/com/tableorder/integration/
├── OrderIntegrationTest.java           # 주문 전체 흐름
├── MenuIntegrationTest.java            # 메뉴 관리 흐름
├── TableSessionIntegrationTest.java    # 테이블 세션 흐름
├── AuthIntegrationTest.java            # 인증 흐름
├── SSEIntegrationTest.java             # SSE 이벤트 흐름
└── FileUploadIntegrationTest.java      # 파일 업로드 흐름
```

---

## Test Scenarios

### Scenario 1: 주문 생성 전체 흐름

**Description**: 고객이 메뉴를 선택하고 주문을 생성하는 전체 프로세스

**Test**: `OrderIntegrationTest.java`
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.yml")
@Sql(scripts = "/test-data.sql", executionPhase = Sql.ExecutionPhase.BEFORE_TEST_METHOD)
@Transactional
class OrderIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private OrderMapper orderMapper;
    
    @Test
    @DisplayName("주문 생성 전체 흐름 - 세션 시작 → 메뉴 조회 → 주문 생성 → 주문 조회")
    void completeOrderFlow() {
        // 1. 테이블 세션 시작
        StartSessionRequest sessionRequest = new StartSessionRequest();
        sessionRequest.setTableId(1L);
        
        ResponseEntity<ApiResponse<SessionResponse>> sessionResponse = 
            restTemplate.postForEntity("/api/admin/tables/session/start", 
                sessionRequest, 
                new ParameterizedTypeReference<ApiResponse<SessionResponse>>() {});
        
        assertThat(sessionResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        String sessionId = sessionResponse.getBody().getData().getSessionId();
        
        // 2. 메뉴 조회
        ResponseEntity<ApiResponse<List<MenuResponse>>> menuResponse = 
            restTemplate.exchange("/api/customer/menus?storeId=1", 
                HttpMethod.GET, 
                null, 
                new ParameterizedTypeReference<ApiResponse<List<MenuResponse>>>() {});
        
        assertThat(menuResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(menuResponse.getBody().getData()).hasSize(2);
        
        // 3. 주문 생성
        CreateOrderRequest orderRequest = new CreateOrderRequest();
        orderRequest.setSessionId(sessionId);
        orderRequest.setTableId(1L);
        orderRequest.setItems(Arrays.asList(
            new OrderItemRequest(1L, 2),  // Menu 1 x 2
            new OrderItemRequest(2L, 1)   // Menu 2 x 1
        ));
        
        ResponseEntity<ApiResponse<OrderResponse>> orderResponse = 
            restTemplate.postForEntity("/api/customer/orders", 
                orderRequest, 
                new ParameterizedTypeReference<ApiResponse<OrderResponse>>() {});
        
        assertThat(orderResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(orderResponse.getBody().getData().getOrderNumber()).startsWith("ORD-");
        assertThat(orderResponse.getBody().getData().getTotalAmount()).isEqualTo(35000);
        
        // 4. 주문 조회 (Database 검증)
        Long orderId = orderResponse.getBody().getData().getId();
        Order order = orderMapper.findById(orderId);
        
        assertThat(order).isNotNull();
        assertThat(order.getStatus()).isEqualTo("PENDING");
        assertThat(order.getItems()).hasSize(2);
    }
}
```

**Expected Results**:
- ✅ 세션 시작 성공 (200 OK)
- ✅ 메뉴 조회 성공 (2개 메뉴)
- ✅ 주문 생성 성공 (주문 번호 생성)
- ✅ 총액 계산 정확 (35,000원)
- ✅ Database에 주문 저장 확인

---

### Scenario 2: 주문 상태 변경 및 SSE 이벤트

**Description**: 관리자가 주문 상태를 변경하고 고객에게 SSE 이벤트 전송

**Test**: `SSEIntegrationTest.java`
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.yml")
class SSEIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private SSEService sseService;
    
    @Test
    @DisplayName("주문 상태 변경 시 SSE 이벤트 전송")
    void orderStatusChange_SendsSSEEvent() throws Exception {
        // 1. SSE 연결 (고객)
        WebClient webClient = WebClient.create("http://localhost:" + port);
        
        Flux<ServerSentEvent<String>> eventStream = webClient.get()
            .uri("/api/customer/sse/connect?sessionId=test-session")
            .retrieve()
            .bodyToFlux(new ParameterizedTypeReference<ServerSentEvent<String>>() {});
        
        List<String> receivedEvents = new ArrayList<>();
        eventStream.subscribe(event -> receivedEvents.add(event.data()));
        
        // 2. 주문 생성
        CreateOrderRequest orderRequest = new CreateOrderRequest();
        // ... setup order
        
        ResponseEntity<ApiResponse<OrderResponse>> orderResponse = 
            restTemplate.postForEntity("/api/customer/orders", orderRequest, ...);
        
        Long orderId = orderResponse.getBody().getData().getId();
        
        // 3. 주문 상태 변경 (관리자)
        UpdateOrderStatusRequest statusRequest = new UpdateOrderStatusRequest();
        statusRequest.setStatus("PREPARING");
        
        restTemplate.put("/api/admin/orders/" + orderId + "/status", statusRequest);
        
        // 4. SSE 이벤트 수신 확인
        Thread.sleep(1000);  // Wait for event
        
        assertThat(receivedEvents).isNotEmpty();
        assertThat(receivedEvents.get(0)).contains("PREPARING");
    }
}
```

**Expected Results**:
- ✅ SSE 연결 성공
- ✅ 주문 생성 성공
- ✅ 상태 변경 성공
- ✅ SSE 이벤트 수신 확인

---

### Scenario 3: 관리자 인증 및 JWT 검증

**Description**: 관리자 로그인 → JWT 발급 → 인증 필요 API 호출

**Test**: `AuthIntegrationTest.java`
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.yml")
@Sql(scripts = "/test-data.sql")
class AuthIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Test
    @DisplayName("관리자 인증 전체 흐름 - 로그인 → JWT 발급 → 인증 API 호출")
    void adminAuthenticationFlow() {
        // 1. 로그인
        LoginRequest loginRequest = new LoginRequest();
        loginRequest.setUsername("admin");
        loginRequest.setPassword("admin");
        
        ResponseEntity<ApiResponse<LoginResponse>> loginResponse = 
            restTemplate.postForEntity("/api/auth/login", 
                loginRequest, 
                new ParameterizedTypeReference<ApiResponse<LoginResponse>>() {});
        
        assertThat(loginResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        String token = loginResponse.getBody().getData().getToken();
        assertThat(token).isNotEmpty();
        
        // 2. JWT로 인증 필요 API 호출
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        HttpEntity<Void> entity = new HttpEntity<>(headers);
        
        ResponseEntity<ApiResponse<List<OrderResponse>>> ordersResponse = 
            restTemplate.exchange("/api/admin/orders?storeId=1", 
                HttpMethod.GET, 
                entity, 
                new ParameterizedTypeReference<ApiResponse<List<OrderResponse>>>() {});
        
        assertThat(ordersResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        
        // 3. 잘못된 토큰으로 API 호출
        headers.setBearerAuth("invalid-token");
        HttpEntity<Void> invalidEntity = new HttpEntity<>(headers);
        
        ResponseEntity<ApiResponse> unauthorizedResponse = 
            restTemplate.exchange("/api/admin/orders?storeId=1", 
                HttpMethod.GET, 
                invalidEntity, 
                ApiResponse.class);
        
        assertThat(unauthorizedResponse.getStatusCode()).isEqualTo(HttpStatus.UNAUTHORIZED);
    }
}
```

**Expected Results**:
- ✅ 로그인 성공 (JWT 발급)
- ✅ 유효한 JWT로 API 호출 성공
- ✅ 잘못된 JWT로 API 호출 실패 (401)

---

### Scenario 4: 메뉴 관리 및 파일 업로드

**Description**: 메뉴 생성 → 이미지 업로드 → 메뉴 조회 → 메뉴 삭제

**Test**: `MenuIntegrationTest.java`
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.yml")
class MenuIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private FileService fileService;
    
    @Test
    @DisplayName("메뉴 관리 전체 흐름 - 생성 → 이미지 업로드 → 조회 → 삭제")
    void completeMenuManagementFlow() throws IOException {
        // 1. 관리자 로그인 (JWT 획득)
        String token = loginAsAdmin();
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        
        // 2. 메뉴 생성
        CreateMenuRequest menuRequest = new CreateMenuRequest();
        menuRequest.setStoreId(1L);
        menuRequest.setName("New Menu");
        menuRequest.setPrice(20000);
        
        HttpEntity<CreateMenuRequest> menuEntity = new HttpEntity<>(menuRequest, headers);
        
        ResponseEntity<ApiResponse<MenuResponse>> menuResponse = 
            restTemplate.postForEntity("/api/admin/menus", 
                menuEntity, 
                new ParameterizedTypeReference<ApiResponse<MenuResponse>>() {});
        
        assertThat(menuResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        Long menuId = menuResponse.getBody().getData().getId();
        
        // 3. 이미지 업로드
        MockMultipartFile file = new MockMultipartFile(
            "file", 
            "menu.jpg", 
            "image/jpeg", 
            "test image content".getBytes()
        );
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", file.getResource());
        
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> fileEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<ApiResponse<String>> uploadResponse = 
            restTemplate.postForEntity("/api/admin/menus/" + menuId + "/image", 
                fileEntity, 
                new ParameterizedTypeReference<ApiResponse<String>>() {});
        
        assertThat(uploadResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        String imageUrl = uploadResponse.getBody().getData();
        assertThat(imageUrl).isNotEmpty();
        
        // 4. 메뉴 조회 (이미지 URL 확인)
        ResponseEntity<ApiResponse<MenuResponse>> getResponse = 
            restTemplate.exchange("/api/customer/menus/" + menuId, 
                HttpMethod.GET, 
                null, 
                new ParameterizedTypeReference<ApiResponse<MenuResponse>>() {});
        
        assertThat(getResponse.getBody().getData().getImageUrl()).isEqualTo(imageUrl);
        
        // 5. 메뉴 삭제 (논리적 삭제)
        HttpEntity<Void> deleteEntity = new HttpEntity<>(headers);
        
        restTemplate.exchange("/api/admin/menus/" + menuId, 
            HttpMethod.DELETE, 
            deleteEntity, 
            ApiResponse.class);
        
        // 6. 삭제된 메뉴 조회 불가 확인
        ResponseEntity<ApiResponse> notFoundResponse = 
            restTemplate.exchange("/api/customer/menus/" + menuId, 
                HttpMethod.GET, 
                null, 
                ApiResponse.class);
        
        assertThat(notFoundResponse.getStatusCode()).isEqualTo(HttpStatus.NOT_FOUND);
    }
    
    private String loginAsAdmin() {
        // ... login logic
    }
}
```

**Expected Results**:
- ✅ 메뉴 생성 성공
- ✅ 이미지 업로드 성공
- ✅ 메뉴 조회 시 이미지 URL 확인
- ✅ 메뉴 삭제 성공 (논리적 삭제)
- ✅ 삭제된 메뉴 조회 불가

---

### Scenario 5: 테이블 세션 관리

**Description**: 세션 시작 → 주문 생성 → 세션 종료 → 주문 이력 저장

**Test**: `TableSessionIntegrationTest.java`
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@TestPropertySource(locations = "classpath:application-test.yml")
class TableSessionIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private OrderHistoryMapper orderHistoryMapper;
    
    @Test
    @DisplayName("테이블 세션 전체 흐름 - 시작 → 주문 → 종료 → 이력 저장")
    void completeTableSessionFlow() {
        String token = loginAsAdmin();
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(token);
        
        // 1. 세션 시작
        StartSessionRequest sessionRequest = new StartSessionRequest();
        sessionRequest.setTableId(1L);
        
        HttpEntity<StartSessionRequest> sessionEntity = new HttpEntity<>(sessionRequest, headers);
        
        ResponseEntity<ApiResponse<SessionResponse>> sessionResponse = 
            restTemplate.postForEntity("/api/admin/tables/session/start", 
                sessionEntity, 
                new ParameterizedTypeReference<ApiResponse<SessionResponse>>() {});
        
        String sessionId = sessionResponse.getBody().getData().getSessionId();
        
        // 2. 주문 생성
        CreateOrderRequest orderRequest = new CreateOrderRequest();
        orderRequest.setSessionId(sessionId);
        orderRequest.setTableId(1L);
        // ... setup items
        
        ResponseEntity<ApiResponse<OrderResponse>> orderResponse = 
            restTemplate.postForEntity("/api/customer/orders", orderRequest, ...);
        
        Long orderId = orderResponse.getBody().getData().getId();
        
        // 3. 주문 완료 처리
        UpdateOrderStatusRequest statusRequest = new UpdateOrderStatusRequest();
        statusRequest.setStatus("COMPLETED");
        
        HttpEntity<UpdateOrderStatusRequest> statusEntity = new HttpEntity<>(statusRequest, headers);
        
        restTemplate.exchange("/api/admin/orders/" + orderId + "/status", 
            HttpMethod.PUT, 
            statusEntity, 
            ApiResponse.class);
        
        // 4. 세션 종료
        EndSessionRequest endRequest = new EndSessionRequest();
        endRequest.setTableId(1L);
        
        HttpEntity<EndSessionRequest> endEntity = new HttpEntity<>(endRequest, headers);
        
        restTemplate.postForEntity("/api/admin/tables/session/end", endEntity, ApiResponse.class);
        
        // 5. 주문 이력 저장 확인
        List<OrderHistory> histories = orderHistoryMapper.findBySessionId(sessionId);
        
        assertThat(histories).hasSize(1);
        assertThat(histories.get(0).getOrderNumber()).isEqualTo(orderResponse.getBody().getData().getOrderNumber());
    }
}
```

**Expected Results**:
- ✅ 세션 시작 성공
- ✅ 주문 생성 성공
- ✅ 주문 완료 처리 성공
- ✅ 세션 종료 성공
- ✅ OrderHistory에 주문 이력 저장 확인

---

## Run Integration Tests

### 1. Run All Integration Tests
```bash
cd backend
mvn verify
```

**Note**: `mvn verify`는 `mvn test`와 달리 integration-test 단계를 포함합니다.

### 2. Run Specific Integration Test
```bash
mvn verify -Dit.test=OrderIntegrationTest
```

### 3. Run Integration Tests Only (Skip Unit Tests)
```bash
mvn verify -DskipUnitTests
```

---

## Test Execution Strategy

### Phase 1: 기본 흐름 테스트
```bash
mvn verify -Dit.test=OrderIntegrationTest,MenuIntegrationTest
```
**Duration**: ~20-30초
**Expected**: 기본 CRUD 흐름 검증

### Phase 2: 인증 및 보안 테스트
```bash
mvn verify -Dit.test=AuthIntegrationTest
```
**Duration**: ~10-15초
**Expected**: JWT 인증 흐름 검증

### Phase 3: 실시간 기능 테스트
```bash
mvn verify -Dit.test=SSEIntegrationTest
```
**Duration**: ~15-20초
**Expected**: SSE 이벤트 전송/수신 검증

### Phase 4: 세션 관리 테스트
```bash
mvn verify -Dit.test=TableSessionIntegrationTest
```
**Duration**: ~15-20초
**Expected**: 세션 전체 라이프사이클 검증

### Phase 5: 전체 통합 테스트
```bash
mvn verify
```
**Duration**: ~60-90초
**Expected**: 모든 통합 시나리오 검증

---

## Cleanup

### Test Data Cleanup
```java
@AfterEach
void cleanup() {
    // Database는 @Transactional로 자동 롤백
    
    // 파일 시스템 정리
    File uploadDir = new File("/tmp/test-uploads/");
    if (uploadDir.exists()) {
        FileUtils.deleteDirectory(uploadDir);
    }
}
```

---

## Troubleshooting

### Issue 1: Port Already in Use
**Symptoms**:
```
Port 8080 is already in use
```

**Solutions**:
1. `@SpringBootTest(webEnvironment = RANDOM_PORT)` 사용
2. 기존 프로세스 종료

### Issue 2: SSE Connection Timeout
**Symptoms**:
```
SSE connection timeout
```

**Solutions**:
1. Timeout 증가: `@Timeout(value = 30, unit = TimeUnit.SECONDS)`
2. SSE 연결 확인
3. 비동기 처리 확인

### Issue 3: File Upload Failure
**Symptoms**:
```
FileNotFoundException: /tmp/test-uploads/
```

**Solutions**:
1. 디렉토리 생성: `new File("/tmp/test-uploads/").mkdirs()`
2. 권한 확인
3. 경로 확인

---

## Integration Test Checklist

- [ ] 주문 생성 전체 흐름 테스트
- [ ] 주문 상태 변경 및 SSE 이벤트 테스트
- [ ] 관리자 인증 및 JWT 검증 테스트
- [ ] 메뉴 관리 및 파일 업로드 테스트
- [ ] 테이블 세션 관리 테스트
- [ ] 트랜잭션 롤백 테스트
- [ ] 예외 처리 및 에러 응답 테스트
- [ ] 캐싱 동작 테스트

---

## Next Steps

Integration 테스트 성공 후:
1. ✅ **Performance Tests**: `performance-test-instructions.md` 참고 (optional)
2. ✅ **Test Summary**: `build-and-test-summary.md` 참고
3. ✅ **Deployment**: `deployment-architecture.md` 참고

---

## References

- **Spring Boot Integration Testing**: https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.testing.spring-boot-applications
- **TestRestTemplate**: https://docs.spring.io/spring-boot/docs/current/api/org/springframework/boot/test/web/client/TestRestTemplate.html
- **WebClient**: https://docs.spring.io/spring-framework/docs/current/reference/html/web-reactive.html#webflux-client
