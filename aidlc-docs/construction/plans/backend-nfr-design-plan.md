# Backend NFR Design Plan - 테이블오더 서비스

## Plan Overview
Backend 유닛의 NFR 요구사항을 설계 패턴과 논리적 컴포넌트로 구체화합니다. Functional Design과 NFR Requirements를 기반으로 시스템 품질 속성을 보장하는 아키텍처 설계를 수립합니다.

---

## NFR Requirements Context

### 주요 NFR 요구사항
- **성능**: API 응답 1초, SSE 이벤트 2초, DB 쿼리 100ms
- **확장성**: 동시 50명, 5개 매장, 일일 500건 주문
- **가용성**: 95% (개발 환경), 30분 복구 시간
- **보안**: JWT 16시간, bcrypt, SHA-256, CORS
- **신뢰성**: 단순 재시도 3회, 낙관적 잠금, 트랜잭션 관리
- **유지보수성**: 표준 로깅, Swagger, 코드 품질

### 기술 스택
- Spring Boot 3.x, Java 17, H2 In-Memory
- MyBatis, Spring Cache + Caffeine
- Spring Security + JWT, SSE
- Logback, HikariCP, GitHub Actions

---

## NFR Design Methodology

### 1. Resilience Patterns
- [x] 에러 처리 패턴
- [x] 재시도 메커니즘
- [x] Circuit Breaker (필요 시)
- [x] Fallback 전략

### 2. Performance Patterns
- [x] 캐싱 전략 구체화
- [x] 데이터베이스 최적화
- [x] 비동기 처리
- [x] 연결 풀 관리

### 3. Security Patterns
- [x] 인증/인가 아키텍처
- [x] 보안 필터 체인
- [x] 에러 응답 보안
- [x] 입력 검증 전략

### 4. Scalability Patterns
- [x] 동시성 제어
- [x] 리소스 관리
- [x] SSE 연결 관리
- [x] 데이터 격리

### 5. Logical Components
- [x] 공통 컴포넌트 정의
- [x] 인프라 컴포넌트
- [x] 유틸리티 컴포넌트
- [x] 설정 컴포넌트

---

## Context-Appropriate Questions

다음 질문들에 답변해주시면 Backend 유닛의 NFR Design을 정확히 정의할 수 있습니다.

### Q1: Global Exception Handler 구조
모든 예외를 처리하는 Global Exception Handler를 어떻게 구성할까요?

A) **단일 핸들러** - @RestControllerAdvice 하나로 모든 예외 처리
B) **계층별 핸들러** - 비즈니스/시스템/검증 예외별 핸들러 분리
C) **도메인별 핸들러** - Order/Menu/Table 등 도메인별 핸들러
D) **혼합 구조** - 공통 핸들러 + 도메인별 핸들러

[Answer]: A

**Reasoning**: Exception Handler 구조는 에러 처리의 일관성과 유지보수성에 영향을 줍니다.

---

### Q2: 재시도 메커니즘 구현
파일 저장 및 SSE 전송 실패 시 재시도를 어떻게 구현할까요?

A) **수동 구현** - try-catch 블록에서 직접 재시도 로직 작성
B) **Spring Retry** - @Retryable 어노테이션 사용
C) **Resilience4j** - Retry 모듈 사용 (Circuit Breaker 포함)
D) **커스텀 AOP** - 재시도 로직을 AOP로 구현

[Answer]: B

**Reasoning**: 재시도 메커니즘은 시스템 안정성과 코드 복잡도에 영향을 줍니다.

---

### Q3: 캐싱 적용 범위 및 전략
Spring Cache + Caffeine을 어떤 데이터에 적용할까요?

A) **최소 캐싱** - 메뉴 목록만 캐싱
B) **표준 캐싱** - 메뉴 목록 + 매장 정보 캐싱
C) **확장 캐싱** - 메뉴 + 매장 + 사용자 정보 캐싱
D) **동적 캐싱** - 조회 빈도에 따라 자동 캐싱

[Answer]: B

**Reasoning**: 캐싱 범위는 성능과 데이터 일관성 간 트레이드오프에 영향을 줍니다.

---

### Q4: 데이터베이스 인덱스 전략
성능 최적화를 위한 인덱스를 어떻게 설계할까요?

A) **최소 인덱스** - Primary Key만 사용
B) **표준 인덱스** - PK + Foreign Key + 자주 조회되는 컬럼
C) **복합 인덱스** - 다중 컬럼 조합 인덱스 추가
D) **전체 인덱스** - 모든 조회 컬럼에 인덱스

[Answer]: B

**Reasoning**: 인덱스 전략은 조회 성능과 쓰기 성능 간 트레이드오프에 영향을 줍니다.

---

### Q5: JWT 토큰 검증 필터 위치
JWT 인증 필터를 Spring Security 필터 체인의 어디에 배치할까요?

A) **UsernamePasswordAuthenticationFilter 이전** - 토큰 우선 검증
B) **UsernamePasswordAuthenticationFilter 이후** - 폼 로그인 후 토큰 검증
C) **OncePerRequestFilter 상속** - 독립적인 필터로 구현
D) **커스텀 필터 체인** - 별도 필터 체인 구성

[Answer]: A

**Reasoning**: 필터 위치는 인증 순서와 보안 수준에 영향을 줍니다.

---

### Q6: SSE 연결 관리 구조
SSE 연결을 어떻게 관리하고 저장할까요?

A) **단일 Map** - ConcurrentHashMap<String, SseEmitter> 하나로 관리
B) **이중 Map** - 고객용/관리자용 Map 분리
C) **매장별 Map** - Map<Long, Map<String, SseEmitter>> (storeId별)
D) **Redis 기반** - Redis Pub/Sub로 분산 관리

[Answer]: B

**Reasoning**: SSE 연결 관리 구조는 이벤트 전송 효율성과 확장성에 영향을 줍니다.

---

### Q7: 비동기 처리 전략
SSE 이벤트 전송 등 비동기 작업을 어떻게 처리할까요?

A) **동기 처리** - 비동기 없이 순차 처리
B) **@Async** - Spring @Async 어노테이션 사용
C) **CompletableFuture** - Java CompletableFuture 사용
D) **TaskExecutor** - 커스텀 ThreadPoolTaskExecutor 구성

[Answer]: B

**Reasoning**: 비동기 처리 전략은 응답 시간과 리소스 사용에 영향을 줍니다.

---

### Q8: 입력 검증 레이어
API 요청 데이터 검증을 어디서 수행할까요?

A) **Controller만** - @Valid 어노테이션으로 Controller에서만 검증
B) **Controller + Service** - Controller에서 형식 검증, Service에서 비즈니스 검증
C) **Service만** - Service 레이어에서 모든 검증 수행
D) **Validator 클래스** - 별도 Validator 클래스로 검증 로직 분리

[Answer]: B

**Reasoning**: 검증 레이어는 코드 구조와 책임 분리에 영향을 줍니다.

---

### Q9: 로깅 전략 구체화
어떤 정보를 어떤 레벨로 로깅할까요?

A) **최소 로깅** - ERROR만 로깅 (예외 발생 시)
B) **표준 로깅** - INFO (API 요청/응답), WARN (재시도), ERROR (예외)
C) **상세 로깅** - DEBUG 포함, 모든 메서드 진입/종료 로깅
D) **구조화 로깅** - JSON 형식, MDC로 요청 ID 추적

[Answer]: A

**Reasoning**: 로깅 전략은 디버깅 효율성과 성능에 영향을 줍니다.

---

### Q10: 공통 응답 형식
API 응답을 표준화된 형식으로 래핑할까요?

A) **래핑 없음** - 도메인 객체를 직접 반환
B) **성공 응답만 래핑** - ApiResponse<T> { data, timestamp }
C) **전체 래핑** - ApiResponse<T> { success, data, error, timestamp }
D) **에러만 래핑** - 성공은 직접 반환, 에러만 ErrorResponse

[Answer]: C

**Reasoning**: 응답 형식은 API 일관성과 클라이언트 처리 편의성에 영향을 줍니다.

---

## Mandatory NFR Design Artifacts

### 1. nfr-design-patterns.md
- [x] Resilience Patterns (에러 처리, 재시도, Fallback)
- [x] Performance Patterns (캐싱, DB 최적화, 비동기)
- [x] Security Patterns (인증/인가, 필터 체인, 입력 검증)
- [x] Scalability Patterns (동시성 제어, SSE 관리, 리소스 관리)
- [x] 각 패턴의 구현 방법 및 코드 예시

### 2. logical-components.md
- [x] 공통 컴포넌트 (Exception Handler, Response Wrapper, Validator)
- [x] 인프라 컴포넌트 (SSE Manager, Cache Manager, File Manager)
- [x] 보안 컴포넌트 (JWT Filter, Security Config, Password Encoder)
- [x] 유틸리티 컴포넌트 (Date Util, String Util, Mapper Util)
- [x] 설정 컴포넌트 (Application Config, Cache Config, Security Config)
- [x] 각 컴포넌트의 책임 및 인터페이스

---

## Next Steps After Plan Approval

1. 사용자가 모든 [Answer]: 태그를 채움
2. AI가 답변을 분석하고 모호한 부분 확인
3. 필요시 추가 질문으로 명확화
4. 사용자가 계획 승인
5. 승인된 계획에 따라 NFR Design 아티팩트 생성 시작

---

**참고**: 이 계획은 사용자의 답변에 따라 조정될 수 있습니다. 모든 질문에 답변해주시면 최적의 NFR Design을 생성할 수 있습니다.

---

## Follow-up Questions for Clarification

답변을 검토한 결과, 1개 항목에서 명확화가 필요합니다.

### FQ1: 로깅 전략 불일치 확인
Q9에서 "A - 최소 로깅 (ERROR만)"을 선택하셨는데, 이는 NFR Requirements의 NFR-6.1과 불일치합니다.

**NFR-6.1 요구사항**:
- INFO: 주요 비즈니스 이벤트 (주문 생성, 상태 변경)
- WARN: 경고 (재시도, 데이터 불일치)
- ERROR: 에러 (예외 발생, 시스템 오류)

**Q9 답변**: ERROR만 로깅

**질문**: 로깅 전략을 어떻게 할까요?

A) **NFR 요구사항 따름** - INFO, WARN, ERROR 로깅 (NFR-6.1)
B) **최소 로깅 유지** - ERROR만 로깅 (NFR-6.1 변경)
C) **절충안** - WARN, ERROR만 로깅 (INFO 제외)

[Answer]: A

**Reasoning**: 로깅 전략은 디버깅, 모니터링, 운영 효율성에 직접적인 영향을 줍니다. NFR Requirements와 일치시키는 것이 중요합니다.
