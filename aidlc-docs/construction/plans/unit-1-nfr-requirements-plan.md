# NFR Requirements Plan - Unit 1: Shared Foundation

## Overview

**Unit**: Unit 1 - Shared Foundation  
**Purpose**: 공통 인프라, 엔티티, 유틸리티 제공  
**Scope**: Unit 1의 비기능 요구사항 및 기술 스택 결정

**Note**: Requirements Analysis에서 이미 많은 기술 스택이 결정되었습니다. 이 단계에서는 Unit 1에 특화된 NFR과 구체적인 기술 선택을 확정합니다.

---

## Already Decided (from Requirements Analysis)

### Backend
- Language: Python
- Framework: FastAPI, Django, 또는 Flask 중 선택
- Database: 인메모리 (SQLite 또는 Redis)
- Authentication: JWT
- Password Hashing: bcrypt
- Real-time: Server-Sent Events (SSE)

### Frontend
- Framework: React
- State Management: Context API (결정됨)
- HTTP Client: Axios 또는 Fetch API
- Storage: SessionStorage (customer), LocalStorage (admin)

### Development
- Containerization: Docker Compose
- Version Control: Git (GitHub Flow)
- API Documentation: Swagger/OpenAPI
- Linting: ESLint (JS), Pylint/Black (Python)

### NFR Targets
- Order creation response: < 2초
- Menu query response: < 1초
- Real-time update delay: < 2초
- Concurrent users: 10 tables

---

## Execution Steps

### Step 1: Backend Framework Selection
[x] Python 프레임워크 선택 (FastAPI vs Django vs Flask)
[x] ORM 선택 (SQLAlchemy vs Django ORM vs Peewee)
[x] 선택 근거 문서화

### Step 2: Database Technology Selection
[x] 인메모리 DB 선택 (SQLite vs Redis)
[x] 데이터 영속성 전략 결정
[x] 선택 근거 문서화

### Step 3: Frontend Technology Details
[x] HTTP 클라이언트 선택 (Axios vs Fetch API)
[x] Styling 방식 선택 (CSS Modules vs Styled Components vs Tailwind CSS)
[x] 선택 근거 문서화

### Step 4: Security Implementation Details
[x] JWT 라이브러리 선택
[x] bcrypt 라이브러리 선택
[x] 토큰 저장 및 관리 전략 확정
[x] CORS 정책 결정

### Step 5: File Storage Strategy
[x] 이미지 저장 방식 결정 (로컬 파일 시스템 vs 메모리)
[x] 파일 경로 구조 설계
[x] 파일 크기 제한 확정

### Step 6: Logging Strategy
[x] 로깅 라이브러리 선택
[x] 로그 레벨 정책 결정
[x] 로그 파일 관리 전략 (rotation, retention)

### Step 7: Error Handling Strategy
[x] 에러 응답 형식 표준화
[x] 에러 코드 체계 설계
[x] 클라이언트 에러 처리 전략

### Step 8: Performance Optimization
[x] 데이터베이스 인덱스 전략
[x] API 응답 캐싱 전략 (필요 시)
[x] 프론트엔드 최적화 전략

---

## Clarification Questions

다음 질문들에 답변하여 Unit 1의 NFR 요구사항과 기술 스택을 확정해주세요.

### Q1: Python 프레임워크 선택
Unit 1의 백엔드 프레임워크로 어떤 것을 사용할까요?

A) FastAPI (비동기, 빠름, 자동 API 문서화)
B) Django (풍부한 기능, ORM 내장, Admin 패널)
C) Flask (경량, 유연함, 간단함)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 프레임워크 선택은 개발 속도, 성능, 유지보수성에 영향을 미칩니다.

---

### Q2: 인메모리 데이터베이스 선택
어떤 인메모리 데이터베이스를 사용할까요?

A) SQLite (파일 기반, SQL, 관계형)
B) Redis (메모리 기반, Key-Value, 빠름)
C) SQLite in-memory mode (완전 메모리, 재시작 시 데이터 손실)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: C

**Rationale**: 데이터베이스 선택은 데이터 영속성, 성능, 쿼리 복잡도에 영향을 미칩니다.

---

### Q3: ORM (Object-Relational Mapping) 선택
데이터베이스 ORM으로 어떤 것을 사용할까요?

A) SQLAlchemy (강력함, 유연함, 프레임워크 독립적)
B) Django ORM (Django 전용, 간단함)
C) Peewee (경량, 간단함)
D) ORM 없이 Raw SQL
E) Other (설명해주세요)

[Answer]: A

**Rationale**: ORM 선택은 개발 생산성과 쿼리 성능에 영향을 미칩니다.

---

### Q4: HTTP 클라이언트 선택 (Frontend)
프론트엔드에서 API 호출 시 어떤 HTTP 클라이언트를 사용할까요?

A) Axios (풍부한 기능, 인터셉터, 자동 JSON 변환)
B) Fetch API (브라우저 내장, 가벼움)
C) 둘 다 사용 (Axios for complex, Fetch for simple)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: HTTP 클라이언트 선택은 개발 편의성과 번들 크기에 영향을 미칩니다.

---

### Q5: CSS 스타일링 방식
프론트엔드 스타일링 방식으로 어떤 것을 사용할까요?

A) CSS Modules (스코프 CSS, 간단함)
B) Styled Components (CSS-in-JS, 동적 스타일링)
C) Tailwind CSS (유틸리티 클래스, 빠른 개발)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: C

**Rationale**: 스타일링 방식은 개발 속도, 유지보수성, 번들 크기에 영향을 미칩니다.

---

### Q6: 이미지 저장 방식
메뉴 이미지를 어떻게 저장할까요?

A) 로컬 파일 시스템 (uploads/ 디렉토리)
B) 메모리 (Base64 인코딩, DB 저장)
C) 추천해줘
D) Other (설명해주세요)

[Answer]: A

**Rationale**: 이미지 저장 방식은 성능, 확장성, 관리 편의성에 영향을 미칩니다.

---

### Q7: 로깅 라이브러리
로깅에 어떤 라이브러리를 사용할까요?

A) Python 내장 logging 모듈
B) Loguru (간단하고 강력함)
C) structlog (구조화된 로깅)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 로깅 라이브러리 선택은 로그 관리 및 디버깅 효율성에 영향을 미칩니다.

---

### Q8: 로그 파일 관리
로그 파일을 어떻게 관리할까요?

A) 단일 파일 (logs/app.log)
B) 날짜별 파일 (logs/app-2026-02-09.log)
C) 크기별 로테이션 (10MB마다 새 파일)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: B

**Rationale**: 로그 파일 관리 방식은 디스크 사용량과 로그 분석 편의성에 영향을 미칩니다.

---

### Q9: CORS (Cross-Origin Resource Sharing) 정책
CORS 정책을 어떻게 설정할까요?

A) 모든 Origin 허용 (개발 편의성)
B) 특정 Origin만 허용 (보안 강화)
C) 추천해줘
D) Other (설명해주세요)

[Answer]: A

**Rationale**: CORS 정책은 보안과 개발 편의성의 균형에 영향을 미칩니다.

---

### Q10: 데이터베이스 인덱스 전략
어떤 필드에 인덱스를 생성할까요?

A) Primary Key만 (최소한)
B) Foreign Key + 자주 조회되는 필드 (균형)
C) 모든 조회 필드 (성능 최우선)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 인덱스 전략은 조회 성능과 쓰기 성능의 균형에 영향을 미칩니다.

---

### Q11: API 응답 캐싱
API 응답을 캐싱할까요?

A) 캐싱 없음 (단순함)
B) 메뉴 조회만 캐싱 (자주 변경되지 않음)
C) 모든 GET 요청 캐싱 (성능 최우선)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: B

**Rationale**: 캐싱 전략은 성능과 데이터 일관성의 균형에 영향을 미칩니다.

---

### Q12: 프론트엔드 번들 최적화
프론트엔드 번들을 어떻게 최적화할까요?

A) 최적화 없음 (개발 속도 우선)
B) 기본 최적화 (Code splitting, Tree shaking)
C) 고급 최적화 (Lazy loading, Dynamic imports)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 번들 최적화는 초기 로딩 속도와 개발 복잡도에 영향을 미칩니다.

---

### Q13: 에러 코드 체계
에러 코드를 어떻게 설계할까요?

A) HTTP 상태 코드만 사용 (간단함)
B) HTTP + 커스텀 에러 코드 (예: ERR_001)
C) 추천해줘
D) Other (설명해주세요)

[Answer]: A

**Rationale**: 에러 코드 체계는 에러 추적 및 디버깅 효율성에 영향을 미칩니다.

---

### Q14: JWT 토큰 저장 위치 (Frontend)
JWT 토큰을 어디에 저장할까요?

A) LocalStorage (간단함, XSS 취약)
B) HttpOnly Cookie (XSS 방어, CSRF 취약)
C) Memory only (가장 안전, 새로고침 시 로그아웃)
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 토큰 저장 위치는 보안과 사용자 경험의 균형에 영향을 미칩니다.

---

### Q15: 비밀번호 정책 구체화
비밀번호 정책을 어떻게 구체화할까요?

A) 최소 8자, 영문+숫자+특수문자 (Functional Design에서 결정됨)
B) 최소 10자, 영문+숫자+특수문자
C) 최소 12자, 영문+숫자+특수문자 + 대소문자 구분
D) 추천해줘
E) Other (설명해주세요)

[Answer]: A

**Rationale**: 비밀번호 정책은 보안 수준과 사용자 편의성에 영향을 미칩니다.

---

## Next Steps

1. 모든 질문에 [Answer]: 태그로 답변해주세요
2. 답변 완료 후 "완료했습니다"라고 알려주세요
3. AI가 답변을 분석하고 모호한 부분이 있으면 추가 질문을 드립니다
4. 모든 답변이 명확해지면 NFR Requirements 아티팩트를 생성합니다

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 질문 대기중
