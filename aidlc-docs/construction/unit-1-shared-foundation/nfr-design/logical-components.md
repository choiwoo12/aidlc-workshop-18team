# Logical Components - Unit 1: Shared Foundation

## Overview

Unit 1의 논리적 컴포넌트 정의입니다. 인프라 독립적이며, 비기능 요구사항을 충족하기 위한 컴포넌트들을 정의합니다.

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  (Business Logic, Domain Entities, Use Cases)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Logical Components Layer                     │
│  (Infrastructure-Independent Components)                      │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Database   │  │     Auth     │  │    Cache     │      │
│  │  Connection  │  │   Manager    │  │   Manager    │      │
│  │   Manager    │  └──────────────┘  └──────────────┘      │
│  └──────────────┘                                            │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Logging    │  │     SSE      │  │    File      │      │
│  │   Manager    │  │   Manager    │  │   Storage    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                         │
│  (SQLite, File System, etc.)                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Database Connection Manager

### Purpose
데이터베이스 연결 생성, 관리, 재사용을 담당하는 컴포넌트

### Responsibilities
- 데이터베이스 연결 풀 관리
- 연결 생성 및 해제
- 트랜잭션 관리
- 연결 상태 모니터링

### Interface
```python
class DatabaseConnectionManager:
    def get_connection() -> Connection
    def release_connection(connection: Connection) -> None
    def begin_transaction() -> Transaction
    def commit_transaction(transaction: Transaction) -> None
    def rollback_transaction(transaction: Transaction) -> None
    def health_check() -> bool
```

### Configuration
- 최소 연결 수: 10개
- 최대 연결 수: 20개
- 연결 타임아웃: 30초
- 유휴 연결 제거 시간: 300초

### Dependencies
- None (Infrastructure Layer와 직접 통신)

---

## 2. Authentication Manager

### Purpose
사용자 인증 및 권한 관리를 담당하는 컴포넌트

### Responsibilities
- 비밀번호 해싱 및 검증
- JWT 토큰 생성 및 검증
- 권한 확인
- 토큰 만료 처리

### Interface
```python
class AuthenticationManager:
    def hash_password(password: str) -> str
    def verify_password(password: str, hash: str) -> bool
    def generate_token(user_data: dict, token_type: str) -> str
    def verify_token(token: str) -> dict
    def check_permission(token: str, required_permission: str) -> bool
```

### Configuration
- bcrypt cost factor: 12
- JWT algorithm: HS256
- Token expiry: Admin 8시간, Table 24시간
- Secret key: 환경 변수로 관리

### Dependencies
- None (Infrastructure Layer와 직접 통신)

---

## 3. Cache Manager

### Purpose
API 응답 캐싱을 담당하는 컴포넌트

### Responsibilities
- 캐시 데이터 저장 및 조회
- 캐시 만료 처리
- 캐시 무효화
- 캐시 키 관리

### Interface
```python
class CacheManager:
    def get(key: str) -> Optional[Any]
    def set(key: str, value: Any, ttl: int) -> None
    def delete(key: str) -> None
    def delete_pattern(pattern: str) -> None
    def clear() -> None
```

### Configuration
- 캐시 만료 시간: 5분 (300초)
- 캐시 저장소: 메모리 (Python dict)
- 캐시 키 패턴:
  - `menu:list:{store_id}`
  - `menu:detail:{menu_id}`
  - `menu:category:{store_id}:{category_level1}`

### Cache Invalidation Rules
- 메뉴 생성: `menu:list:{store_id}`, `menu:category:{store_id}:*` 삭제
- 메뉴 수정: `menu:detail:{menu_id}`, `menu:list:{store_id}`, `menu:category:{store_id}:*` 삭제
- 메뉴 삭제: `menu:detail:{menu_id}`, `menu:list:{store_id}`, `menu:category:{store_id}:*` 삭제

### Dependencies
- None (In-memory storage)

---

## 4. Logging Manager

### Purpose
애플리케이션 로깅을 담당하는 컴포넌트

### Responsibilities
- 로그 메시지 기록
- 로그 레벨 관리
- 로그 파일 로테이션
- 로그 포맷팅

### Interface
```python
class LoggingManager:
    def debug(message: str, context: dict = None) -> None
    def info(message: str, context: dict = None) -> None
    def warning(message: str, context: dict = None) -> None
    def error(message: str, context: dict = None, exception: Exception = None) -> None
    def critical(message: str, context: dict = None, exception: Exception = None) -> None
```

### Configuration
- 로그 레벨: INFO (프로덕션), DEBUG (개발)
- 로그 형식: `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`
- 로그 파일: `logs/app-{date}.log`
- 로그 로테이션: 날짜별, 30일 후 자동 삭제

### Log Levels
- DEBUG: 디버깅 정보 (개발 환경만)
- INFO: 정상 동작 로그 (API 요청, 주문 생성 등)
- WARNING: 비즈니스 규칙 위반, 인증/권한 오류
- ERROR: 시스템 오류, 예상치 못한 오류
- CRITICAL: 치명적 오류 (시스템 중단)

### Dependencies
- File System (로그 파일 저장)

---

## 5. SSE Manager

### Purpose
Server-Sent Events를 통한 실시간 통신을 담당하는 컴포넌트

### Responsibilities
- SSE 연결 관리
- 이벤트 브로드캐스트
- 연결 상태 모니터링
- 자동 재연결 지원

### Interface
```python
class SSEManager:
    def add_connection(connection_id: str, connection: SSEConnection) -> None
    def remove_connection(connection_id: str) -> None
    def broadcast_event(event_type: str, data: dict) -> None
    def send_event(connection_id: str, event_type: str, data: dict) -> None
    def get_active_connections() -> List[str]
```

### Configuration
- 연결 관리: 다중 연결 허용
- 연결 풀: 메모리 기반 (dict)
- 이벤트 타입:
  - `order_created`: 새 주문 생성
  - `order_updated`: 주문 상태 변경
  - `order_deleted`: 주문 삭제

### Event Format
```json
{
  "event": "order_created",
  "data": {
    "order_id": "123",
    "table_id": "5",
    "order_number": "001",
    "total_amount": 10000,
    "status": "PENDING"
  },
  "timestamp": "2026-02-09T10:00:00Z"
}
```

### Dependencies
- None (In-memory storage)

---

## 6. File Storage Manager

### Purpose
파일 저장 및 관리를 담당하는 컴포넌트

### Responsibilities
- 파일 업로드 처리
- 파일 저장 (UUID 기반 파일명)
- 파일 조회
- 파일 삭제
- 파일 검증 (크기, MIME 타입)

### Interface
```python
class FileStorageManager:
    def upload_file(file: File, file_type: str) -> str
    def get_file_url(file_id: str) -> str
    def delete_file(file_id: str) -> None
    def validate_file(file: File) -> bool
```

### Configuration
- 저장 경로: `uploads/menu-images/`
- 파일명 형식: `{uuid}.{extension}`
- 파일 크기 제한: 5MB
- 허용 MIME 타입: `image/*`

### Validation Rules
- 파일 크기: 최대 5MB
- MIME 타입: image/* (image/jpeg, image/png, image/gif 등)
- 파일명: UUID 기반 (경로 탐색 공격 방지)

### Dependencies
- File System (파일 저장)

---

## Component Interactions

### Scenario 1: 주문 생성
```
1. Application Layer → Database Connection Manager: 연결 요청
2. Database Connection Manager → Application Layer: 연결 반환
3. Application Layer → Database: 주문 생성
4. Application Layer → SSE Manager: 이벤트 브로드캐스트
5. SSE Manager → 모든 관리자 클라이언트: 이벤트 전송
6. Application Layer → Logging Manager: 로그 기록
7. Application Layer → Database Connection Manager: 연결 해제
```

### Scenario 2: 메뉴 조회 (캐시 HIT)
```
1. Application Layer → Cache Manager: 캐시 조회
2. Cache Manager → Application Layer: 캐시 데이터 반환
3. Application Layer → Logging Manager: 로그 기록
```

### Scenario 3: 메뉴 조회 (캐시 MISS)
```
1. Application Layer → Cache Manager: 캐시 조회
2. Cache Manager → Application Layer: 캐시 MISS
3. Application Layer → Database Connection Manager: 연결 요청
4. Database Connection Manager → Application Layer: 연결 반환
5. Application Layer → Database: 메뉴 조회
6. Application Layer → Cache Manager: 캐시 저장
7. Application Layer → Logging Manager: 로그 기록
8. Application Layer → Database Connection Manager: 연결 해제
```

### Scenario 4: 관리자 로그인
```
1. Application Layer → Authentication Manager: 비밀번호 검증
2. Authentication Manager → Application Layer: 검증 결과
3. Application Layer → Authentication Manager: JWT 토큰 생성
4. Authentication Manager → Application Layer: 토큰 반환
5. Application Layer → Logging Manager: 로그 기록
```

### Scenario 5: 메뉴 이미지 업로드
```
1. Application Layer → File Storage Manager: 파일 검증
2. File Storage Manager → Application Layer: 검증 결과
3. Application Layer → File Storage Manager: 파일 저장
4. File Storage Manager → File System: 파일 저장
5. File Storage Manager → Application Layer: 파일 URL 반환
6. Application Layer → Logging Manager: 로그 기록
```

---

## Component Dependencies

```
Database Connection Manager
  └─> Infrastructure Layer (SQLite)

Authentication Manager
  └─> Infrastructure Layer (bcrypt, PyJWT)

Cache Manager
  └─> In-memory Storage (Python dict)

Logging Manager
  └─> File System (로그 파일)

SSE Manager
  └─> In-memory Storage (연결 풀)

File Storage Manager
  └─> File System (파일 저장)
```

---

## Configuration Management

### Configuration Sources
1. 환경 변수 (Environment Variables)
2. 설정 파일 (config.yaml)
3. 기본값 (Default Values)

### Configuration Priority
```
환경 변수 > 설정 파일 > 기본값
```

### Configuration Interface
```python
class ConfigurationManager:
    def get(key: str, default: Any = None) -> Any
    def get_int(key: str, default: int = 0) -> int
    def get_bool(key: str, default: bool = False) -> bool
    def get_list(key: str, default: List = []) -> List
```

### Configuration Keys
```
# Database
DB_FILE_PATH: data/app.db
DB_POOL_MIN_SIZE: 10
DB_POOL_MAX_SIZE: 20
DB_CONNECTION_TIMEOUT: 30

# Authentication
JWT_SECRET_KEY: (환경 변수 필수)
JWT_ALGORITHM: HS256
JWT_ADMIN_EXPIRY: 28800  # 8시간 (초)
JWT_TABLE_EXPIRY: 86400  # 24시간 (초)
BCRYPT_COST_FACTOR: 12

# Cache
CACHE_TTL: 300  # 5분 (초)

# Logging
LOG_LEVEL: INFO
LOG_FILE_PATH: logs/app-{date}.log
LOG_RETENTION_DAYS: 30

# File Storage
UPLOAD_DIR: uploads/menu-images
MAX_FILE_SIZE: 5242880  # 5MB (바이트)
ALLOWED_MIME_TYPES: image/*

# SSE
SSE_HEARTBEAT_INTERVAL: 30  # 30초
```

---

## Error Handling Strategy

### Component-Level Error Handling
각 컴포넌트는 자체적으로 에러를 처리하고, 상위 레이어에 적절한 예외를 전파합니다.

### Error Types
```python
# Database Errors
class DatabaseConnectionError(Exception): pass
class DatabaseQueryError(Exception): pass
class DatabaseTransactionError(Exception): pass

# Authentication Errors
class AuthenticationError(Exception): pass
class AuthorizationError(Exception): pass
class TokenExpiredError(Exception): pass

# Cache Errors
class CacheError(Exception): pass

# File Storage Errors
class FileValidationError(Exception): pass
class FileStorageError(Exception): pass

# SSE Errors
class SSEConnectionError(Exception): pass
```

### Error Propagation
```
Component Layer → Application Layer → API Layer → Client
```

---

## Testing Strategy

### Unit Testing
각 컴포넌트는 독립적으로 테스트 가능해야 합니다.

### Test Coverage
- Database Connection Manager: 연결 풀 관리, 트랜잭션
- Authentication Manager: 비밀번호 해싱, JWT 토큰
- Cache Manager: 캐시 저장/조회/삭제
- Logging Manager: 로그 레벨, 로그 포맷
- SSE Manager: 연결 관리, 이벤트 브로드캐스트
- File Storage Manager: 파일 검증, 파일 저장

### Mock Objects
테스트 시 Infrastructure Layer는 Mock 객체로 대체합니다.

---

## Component Summary

| Component | Purpose | Dependencies | Priority |
|-----------|---------|--------------|----------|
| Database Connection Manager | DB 연결 관리 | SQLite | High |
| Authentication Manager | 인증/권한 관리 | bcrypt, PyJWT | High |
| Cache Manager | 응답 캐싱 | In-memory | High |
| Logging Manager | 로깅 | File System | High |
| SSE Manager | 실시간 통신 | In-memory | High |
| File Storage Manager | 파일 저장 | File System | Medium |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
