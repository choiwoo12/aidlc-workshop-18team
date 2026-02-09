# Application Design Plan

## Plan Overview
이 계획은 테이블오더 서비스의 고수준 컴포넌트 식별, 서비스 레이어 설계, 컴포넌트 간 의존성을 정의합니다.

---

## Design Context Analysis

### Key Business Capabilities
1. **고객 주문 관리**: 메뉴 조회, 장바구니, 주문 생성/조회
2. **관리자 운영 관리**: 실시간 주문 모니터링, 테이블 관리, 메뉴 관리
3. **인증 및 세션 관리**: 테이블 자동 로그인, 관리자 인증, 세션 추적
4. **실시간 통신**: Server-Sent Events를 통한 주문 업데이트

### Functional Areas
- **Customer Interface**: 고객용 웹 UI (React)
- **Admin Interface**: 관리자용 웹 UI (React)
- **Backend API**: REST API 서버 (Python)
- **Real-time Communication**: SSE 엔드포인트
- **Data Layer**: 인메모리 데이터베이스

---

## Application Design Questions

다음 질문들에 답변하여 Application Design 방향을 결정해주세요.

### Question 1: Component Organization Approach
프론트엔드 컴포넌트를 어떻게 구조화할까요?

A) Feature-based (기능별로 그룹화: menu/, cart/, order/)
B) Layer-based (레이어별로 그룹화: components/, services/, utils/)
C) Hybrid (기능별 + 공통 컴포넌트 분리)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 2: Backend API Architecture
백엔드 API 아키텍처 스타일은?

A) Layered Architecture (Controller → Service → Repository)
B) Clean Architecture (Domain-centric with adapters)
C) Simple MVC (Model-View-Controller)
D) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 3: State Management (Frontend)
프론트엔드 상태 관리 방식은?

A) React Context API only
B) Redux or similar state management library
C) Component local state + Context for global state
D) Other (please describe after [Answer]: tag below)

[Answer]: 추천해줘

### Question 4: API Communication Pattern
프론트엔드와 백엔드 간 통신 패턴은?

A) Direct API calls from components
B) Service layer abstraction (API service classes)
C) Custom hooks for API calls
D) Hybrid (service layer + custom hooks)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 5: Authentication Flow
인증 처리 방식은?

A) Centralized auth service/module
B) Auth middleware/interceptor
C) Per-component auth handling
D) Hybrid (centralized + middleware)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 6: Real-time Communication (SSE) Integration
SSE 실시간 통신을 어떻게 통합할까요?

A) Dedicated SSE service/module
B) Integrated into existing API service
C) Custom hook for SSE connection
D) Hybrid (service + hook)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 7: Error Handling Strategy
에러 처리 전략은?

A) Centralized error handler
B) Per-component error handling
C) Error boundary + centralized handler
D) Other (please describe after [Answer]: tag below)

[Answer]: B

### Question 8: Data Validation
데이터 유효성 검증 위치는?

A) Frontend only
B) Backend only
C) Both frontend and backend
D) Other (please describe after [Answer]: tag below)

[Answer]: C

### Question 9: Image Upload Handling
이미지 업로드 처리 방식은?

A) Direct upload to backend API
B) Separate file upload service
C) Base64 encoding in API request
D) Other (please describe after [Answer]: tag below)

[Answer]: A

### Question 10: Database Access Pattern
데이터베이스 접근 패턴은?

A) Direct database queries in API handlers
B) Repository pattern (data access layer)
C) ORM/ODM (SQLAlchemy, etc.)
D) Hybrid (ORM + repository pattern)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Application Design Execution Plan

답변을 기반으로 다음 단계를 순차적으로 실행합니다:

### Phase 1: Component Identification
- [x] Step 1.1: 프론트엔드 컴포넌트 식별
  - [x] 고객 UI 컴포넌트 (메뉴, 장바구니, 주문)
  - [x] 관리자 UI 컴포넌트 (대시보드, 테이블 관리, 메뉴 관리)
  - [x] 공통 컴포넌트 (인증, 에러 처리, 로딩)
- [x] Step 1.2: 백엔드 컴포넌트 식별
  - [x] API 엔드포인트 컴포넌트
  - [x] 비즈니스 로직 컴포넌트
  - [x] 데이터 접근 컴포넌트
- [x] Step 1.3: components.md 파일 생성

### Phase 2: Component Methods Definition
- [x] Step 2.1: 각 컴포넌트의 주요 메서드 식별
- [x] Step 2.2: 메서드 시그니처 정의 (입력/출력 타입)
- [x] Step 2.3: 메서드 목적 및 책임 명시
- [x] Step 2.4: component-methods.md 파일 생성

### Phase 3: Service Layer Design
- [x] Step 3.1: 서비스 레이어 식별
  - [x] 인증 서비스
  - [x] 주문 서비스
  - [x] 메뉴 서비스
  - [x] 실시간 통신 서비스
- [x] Step 3.2: 서비스 책임 및 오케스트레이션 정의
- [x] Step 3.3: services.md 파일 생성

### Phase 4: Component Dependencies
- [x] Step 4.1: 컴포넌트 간 의존성 매트릭스 생성
- [x] Step 4.2: 통신 패턴 정의 (REST, SSE, 내부 호출)
- [x] Step 4.3: 데이터 흐름 다이어그램 생성
- [x] Step 4.4: component-dependency.md 파일 생성

### Phase 5: Design Validation
- [x] Step 5.1: 설계 완전성 검증
  - [x] 모든 User Stories가 컴포넌트에 매핑되는지 확인
  - [x] 순환 의존성 확인
  - [x] 단일 책임 원칙 준수 확인
- [x] Step 5.2: 설계 일관성 검증
- [x] Step 5.3: 최종 검토 및 완성도 확인

---

**답변 완료 후 "완료했습니다" 또는 "done"이라고 알려주세요.**
