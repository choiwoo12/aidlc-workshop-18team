# Tech Stack Decisions - Unit 1: Shared Foundation

## Overview

Unit 1의 기술 스택 결정 및 선택 근거입니다. 각 기술 선택의 장단점과 선택 이유를 문서화합니다.

---

## 1. Backend Technology Stack

### 1.1 Programming Language: Python 3.11+

**Decision**: Python 3.11 이상

**Rationale**:
- Requirements Analysis에서 이미 결정됨
- 빠른 개발 속도
- 풍부한 라이브러리 생태계
- 비동기 처리 지원

---

### 1.2 Web Framework: FastAPI

**Decision**: FastAPI 0.104+

**Alternatives Considered**:
- Django: 풍부한 기능, ORM 내장, Admin 패널
- Flask: 경량, 유연함, 간단함

**Rationale**:
- ✅ 비동기 처리 (async/await) - 성능 우수
- ✅ 자동 API 문서화 (Swagger UI, ReDoc)
- ✅ Pydantic 기반 데이터 검증 - 타입 안전성
- ✅ 빠른 개발 속도
- ✅ 현대적인 Python 기능 활용
- ✅ SSE (Server-Sent Events) 지원

**Trade-offs**:
- ❌ Django보다 기능이 적음 (Admin 패널 없음)
- ❌ Flask보다 학습 곡선이 약간 높음

**Conclusion**: 성능, 자동 문서화, 타입 안전성이 MVP에 가장 적합

---

### 1.3 Database: File-based SQLite

**Decision**: 파일 기반 SQLite 단일 전략

**Alternatives Considered**:
- SQLite 메모리 기반: 모든 데이터 휘발성
- 하이브리드 SQLite: 파일 + 메모리 혼합
- Redis: Key-Value, 빠름

**Rationale**:
- ✅ 모든 데이터 영속성 보장
- ✅ 서버 재시작 시에도 데이터 유지
- ✅ 단일 DB 연결로 복잡도 감소
- ✅ 트랜잭션 관리 단순화
- ✅ 설치 및 설정 간단
- ✅ SQL 쿼리 지원
- ✅ 관계형 데이터 모델 지원

**Implementation**:
```python
# File-based DB
engine = create_engine('sqlite:///data/app.db')
```

**Data Storage**:
- All entities: Store, Table, Menu, Order, OrderItem, OrderHistory

**Trade-offs**:
- ✅ 복잡도 감소 (단일 DB 연결)
- ✅ 데이터 손실 위험 없음
- ❌ 메모리 기반 대비 성능 약간 저하 (MVP 범위에서 무시 가능)

**Conclusion**: 단순성과 데이터 안정성이 MVP에 가장 적합

---

### 1.4 ORM: SQLAlchemy 2.0+

**Decision**: SQLAlchemy 2.0+

**Alternatives Considered**:
- Django ORM: Django 전용
- Peewee: 경량, 간단함
- Raw SQL: ORM 없음

**Rationale**:
- ✅ 프레임워크 독립적 (FastAPI와 호환)
- ✅ 강력하고 유연함
- ✅ 비동기 지원 (SQLAlchemy 2.0+)
- ✅ 타입 힌팅 지원
- ✅ 마이그레이션 도구 (Alembic)

**Trade-offs**:
- ❌ 학습 곡선이 높음
- ❌ Django ORM보다 복잡함

**Conclusion**: 유연성과 강력함이 장기적으로 유리

---

### 1.5 Authentication: JWT (JSON Web Token)

**Decision**: PyJWT 2.8+

**Implementation**:
- Algorithm: HS256
- Secret Key: 환경 변수로 관리
- Token Expiry: Admin 8시간, Table 24시간

**Rationale**:
- ✅ Stateless 인증
- ✅ 확장 가능
- ✅ 표준 기술

---

### 1.6 Password Hashing: bcrypt

**Decision**: bcrypt 4.1+

**Implementation**:
- Cost Factor: 12
- Salt: 자동 생성

**Rationale**:
- ✅ 업계 표준
- ✅ 안전한 해싱 알고리즘
- ✅ Rainbow Table 공격 방어

---

### 1.7 Real-time Communication: Server-Sent Events (SSE)

**Decision**: FastAPI SSE (sse-starlette)

**Alternatives Considered**:
- WebSocket: 양방향 통신
- Polling: 주기적 요청

**Rationale**:
- ✅ 단방향 통신 (서버 → 클라이언트)만 필요
- ✅ WebSocket보다 간단함
- ✅ HTTP 기반 (방화벽 친화적)
- ✅ 자동 재연결

**Trade-offs**:
- ❌ 양방향 통신 불가 (필요 없음)

**Conclusion**: 요구사항에 가장 적합

---

### 1.8 Logging: Python logging module

**Decision**: Python 내장 logging 모듈

**Alternatives Considered**:
- Loguru: 간단하고 강력함
- structlog: 구조화된 로깅

**Rationale**:
- ✅ 내장 모듈 (추가 의존성 없음)
- ✅ 충분한 기능
- ✅ 표준 라이브러리

**Configuration**:
- Log Level: INFO (프로덕션), DEBUG (개발)
- Log Format: `[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s`
- Log File: 날짜별 파일 (logs/app-2026-02-09.log)

**Trade-offs**:
- ❌ Loguru보다 설정이 복잡함

**Conclusion**: MVP에 충분하며 표준 라이브러리 사용

---

## 2. Frontend Technology Stack

### 2.1 Framework: React 18+

**Decision**: React 18+

**Rationale**:
- Requirements Analysis에서 이미 결정됨
- 컴포넌트 기반 아키텍처
- 풍부한 생태계
- 높은 개발자 커뮤니티

---

### 2.2 State Management: React Context API

**Decision**: React Context API

**Alternatives Considered**:
- Redux: 강력하지만 복잡함
- Zustand: 간단하고 가벼움
- Recoil: Facebook 제작

**Rationale**:
- ✅ React 내장 (추가 의존성 없음)
- ✅ 간단한 상태 관리에 적합
- ✅ MVP 범위에 충분

**Usage**:
- AuthContext: 인증 상태
- CartContext: 장바구니 상태

**Trade-offs**:
- ❌ 복잡한 상태 관리에는 부족
- ❌ Redux보다 디버깅 도구가 약함

**Conclusion**: MVP 범위에 가장 적합

---

### 2.3 HTTP Client: Axios

**Decision**: Axios 1.6+

**Alternatives Considered**:
- Fetch API: 브라우저 내장
- 둘 다 사용: 복잡도 증가

**Rationale**:
- ✅ 인터셉터 (요청/응답 가로채기)
- ✅ 자동 JSON 변환
- ✅ 요청 취소 지원
- ✅ 에러 처리 간편
- ✅ 타임아웃 설정

**Trade-offs**:
- ❌ 번들 크기 증가 (약 13KB)

**Conclusion**: 개발 편의성이 번들 크기보다 중요

---

### 2.4 Styling: Tailwind CSS

**Decision**: Tailwind CSS 3.4+

**Alternatives Considered**:
- CSS Modules: 스코프 CSS
- Styled Components: CSS-in-JS

**Rationale**:
- ✅ 빠른 개발 속도 (유틸리티 클래스)
- ✅ 일관된 디자인 시스템
- ✅ 반응형 디자인 간편
- ✅ 프로덕션 빌드 시 미사용 CSS 제거

**Trade-offs**:
- ❌ HTML이 클래스로 복잡해짐
- ❌ 학습 곡선

**Conclusion**: 빠른 개발과 일관성이 MVP에 적합

---

### 2.5 Build Tool: Vite

**Decision**: Vite 5+

**Alternatives Considered**:
- Create React App: 설정 간편
- Webpack: 강력하지만 복잡함

**Rationale**:
- ✅ 빠른 개발 서버 (HMR)
- ✅ 빠른 빌드 속도
- ✅ 현대적인 도구
- ✅ 기본 최적화 (Code splitting, Tree shaking)

**Trade-offs**:
- ❌ CRA보다 설정이 필요

**Conclusion**: 성능과 개발 경험이 우수

---

### 2.6 Storage: LocalStorage & SessionStorage

**Decision**: 
- LocalStorage: 관리자 JWT 토큰
- SessionStorage: 고객 장바구니, 테이블 JWT 토큰

**Rationale**:
- ✅ 브라우저 내장 (추가 의존성 없음)
- ✅ 간단한 API
- ✅ 요구사항 충족

**Security Note**:
- LocalStorage는 XSS 공격에 취약
- 로컬 개발 환경만 사용하므로 MVP 범위에서 허용
- 프로덕션 배포 시 HttpOnly Cookie로 변경 권장

---

## 3. Development Tools

### 3.1 Containerization: Docker Compose

**Decision**: Docker Compose 2.0+

**Rationale**:
- Requirements Analysis에서 이미 결정됨
- 일관된 개발 환경
- 간편한 설정 및 실행

**Services**:
- backend: FastAPI 서버
- frontend: React 개발 서버

---

### 3.2 Version Control: Git (GitHub Flow)

**Decision**: Git + GitHub Flow

**Rationale**:
- Requirements Analysis에서 이미 결정됨
- 간단한 브랜치 전략
- MVP에 적합

---

### 3.3 Linting & Formatting

**Backend**:
- Black: 코드 포맷팅
- Pylint: 린팅
- mypy: 타입 체킹 (선택)

**Frontend**:
- ESLint: 린팅
- Prettier: 코드 포맷팅

**Rationale**:
- 일관된 코드 스타일
- 버그 조기 발견
- 코드 품질 향상

---

### 3.4 Testing

**Backend**:
- pytest: 단위 테스트, 통합 테스트
- pytest-asyncio: 비동기 테스트
- httpx: API 테스트

**Frontend**:
- Jest: 단위 테스트
- React Testing Library: 컴포넌트 테스트
- Playwright: E2E 테스트 (선택)

**Rationale**:
- 포괄적인 테스트 커버리지
- 버그 조기 발견
- 리팩토링 안전성

---

## 4. Performance Optimization

### 4.1 Database Indexing

**Strategy**: Foreign Key + 자주 조회되는 필드

**Indexed Fields**:
- All Primary Keys
- All Foreign Keys
- table_number (Table)
- category_level1 (Menu)
- status (Order)

**Rationale**:
- JOIN 성능 향상
- WHERE 절 성능 향상
- 조회 성능 최적화

---

### 4.2 API Response Caching

**Strategy**: 메뉴 조회 API만 캐싱

**Implementation**:
- 메모리 캐싱 (Python dict)
- 캐시 만료 시간: 5분
- 메뉴 변경 시 캐시 무효화

**Rationale**:
- 메뉴는 자주 변경되지 않음
- 조회 빈도가 높음
- 응답 시간 단축

---

### 4.3 Frontend Bundle Optimization

**Strategy**: 기본 최적화 (Code splitting, Tree shaking)

**Implementation**:
- Vite 기본 최적화 활용
- 고객/관리자 코드 분리
- 이미지 최적화

**Rationale**:
- 초기 로딩 시간 단축
- 사용하지 않는 코드 제거
- 사용자 경험 향상

---

## 5. Security Measures

### 5.1 CORS Policy

**Development**: 모든 Origin 허용

**Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Note**: 특정 Origin만 허용하도록 변경 필요

---

### 5.2 Input Validation

**Strategy**: 양방향 검증 (클라이언트 + 서버)

**Implementation**:
- Frontend: React Hook Form + Yup
- Backend: FastAPI Pydantic models

**Rationale**:
- 사용자 경험 (즉각적인 피드백)
- 보안 (악의적인 요청 차단)

---

## 6. File Storage

### 6.1 Image Storage

**Strategy**: 로컬 파일 시스템

**Implementation**:
- 저장 경로: `uploads/menu-images/`
- 파일명: UUID 기반 고유 이름
- 파일 크기 제한: 5MB

**Rationale**:
- 간단한 구현
- 로컬 개발 환경에 적합
- 추가 서비스 불필요

**Future Considerations**:
- 프로덕션 배포 시 클라우드 스토리지 (S3, GCS) 고려

---

## 7. Error Handling

### 7.1 Error Code System

**Strategy**: HTTP 상태 코드만 사용

**Rationale**:
- 간단함
- 표준 HTTP 상태 코드로 충분
- MVP 범위에 적합

**Status Codes**:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error

---

## Tech Stack Summary

| Category | Technology | Version | Rationale |
|----------|-----------|---------|-----------|
| **Backend** |
| Language | Python | 3.11+ | 빠른 개발, 풍부한 생태계 |
| Framework | FastAPI | 0.104+ | 비동기, 자동 문서화, 타입 안전성 |
| Database | SQLite | 3.40+ | 간단함, SQL 지원, 파일 기반 영속성 |
| ORM | SQLAlchemy | 2.0+ | 강력함, 유연함, 비동기 지원 |
| Auth | PyJWT | 2.8+ | 표준 JWT 구현 |
| Password | bcrypt | 4.1+ | 안전한 해싱 |
| Real-time | sse-starlette | 1.8+ | SSE 지원 |
| Logging | logging | Built-in | 표준 라이브러리 |
| **Frontend** |
| Framework | React | 18+ | 컴포넌트 기반, 풍부한 생태계 |
| State | Context API | Built-in | 간단함, MVP에 충분 |
| HTTP | Axios | 1.6+ | 인터셉터, 자동 JSON 변환 |
| Styling | Tailwind CSS | 3.4+ | 빠른 개발, 일관성 |
| Build | Vite | 5+ | 빠른 HMR, 빠른 빌드 |
| Storage | LocalStorage/SessionStorage | Built-in | 간단함, 요구사항 충족 |
| **Development** |
| Container | Docker Compose | 2.0+ | 일관된 환경 |
| VCS | Git | 2.40+ | 표준 버전 관리 |
| Linting (BE) | Black + Pylint | Latest | 코드 품질 |
| Linting (FE) | ESLint + Prettier | Latest | 코드 품질 |
| Testing (BE) | pytest | 7.4+ | 포괄적 테스트 |
| Testing (FE) | Jest + RTL | Latest | 컴포넌트 테스트 |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
