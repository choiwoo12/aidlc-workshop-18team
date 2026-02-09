# Tech Stack Decisions - Backend

## Overview
Backend 유닛의 기술 스택 선택과 그 근거를 문서화합니다. 각 기술 선택은 NFR 요구사항과 프로젝트 제약조건을 기반으로 결정되었습니다.

---

## 1. 프레임워크 및 언어

### Spring Boot 3.x
**선택 이유**:
- 엔터프라이즈급 Java 프레임워크
- 풍부한 생태계 및 커뮤니티
- 자동 설정 및 빠른 개발
- 내장 서버 (Tomcat) 제공

**대안 고려**:
- Spring MVC: Spring Boot가 더 간편
- Quarkus: 학습 곡선 및 생태계 부족
- Micronaut: 성능 우수하나 생태계 부족

**버전**: 3.x (최신 LTS)

**근거**:
- 기존 요구사항에서 Java (Spring Boot) 선택됨
- 중규모 확장성 요구사항 충족
- 풍부한 라이브러리 및 통합 지원

---

### Java 17+
**선택 이유**:
- Spring Boot 3.x 최소 요구사항
- LTS (Long Term Support) 버전
- 현대적인 언어 기능 (Records, Pattern Matching)

**대안 고려**:
- Java 11: Spring Boot 3.x 미지원
- Java 21: 최신 LTS이나 안정성 검증 필요

**버전**: Java 17 (LTS)

---

## 2. 데이터베이스

### H2 Database (In-Memory)
**선택 이유**:
- 개발/테스트 환경에 적합
- 설정 및 관리 간편
- 빠른 성능 (메모리 기반)
- 데이터 영속성 불필요 (요구사항)

**설정**:
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:tableorder
    driver-class-name: org.h2.Driver
    username: sa
    password:
  h2:
    console:
      enabled: true
      path: /h2-console
```

**대안 고려**:
- H2 File-based: 데이터 영속성 필요 시
- MySQL/PostgreSQL: 프로덕션 환경 시
- 현재 선택: In-Memory (개발 환경)

**제약사항**:
- 애플리케이션 재시작 시 데이터 손실
- 단일 인스턴스만 지원
- 프로덕션 환경에는 부적합

**마이그레이션 계획** (향후 프로덕션):
- MySQL 8.0 또는 PostgreSQL 14+
- 데이터 마이그레이션 스크립트 작성
- 연결 풀 설정 조정

---

## 3. 데이터 액세스

### MyBatis 3.x
**선택 이유**:
- SQL 중심 개발 (복잡한 쿼리 작성 용이)
- XML 또는 Annotation 기반 매핑
- 동적 SQL 지원
- 기존 요구사항에서 선택됨

**설정**:
```yaml
mybatis:
  mapper-locations: classpath:mybatis/mapper/**/*.xml
  type-aliases-package: com.tableorder.domain
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl
```

**대안 고려**:
- JPA/Hibernate: 객체 중심, 학습 곡선
- JDBC Template: 낮은 수준, 보일러플레이트 코드
- jOOQ: 타입 안전, 복잡한 설정

**선택 근거**:
- SQL 제어 필요 (성능 최적화)
- 동적 쿼리 작성 용이
- 간단한 설정 및 학습 곡선

---

## 4. 캐싱

### Spring Cache + Caffeine
**선택 이유**:
- 애플리케이션 레벨 캐싱
- 간단한 설정 (Annotation 기반)
- 고성능 인메모리 캐시
- 단일 인스턴스 환경에 적합

**설정**:
```yaml
spring:
  cache:
    type: caffeine
    caffeine:
      spec: maximumSize=500,expireAfterWrite=10m
```

**캐싱 대상**:
- 메뉴 목록 (storeId별)
- 매장 정보
- 사용자 정보 (선택적)

**캐시 무효화**:
- 메뉴 생성/수정/삭제 시 자동 무효화
- @CacheEvict 사용

**대안 고려**:
- Redis: 분산 캐시, 다중 인스턴스 환경
- EhCache: Caffeine보다 낮은 성능
- 캐싱 없음: 단순성 우선

**선택 근거**:
- 중규모 확장성 (50명 동시 접속)
- 단일 인스턴스 환경
- 간단한 설정 및 관리

---

## 5. 보안

### Spring Security + JWT
**선택 이유**:
- 엔터프라이즈급 보안 프레임워크
- JWT 토큰 기반 인증
- 역할 기반 권한 관리 (RBAC)
- 기존 요구사항에서 선택됨

**JWT 설정**:
- 알고리즘: HS256 (HMAC with SHA-256)
- 만료 시간: 16시간
- Refresh Token: 없음 (단순화)

**비밀번호 해싱**:
- bcrypt (strength: 10)
- BCryptPasswordEncoder 사용

**PIN 해싱**:
- SHA-256
- MessageDigest 사용

**CORS 설정**:
```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(Arrays.asList("http://localhost:3000", "http://localhost:3001"));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
        config.setAllowedHeaders(Arrays.asList("Authorization", "Content-Type"));
        // ...
    }
}
```

**대안 고려**:
- OAuth 2.0: 과도한 복잡성
- Session 기반: Stateful, 확장성 제한
- API Key: 보안 수준 낮음

---

## 6. 실시간 통신

### Server-Sent Events (SSE)
**선택 이유**:
- 단방향 실시간 통신 (서버 → 클라이언트)
- HTTP 기반, 방화벽 친화적
- 간단한 구현 (Spring WebFlux SseEmitter)
- 기존 요구사항에서 선택됨

**설정**:
```java
@GetMapping(value = "/sse/customer", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public SseEmitter connectCustomer(@RequestParam String tableId, @RequestParam String sessionId) {
    SseEmitter emitter = new SseEmitter(30000L); // 30초 타임아웃
    // ...
}
```

**연결 관리**:
- ConcurrentHashMap<String, SseEmitter>
- 타임아웃: 30초
- 재연결: 클라이언트 책임 (3회 시도)

**대안 고려**:
- WebSocket: 양방향 통신 불필요
- Long Polling: 비효율적
- Server Push (HTTP/2): 브라우저 지원 제한

**선택 근거**:
- 단방향 통신으로 충분 (서버 → 클라이언트)
- 간단한 구현 및 관리
- 브라우저 호환성 우수

---

## 7. 파일 저장소

### 로컬 파일 시스템
**선택 이유**:
- 간단한 구현 및 관리
- 추가 인프라 불필요
- 개발/테스트 환경에 적합
- 비용 절감

**저장 경로**:
- `uploads/menus/` 디렉토리
- 파일명: `{timestamp}.{extension}`

**파일 업로드 설정**:
```yaml
spring:
  servlet:
    multipart:
      max-file-size: 5MB
      max-request-size: 5MB
```

**대안 고려**:
- AWS S3: 클라우드 스토리지, 확장성 우수
- Azure Blob Storage: 클라우드 스토리지
- NFS/SMB: 네트워크 스토리지

**제약사항**:
- 단일 서버 환경만 지원
- 서버 장애 시 파일 손실 가능
- 확장성 제한

**마이그레이션 계획** (향후 프로덕션):
- AWS S3 또는 Azure Blob Storage
- CDN 연동 (CloudFront, Cloudflare)

---

## 8. 로깅

### SLF4J + Logback
**선택 이유**:
- Spring Boot 기본 로깅 프레임워크
- 유연한 설정 (XML 기반)
- 다양한 Appender 지원
- 성능 우수

**로깅 레벨**:
- INFO: 주요 비즈니스 이벤트
- WARN: 경고 및 재시도
- ERROR: 에러 및 예외

**로그 출력**:
- Console Appender (개발 환경)
- File Appender (선택적)

**설정 예시**:
```xml
<configuration>
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE" />
    </root>
</configuration>
```

**대안 고려**:
- Log4j2: 성능 우수하나 설정 복잡
- JUL (Java Util Logging): 기능 제한적

---

## 9. 모니터링

### 개발 환경 - 모니터링 없음
**선택 이유**:
- 개발/테스트 환경으로 모니터링 불필요
- 수동 확인으로 충분
- 인프라 비용 절감

**향후 프로덕션 환경**:
- Spring Boot Actuator
- Prometheus + Grafana (선택적)
- AWS CloudWatch (클라우드 환경)

**Actuator 설정** (향후):
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,info
  endpoint:
    health:
      show-details: always
```

---

## 10. API 문서화

### Springdoc OpenAPI (Swagger)
**선택 이유**:
- 자동 API 문서 생성
- Swagger UI 제공
- Annotation 기반 설정
- 기존 요구사항에서 선택됨

**의존성**:
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.3.0</version>
</dependency>
```

**접근 경로**:
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- OpenAPI JSON: `http://localhost:8080/v3/api-docs`

**설정**:
```java
@Configuration
public class OpenAPIConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("Table Order API")
                .version("1.0")
                .description("테이블오더 서비스 REST API"));
    }
}
```

---

## 11. 빌드 도구

### Maven 3.x
**선택 이유**:
- 표준 Java 빌드 도구
- 풍부한 플러그인 생태계
- Spring Initializr 기본 지원
- 간단한 의존성 관리

**pom.xml 주요 의존성**:
- spring-boot-starter-web
- spring-boot-starter-security
- spring-boot-starter-webflux (SSE)
- mybatis-spring-boot-starter
- h2
- jjwt (JWT)
- caffeine (캐싱)
- springdoc-openapi (Swagger)

**대안 고려**:
- Gradle: 빌드 속도 우수, 학습 곡선
- Ant: 구식, 사용 안 함

---

## 12. 배포

### CI/CD 파이프라인
**선택 이유**:
- 자동화된 빌드 및 배포
- 일관된 배포 프로세스
- 빠른 피드백 루프

**도구 선택**:
- GitHub Actions (권장)
- Jenkins (대안)
- GitLab CI (대안)

**배포 프로세스**:
1. 코드 푸시 (Git)
2. 자동 빌드 (Maven)
3. 테스트 실행 (Unit + Integration)
4. JAR 파일 생성
5. 서버 배포 (SSH 또는 Docker)
6. 애플리케이션 재시작

**GitHub Actions 예시**:
```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up JDK 17
        uses: actions/setup-java@v2
        with:
          java-version: '17'
      - name: Build with Maven
        run: mvn clean package
      - name: Deploy to Server
        # SSH 또는 Docker 배포
```

**대안 고려**:
- 수동 배포: 비효율적, 오류 가능성
- 스크립트 배포: 부분 자동화
- 컨테이너 배포 (Docker): 향후 고려

---

## 13. 데이터베이스 연결 풀

### HikariCP
**선택 이유**:
- Spring Boot 기본 연결 풀
- 최고 성능
- 간단한 설정

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
```

**연결 풀 크기**:
- 최대: 10개 (중규모 환경)
- 최소 유휴: 5개

**대안 고려**:
- Tomcat JDBC Pool: HikariCP보다 낮은 성능
- C3P0: 구식

---

## 14. 트랜잭션 관리

### Spring Transaction Management
**선택 이유**:
- 선언적 트랜잭션 (@Transactional)
- AOP 기반 자동 관리
- 다양한 전파 옵션

**격리 수준**:
- READ_COMMITTED (기본값)

**전파 옵션**:
- REQUIRED (기본값): 기존 트랜잭션 참여 또는 새로 생성
- REQUIRES_NEW: 항상 새 트랜잭션 생성

**읽기 전용 트랜잭션**:
```java
@Transactional(readOnly = true)
public List<Menu> getMenus(Long storeId) {
    // ...
}
```

---

## Tech Stack Summary

| 카테고리 | 기술 | 버전 | 근거 |
|----------|------|------|------|
| 프레임워크 | Spring Boot | 3.x | 엔터프라이즈급, 자동 설정 |
| 언어 | Java | 17 | LTS, 현대적 기능 |
| 데이터베이스 | H2 | In-Memory | 개발 환경, 간편성 |
| 데이터 액세스 | MyBatis | 3.x | SQL 중심, 동적 쿼리 |
| 캐싱 | Caffeine | - | 고성능, 단일 인스턴스 |
| 보안 | Spring Security + JWT | - | 엔터프라이즈급, 토큰 인증 |
| 실시간 통신 | SSE | - | 단방향, 간단한 구현 |
| 파일 저장소 | 로컬 파일 시스템 | - | 간편성, 비용 절감 |
| 로깅 | SLF4J + Logback | - | Spring Boot 기본 |
| 모니터링 | 없음 | - | 개발 환경 |
| API 문서 | Springdoc OpenAPI | 2.3.0 | 자동 생성, Swagger UI |
| 빌드 도구 | Maven | 3.x | 표준, 간단한 설정 |
| 배포 | CI/CD (GitHub Actions) | - | 자동화, 일관성 |
| 연결 풀 | HikariCP | - | 최고 성능 |

---

## Migration Path (향후 프로덕션)

### 데이터베이스
- H2 In-Memory → MySQL 8.0 또는 PostgreSQL 14+
- 데이터 마이그레이션 스크립트 작성
- 연결 풀 크기 조정 (20개 이상)

### 캐싱
- Caffeine → Redis (분산 캐시)
- 다중 인스턴스 환경 지원

### 파일 저장소
- 로컬 파일 시스템 → AWS S3 또는 Azure Blob Storage
- CDN 연동 (CloudFront, Cloudflare)

### 모니터링
- 없음 → Spring Boot Actuator + Prometheus + Grafana
- 또는 AWS CloudWatch (클라우드 환경)

### 보안
- CORS만 → HSTS, CSP, X-Frame-Options 추가
- JWT Refresh Token 추가 고려

### 가용성
- 단일 인스턴스 → 로드 밸런서 + 다중 인스턴스
- 헬스 체크 및 자동 복구

---

## Notes

- 현재 기술 스택은 개발/테스트 환경에 최적화됨
- 프로덕션 환경으로 전환 시 마이그레이션 계획 참조
- 성능 및 확장성 요구사항 변경 시 기술 스택 재검토 필요
- 모든 기술 선택은 NFR 요구사항과 일치함

