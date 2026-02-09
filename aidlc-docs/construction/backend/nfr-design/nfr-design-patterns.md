# NFR Design Patterns - Backend

## Overview
Backend 유닛의 NFR 요구사항을 구현하기 위한 설계 패턴을 정의합니다. 각 패턴은 시스템 품질 속성(성능, 확장성, 보안, 신뢰성)을 보장하기 위한 구체적인 구현 방법을 제시합니다.

---

## 1. Resilience Patterns (복원력 패턴)

### 1.1 Global Exception Handler Pattern

**목적**: 모든 예외를 일관되게 처리하고 클라이언트에게 명확한 에러 응답 제공

**구현 방식**: 단일 @RestControllerAdvice

**패턴 구조**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    // 비즈니스 예외 처리
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusinessException(BusinessException ex) {
        return ResponseEntity
            .status(ex.getHttpStatus())
            .body(ApiResponse.error(ex.getMessage()));
    }
    
    // 검증 예외 처리
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Void>> handleValidationException(
            MethodArgumentNotValidException ex) {
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error -> 
            errors.put(error.getField(), error.getDefaultMessage())
        );
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(ApiResponse.error("입력 검증 실패", errors));
    }
    
    // 시스템 예외 처리
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleSystemException(Exception ex) {
        log.error("Unexpected error occurred", ex);
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(ApiResponse.error("시스템 오류가 발생했습니다"));
    }
}
```

**예외 계층 구조**:
```
BusinessException (추상 클래스)
├── OrderNotFoundException
├── InvalidSessionException
├── MenuNotFoundException
├── InvalidStatusTransitionException
├── OptimisticLockException
└── AccountLockedException
```

**장점**:
- 일관된 에러 응답 형식
- 중복 코드 제거
- 유지보수 용이

**적용 범위**: 모든 REST API 엔드포인트

---

### 1.2 Retry Pattern (재시도 패턴)

**목적**: 일시적 장애 시 자동 재시도로 시스템 안정성 향상

**구현 방식**: Spring Retry (@Retryable)

**패턴 구조**:
```java
@Configuration
@EnableRetry
public class RetryConfig {
    // Spring Retry 활성화
}

@Service
public class FileService {
    
    @Retryable(
        value = {IOException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000)
    )
    public String saveFile(MultipartFile file) throws IOException {
        // 파일 저장 로직
        // IOException 발생 시 1초 간격으로 최대 3회 재시도
    }
    
    @Recover
    public String recoverSaveFile(IOException ex, MultipartFile file) {
        log.error("File save failed after 3 retries", ex);
        throw new FileUploadException("파일 저장에 실패했습니다");
    }
}
```

**SSE 이벤트 전송 재시도**:
```java
@Service
public class SSEService {
    
    @Retryable(
        value = {IOException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000)
    )
    public void sendEvent(String clientId, SseEvent event) throws IOException {
        SseEmitter emitter = emitters.get(clientId);
        if (emitter != null) {
            emitter.send(event);
        }
    }
    
    @Recover
    public void recoverSendEvent(IOException ex, String clientId, SseEvent event) {
        log.warn("SSE event send failed after 3 retries: clientId={}", clientId);
        removeEmitter(clientId); // 연결 제거
    }
}
```

**재시도 정책**:
- 최대 시도 횟수: 3회
- 재시도 간격: 1초 (고정)
- 재시도 대상: IOException (파일 저장, SSE 전송)

**적용 범위**: FileService, SSEService

---

## 2. Performance Patterns (성능 패턴)

### 2.1 Caching Pattern (캐싱 패턴)

**목적**: 자주 조회되는 데이터를 캐싱하여 DB 부하 감소 및 응답 시간 단축

**구현 방식**: Spring Cache + Caffeine

**패턴 구조**:
```java
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public CacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(Caffeine.newBuilder()
            .maximumSize(500)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .recordStats());
        return cacheManager;
    }
}
```

**캐싱 적용 예시**:
```java
@Service
public class MenuService {
    
    @Cacheable(value = "menus", key = "#storeId")
    public List<Menu> getMenusByStore(Long storeId) {
        return menuMapper.selectMenusByStore(storeId);
    }
    
    @CacheEvict(value = "menus", key = "#menu.storeId")
    public Menu createMenu(Menu menu) {
        menuMapper.insertMenu(menu);
        return menu;
    }
    
    @CacheEvict(value = "menus", key = "#menu.storeId")
    public Menu updateMenu(Menu menu) {
        menuMapper.updateMenu(menu);
        return menu;
    }
    
    @CacheEvict(value = "menus", key = "#storeId")
    public void deleteMenu(Long menuId, Long storeId) {
        menuMapper.updateMenuDeleted(menuId);
    }
}

@Service
public class StoreService {
    
    @Cacheable(value = "stores", key = "#storeId")
    public Store getStore(Long storeId) {
        return storeMapper.selectStoreById(storeId);
    }
}
```

**캐싱 전략**:
- **메뉴 목록**: storeId별 캐싱, 10분 TTL
- **매장 정보**: storeId별 캐싱, 10분 TTL
- **캐시 무효화**: 생성/수정/삭제 시 자동 무효화

**캐시 설정**:
- 최대 크기: 500개 엔트리
- 만료 시간: 10분 (Write 기준)
- 통계 수집: 활성화

**적용 범위**: MenuService, StoreService

---

### 2.2 Database Optimization Pattern (DB 최적화 패턴)

**목적**: 쿼리 성능 최적화로 응답 시간 단축 (목표: 100ms 이내)

**인덱스 전략**: 표준 인덱스 (PK + FK + 자주 조회되는 컬럼)

**인덱스 설계**:
```sql
-- Order 테이블
CREATE INDEX idx_order_store_table ON orders(store_id, table_id);
CREATE INDEX idx_order_session ON orders(session_id);
CREATE INDEX idx_order_status ON orders(status);
CREATE INDEX idx_order_time ON orders(order_time);

-- Menu 테이블
CREATE INDEX idx_menu_store ON menus(store_id);
CREATE INDEX idx_menu_category ON menus(category);
CREATE INDEX idx_menu_deleted ON menus(deleted);

-- OrderItem 테이블
CREATE INDEX idx_order_item_order ON order_items(order_id);
CREATE INDEX idx_order_item_menu ON order_items(menu_id);

-- Table 테이블
CREATE INDEX idx_table_store ON tables(store_id);
CREATE INDEX idx_table_session ON tables(session_id);

-- User 테이블
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_user_store ON users(store_id);
```

**N+1 쿼리 방지**:
```xml
<!-- MyBatis Mapper: JOIN으로 한 번에 조회 -->
<select id="selectOrderWithItems" resultMap="OrderWithItemsResultMap">
    SELECT 
        o.*, 
        oi.id as item_id,
        oi.menu_id,
        oi.menu_name,
        oi.quantity,
        oi.unit_price
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id
    WHERE o.id = #{orderId}
</select>
```

**쿼리 최적화 원칙**:
- WHERE 절에 인덱스 컬럼 사용
- SELECT 시 필요한 컬럼만 조회
- JOIN 대신 캐싱 활용 (가능한 경우)
- 페이지네이션 적용 (대량 데이터)

---

### 2.3 Asynchronous Processing Pattern (비동기 처리 패턴)

**목적**: SSE 이벤트 전송을 비동기로 처리하여 API 응답 시간 단축

**구현 방식**: Spring @Async

**패턴 구조**:
```java
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
}

@Service
public class SSEService {
    
    @Async
    public void broadcastEventToStore(Long storeId, SseEvent event) {
        // 매장의 모든 관리자에게 이벤트 전송
        emitters.entrySet().stream()
            .filter(entry -> entry.getKey().startsWith("admin-" + storeId))
            .forEach(entry -> {
                try {
                    entry.getValue().send(event);
                } catch (IOException e) {
                    log.warn("Failed to send SSE event to {}", entry.getKey());
                    emitters.remove(entry.getKey());
                }
            });
    }
    
    @Async
    public void sendEventToClient(String clientId, SseEvent event) {
        // 특정 클라이언트에게 이벤트 전송
        SseEmitter emitter = emitters.get(clientId);
        if (emitter != null) {
            try {
                emitter.send(event);
            } catch (IOException e) {
                log.warn("Failed to send SSE event to {}", clientId);
                emitters.remove(clientId);
            }
        }
    }
}
```

**비동기 처리 흐름**:
```
1. OrderService.createOrder() 실행
2. Order 저장 (동기)
3. SSEService.broadcastEventToStore() 호출 (비동기)
4. API 응답 즉시 반환
5. 백그라운드에서 SSE 이벤트 전송
```

**ThreadPool 설정**:
- Core Pool Size: 5
- Max Pool Size: 10
- Queue Capacity: 100

**적용 범위**: SSE 이벤트 전송

---

## 3. Security Patterns (보안 패턴)

### 3.1 JWT Authentication Filter Pattern

**목적**: JWT 토큰 기반 인증 및 권한 검증

**구현 방식**: UsernamePasswordAuthenticationFilter 이전에 JWT 필터 배치

**패턴 구조**:
```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    @Autowired
    private JwtTokenProvider jwtTokenProvider;
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                    HttpServletResponse response, 
                                    FilterChain filterChain) 
            throws ServletException, IOException {
        
        String token = extractToken(request);
        
        if (token != null && jwtTokenProvider.validateToken(token)) {
            Authentication auth = jwtTokenProvider.getAuthentication(token);
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        
        filterChain.doFilter(request, response);
    }
    
    private String extractToken(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Autowired
    private JwtAuthenticationFilter jwtAuthenticationFilter;
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .cors()
            .and()
            .sessionManagement()
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            .and()
            .authorizeHttpRequests()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/customer/**").permitAll()
                .requestMatchers("/api/auth/**").permitAll()
            .and()
            .addFilterBefore(jwtAuthenticationFilter, 
                           UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
}
```

**JWT 토큰 생성 및 검증**:
```java
@Component
public class JwtTokenProvider {
    
    @Value("${jwt.secret}")
    private String secretKey;
    
    @Value("${jwt.expiration}")
    private long expirationTime; // 16시간 (밀리초)
    
    public String generateToken(User user) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + expirationTime);
        
        return Jwts.builder()
            .setSubject(user.getUsername())
            .claim("userId", user.getId())
            .claim("storeId", user.getStoreId())
            .claim("role", user.getRole())
            .setIssuedAt(now)
            .setExpiration(expiryDate)
            .signWith(SignatureAlgorithm.HS256, secretKey)
            .compact();
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(secretKey).parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
    
    public Authentication getAuthentication(String token) {
        Claims claims = Jwts.parser()
            .setSigningKey(secretKey)
            .parseClaimsJws(token)
            .getBody();
        
        Long userId = claims.get("userId", Long.class);
        String username = claims.getSubject();
        String role = claims.get("role", String.class);
        
        UserDetails userDetails = new User(username, "", 
            Collections.singletonList(new SimpleGrantedAuthority("ROLE_" + role)));
        
        return new UsernamePasswordAuthenticationToken(
            userDetails, "", userDetails.getAuthorities());
    }
}
```

**보안 설정**:
- JWT 만료 시간: 16시간
- 알고리즘: HS256
- Stateless 세션 관리
- CSRF 비활성화 (JWT 사용)

---

### 3.2 Input Validation Pattern (입력 검증 패턴)

**목적**: API 요청 데이터의 형식 및 비즈니스 규칙 검증

**구현 방식**: Controller (형식 검증) + Service (비즈니스 검증)

**패턴 구조**:
```java
// Controller: 형식 검증
@RestController
@RequestMapping("/api/customer/orders")
public class OrderController {
    
    @PostMapping
    public ResponseEntity<ApiResponse<OrderResponse>> createOrder(
            @Valid @RequestBody CreateOrderRequest request) {
        // @Valid가 형식 검증 수행
        OrderResponse order = orderService.createOrder(request);
        return ResponseEntity.ok(ApiResponse.success(order));
    }
}

// DTO: 검증 어노테이션
public class CreateOrderRequest {
    
    @NotNull(message = "매장 ID는 필수입니다")
    private Long storeId;
    
    @NotNull(message = "테이블 ID는 필수입니다")
    private Long tableId;
    
    @NotBlank(message = "세션 ID는 필수입니다")
    private String sessionId;
    
    @NotEmpty(message = "주문 항목은 최소 1개 이상이어야 합니다")
    @Valid
    private List<OrderItemRequest> items;
}

public class OrderItemRequest {
    
    @NotNull(message = "메뉴 ID는 필수입니다")
    private Long menuId;
    
    @Min(value = 1, message = "수량은 1개 이상이어야 합니다")
    private Integer quantity;
}

// Service: 비즈니스 검증
@Service
public class OrderService {
    
    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        // 1. 테이블 세션 검증
        Table table = tableMapper.selectById(request.getTableId());
        if (table == null) {
            throw new TableNotFoundException("테이블을 찾을 수 없습니다");
        }
        if (!table.getStoreId().equals(request.getStoreId())) {
            throw new InvalidSessionException("테이블이 해당 매장에 속하지 않습니다");
        }
        if (!table.getSessionId().equals(request.getSessionId())) {
            throw new InvalidSessionException("유효하지 않은 세션입니다");
        }
        if (!"ACTIVE".equals(table.getSessionStatus())) {
            throw new InvalidSessionException("활성 세션이 아닙니다");
        }
        
        // 2. 메뉴 검증
        for (OrderItemRequest item : request.getItems()) {
            Menu menu = menuMapper.selectById(item.getMenuId());
            if (menu == null || menu.getDeleted()) {
                throw new MenuNotFoundException("메뉴를 찾을 수 없거나 비활성 상태입니다");
            }
            if (!menu.getStoreId().equals(request.getStoreId())) {
                throw new MenuNotFoundException("메뉴가 해당 매장에 속하지 않습니다");
            }
        }
        
        // 주문 생성 로직...
    }
}
```

**검증 레이어 분리**:
- **Controller**: @Valid, @NotNull, @NotBlank, @Min 등 형식 검증
- **Service**: 비즈니스 규칙 검증 (세션 유효성, 메뉴 활성 상태 등)

---

## 4. Scalability Patterns (확장성 패턴)

### 4.1 SSE Connection Management Pattern

**목적**: SSE 연결을 효율적으로 관리하여 실시간 이벤트 전송

**구현 방식**: 이중 Map (고객용/관리자용 분리)

**패턴 구조**:
```java
@Service
public class SSEService {
    
    // 고객용 SSE 연결 (tableId-sessionId → SseEmitter)
    private final ConcurrentHashMap<String, SseEmitter> customerEmitters 
        = new ConcurrentHashMap<>();
    
    // 관리자용 SSE 연결 (admin-storeId-userId → SseEmitter)
    private final ConcurrentHashMap<String, SseEmitter> adminEmitters 
        = new ConcurrentHashMap<>();
    
    private static final long SSE_TIMEOUT = 30000L; // 30초
    
    // 고객 연결 등록
    public SseEmitter connectCustomer(Long tableId, String sessionId) {
        String clientId = "customer-" + tableId + "-" + sessionId;
        SseEmitter emitter = new SseEmitter(SSE_TIMEOUT);
        
        emitter.onCompletion(() -> customerEmitters.remove(clientId));
        emitter.onTimeout(() -> customerEmitters.remove(clientId));
        emitter.onError(e -> customerEmitters.remove(clientId));
        
        customerEmitters.put(clientId, emitter);
        
        // 연결 성공 메시지 전송
        try {
            emitter.send(SseEmitter.event()
                .name("connected")
                .data("SSE connection established"));
        } catch (IOException e) {
            customerEmitters.remove(clientId);
            throw new RuntimeException("Failed to send initial message", e);
        }
        
        return emitter;
    }
    
    // 관리자 연결 등록
    public SseEmitter connectAdmin(Long storeId, Long userId) {
        String clientId = "admin-" + storeId + "-" + userId;
        SseEmitter emitter = new SseEmitter(SSE_TIMEOUT);
        
        emitter.onCompletion(() -> adminEmitters.remove(clientId));
        emitter.onTimeout(() -> adminEmitters.remove(clientId));
        emitter.onError(e -> adminEmitters.remove(clientId));
        
        adminEmitters.put(clientId, emitter);
        
        try {
            emitter.send(SseEmitter.event()
                .name("connected")
                .data("SSE connection established"));
        } catch (IOException e) {
            adminEmitters.remove(clientId);
            throw new RuntimeException("Failed to send initial message", e);
        }
        
        return emitter;
    }

    
    // 특정 고객에게 이벤트 전송
    @Async
    public void sendEventToCustomer(Long tableId, String sessionId, SseEvent event) {
        String clientId = "customer-" + tableId + "-" + sessionId;
        SseEmitter emitter = customerEmitters.get(clientId);
        
        if (emitter != null) {
            try {
                emitter.send(SseEmitter.event()
                    .name(event.getType())
                    .data(event.getData()));
            } catch (IOException e) {
                log.warn("Failed to send event to customer: {}", clientId);
                customerEmitters.remove(clientId);
            }
        }
    }
    
    // 매장의 모든 관리자에게 브로드캐스트
    @Async
    public void broadcastEventToStore(Long storeId, SseEvent event) {
        String prefix = "admin-" + storeId + "-";
        
        adminEmitters.entrySet().stream()
            .filter(entry -> entry.getKey().startsWith(prefix))
            .forEach(entry -> {
                try {
                    entry.getValue().send(SseEmitter.event()
                        .name(event.getType())
                        .data(event.getData()));
                } catch (IOException e) {
                    log.warn("Failed to send event to admin: {}", entry.getKey());
                    adminEmitters.remove(entry.getKey());
                }
            });
    }
}
```

**연결 관리 전략**:
- **고객 연결**: `customer-{tableId}-{sessionId}` 형식
- **관리자 연결**: `admin-{storeId}-{userId}` 형식
- **타임아웃**: 30초
- **자동 정리**: onCompletion, onTimeout, onError 시 Map에서 제거

**이벤트 전송 방식**:
- 특정 고객: clientId로 직접 전송
- 매장 관리자: storeId prefix로 필터링 후 브로드캐스트

---

### 4.2 Optimistic Locking Pattern (낙관적 잠금 패턴)

**목적**: 동시 주문 상태 변경 시 충돌 감지 및 처리

**구현 방식**: Version 컬럼 사용

**패턴 구조**:
```java
// Order 엔티티
public class Order {
    private Long id;
    private String orderNumber;
    private String status;
    private Integer version; // 낙관적 잠금용
    // ... 기타 필드
}

// MyBatis Mapper
@Mapper
public interface OrderMapper {
    
    @Update("UPDATE orders SET status = #{status}, version = version + 1, " +
            "updated_at = NOW() WHERE id = #{id} AND version = #{version}")
    int updateOrderStatus(@Param("id") Long id, 
                         @Param("status") String status, 
                         @Param("version") Integer version);
}

// Service
@Service
public class OrderService {
    
    @Transactional
    public OrderResponse updateOrderStatus(Long orderId, String newStatus, Integer version) {
        // 1. 주문 조회
        Order order = orderMapper.selectById(orderId);
        if (order == null || order.getDeleted()) {
            throw new OrderNotFoundException("주문을 찾을 수 없습니다");
        }
        
        // 2. 상태 전이 검증
        if ("완료".equals(order.getStatus())) {
            throw new InvalidStatusTransitionException("완료된 주문은 변경할 수 없습니다");
        }
        
        // 3. 낙관적 잠금으로 업데이트
        int updated = orderMapper.updateOrderStatus(orderId, newStatus, version);
        
        if (updated == 0) {
            // version 불일치 → 다른 사용자가 먼저 수정함
            throw new OptimisticLockException("주문이 다른 사용자에 의해 수정되었습니다. 다시 시도해주세요");
        }
        
        // 4. 업데이트된 주문 조회
        order = orderMapper.selectById(orderId);
        
        // 5. SSE 이벤트 전송 (비동기)
        sseService.sendEventToCustomer(order.getTableId(), order.getSessionId(), 
            new SseEvent("ORDER_STATUS_CHANGED", order));
        sseService.broadcastEventToStore(order.getStoreId(), 
            new SseEvent("ORDER_STATUS_CHANGED", order));
        
        return OrderResponse.from(order);
    }
}
```

**충돌 처리 흐름**:
```
1. 사용자 A가 주문 조회 (version = 1)
2. 사용자 B가 주문 조회 (version = 1)
3. 사용자 A가 상태 변경 (version = 1 → 2) ✓ 성공
4. 사용자 B가 상태 변경 시도 (version = 1) ✗ 실패
5. OptimisticLockException 발생 (409 Conflict)
6. 사용자 B는 최신 데이터를 다시 조회하여 재시도
```

**적용 범위**: Order 상태 변경

---

## 5. Maintainability Patterns (유지보수성 패턴)

### 5.1 Logging Pattern (로깅 패턴)

**목적**: 시스템 동작 추적 및 디버깅 지원

**구현 방식**: SLF4J + Logback (INFO, WARN, ERROR)

**패턴 구조**:
```java
@Service
@Slf4j
public class OrderService {
    
    @Transactional
    public OrderResponse createOrder(CreateOrderRequest request) {
        log.info("Creating order: storeId={}, tableId={}, items={}", 
            request.getStoreId(), request.getTableId(), request.getItems().size());
        
        try {
            // 주문 생성 로직
            Order order = // ...
            
            log.info("Order created successfully: orderId={}, orderNumber={}, totalAmount={}", 
                order.getId(), order.getOrderNumber(), order.getTotalAmount());
            
            return OrderResponse.from(order);
            
        } catch (BusinessException e) {
            log.warn("Order creation failed: {}", e.getMessage());
            throw e;
        } catch (Exception e) {
            log.error("Unexpected error during order creation", e);
            throw new SystemException("주문 생성 중 오류가 발생했습니다", e);
        }
    }
    
    @Transactional
    public OrderResponse updateOrderStatus(Long orderId, String newStatus, Integer version) {
        log.info("Updating order status: orderId={}, newStatus={}, version={}", 
            orderId, newStatus, version);
        
        try {
            // 상태 변경 로직
            int updated = orderMapper.updateOrderStatus(orderId, newStatus, version);
            
            if (updated == 0) {
                log.warn("Optimistic lock conflict: orderId={}, version={}", orderId, version);
                throw new OptimisticLockException("주문이 다른 사용자에 의해 수정되었습니다");
            }
            
            log.info("Order status updated: orderId={}, newStatus={}", orderId, newStatus);
            
            return // ...
            
        } catch (Exception e) {
            log.error("Error updating order status: orderId={}", orderId, e);
            throw e;
        }
    }
}

@Service
@Slf4j
public class FileService {
    
    @Retryable(value = {IOException.class}, maxAttempts = 3)
    public String saveFile(MultipartFile file) throws IOException {
        log.info("Saving file: filename={}, size={}", file.getOriginalFilename(), file.getSize());
        
        try {
            String savedPath = // 파일 저장 로직
            log.info("File saved successfully: path={}", savedPath);
            return savedPath;
            
        } catch (IOException e) {
            log.warn("File save failed, will retry: {}", e.getMessage());
            throw e;
        }
    }
    
    @Recover
    public String recoverSaveFile(IOException ex, MultipartFile file) {
        log.error("File save failed after 3 retries: filename={}", 
            file.getOriginalFilename(), ex);
        throw new FileUploadException("파일 저장에 실패했습니다");
    }
}
```

**로깅 레벨 가이드**:
- **INFO**: 주요 비즈니스 이벤트 (주문 생성, 상태 변경, 로그인 성공)
- **WARN**: 경고 및 재시도 (낙관적 잠금 충돌, 파일 저장 재시도)
- **ERROR**: 에러 및 예외 (예외 발생, 시스템 오류)

**Logback 설정** (logback-spring.xml):
```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>logs/application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>logs/application-%d{yyyy-MM-dd}.log</fileNamePattern>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE" />
        <appender-ref ref="FILE" />
    </root>
    
    <logger name="com.tableorder" level="INFO" />
    <logger name="org.springframework" level="WARN" />
    <logger name="org.mybatis" level="WARN" />
</configuration>
```

---

### 5.2 API Response Wrapper Pattern

**목적**: 일관된 API 응답 형식 제공

**구현 방식**: 전체 래핑 (ApiResponse<T>)

**패턴 구조**:
```java
@Getter
@AllArgsConstructor
public class ApiResponse<T> {
    private boolean success;
    private T data;
    private String message;
    private Object error;
    private LocalDateTime timestamp;
    
    public static <T> ApiResponse<T> success(T data) {
        return new ApiResponse<>(true, data, null, null, LocalDateTime.now());
    }
    
    public static <T> ApiResponse<T> success(T data, String message) {
        return new ApiResponse<>(true, data, message, null, LocalDateTime.now());
    }
    
    public static <T> ApiResponse<T> error(String message) {
        return new ApiResponse<>(false, null, message, null, LocalDateTime.now());
    }
    
    public static <T> ApiResponse<T> error(String message, Object error) {
        return new ApiResponse<>(false, null, message, error, LocalDateTime.now());
    }
}
```

**Controller 사용 예시**:
```java
@RestController
@RequestMapping("/api/customer/orders")
public class OrderController {
    
    @PostMapping
    public ResponseEntity<ApiResponse<OrderResponse>> createOrder(
            @Valid @RequestBody CreateOrderRequest request) {
        OrderResponse order = orderService.createOrder(request);
        return ResponseEntity.ok(ApiResponse.success(order, "주문이 생성되었습니다"));
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<OrderResponse>> getOrder(@PathVariable Long id) {
        OrderResponse order = orderService.getOrder(id);
        return ResponseEntity.ok(ApiResponse.success(order));
    }
    
    @PutMapping("/{id}/status")
    public ResponseEntity<ApiResponse<OrderResponse>> updateOrderStatus(
            @PathVariable Long id,
            @RequestBody UpdateOrderStatusRequest request) {
        OrderResponse order = orderService.updateOrderStatus(id, request.getStatus(), request.getVersion());
        return ResponseEntity.ok(ApiResponse.success(order, "주문 상태가 변경되었습니다"));
    }
}
```

**성공 응답 예시**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "orderNumber": "ORD-20260209-0001",
    "totalAmount": 25000,
    "status": "대기중"
  },
  "message": "주문이 생성되었습니다",
  "error": null,
  "timestamp": "2026-02-09T14:30:00"
}
```

**에러 응답 예시**:
```json
{
  "success": false,
  "data": null,
  "message": "주문을 찾을 수 없습니다",
  "error": {
    "code": "ORDER_NOT_FOUND",
    "details": "orderId: 999"
  },
  "timestamp": "2026-02-09T14:30:00"
}
```

**장점**:
- 클라이언트가 응답 형식을 예측 가능
- 성공/실패 여부를 명확히 구분
- 타임스탬프로 응답 시각 추적

---

## Pattern Summary

| 패턴 카테고리 | 패턴 이름 | 구현 방식 | 적용 범위 |
|--------------|----------|----------|----------|
| Resilience | Global Exception Handler | @RestControllerAdvice | 모든 API |
| Resilience | Retry | Spring Retry | FileService, SSEService |
| Performance | Caching | Spring Cache + Caffeine | MenuService, StoreService |
| Performance | DB Optimization | 인덱스 + N+1 방지 | 모든 Mapper |
| Performance | Async Processing | @Async | SSE 이벤트 전송 |
| Security | JWT Authentication | Filter Chain | 모든 API |
| Security | Input Validation | Controller + Service | 모든 API |
| Scalability | SSE Management | 이중 Map | SSEService |
| Scalability | Optimistic Locking | Version 컬럼 | Order 상태 변경 |
| Maintainability | Logging | SLF4J + Logback | 모든 Service |
| Maintainability | Response Wrapper | ApiResponse<T> | 모든 API |

---

## Notes

- 모든 패턴은 NFR 요구사항을 충족하도록 설계됨
- 패턴 간 상호 보완적으로 동작 (예: Retry + Logging)
- 개발 환경에 최적화되어 있으며, 프로덕션 환경에서는 추가 패턴 고려 필요
- 각 패턴은 독립적으로 적용 가능하며, 필요에 따라 선택적 사용 가능
