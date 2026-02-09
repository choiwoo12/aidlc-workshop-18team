# Infrastructure Design - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 인프라 설계입니다. Unit 1의 인프라를 재사용하며, 추가 인프라 구성이 불필요합니다.

---

## Infrastructure Reuse Strategy

Unit 2는 Unit 1 (Shared Foundation)의 인프라를 100% 재사용합니다. 모든 논리적 컴포넌트는 애플리케이션 레벨에서 구현되거나 브라우저/FastAPI 내장 기능을 사용합니다.

---

## Component Infrastructure Mapping

### Frontend Components

#### 1. SSE Connection Manager

**Logical Component**: SSE 연결 생명주기 관리

**Infrastructure Mapping**:
- **Technology**: Browser EventSource API (브라우저 내장)
- **Infrastructure**: 없음 (브라우저 표준 API)
- **Configuration**: JavaScript 코드 레벨

**Implementation**:
```javascript
// 브라우저 내장 API 사용
const eventSource = new EventSource('/api/sse/orders/1');
```

**Rationale**: 
- 브라우저 표준 API로 추가 인프라 불필요
- 자동 재연결 기능 내장
- 모든 모던 브라우저 지원

---

#### 2. Cart Manager

**Logical Component**: 장바구니 상태 관리 및 영속성

**Infrastructure Mapping**:
- **Technology**: SessionStorage (브라우저 내장)
- **Infrastructure**: 없음 (브라우저 Web Storage API)
- **Storage Location**: 브라우저 메모리
- **Capacity**: 5-10MB (브라우저별 상이)

**Implementation**:
```javascript
// 브라우저 내장 API 사용
sessionStorage.setItem('cart', JSON.stringify(cart));
const cart = JSON.parse(sessionStorage.getItem('cart'));
```

**Rationale**:
- 브라우저 내장 API로 추가 인프라 불필요
- 탭별 독립적인 세션 관리
- 브라우저 종료 시 자동 삭제

---

#### 3. Order Manager

**Logical Component**: 주문 생성 및 주문 내역 관리

**Infrastructure Mapping**:
- **Technology**: React Component + Axios
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**: 
  - HTTP Client: Axios (Unit 1)
  - SSE Connection Manager (Unit 2)
  - Cart Manager (Unit 2)

**Rationale**: 애플리케이션 레벨 로직으로 인프라 불필요

---

#### 4. Menu Manager

**Logical Component**: 메뉴 조회 및 필터링

**Infrastructure Mapping**:
- **Technology**: React Component + Axios
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**: HTTP Client: Axios (Unit 1)

**Rationale**: 애플리케이션 레벨 로직으로 인프라 불필요

---

#### 5. Validation Service (Frontend)

**Logical Component**: 클라이언트 측 데이터 유효성 검증

**Infrastructure Mapping**:
- **Technology**: JavaScript Pure Functions
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**: 없음

**Rationale**: Pure function으로 인프라 불필요

---

#### 6. Error Handler

**Logical Component**: 에러 처리 및 사용자 피드백

**Infrastructure Mapping**:
- **Technology**: React Component + Toast/Modal
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**: UI Component Library

**Rationale**: 애플리케이션 레벨 로직으로 인프라 불필요

---

### Backend Components

#### 7. SSE Service

**Logical Component**: SSE 이벤트 생성 및 브로드캐스트

**Infrastructure Mapping**:
- **Technology**: FastAPI StreamingResponse
- **Infrastructure**: 없음 (FastAPI 내장 기능)
- **Protocol**: HTTP/1.1 (Server-Sent Events)
- **Port**: 8000 (Backend 포트 공유)

**Implementation**:
```python
from fastapi.responses import StreamingResponse

@app.get("/api/sse/orders/{table_id}")
async def sse_orders(table_id: int):
    return StreamingResponse(
        event_generator(table_id),
        media_type="text/event-stream"
    )
```

**Rationale**:
- FastAPI 내장 기능으로 추가 인프라 불필요
- HTTP/1.1 프로토콜 사용
- 기존 백엔드 포트 공유

---

#### 8. Order Service

**Logical Component**: 주문 생성 및 관리 비즈니스 로직

**Infrastructure Mapping**:
- **Technology**: Python Class (FastAPI Service Layer)
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**:
  - Order Repository (Unit 1)
  - OrderItem Repository (Unit 1)
  - Database Connection (Unit 1)
  - Order Number Generator (Unit 2)
  - Validation Service (Unit 2)
  - SSE Service (Unit 2)

**Database Access**:
- **Database**: SQLite 파일 기반 (Unit 1)
- **Location**: `./data/app.db` (Docker 볼륨 마운트)
- **ORM**: SQLAlchemy 2.0+ (Unit 1)

**Rationale**: Unit 1의 데이터베이스 인프라 재사용

---

#### 9. Menu Service

**Logical Component**: 메뉴 조회 비즈니스 로직

**Infrastructure Mapping**:
- **Technology**: Python Class (FastAPI Service Layer)
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**:
  - Menu Repository (Unit 1)
  - Database Connection (Unit 1)

**Database Access**:
- **Database**: SQLite 파일 기반 (Unit 1)
- **Location**: `./data/app.db` (Docker 볼륨 마운트)
- **ORM**: SQLAlchemy 2.0+ (Unit 1)

**Rationale**: Unit 1의 데이터베이스 인프라 재사용

---

#### 10. Validation Service (Backend)

**Logical Component**: 서버 측 데이터 유효성 검증

**Infrastructure Mapping**:
- **Technology**: Python Class (FastAPI Service Layer)
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**:
  - Menu Repository (Unit 1)
  - Database Connection (Unit 1)

**Rationale**: 애플리케이션 레벨 로직으로 인프라 불필요

---

#### 11. Order Number Generator

**Logical Component**: 주문 번호 생성

**Infrastructure Mapping**:
- **Technology**: Python Class
- **Infrastructure**: 없음 (애플리케이션 레벨)
- **Dependencies**:
  - Order Repository (Unit 1)
  - Database Connection (Unit 1)

**Database Access**:
- **Database**: SQLite 파일 기반 (Unit 1)
- **AUTO_INCREMENT**: SQLite 내장 기능 활용

**Rationale**: 데이터베이스 내장 기능 활용

---

## Infrastructure Summary

### Unit 1 Infrastructure Reuse

Unit 2는 다음 Unit 1 인프라를 재사용합니다:

| Infrastructure | Technology | Location | Purpose |
|---------------|-----------|----------|---------|
| Database | SQLite (파일 기반) | `./data/app.db` | 데이터 저장 |
| File Storage | 로컬 파일 시스템 | `./uploads/` | 이미지 저장 |
| Logging | 로컬 파일 시스템 | `./logs/` | 로그 저장 |
| Cache | 인메모리 (Python dict) | 애플리케이션 메모리 | 메뉴 캐싱 |
| Authentication | JWT | 애플리케이션 레벨 | 인증/권한 |
| Deployment | Docker Compose | 컨테이너 | 배포 |

### Unit 2 Specific Infrastructure

Unit 2 특화 인프라는 **없음**. 모든 컴포넌트는 다음과 같이 구현됩니다:

| Component Type | Implementation | Infrastructure |
|---------------|---------------|---------------|
| Frontend Components | React + Browser APIs | 없음 |
| Backend Components | FastAPI + Python | 없음 |
| SSE | FastAPI StreamingResponse | 없음 |
| SessionStorage | Browser Web Storage API | 없음 |

---

## Deployment Architecture

Unit 2는 Unit 1과 동일한 Docker Compose 환경을 사용합니다.

### Docker Compose Services

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data          # Unit 1: Database
      - ./logs:/app/logs          # Unit 1: Logs
      - ./uploads:/app/uploads    # Unit 1: File Storage
    environment:
      - DATABASE_URL=sqlite:///./data/app.db
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    # Unit 2 코드는 backend 서비스에 포함됨

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    # Unit 2 코드는 frontend 서비스에 포함됨
```

**Unit 2 통합**:
- Backend: Unit 2 서비스 및 API 컨트롤러가 backend 서비스에 추가됨
- Frontend: Unit 2 컴포넌트 및 페이지가 frontend 서비스에 추가됨
- 추가 서비스 불필요

---

## Network Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Host Machine                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Docker Compose Network                  │   │
│  │                                                       │   │
│  │  ┌──────────────────┐      ┌──────────────────┐    │   │
│  │  │   Frontend       │      │   Backend        │    │   │
│  │  │   (React)        │◄────►│   (FastAPI)      │    │   │
│  │  │   Port: 3000     │ HTTP │   Port: 8000     │    │   │
│  │  │                  │ SSE  │                  │    │   │
│  │  └──────────────────┘      └──────────────────┘    │   │
│  │                                      │               │   │
│  │                                      ▼               │   │
│  │                             ┌──────────────────┐    │   │
│  │                             │  SQLite DB       │    │   │
│  │                             │  (./data/)       │    │   │
│  │                             └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Host Volumes                            │   │
│  │  - ./data/app.db (Database)                         │   │
│  │  - ./logs/ (Logs)                                   │   │
│  │  - ./uploads/ (Images)                              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Unit 2 통합**:
- Frontend → Backend: HTTP 요청 (메뉴 조회, 주문 생성, 주문 내역)
- Frontend → Backend: SSE 연결 (주문 상태 실시간 업데이트)
- Backend → Database: SQLAlchemy ORM (Order, OrderItem, Menu 조회/생성)

---

## Data Flow

### 주문 생성 플로우

```
[고객 브라우저]
    ↓ (SessionStorage)
[Cart Manager] → 장바구니 데이터
    ↓ (HTTP POST /api/orders)
[Backend: Order Service]
    ↓ (SQLAlchemy)
[SQLite Database: ./data/app.db]
    ↓ (Order + OrderItem 생성)
[Backend: SSE Service]
    ↓ (SSE Event)
[고객 브라우저: SSE Connection Manager]
    ↓ (주문 상태 업데이트)
[Order Manager] → UI 업데이트
```

### 메뉴 조회 플로우

```
[고객 브라우저]
    ↓ (HTTP GET /api/menus)
[Backend: Menu Service]
    ↓ (SQLAlchemy)
[SQLite Database: ./data/app.db]
    ↓ (Menu 조회)
[Backend: Menu Service] → 판매 가능 메뉴 필터링
    ↓ (JSON Response)
[고객 브라우저: Menu Manager]
    ↓ (메뉴 카드 렌더링)
[React UI]
```

---

## Infrastructure Configuration

### Environment Variables

Unit 2는 Unit 1의 환경 변수를 재사용합니다:

```bash
# .env (Unit 1)
DATABASE_URL=sqlite:///./data/app.db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=16

# Unit 2 추가 환경 변수 없음
```

### Application Configuration

```python
# backend/app/config.py (Unit 1 확장)
class Settings(BaseSettings):
    # Unit 1 설정
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 16
    
    # Unit 2 설정 (추가)
    SSE_KEEP_ALIVE_INTERVAL: int = 30  # seconds
    SSE_CONNECTION_TIMEOUT: int = 60   # seconds
    ORDER_NUMBER_FORMAT: str = "T{table_number}-{sequence:03d}"
```

---

## Infrastructure Dependencies

### External Dependencies

**없음**. Unit 2는 외부 인프라 서비스를 사용하지 않습니다.

### Internal Dependencies (Unit 1)

Unit 2는 다음 Unit 1 인프라에 의존합니다:

1. **Database Connection Manager** (Unit 1)
   - SQLite 연결 관리
   - 트랜잭션 관리
   - 연결 풀 관리

2. **Repository Layer** (Unit 1)
   - Order Repository
   - OrderItem Repository
   - Menu Repository
   - Table Repository

3. **Authentication Manager** (Unit 1)
   - JWT 토큰 검증
   - 테이블 세션 관리

4. **Logging Manager** (Unit 1)
   - 파일 로깅
   - 로그 로테이션

5. **File Storage Manager** (Unit 1)
   - 이미지 저장 (메뉴 이미지)

---

## Scalability Considerations

### Current Capacity

- **동시 주문 처리**: 5개 테이블
- **SSE 동시 연결**: 10개
- **데이터베이스 연결 풀**: 최소 10개, 최대 20개 (Unit 1)

### Scaling Strategy (Future)

Unit 2는 현재 로컬 개발 환경만 지원하지만, 향후 확장 시 다음 전략을 고려할 수 있습니다:

1. **Database Scaling**:
   - SQLite → PostgreSQL/MySQL 마이그레이션
   - 읽기 전용 복제본 추가

2. **SSE Scaling**:
   - Redis Pub/Sub로 SSE 이벤트 브로드캐스트
   - 다중 백엔드 인스턴스 지원

3. **Caching**:
   - Redis 캐시 추가 (메뉴 조회)
   - 캐시 무효화 전략

4. **Load Balancing**:
   - Nginx 리버스 프록시 추가
   - 다중 백엔드 인스턴스

**현재 상태**: 위 확장은 MVP 범위 밖이며, 현재 인프라로 충분합니다.

---

## Infrastructure Summary Table

| Category | Unit 1 | Unit 2 | Notes |
|----------|--------|--------|-------|
| Database | SQLite 파일 기반 | 재사용 | Unit 1 인프라 |
| File Storage | 로컬 파일 시스템 | 재사용 | Unit 1 인프라 |
| Logging | 로컬 파일 시스템 | 재사용 | Unit 1 인프라 |
| Cache | 인메모리 (Python dict) | 재사용 | Unit 1 인프라 |
| Authentication | JWT | 재사용 | Unit 1 인프라 |
| SSE | - | FastAPI 내장 | 추가 인프라 불필요 |
| SessionStorage | - | 브라우저 내장 | 추가 인프라 불필요 |
| Deployment | Docker Compose | 재사용 | Unit 1 인프라 |

---

## Conclusion

Unit 2 (Customer Order Domain)는 Unit 1 (Shared Foundation)의 인프라를 100% 재사용합니다. 모든 Unit 2 컴포넌트는 애플리케이션 레벨에서 구현되거나 브라우저/FastAPI 내장 기능을 사용하므로, **추가 인프라 구성이 불필요**합니다.

이는 다음과 같은 이점을 제공합니다:

1. **단순성**: 추가 인프라 설정 불필요
2. **비용 절감**: 추가 인프라 비용 없음
3. **유지보수 용이**: 인프라 관리 포인트 최소화
4. **빠른 개발**: 인프라 설정 시간 절약

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
