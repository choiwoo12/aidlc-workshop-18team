# Logical Components - Backend

## Overview
Backend 유닛의 논리적 컴포넌트를 정의합니다. 각 컴포넌트는 특정 책임을 가지며, NFR 요구사항을 구현하기 위한 인프라 및 공통 기능을 제공합니다.

---

## 1. Common Components (공통 컴포넌트)

### 1.1 GlobalExceptionHandler

**책임**: 모든 예외를 일관되게 처리하고 클라이언트에게 명확한 에러 응답 제공

**위치**: `com.tableorder.common.exception.GlobalExceptionHandler`

**주요 메서드**:
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    // 비즈니스 예외 처리
    ResponseEntity<ApiResponse<Void>> handleBusinessException(BusinessException ex);
    
    // 검증 예외 처리
    ResponseEntity<ApiResponse<Void>> handleValidationException(MethodArgumentNotValidException ex);
    
    // 낙관적 잠금 예외 처리
    ResponseEntity<ApiResponse<Void>> handleOptimisticLockException(OptimisticLockException ex);
    
    // 시스템 예외 처리
    ResponseEntity<ApiResponse<Void>> handleSystemException(Exception ex);
}
```

**의존성**: 없음

**사용처**: 모든 REST API 엔드포인트

---

### 1.2 ApiResponse<T>

**책임**: 일관된 API 응답 형식 제공

**위치**: `com.tableorder.common.dto.ApiResponse`

**구조**:
```java
public class ApiResponse<T> {
    private boolean success;
    private T data;
    private String message;
    private Object error;
    private LocalDateTime timestamp;
    
    // 정적 팩토리 메서드
    static <T> ApiResponse<T> success(T data);
    static <T> ApiResponse<T> success(T data, String message);
    static <T> ApiResponse<T> error(String message);
    static <T> ApiResponse<T> error(String message, Object error);
}
```

**의존성**: 없음

**사용처**: 모든 Controller

---

### 1.3 BusinessException (추상 클래스)

**책임**: 비즈니스 예외의 기본 클래스

**위치**: `com.tableorder.common.exception.BusinessException`

**구조**:
```java
public abstract class BusinessException extends RuntimeException {
    private final HttpStatus httpStatus;
    private final String errorCode;
    
    protected BusinessException(String message, HttpStatus httpStatus, String errorCode);
    
    public HttpStatus getHttpStatus();
    public String getErrorCode();
}
```

**하위 예외 클래스**:
- `OrderNotFoundException` (404)
- `InvalidSessionException` (400)
- `MenuNotFoundException` (404)
- `InvalidStatusTransitionException` (400)
- `OptimisticLockException` (409)
- `AccountLockedException` (423)
- `FileUploadException` (500)

**의존성**: 없음

**사용처**: 모든 Service 레이어

---

## 2. Infrastructure Components (인프라 컴포넌트)

### 2.1 SSEService

**책임**: SSE 연결 관리 및 실시간 이벤트 전송

**위치**: `com.tableorder.infrastructure.sse.SSEService`

**주요 메서드**:
```java
@Service
public class SSEService {
    
    // 연결 관리
    SseEmitter connectCustomer(Long tableId, String sessionId);
    SseEmitter connectAdmin(Long storeId, Long userId);
    void removeEmitter(String clientId);
    
    // 이벤트 전송
    @Async
    void sendEventToCustomer(Long tableId, String sessionId, SseEvent event);
    
    @Async
    void broadcastEventToStore(Long storeId, SseEvent event);
}
```

**내부 상태**:
```java
private final ConcurrentHashMap<String, SseEmitter> customerEmitters;
private final ConcurrentHashMap<String, SseEmitter> adminEmitters;
private static final long SSE_TIMEOUT = 30000L;
```

**의존성**: 없음

**사용처**: OrderService, TableService

---

### 2.2 FileService

**책임**: 파일 업로드, 저장, 삭제 관리

**위치**: `com.tableorder.infrastructure.file.FileService`

**주요 메서드**:
```java
@Service
public class FileService {
    
    @Retryable(value = {IOException.class}, maxAttempts = 3)
    String saveFile(MultipartFile file) throws IOException;
    
    @Recover
    String recoverSaveFile(IOException ex, MultipartFile file);
    
    void deleteFile(String filePath);
    
    String generateFileName(String originalFilename);
    
    void validateFile(MultipartFile file);
}
```

**설정**:
```java
private static final String UPLOAD_DIR = "uploads/menus/";
private static final long MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
private static final Set<String> ALLOWED_EXTENSIONS = Set.of("jpg", "jpeg", "png");
```

**의존성**: 없음

**사용처**: MenuService

---

### 2.3 CacheManager

**책임**: 캐시 설정 및 관리

**위치**: `com.tableorder.infrastructure.cache.CacheConfig`

**구조**:
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

**캐시 이름**:
- `menus`: 메뉴 목록 캐시
- `stores`: 매장 정보 캐시

**의존성**: Caffeine

**사용처**: MenuService, StoreService

---

## 3. Security Components (보안 컴포넌트)

### 3.1 JwtAuthenticationFilter

**책임**: JWT 토큰 검증 및 인증 처리

**위치**: `com.tableorder.security.JwtAuthenticationFilter`

**주요 메서드**:
```java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                    HttpServletResponse response, 
                                    FilterChain filterChain);
    
    private String extractToken(HttpServletRequest request);
}
```

**의존성**: JwtTokenProvider

**사용처**: Spring Security Filter Chain

---

### 3.2 JwtTokenProvider

**책임**: JWT 토큰 생성, 검증, 파싱

**위치**: `com.tableorder.security.JwtTokenProvider`

**주요 메서드**:
```java
@Component
public class JwtTokenProvider {
    
    String generateToken(User user);
    
    boolean validateToken(String token);
    
    Authentication getAuthentication(String token);
    
    Claims getClaims(String token);
}
```

**설정**:
```java
@Value("${jwt.secret}")
private String secretKey;

@Value("${jwt.expiration}")
private long expirationTime; // 16시간
```

**의존성**: JJWT 라이브러리

**사용처**: AuthService, JwtAuthenticationFilter

---

### 3.3 SecurityConfig

**책임**: Spring Security 설정 및 필터 체인 구성

**위치**: `com.tableorder.security.SecurityConfig`

**주요 메서드**:
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http);
    
    @Bean
    public PasswordEncoder passwordEncoder();
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource();
}
```

**보안 설정**:
- JWT 필터를 UsernamePasswordAuthenticationFilter 이전에 배치
- CSRF 비활성화 (JWT 사용)
- Stateless 세션 관리
- CORS 설정

**의존성**: JwtAuthenticationFilter

**사용처**: Spring Security

---

### 3.4 PasswordEncoder

**책임**: 비밀번호 해싱 및 검증

**위치**: `com.tableorder.security.SecurityConfig`

**구현**:
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(10); // strength: 10
}
```

**사용처**: AuthService (로그인, 회원가입)

---

## 4. Utility Components (유틸리티 컴포넌트)

### 4.1 OrderNumberGenerator

**책임**: 주문 번호 생성 (ORD-YYYYMMDD-NNNN)

**위치**: `com.tableorder.util.OrderNumberGenerator`

**주요 메서드**:
```java
@Component
public class OrderNumberGenerator {
    
    String generateOrderNumber(LocalDate date, int sequence);
    
    int getNextSequence(LocalDate date);
}
```

**형식**: `ORD-{YYYYMMDD}-{NNNN}`

**의존성**: OrderMapper (시퀀스 조회)

**사용처**: OrderService

---

### 4.2 DateTimeUtil

**책임**: 날짜/시간 관련 유틸리티 메서드

**위치**: `com.tableorder.util.DateTimeUtil`

**주요 메서드**:
```java
public class DateTimeUtil {
    
    static LocalDateTime now();
    
    static String format(LocalDateTime dateTime, String pattern);
    
    static LocalDateTime parse(String dateTimeStr, String pattern);
    
    static boolean isExpired(LocalDateTime expiryTime);
}
```

**의존성**: 없음

**사용처**: 모든 Service

---

### 4.3 HashUtil

**책임**: 해싱 관련 유틸리티 (SHA-256)

**위치**: `com.tableorder.util.HashUtil`

**주요 메서드**:
```java
public class HashUtil {
    
    static String sha256(String input);
    
    static boolean verifySha256(String input, String hash);
}
```

**사용처**: TableService (PIN 해싱)

---

## 5. Configuration Components (설정 컴포넌트)

### 5.1 AsyncConfig

**책임**: 비동기 처리 설정

**위치**: `com.tableorder.config.AsyncConfig`

**구조**:
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
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return new SimpleAsyncUncaughtExceptionHandler();
    }
}
```

**ThreadPool 설정**:
- Core Pool Size: 5
- Max Pool Size: 10
- Queue Capacity: 100

**의존성**: 없음

**사용처**: SSEService (비동기 이벤트 전송)

---

### 5.2 RetryConfig

**책임**: 재시도 메커니즘 설정

**위치**: `com.tableorder.config.RetryConfig`

**구조**:
```java
@Configuration
@EnableRetry
public class RetryConfig {
    // Spring Retry 활성화
}
```

**재시도 정책**:
- 최대 시도: 3회
- 재시도 간격: 1초 (고정)
- 재시도 대상: IOException

**의존성**: Spring Retry

**사용처**: FileService, SSEService

---

### 5.3 CorsConfig

**책임**: CORS 설정

**위치**: `com.tableorder.config.CorsConfig`

**구조**:
```java
@Configuration
public class CorsConfig {
    
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(Arrays.asList(
            "http://localhost:3000",  // Customer Frontend
            "http://localhost:3001"   // Admin Frontend
        ));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
        config.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        
        return new CorsFilter(source);
    }
}
```

**CORS 설정**:
- 허용 Origin: localhost:3000, localhost:3001
- 허용 Method: GET, POST, PUT, DELETE
- 허용 Header: Authorization, Content-Type

**의존성**: 없음

**사용처**: Spring Security

---

### 5.4 SwaggerConfig

**책임**: Swagger/OpenAPI 설정

**위치**: `com.tableorder.config.SwaggerConfig`

**구조**:
```java
@Configuration
public class SwaggerConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Table Order API")
                .version("1.0")
                .description("테이블오더 서비스 REST API 문서")
                .contact(new Contact()
                    .name("Table Order Team")
                    .email("support@tableorder.com")))
            .addSecurityItem(new SecurityRequirement().addList("Bearer Authentication"))
            .components(new Components()
                .addSecuritySchemes("Bearer Authentication", 
                    new SecurityScheme()
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")));
    }
}
```

**접근 경로**:
- Swagger UI: `/swagger-ui.html`
- OpenAPI JSON: `/v3/api-docs`

**의존성**: Springdoc OpenAPI

**사용처**: API 문서화

---

### 5.5 HikariConfig

**책임**: 데이터베이스 연결 풀 설정

**위치**: `application.yml`

**설정**:
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
      idle-timeout: 600000
      max-lifetime: 1800000
      pool-name: TableOrderHikariPool
```

**연결 풀 설정**:
- 최대 풀 크기: 10
- 최소 유휴 연결: 5
- 연결 타임아웃: 30초
- 유휴 타임아웃: 10분
- 최대 수명: 30분

**의존성**: HikariCP (Spring Boot 기본)

**사용처**: MyBatis Mapper

---

## Component Dependency Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Controller Layer                      │
│  OrderController, MenuController, TableController, etc.     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ uses
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                        Service Layer                         │
│  OrderService, MenuService, TableService, AuthService       │
└─┬──────────┬──────────┬──────────┬──────────┬──────────────┘
  │          │          │          │          │
  │ uses     │ uses     │ uses     │ uses     │ uses
  ▼          ▼          ▼          ▼          ▼
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────────┐
│Mapper│  │SSE   │  │File  │  │JWT   │  │Password  │
│      │  │Service│  │Service│  │Token │  │Encoder   │
└──────┘  └──────┘  └──────┘  │Provider│  └──────────┘
                               └──────┘
                                  │
                                  │ uses
                                  ▼
                            ┌──────────────┐
                            │Security      │
                            │Filter Chain  │
                            └──────────────┘
```

---

## Component Interaction Patterns

### 패턴 1: 주문 생성 흐름
```
OrderController
  → OrderService
    → OrderMapper (주문 저장)
    → SSEService (이벤트 전송, 비동기)
  → ApiResponse 래핑
  → GlobalExceptionHandler (에러 시)
```

### 패턴 2: 메뉴 생성 흐름
```
MenuController
  → MenuService
    → FileService (이미지 업로드, 재시도)
    → MenuMapper (메뉴 저장)
    → CacheManager (캐시 무효화)
  → ApiResponse 래핑
  → GlobalExceptionHandler (에러 시)
```

### 패턴 3: 로그인 흐름
```
AuthController
  → AuthService
    → UserMapper (사용자 조회)
    → PasswordEncoder (비밀번호 검증)
    → JwtTokenProvider (토큰 생성)
  → ApiResponse 래핑
  → GlobalExceptionHandler (에러 시)
```

### 패턴 4: JWT 인증 흐름
```
HTTP Request
  → JwtAuthenticationFilter
    → JwtTokenProvider (토큰 검증)
    → SecurityContextHolder (인증 정보 저장)
  → Controller
```

---

## Component Summary Table

| 카테고리 | 컴포넌트 | 책임 | 의존성 |
|---------|---------|------|--------|
| Common | GlobalExceptionHandler | 예외 처리 | 없음 |
| Common | ApiResponse<T> | 응답 래핑 | 없음 |
| Common | BusinessException | 비즈니스 예외 | 없음 |
| Infrastructure | SSEService | SSE 연결 관리 | 없음 |
| Infrastructure | FileService | 파일 관리 | 없음 |
| Infrastructure | CacheManager | 캐시 관리 | Caffeine |
| Security | JwtAuthenticationFilter | JWT 필터 | JwtTokenProvider |
| Security | JwtTokenProvider | JWT 토큰 관리 | JJWT |
| Security | SecurityConfig | 보안 설정 | JwtAuthenticationFilter |
| Security | PasswordEncoder | 비밀번호 해싱 | BCrypt |
| Utility | OrderNumberGenerator | 주문 번호 생성 | OrderMapper |
| Utility | DateTimeUtil | 날짜/시간 유틸 | 없음 |
| Utility | HashUtil | SHA-256 해싱 | 없음 |
| Config | AsyncConfig | 비동기 설정 | 없음 |
| Config | RetryConfig | 재시도 설정 | Spring Retry |
| Config | CorsConfig | CORS 설정 | 없음 |
| Config | SwaggerConfig | API 문서 설정 | Springdoc |
| Config | HikariConfig | 연결 풀 설정 | HikariCP |

---

## Package Structure

```
com.tableorder
├── common
│   ├── dto
│   │   └── ApiResponse.java
│   └── exception
│       ├── BusinessException.java
│       ├── GlobalExceptionHandler.java
│       ├── OrderNotFoundException.java
│       ├── InvalidSessionException.java
│       ├── MenuNotFoundException.java
│       ├── InvalidStatusTransitionException.java
│       ├── OptimisticLockException.java
│       ├── AccountLockedException.java
│       └── FileUploadException.java
├── config
│   ├── AsyncConfig.java
│   ├── RetryConfig.java
│   ├── CorsConfig.java
│   └── SwaggerConfig.java
├── infrastructure
│   ├── sse
│   │   ├── SSEService.java
│   │   └── SseEvent.java
│   ├── file
│   │   └── FileService.java
│   └── cache
│       └── CacheConfig.java
├── security
│   ├── JwtAuthenticationFilter.java
│   ├── JwtTokenProvider.java
│   ├── SecurityConfig.java
│   └── PasswordEncoder.java (Bean)
└── util
    ├── OrderNumberGenerator.java
    ├── DateTimeUtil.java
    └── HashUtil.java
```

---

## Component Lifecycle

### 1. Application Startup
```
1. Spring Boot 시작
2. Configuration 컴포넌트 로드
   - AsyncConfig
   - RetryConfig
   - CorsConfig
   - SwaggerConfig
   - CacheConfig
   - SecurityConfig
3. Infrastructure 컴포넌트 초기화
   - SSEService (빈 Map 초기화)
   - FileService
   - CacheManager
4. Security 컴포넌트 초기화
   - JwtTokenProvider
   - JwtAuthenticationFilter
   - PasswordEncoder
5. 애플리케이션 준비 완료
```

### 2. Request Processing
```
1. HTTP 요청 수신
2. JwtAuthenticationFilter 실행 (인증)
3. Controller 실행 (입력 검증)
4. Service 실행 (비즈니스 로직)
5. Infrastructure 컴포넌트 사용
   - Mapper (DB 접근)
   - SSEService (이벤트 전송)
   - FileService (파일 처리)
   - CacheManager (캐싱)
6. ApiResponse 래핑
7. HTTP 응답 반환
```

### 3. Exception Handling
```
1. 예외 발생 (Service 또는 Infrastructure)
2. GlobalExceptionHandler 캐치
3. 예외 타입별 처리
4. ApiResponse.error() 생성
5. HTTP 에러 응답 반환
```

---

## Notes

- 모든 컴포넌트는 단일 책임 원칙(SRP)을 따름
- 컴포넌트 간 의존성은 최소화되어 있음
- Infrastructure 컴포넌트는 재사용 가능하도록 설계됨
- Configuration 컴포넌트는 환경별로 설정 변경 가능
- 모든 컴포넌트는 Spring Bean으로 관리됨
