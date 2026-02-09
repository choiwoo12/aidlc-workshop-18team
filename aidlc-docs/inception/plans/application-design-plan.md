# Application Design Plan - 테이블오더 서비스

## Plan Overview
테이블오더 서비스의 애플리케이션 아키텍처를 설계합니다. 주요 컴포넌트, 서비스 계층, 컴포넌트 간 의존성을 정의합니다.

---

## Design Methodology

### 1. Component Identification
- [x] 프론트엔드 컴포넌트 식별 (고객용, 관리자용)
- [x] 백엔드 컴포넌트 식별 (API, 비즈니스 로직, 데이터 액세스)
- [x] 공통 컴포넌트 식별 (인증, 세션 관리, 실시간 통신)
- [x] 각 컴포넌트의 책임 정의

### 2. Component Methods Definition
- [x] 각 컴포넌트의 주요 메서드 시그니처 정의
- [x] 메서드의 입력/출력 타입 정의
- [x] 메서드의 고수준 목적 정의
- [x] 비즈니스 규칙은 Functional Design에서 상세화 예정

### 3. Service Layer Design
- [x] 서비스 계층 식별 (주문 서비스, 메뉴 서비스, 테이블 서비스 등)
- [x] 서비스 간 오케스트레이션 패턴 정의
- [x] 서비스 책임 및 경계 정의

### 4. Component Dependency Analysis
- [x] 컴포넌트 간 의존성 매트릭스 생성
- [x] 통신 패턴 정의 (REST API, SSE, 로컬 스토리지)
- [x] 데이터 흐름 다이어그램 생성

### 5. Design Validation
- [x] 모든 User Stories가 컴포넌트에 매핑되는지 확인
- [x] 컴포넌트 간 순환 의존성 확인
- [x] 설계 일관성 검증

---

## Context-Appropriate Questions

다음 질문들에 답변해주시면 더 정확한 애플리케이션 설계를 생성할 수 있습니다.

### Q1: 프론트엔드 아키텍처 패턴
React 프론트엔드의 아키텍처 패턴을 어떻게 구성할까요?

A) **Component-Based** - 기능별 컴포넌트 구성 (MenuList, Cart, OrderHistory 등)
B) **Feature-Based** - 기능 모듈별 구성 (customer/, admin/, common/)
C) **Atomic Design** - Atoms, Molecules, Organisms, Templates, Pages 계층
D) **Hybrid** - 기능 모듈 + 컴포넌트 계층 혼합

[Answer]: C

**Reasoning**: 프론트엔드 구조는 코드 조직과 유지보수성에 영향을 줍니다.

---

### Q2: 백엔드 레이어 구조
Spring Boot 백엔드의 레이어 구조를 어떻게 설계할까요?

A) **3-Layer** - Controller, Service, Repository
B) **4-Layer** - Controller, Service, Domain, Repository
C) **Hexagonal** - Ports and Adapters (Domain 중심)
D) **Clean Architecture** - Entities, Use Cases, Interface Adapters, Frameworks

[Answer]:  A

**Reasoning**: 레이어 구조는 비즈니스 로직 분리와 테스트 용이성에 영향을 줍니다.

---

### Q3: 상태 관리 전략
React 프론트엔드의 상태 관리를 어떻게 할까요?

A) **React Context API** - 내장 Context API 사용
B) **Redux** - 중앙 집중식 상태 관리
C) **Zustand** - 경량 상태 관리 라이브러리
D) **React Query + Local State** - 서버 상태는 React Query, 로컬 상태는 useState

[Answer]: C

**Reasoning**: 상태 관리 전략은 데이터 흐름과 컴포넌트 간 통신에 영향을 줍니다.

---

### Q4: API 통신 패턴
프론트엔드와 백엔드 간 API 통신을 어떻게 구성할까요?

A) **Axios** - HTTP 클라이언트 라이브러리 직접 사용
B) **Fetch API** - 브라우저 내장 Fetch API 사용
C) **React Query** - 서버 상태 관리 및 캐싱 포함
D) **Custom API Client** - Axios/Fetch 기반 커스텀 클라이언트

[Answer]: A

**Reasoning**: API 통신 패턴은 에러 처리, 캐싱, 재시도 로직에 영향을 줍니다.

---

### Q5: 실시간 통신 (SSE) 구현
SSE(Server-Sent Events) 실시간 통신을 어떻게 구현할까요?

A) **Native EventSource** - 브라우저 내장 EventSource API 직접 사용
B) **Custom SSE Client** - EventSource 래핑하여 재연결 로직 추가
C) **Library-Based** - SSE 라이브러리 사용 (예: sse.js)
D) **WebSocket Fallback** - SSE 실패 시 WebSocket으로 폴백

[Answer]: C

**Reasoning**: SSE 구현 방식은 연결 안정성과 에러 처리에 영향을 줍니다.

---

### Q6: 인증 및 세션 관리
인증 토큰 및 세션 정보를 어디에 저장할까요?

A) **localStorage** - 브라우저 로컬 스토리지
B) **sessionStorage** - 브라우저 세션 스토리지
C) **Cookie (HttpOnly)** - 서버에서 설정하는 HttpOnly 쿠키
D) **Memory + Refresh Token** - 메모리에 액세스 토큰, 쿠키에 리프레시 토큰

[Answer]: A

**Reasoning**: 토큰 저장 방식은 보안과 세션 지속성에 영향을 줍니다.

---

### Q7: 데이터 액세스 레이어
백엔드의 데이터 액세스를 어떻게 구현할까요?

A) **Spring Data JPA** - JPA 기반 Repository 패턴
B) **JDBC Template** - 직접 SQL 작성 및 실행
C) **MyBatis** - SQL 매퍼 프레임워크
D) **Hybrid** - 복잡한 쿼리는 JDBC/MyBatis, 단순 CRUD는 JPA

[Answer]: C

**Reasoning**: 데이터 액세스 방식은 쿼리 성능과 유지보수성에 영향을 줍니다.

---

### Q8: 파일 업로드 처리
메뉴 이미지 업로드를 어떻게 처리할까요?

A) **Direct Upload** - 프론트엔드에서 백엔드로 직접 업로드
B) **Multipart Form Data** - Spring MultipartFile로 처리
C) **Base64 Encoding** - 이미지를 Base64로 인코딩하여 JSON으로 전송
D) **Presigned URL** - 향후 S3 등 클라우드 스토리지 사용 시 대비

[Answer]: B

**Reasoning**: 파일 업로드 방식은 성능과 확장성에 영향을 줍니다.

---

### Q9: 에러 처리 전략
애플리케이션 전반의 에러 처리를 어떻게 할까요?

A) **Global Error Handler** - 백엔드에 @ControllerAdvice, 프론트엔드에 Error Boundary
B) **Try-Catch per Method** - 각 메서드에서 개별적으로 에러 처리
C) **Error Response DTO** - 표준화된 에러 응답 형식 정의
D) **Hybrid** - Global Handler + 특정 케이스는 개별 처리

[Answer]: A

**Reasoning**: 에러 처리 전략은 사용자 경험과 디버깅 용이성에 영향을 줍니다.

---

### Q10: 컴포넌트 간 통신 패턴
프론트엔드 컴포넌트 간 통신을 어떻게 할까요?

A) **Props Drilling** - 부모에서 자식으로 props 전달
B) **Context API** - Context를 통한 전역 상태 공유
C) **Event Bus** - 커스텀 이벤트 버스 패턴
D) **State Management Library** - Redux/Zustand 등을 통한 중앙 관리

[Answer]: B

**Reasoning**: 컴포넌트 간 통신 패턴은 코드 복잡도와 유지보수성에 영향을 줍니다.

---

## Mandatory Design Artifacts

### 1. components.md
- [x] 모든 주요 컴포넌트 식별 및 정의
- [x] 각 컴포넌트의 책임 명시
- [x] 컴포넌트 인터페이스 정의

### 2. component-methods.md
- [x] 각 컴포넌트의 메서드 시그니처 정의
- [x] 메서드의 입력/출력 타입 명시
- [x] 메서드의 고수준 목적 설명
- [x] 비즈니스 규칙은 Functional Design에서 상세화 예정

### 3. services.md
- [x] 서비스 계층 정의
- [x] 서비스 책임 및 오케스트레이션 패턴
- [x] 서비스 간 상호작용 정의

### 4. component-dependency.md
- [x] 컴포넌트 간 의존성 매트릭스
- [x] 통신 패턴 및 프로토콜
- [x] 데이터 흐름 다이어그램

---

## Design Principles

설계 시 다음 원칙을 준수합니다:

- **Single Responsibility**: 각 컴포넌트는 하나의 명확한 책임
- **Separation of Concerns**: UI, 비즈니스 로직, 데이터 액세스 분리
- **Dependency Inversion**: 고수준 모듈이 저수준 모듈에 의존하지 않음
- **Interface Segregation**: 클라이언트는 사용하지 않는 인터페이스에 의존하지 않음
- **DRY (Don't Repeat Yourself)**: 코드 중복 최소화

---

## Next Steps After Plan Approval

1. 사용자가 모든 [Answer]: 태그를 채움
2. AI가 답변을 분석하고 모호한 부분 확인
3. 필요시 추가 질문으로 명확화
4. 사용자가 계획 승인
5. 승인된 계획에 따라 설계 문서 생성 시작

---

**참고**: 이 계획은 사용자의 답변에 따라 조정될 수 있습니다. 모든 질문에 답변해주시면 최적의 애플리케이션 설계를 생성할 수 있습니다.
