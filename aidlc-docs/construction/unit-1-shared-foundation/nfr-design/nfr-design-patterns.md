# NFR Design Patterns - Unit 1: Shared Foundation

## Overview

Unit 1의 비기능 요구사항을 충족하기 위한 설계 패턴입니다. 인프라 독립적이며 논리적 컴포넌트 수준에서 정의됩니다.

---

## 1. Performance Optimization Patterns (성능 최적화 패턴)

### Pattern 1.1: Database Indexing Strategy
**Purpose**: 데이터베이스 조회 성능 최적화

**Pattern**: Composite Index Pattern

**Implementation**:
- Primary Key 인덱스 (자동 생성)
- Foreign Key 인덱스 (JOIN 성능 향상)
- 자주 조회되는 필드 인덱스 (WHERE 절 성능 향상)

**Indexed Fields**:
```
Store:
  - id (PK)

Table:
  - id (PK)
  - store_id (FK)
  - table_number (조회 빈도 높음)

Menu:
  - id (PK)
  - store_id (FK)
  - category_level1 (조회 빈도 높음)

Order:
  - id (PK)
  - store_id (FK)
  - table_id (FK)
  - status (조회 빈도 높음)

OrderItem:
  - id (PK)
  - order_id (FK)

OrderHistory:
  - id (PK)
  - store_id (FK)
  - table_id (FK)
```

**Benefits**:
- JOIN 성능 향상 (Foreign Key 인덱스)
- WHERE 절 성능 향상 (자주 조회되는 필드 인덱스)
- 조회 응답 시간 단축

---

### Pattern 1.2: Response Caching Pattern
**Purpose**: API 응답 시간 단축

**Pattern**: Cache-Aside Pattern (Lazy Loading)

**Implementation**:
- 메뉴 조회 API 응답 캐싱
- 캐시 만료 시간: 5분
- 캐시 무효화: 메뉴 변경 시 즉시 삭제 (동기)

**Cache Flow**:
```
1. 클라이언트 요청 → API
2. 캐시 확인
   - 캐시 HIT: 캐시 데이터 반환
   - 캐시 MISS: DB 조회 → 캐시 저장 → 데이터 반환
3. 메뉴 변경 시: 캐시 즉시 삭제
```

**Cache Key Strategy**:
```
menu:list:{store_id}
menu:detail:{menu_id}
menu:category:{store_id}:{category_level1}
```

**Benefits**:
- 메뉴 조회 응답 시간 단축
- 데이터베이스 부하 감소
- 자주 변경되지 않는 데이터에 적합

---

### Pattern 1.3: Asynchronous Processing Pattern
**Purpose**: 비동기 처리로 응답 시간 단축

**Pattern**: Async/Await Pattern

**Implementation**:
- FastAPI의 async/await 활용
- 데이터베이스 I/O 비동기 처리
- SSE 이벤트 전송 비동기 처리

**Example Flow**:
```
async def create_order(order_data):
    # 비동기 DB 작업
    order = await db.create_order(order_data)
    
    # 비동기 SSE 이벤트 전송
    await sse_manager.broadcast_order_created(order)
    
    return order
```

**Benefits**:
- I/O 대기 시간 동안 다른 요청 처리 가능
- 동시 접속자 처리 능력 향상
- 응답 시간 단축

---

### Pattern 1.4: Connection Pool Pattern
**Purpose**: 데이터베이스 연결 재사용

**Pattern**: Connection Pool Pattern

**Configuration**:
- 최소 연결 수: 10개
- 최대 연결 수: 20개
- 연결 타임아웃: 30초
- 유휴 연결 제거 시간: 300초

**Benefits**:
- 연결 생성/해제 오버헤드 감소
- 동시 요청 처리 능력 향상
- 리소스 효율적 관리

---

### Pattern 1.5: Frontend Bundle Optimization Pattern
**Purpose**: 프론트엔드 초기 로딩 시간 단축

**Pattern**: Code Splitting + Tree Shaking

**Implementation**:
- 고객/관리자 코드 분리 (Route-based splitting)
- 사용하지 않는 코드 제거 (Tree shaking)
- 이미지 최적화 (적절한 크기 및 형식)

**Bundle Structure**:
```
main.js (공통 코드)
customer.js (고객 전용 코드)
admin.js (관리자 전용 코드)
```

**Benefits**:
- 초기 로딩 시간 단축
- 번들 크기 감소
- 사용자 경험 향상

---

## 2. Security Patterns (보안 패턴)

### Pattern 2.1: Password Hashing Pattern
**Purpose**: 비밀번호 안전한 저장

**Pattern**: Salted Hash Pattern (bcrypt)

**Implementation**:
- bcrypt 알고리즘 사용
- Cost Factor: 12
- Salt 자동 생성

**Flow**:
```
1. 비밀번호 입력
2. bcrypt.hash(password, cost_factor=12)
3. 해시 값 저장
4. 로그인 시: bcrypt.verify(input_password, stored_hash)
```

**Benefits**:
- Rainbow Table 공격 방어
- 브루트 포스 공격 지연
- 업계 표준 보안 수준

---

### Pattern 2.2: JWT Authentication Pattern
**Purpose**: Stateless 인증

**Pattern**: JWT Token Pattern

**Implementation**:
- Algorithm: HS256
- Token Expiry: Admin 8시간, Table 24시간
- Token Structure:
```json
{
  "type": "admin" | "table",
  "store_id": "매장 ID",
  "table_id": "테이블 ID (table 타입만)",
  "issued_at": "발급 시간",
  "expires_at": "만료 시간"
}
```

**Flow**:
```
1. 로그인 성공 → JWT 토큰 발급
2. 클라이언트: 토큰 저장 (LocalStorage/SessionStorage)
3. API 요청 시: Authorization 헤더에 토큰 포함
4. 서버: 토큰 검증 → 요청 처리
```

**Benefits**:
- Stateless 인증 (서버 세션 불필요)
- 확장 가능
- 표준 기술

---

### Pattern 2.3: Input Validation Pattern
**Purpose**: 악의적인 입력 차단

**Pattern**: Dual Validation Pattern (Client + Server)

**Implementation**:
- 클라이언트 측: 즉각적인 피드백 (React Hook Form + Yup)
- 서버 측: 보안 및 데이터 무결성 (FastAPI Pydantic)

**Validation Types**:
- 필수 필드 검증
- 데이터 타입 검증
- 형식 검증 (이메일, 전화번호 등)
- 길이 제한 검증
- 비즈니스 규칙 검증

**Benefits**:
- 사용자 경험 향상 (즉각적인 피드백)
- 보안 강화 (악의적인 요청 차단)
- 데이터 무결성 보장

---

### Pattern 2.4: File Upload Validation Pattern
**Purpose**: 악의적인 파일 업로드 방지

**Pattern**: Multi-Layer Validation Pattern

**Implementation**:
- Layer 1: 파일 크기 검증 (최대 5MB)
- Layer 2: MIME 타입 검증 (image/*)
- Layer 3: 파일명 UUID 변환 (경로 탐색 공격 방지)

**Flow**:
```
1. 파일 업로드 요청
2. 파일 크기 검증 (> 5MB → 거부)
3. MIME 타입 검증 (image/* 아님 → 거부)
4. UUID 기반 파일명 생성
5. 파일 저장 (uploads/menu-images/{uuid}.{ext})
6. URL 반환
```

**Benefits**:
- 악의적인 파일 업로드 방지
- 경로 탐색 공격 방어
- 파일명 충돌 방지

---

## 3. Error Handling Patterns (에러 처리 패턴)

### Pattern 3.1: Centralized Error Handling Pattern
**Purpose**: 일관된 에러 응답

**Pattern**: Exception Handler Middleware Pattern

**Implementation**:
- 모든 예외를 중앙에서 처리
- 일관된 에러 응답 형식
- 에러 로깅

**Error Response Format**:
```json
{
  "error": {
    "code": "HTTP_STATUS_CODE",
    "message": "사용자 친화적 메시지"
  }
}
```

**HTTP Status Codes**:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error

**Benefits**:
- 일관된 에러 응답
- 에러 처리 로직 중앙화
- 유지보수 용이

---

### Pattern 3.2: Graceful Degradation Pattern
**Purpose**: 에러 발생 시에도 서비스 지속

**Pattern**: Try-Catch with Fallback Pattern

**Implementation**:
- 모든 API 엔드포인트에 try-catch
- 에러 발생 시 로그 기록
- 사용자 친화적 에러 메시지 반환
- 재시도 로직 (네트워크 에러)

**Example**:
```python
try:
    result = await perform_operation()
    return result
except NetworkError as e:
    logger.error(f"Network error: {e}")
    # 재시도 로직
    return await retry_operation()
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return {"error": {"code": 500, "message": "서버 오류가 발생했습니다"}}
```

**Benefits**:
- 서비스 안정성 향상
- 사용자 경험 개선
- 에러 추적 용이

---

## 4. Caching Patterns (캐싱 패턴)

### Pattern 4.1: Cache-Aside Pattern
**Purpose**: 메뉴 조회 성능 최적화

**Pattern**: Cache-Aside (Lazy Loading)

**Implementation**:
- 메뉴 조회 시 캐시 확인
- 캐시 MISS 시 DB 조회 후 캐시 저장
- 캐시 만료 시간: 5분
- 캐시 무효화: 메뉴 변경 시 즉시 삭제

**Cache Invalidation Strategy**:
- 메뉴 생성: 관련 캐시 삭제
- 메뉴 수정: 해당 메뉴 캐시 삭제
- 메뉴 삭제: 해당 메뉴 캐시 삭제

**Benefits**:
- 응답 시간 단축
- 데이터베이스 부하 감소
- 캐시 관리 간편

---

## 5. Concurrency Control Patterns (동시성 제어 패턴)

### Pattern 5.1: Pessimistic Locking Pattern
**Purpose**: 주문 수정 시 데이터 일관성 보장

**Pattern**: Pessimistic Locking (Row-Level Lock)

**Implementation**:
- 주문 수정 시 해당 주문 잠금
- 잠금 범위: 주문 단위 (Order 엔티티 전체)
- 잠금 타임아웃: 30초

**Flow**:
```
1. 주문 수정 요청
2. 데이터베이스에서 주문 잠금 획득
3. 수정 작업 수행
4. 잠금 해제
```

**Benefits**:
- 동시 수정 방지
- 데이터 일관성 보장
- 충돌 방지

---

### Pattern 5.2: Sequential Number Generation Pattern
**Purpose**: 주문 번호 순차 생성

**Pattern**: Database Sequence Pattern

**Implementation**:
- 매장별 마지막 주문 번호 조회 (잠금)
- 번호 증가 (001 → 002)
- 새 주문에 번호 할당
- 잠금 해제

**Format**: 3자리 숫자 (001, 002, ..., 999)

**Overflow Handling**: 999 이후 001로 순환

**Benefits**:
- 고유한 주문 번호 보장
- 순차적 증가
- 충돌 방지

---

## 6. Real-time Communication Patterns (실시간 통신 패턴)

### Pattern 6.1: Server-Sent Events (SSE) Pattern
**Purpose**: 실시간 주문 업데이트

**Pattern**: Publish-Subscribe Pattern (SSE)

**Implementation**:
- 관리자 클라이언트: SSE 연결 생성
- 서버: 연결 관리 (다중 연결 허용)
- 주문 생성/변경 시: 모든 연결에 이벤트 브로드캐스트

**Connection Management**:
- 다중 연결 허용 (여러 디바이스 동시 모니터링)
- 연결 풀 관리 (메모리 기반)
- 자동 재연결 (클라이언트 측)

**Event Types**:
```
order_created: 새 주문 생성
order_updated: 주문 상태 변경
order_deleted: 주문 삭제
```

**Benefits**:
- 실시간 업데이트 (< 2초)
- 단방향 통신 (서버 → 클라이언트)
- HTTP 기반 (방화벽 친화적)

---

## 7. Logging Patterns (로깅 패턴)

### Pattern 7.1: Structured Logging Pattern
**Purpose**: 체계적인 로깅 및 모니터링

**Pattern**: Structured Logging Pattern

**Implementation**:
- 로그 레벨: DEBUG, INFO, WARNING, ERROR, CRITICAL
- 로그 형식: `[timestamp] [level] [component] [message]`
- 로그 파일: 날짜별 파일 (logs/app-2026-02-09.log)
- 로그 로테이션: 30일 후 자동 삭제

**Log Levels**:
- ERROR: 시스템 오류, 예상치 못한 오류
- WARNING: 비즈니스 규칙 위반, 인증/권한 오류
- INFO: 정상 동작 로그 (API 요청, 주문 생성 등)
- DEBUG: 디버깅 정보 (개발 환경만)

**Benefits**:
- 문제 추적 용이
- 시스템 모니터링
- 디버깅 효율성 향상

---

## 8. Data Persistence Patterns (데이터 영속성 패턴)

### Pattern 8.1: File-based Database Pattern
**Purpose**: 모든 데이터 영속성 보장

**Pattern**: Single File-based Database Pattern

**Implementation**:
- 파일 기반 SQLite (data/app.db)
- 모든 엔티티 저장
- 트랜잭션 관리

**Benefits**:
- 서버 재시작 시에도 데이터 유지
- 단일 DB 연결로 복잡도 감소
- 트랜잭션 관리 단순화

---

### Pattern 8.2: Snapshot Pattern
**Purpose**: 과거 데이터 정확성 보장

**Pattern**: Snapshot Pattern

**Implementation**:
- 주문 생성 시 메뉴 정보 스냅샷 저장
- OrderItem에 menu_name_snapshot, menu_price_snapshot 저장
- 메뉴 변경 시에도 과거 주문 데이터 유지

**Benefits**:
- 과거 주문 데이터 정확성 보장
- 메뉴 변경 영향 없음
- 데이터 무결성 유지

---

## Pattern Summary

| Category | Pattern | Purpose | Priority |
|----------|---------|---------|----------|
| Performance | Database Indexing | 조회 성능 향상 | High |
| Performance | Response Caching | 응답 시간 단축 | High |
| Performance | Async Processing | 동시 처리 능력 향상 | High |
| Performance | Connection Pool | 연결 재사용 | High |
| Performance | Bundle Optimization | 로딩 시간 단축 | Medium |
| Security | Password Hashing | 비밀번호 보안 | High |
| Security | JWT Authentication | Stateless 인증 | High |
| Security | Input Validation | 악의적 입력 차단 | High |
| Security | File Upload Validation | 파일 업로드 보안 | Medium |
| Error Handling | Centralized Error Handling | 일관된 에러 응답 | High |
| Error Handling | Graceful Degradation | 서비스 안정성 | High |
| Caching | Cache-Aside | 메뉴 조회 최적화 | High |
| Concurrency | Pessimistic Locking | 데이터 일관성 | High |
| Concurrency | Sequential Number | 주문 번호 생성 | High |
| Real-time | SSE Pub-Sub | 실시간 업데이트 | High |
| Logging | Structured Logging | 체계적 로깅 | High |
| Data Persistence | File-based DB | 데이터 영속성 | High |
| Data Persistence | Snapshot | 과거 데이터 정확성 | High |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
