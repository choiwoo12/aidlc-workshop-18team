# NFR Requirements - Unit 1: Shared Foundation

## Overview

Unit 1의 비기능 요구사항(Non-Functional Requirements) 명세입니다. 성능, 보안, 확장성, 유지보수성 등의 품질 속성을 정의합니다.

---

## 1. Performance Requirements (성능 요구사항)

### PR-001: API 응답 시간
**Requirement**: API 응답 시간 목표 달성

**Targets**:
- 주문 생성 (POST /orders): < 2초
- 메뉴 조회 (GET /menus): < 1초
- 주문 조회 (GET /orders): < 1초
- 주문 상태 변경 (PATCH /orders/{id}): < 1초

**Implementation Strategy**:
- 데이터베이스 인덱스 최적화 (Foreign Key + 자주 조회되는 필드)
- 메뉴 조회 API 응답 캐싱
- 비동기 처리 (FastAPI 활용)

**Measurement**:
- API 응답 시간 로깅
- 성능 테스트 (단위: 밀리초)

---

### PR-002: 실시간 업데이트 지연
**Requirement**: SSE를 통한 실시간 주문 업데이트 지연 최소화

**Target**: < 2초

**Implementation Strategy**:
- Server-Sent Events (SSE) 사용
- 주문 생성/변경 시 즉시 SSE 이벤트 전송
- 연결 유지 및 재연결 로직

**Measurement**:
- 주문 생성 시각 ~ 관리자 화면 표시 시각 측정

---

### PR-003: 동시 접속 지원
**Requirement**: 소규모 매장 동시 접속 지원

**Target**: 10개 테이블 (고객 10명 + 관리자 1-2명)

**Implementation Strategy**:
- 인메모리 데이터베이스 (SQLite)
- 비동기 처리 (FastAPI)
- 연결 풀 관리

**Measurement**:
- 부하 테스트 (동시 사용자 수)

---

### PR-004: 프론트엔드 초기 로딩 시간
**Requirement**: 프론트엔드 초기 로딩 시간 최소화

**Target**: < 3초 (3G 네트워크 기준)

**Implementation Strategy**:
- 기본 번들 최적화 (Code splitting, Tree shaking)
- 고객/관리자 코드 분리
- 이미지 최적화 (적절한 크기 및 형식)

**Measurement**:
- Lighthouse 성능 점수
- 초기 로딩 시간 측정

---

## 2. Security Requirements (보안 요구사항)

### SR-001: 비밀번호 보안
**Requirement**: 비밀번호 안전한 저장 및 관리

**Implementation**:
- bcrypt 해싱 (cost factor: 12)
- 비밀번호 정책: 최소 8자, 영문 대소문자 + 숫자 + 특수문자 포함
- 평문 비밀번호 로깅 금지

**Validation**:
- 비밀번호 정책 검증 (클라이언트 + 서버)
- 해시 검증 테스트

---

### SR-002: 인증 및 권한 관리
**Requirement**: JWT 기반 인증 및 권한 제어

**Implementation**:
- JWT 토큰 발급 (HS256 알고리즘)
- 토큰 만료 시간: 관리자 8시간, 테이블 24시간
- 토큰 타입별 접근 제어 (admin, table)
- 토큰 저장: LocalStorage (관리자), SessionStorage (고객)

**Validation**:
- 토큰 검증 미들웨어
- 권한 검증 테스트

**Security Note**:
- LocalStorage는 XSS 공격에 취약하지만, 로컬 개발 환경만 사용하므로 MVP 범위에서 허용
- 프로덕션 배포 시 HttpOnly Cookie로 변경 권장

---

### SR-003: CORS 정책
**Requirement**: Cross-Origin Resource Sharing 정책 설정

**Implementation**:
- 개발 환경: 모든 Origin 허용 (개발 편의성)
- 허용 메서드: GET, POST, PUT, PATCH, DELETE
- 허용 헤더: Content-Type, Authorization

**Security Note**:
- 프로덕션 배포 시 특정 Origin만 허용하도록 변경 필요

---

### SR-004: 입력 데이터 검증
**Requirement**: 모든 사용자 입력 데이터 검증

**Implementation**:
- 클라이언트 측 검증 (즉각적인 피드백)
- 서버 측 검증 (보안 및 데이터 무결성)
- FastAPI Pydantic 모델 활용

**Validation Types**:
- 필수 필드 검증
- 데이터 타입 검증
- 형식 검증 (이메일, 전화번호 등)
- 길이 제한 검증
- 비즈니스 규칙 검증

---

## 3. Scalability Requirements (확장성 요구사항)

### SC-001: 데이터 증가 대응
**Requirement**: 데이터 증가에 따른 성능 유지

**Current Scope**: 소규모 (10개 테이블, 일일 주문 100건 미만)

**Implementation**:
- 데이터베이스 인덱스 (Foreign Key + 자주 조회되는 필드)
- 주문 이력 자동 삭제 (1년 후)
- 로그 파일 로테이션 (날짜별)

**Future Considerations**:
- 대규모 확장 시 프로덕션 DB로 마이그레이션 (PostgreSQL, MySQL)
- 캐싱 레이어 추가 (Redis)

---

### SC-002: 동시 사용자 증가 대응
**Requirement**: 동시 사용자 증가 시 성능 유지

**Current Scope**: 10개 테이블 (동시 사용자 10-12명)

**Implementation**:
- 비동기 처리 (FastAPI)
- 연결 풀 관리
- 비관적 잠금 (주문 수정 시)

**Future Considerations**:
- 대규모 확장 시 로드 밸런싱
- 수평 확장 (다중 서버)

---

## 4. Availability Requirements (가용성 요구사항)

### AV-001: 시스템 가동 시간
**Requirement**: 시스템 안정성 및 가동 시간

**Target**: 로컬 개발 환경 (24/7 가동 불필요)

**Implementation**:
- 에러 처리 및 복구
- 로깅 및 모니터링
- 재시작 시 데이터 복구 (하이브리드 DB 전략)

**Error Handling**:
- 모든 API 엔드포인트 에러 처리
- 사용자 친화적 에러 메시지
- 에러 로깅

---

### AV-002: 데이터 영속성
**Requirement**: 모든 데이터의 영속성 보장

**Implementation**: 파일 기반 SQLite 단일 전략

**Persistent Data** (파일 기반 SQLite: `data/app.db`):
- Store (매장 정보)
- Table (테이블 정보)
- Menu (메뉴 정보)
- Order (현재 주문)
- OrderItem (주문 항목)
- OrderHistory (주문 이력)
- Admin credentials (관리자 계정)

**Rationale**:
- 모든 데이터를 파일 기반으로 저장하여 영속성 보장
- 서버 재시작 시에도 모든 데이터 유지
- 단일 DB 연결로 복잡도 감소
- 트랜잭션 관리 단순화
- MVP 범위에서 성능 차이 미미

---

## 5. Maintainability Requirements (유지보수성 요구사항)

### MT-001: 코드 품질
**Requirement**: 높은 코드 품질 유지

**Implementation**:
- 린팅: ESLint (JavaScript/TypeScript), Black + Pylint (Python)
- 코드 포맷팅: Prettier (JS), Black (Python)
- 타입 체킹: TypeScript (Frontend)
- 코드 리뷰 프로세스

**Standards**:
- PEP 8 (Python)
- Airbnb Style Guide (JavaScript)

---

### MT-002: API 문서화
**Requirement**: API 문서 자동 생성 및 유지

**Implementation**:
- FastAPI 자동 API 문서화 (Swagger UI)
- OpenAPI 3.0 스펙 생성
- API 엔드포인트 설명 및 예제

**Access**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

### MT-003: 로깅
**Requirement**: 체계적인 로깅 및 모니터링

**Implementation**:
- Python 내장 logging 모듈
- 로그 레벨: DEBUG, INFO, WARNING, ERROR, CRITICAL
- 로그 파일 관리: 날짜별 파일 (logs/app-2026-02-09.log)

**Log Levels**:
- ERROR: 시스템 오류, 예상치 못한 오류
- WARNING: 비즈니스 규칙 위반, 인증/권한 오류
- INFO: 정상 동작 로그 (API 요청, 주문 생성 등)
- DEBUG: 디버깅 정보 (개발 환경만)

**Log Format**:
```
[2026-02-09 10:00:00] [INFO] [OrderService] Order created: order_id=123, table_id=5
```

---

### MT-004: 테스트 커버리지
**Requirement**: 포괄적인 테스트 커버리지

**Implementation**:
- 단위 테스트: 핵심 비즈니스 로직
- 통합 테스트: API 엔드포인트
- E2E 테스트: 주요 사용자 플로우

**Tools**:
- Backend: pytest (Python)
- Frontend: Jest + React Testing Library

**Target Coverage**: 70% 이상

---

## 6. Usability Requirements (사용성 요구사항)

### US-001: 사용자 인터페이스
**Requirement**: 직관적이고 사용하기 쉬운 UI

**Implementation**:
- 터치 친화적 UI (최소 버튼 크기 44x44px)
- 명확한 시각적 피드백 (로딩, 성공, 에러)
- 반응형 디자인 (태블릿 최적화)
- Tailwind CSS 활용

**Accessibility**:
- 색상 대비 (WCAG AA 기준)
- 키보드 네비게이션 지원

---

### US-002: 에러 메시지
**Requirement**: 사용자 친화적 에러 메시지

**Implementation**:
- 명확하고 이해하기 쉬운 메시지
- 해결 방법 제시
- 기술적 세부사항 숨김

**Examples**:
- ❌ "Database connection failed: SQLSTATE[HY000]"
- ✅ "주문을 처리할 수 없습니다. 잠시 후 다시 시도해주세요."

---

## 7. Reliability Requirements (신뢰성 요구사항)

### RL-001: 에러 복구
**Requirement**: 에러 발생 시 자동 복구 또는 안내

**Implementation**:
- Try-catch 블록으로 에러 처리
- 에러 발생 시 로그 기록
- 사용자에게 에러 메시지 표시
- 재시도 로직 (네트워크 에러)

---

### RL-002: 데이터 무결성
**Requirement**: 데이터 일관성 및 무결성 보장

**Implementation**:
- 데이터베이스 제약사항 (Foreign Key, Unique, Not Null)
- 트랜잭션 관리
- 비관적 잠금 (주문 수정 시)
- 데이터 검증 (클라이언트 + 서버)

---

## 8. Caching Strategy (캐싱 전략)

### CS-001: 메뉴 조회 캐싱
**Requirement**: 메뉴 조회 API 응답 캐싱

**Implementation**:
- 메뉴 조회 API 응답 캐싱 (메모리)
- 캐시 만료 시간: 5분
- 메뉴 변경 시 캐시 무효화

**Rationale**:
- 메뉴는 자주 변경되지 않음
- 조회 빈도가 높음
- 응답 시간 단축

**Cache Invalidation**:
- 메뉴 생성/수정/삭제 시 캐시 삭제

---

## 9. Database Strategy (데이터베이스 전략)

### DS-001: 파일 기반 데이터베이스
**Requirement**: 모든 데이터의 영속성 보장

**Storage** (파일 기반 SQLite: `data/app.db`):
- Store (매장 정보)
- Table (테이블 정보)
- Menu (메뉴 정보)
- Order (현재 주문)
- OrderItem (주문 항목)
- OrderHistory (주문 이력)

**Rationale**:
- 모든 데이터를 파일 기반으로 저장하여 영속성 보장
- 서버 재시작 시에도 모든 데이터 유지
- 단일 DB 연결로 복잡도 감소
- 트랜잭션 관리 단순화
- MVP 범위에서 성능 충분

---

### DS-002: 데이터베이스 인덱스
**Requirement**: 조회 성능 최적화를 위한 인덱스

**Indexed Fields**:

**Store**:
- id (Primary Key)

**Table**:
- id (Primary Key)
- store_id (Foreign Key)
- table_number (자주 조회)

**Menu**:
- id (Primary Key)
- store_id (Foreign Key)
- category_level1 (자주 조회)

**Order**:
- id (Primary Key)
- store_id (Foreign Key)
- table_id (Foreign Key)
- status (자주 조회)

**OrderItem**:
- id (Primary Key)
- order_id (Foreign Key)

**OrderHistory**:
- id (Primary Key)
- store_id (Foreign Key)
- table_id (Foreign Key)

**Rationale**:
- Foreign Key: JOIN 성능 향상
- 자주 조회되는 필드: WHERE 절 성능 향상

---

## 10. Error Handling Strategy (에러 처리 전략)

### EH-001: 에러 응답 형식
**Requirement**: 일관된 에러 응답 형식

**Format**:
```json
{
  "error": {
    "code": "HTTP_STATUS_CODE",
    "message": "사용자 친화적 메시지"
  }
}
```

**HTTP Status Codes**:
- 400: Bad Request (잘못된 요청)
- 401: Unauthorized (인증 실패)
- 403: Forbidden (권한 없음)
- 404: Not Found (리소스 없음)
- 409: Conflict (충돌, 예: 중복 데이터)
- 500: Internal Server Error (서버 오류)

---

### EH-002: 에러 로깅
**Requirement**: 모든 에러 로깅

**Implementation**:
- 에러 발생 시 로그 기록
- 스택 트레이스 포함 (DEBUG 레벨)
- 에러 컨텍스트 정보 (사용자 ID, 요청 URL 등)

---

## NFR Summary

| Category | Key Requirements | Priority |
|----------|------------------|----------|
| Performance | API < 2초, SSE < 2초, 10 users | High |
| Security | bcrypt, JWT, 양방향 검증 | High |
| Scalability | 10 tables, 100 orders/day | Medium |
| Availability | 에러 처리, 하이브리드 DB | High |
| Maintainability | 린팅, API 문서, 로깅 | High |
| Usability | 터치 UI, 명확한 피드백 | High |
| Reliability | 데이터 무결성, 에러 복구 | High |

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
