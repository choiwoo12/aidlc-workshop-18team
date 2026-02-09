# Unit of Work Plan - 테이블오더 서비스

## Plan Overview
테이블오더 서비스를 관리 가능한 작업 단위(Unit of Work)로 분해합니다. 각 유닛은 독립적으로 개발 및 테스트 가능한 논리적 그룹입니다.

---

## Decomposition Methodology

### 1. Unit Identification
- [x] 시스템 아키텍처 분석 (프론트엔드, 백엔드, 공통)
- [x] 기능 영역별 그룹화
- [x] 각 유닛의 책임 및 경계 정의
- [x] 유닛 간 의존성 식별

### 2. Story Mapping
- [x] 각 User Story를 유닛에 매핑
- [x] 유닛별 스토리 개수 확인
- [x] 크로스 유닛 스토리 식별 및 처리

### 3. Dependency Analysis
- [x] 유닛 간 의존성 매트릭스 생성
- [x] 통합 포인트 식별
- [x] 개발 순서 결정

### 4. Code Organization Strategy (Greenfield)
- [x] 프로젝트 디렉토리 구조 정의
- [x] 배포 모델 결정
- [x] 빌드 및 패키징 전략 정의

### 5. Validation
- [x] 모든 스토리가 유닛에 할당되었는지 확인
- [x] 유닛 크기가 적절한지 검증
- [x] 순환 의존성 확인

---

## Context-Appropriate Questions

다음 질문들에 답변해주시면 더 정확한 유닛 분해를 생성할 수 있습니다.

### Q1: 시스템 분해 전략
시스템을 어떻게 분해할까요?

A) **Monolithic** - 단일 애플리케이션 (프론트엔드 + 백엔드 통합)
B) **Separated Frontend/Backend** - 프론트엔드와 백엔드를 별도 유닛으로 분리
C) **Multi-Frontend** - 고객용 프론트엔드, 관리자용 프론트엔드, 백엔드로 분리
D) **Microservices** - 기능별로 독립적인 서비스로 분리

[Answer]: C

**Reasoning**: 시스템 분해 전략은 개발, 배포, 유지보수 방식에 영향을 줍니다.

---

### Q2: 프론트엔드 분리 전략 (Q1에서 B, C, D 선택 시)
프론트엔드를 어떻게 구성할까요?

A) **Single SPA** - 고객용과 관리자용을 하나의 React 앱에 통합
B) **Separate Apps** - 고객용과 관리자용을 완전히 별도 React 앱으로 분리
C) **Monorepo** - 하나의 저장소에 여러 앱을 관리 (Nx, Turborepo 등)

[Answer]: B

**Reasoning**: 프론트엔드 구성은 코드 공유와 배포 전략에 영향을 줍니다.

---

### Q3: 백엔드 모듈 분리 (Monolithic 선택 시)
백엔드를 논리적 모듈로 분리할까요?

A) **No Modules** - 단일 Spring Boot 애플리케이션, 패키지로만 구분
B) **Logical Modules** - 패키지 구조로 모듈 분리 (order, menu, table 등)
C) **Maven/Gradle Modules** - 빌드 도구의 멀티 모듈 프로젝트

[Answer]: B

**Reasoning**: 모듈 분리는 코드 조직과 빌드 전략에 영향을 줍니다.

---

### Q4: 유닛 크기 기준
각 유닛의 크기를 어떻게 결정할까요?

A) **Small Units** - 기능별로 세분화 (주문 생성, 주문 조회, 메뉴 관리 등 각각 별도)
B) **Medium Units** - 도메인별로 그룹화 (주문 관리, 메뉴 관리, 테이블 관리)
C) **Large Units** - 레이어별로 그룹화 (프론트엔드, 백엔드)
D) **Story-Based** - User Story 개수 기준 (10-15개 스토리당 1개 유닛)

[Answer]: B

**Reasoning**: 유닛 크기는 개발 속도와 통합 복잡도에 영향을 줍니다.

---

### Q5: 공통 컴포넌트 처리
공통 컴포넌트(인증, SSE, 파일 관리 등)를 어떻게 처리할까요?

A) **Embedded** - 각 유닛에 포함
B) **Shared Module** - 별도 공통 모듈로 분리
C) **Utility Library** - 독립적인 라이브러리로 관리
D) **No Separation** - 공통 컴포넌트 개념 없이 필요한 곳에 구현

[Answer]: B

**Reasoning**: 공통 컴포넌트 처리는 코드 재사용과 의존성 관리에 영향을 줍니다.

---

### Q6: 개발 순서 우선순위
유닛 개발 순서를 어떻게 결정할까요?

A) **Dependency-First** - 의존성이 없는 유닛부터 개발 (Bottom-Up)
B) **User-Journey-First** - 사용자 여정 순서대로 개발 (고객 → 관리자)
C) **Risk-First** - 기술적 리스크가 높은 유닛부터 개발
D) **Value-First** - 비즈니스 가치가 높은 유닛부터 개발

[Answer]: B

**Reasoning**: 개발 순서는 프로젝트 리스크와 가치 전달 시점에 영향을 줍니다.

---

### Q7: 통합 테스트 전략
유닛 간 통합을 어떻게 테스트할까요?

A) **Per-Unit Integration** - 각 유닛 개발 완료 시마다 통합 테스트
B) **Incremental Integration** - 유닛을 하나씩 추가하며 통합 테스트
C) **Big Bang Integration** - 모든 유닛 완료 후 한 번에 통합 테스트
D) **Continuous Integration** - CI/CD 파이프라인에서 자동 통합 테스트

[Answer]: B

**Reasoning**: 통합 테스트 전략은 버그 발견 시점과 수정 비용에 영향을 줍니다.

---

### Q8: 데이터베이스 스키마 관리
데이터베이스 스키마를 어떻게 관리할까요?

A) **Single Schema** - 모든 유닛이 하나의 스키마 공유
B) **Schema per Domain** - 도메인별로 스키마 분리 (order, menu, table)
C) **Schema per Unit** - 각 유닛이 독립적인 스키마 사용
D) **No Schema** - In-Memory DB 특성상 스키마 관리 불필요

[Answer]: D

**Reasoning**: 스키마 관리 전략은 데이터 격리와 마이그레이션에 영향을 줍니다.

---

### Q9: 배포 전략 (Greenfield)
애플리케이션을 어떻게 배포할까요?

A) **Single Deployment** - 모든 유닛을 하나의 패키지로 배포
B) **Separate Deployments** - 프론트엔드와 백엔드를 별도 배포
C) **Multi-Container** - Docker 컨테이너로 각 유닛 배포
D) **JAR Files** - 각 유닛을 별도 JAR 파일로 배포

[Answer]: B

**Reasoning**: 배포 전략은 인프라 구성과 운영 복잡도에 영향을 줍니다.

---

### Q10: 프로젝트 디렉토리 구조 (Greenfield)
프로젝트 디렉토리를 어떻게 구성할까요?

A) **Flat Structure** - 모든 코드를 하나의 루트 디렉토리에 배치
B) **Layered Structure** - frontend/, backend/ 디렉토리로 분리
C) **Domain Structure** - 도메인별 디렉토리 (order/, menu/, table/)
D) **Monorepo Structure** - packages/ 또는 apps/ 아래 각 유닛 배치

[Answer]: B

**Reasoning**: 디렉토리 구조는 코드 탐색과 빌드 설정에 영향을 줍니다.

---

## Mandatory Unit Artifacts

### 1. unit-of-work.md
- [x] 모든 유닛 정의 및 책임
- [x] 각 유닛의 경계 및 인터페이스
- [x] 유닛별 기술 스택
- [x] 코드 조직 전략 (Greenfield)

### 2. unit-of-work-dependency.md
- [x] 유닛 간 의존성 매트릭스
- [x] 통합 포인트 정의
- [x] 개발 순서 권장사항

### 3. unit-of-work-story-map.md
- [x] User Story를 유닛에 매핑
- [x] 유닛별 스토리 개수
- [x] 크로스 유닛 스토리 처리 방안

---

## Decomposition Principles

유닛 분해 시 다음 원칙을 준수합니다:

- **High Cohesion**: 관련 기능은 같은 유닛에 응집
- **Loose Coupling**: 유닛 간 결합도 최소화
- **Clear Boundaries**: 유닛 경계가 명확하고 이해하기 쉬움
- **Independent Development**: 각 유닛을 독립적으로 개발 가능
- **Testability**: 각 유닛을 독립적으로 테스트 가능

---

## Next Steps After Plan Approval

1. 사용자가 모든 [Answer]: 태그를 채움
2. AI가 답변을 분석하고 모호한 부분 확인
3. 필요시 추가 질문으로 명확화
4. 사용자가 계획 승인
5. 승인된 계획에 따라 유닛 아티팩트 생성 시작

---

**참고**: 이 계획은 사용자의 답변에 따라 조정될 수 있습니다. 모든 질문에 답변해주시면 최적의 유닛 분해를 생성할 수 있습니다.
