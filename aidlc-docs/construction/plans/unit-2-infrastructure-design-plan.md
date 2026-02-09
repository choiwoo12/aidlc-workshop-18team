# Infrastructure Design Plan - Unit 2: Customer Order Domain

## Overview

Unit 2의 논리적 컴포넌트를 실제 인프라 서비스와 매핑하는 계획입니다. Unit 1의 인프라를 재사용하므로 추가 인프라 구성이 불필요합니다.

---

## Execution Plan

### Phase 1: Design Artifacts Analysis
- [x] Functional Design 문서 분석 완료
- [x] NFR Design 문서 분석 완료
- [x] 논리적 컴포넌트 식별 완료

### Phase 2: Infrastructure Mapping
- [x] Unit 1 인프라 재사용 확인
- [x] 추가 인프라 요구사항 분석
- [x] 컴포넌트별 인프라 매핑

### Phase 3: Deployment Architecture
- [x] Unit 1 배포 아키텍처 재사용 확인
- [x] 추가 배포 구성 불필요 확인

### Phase 4: Documentation
- [x] Infrastructure Design 문서 생성

---

## Context Analysis

**프로젝트 특성**:
- Unit 1의 인프라를 그대로 재사용
- 추가 인프라 서비스 불필요
- 동일한 Docker Compose 환경 사용

**Unit 2 논리적 컴포넌트** (NFR Design에서 정의됨):

**Frontend**:
1. SSE Connection Manager → 브라우저 EventSource API (인프라 불필요)
2. Cart Manager → SessionStorage (브라우저 내장)
3. Order Manager → 애플리케이션 레벨
4. Menu Manager → 애플리케이션 레벨
5. Validation Service → 애플리케이션 레벨
6. Error Handler → 애플리케이션 레벨

**Backend**:
1. SSE Service → FastAPI StreamingResponse (인프라 불필요)
2. Order Service → 애플리케이션 레벨
3. Menu Service → 애플리케이션 레벨
4. Validation Service → 애플리케이션 레벨
5. Order Number Generator → 애플리케이션 레벨

**Unit 1 인프라 재사용**:
- Database: SQLite 파일 기반 (Unit 1)
- File Storage: 로컬 파일 시스템 (Unit 1)
- Logging: 로컬 파일 시스템 (Unit 1)
- Cache: 인메모리 (Unit 1)
- Authentication: JWT (Unit 1)
- Deployment: Docker Compose (Unit 1)

---

## Infrastructure Mapping Summary

Unit 2의 모든 컴포넌트는 다음과 같이 매핑됩니다:

| Component | Infrastructure | Notes |
|-----------|---------------|-------|
| SSE Connection Manager | Browser EventSource API | 브라우저 내장 |
| Cart Manager | SessionStorage | 브라우저 내장 |
| Order Manager | Application Level | 인프라 불필요 |
| Menu Manager | Application Level | 인프라 불필요 |
| Validation Service (FE) | Application Level | 인프라 불필요 |
| Error Handler | Application Level | 인프라 불필요 |
| SSE Service | FastAPI StreamingResponse | FastAPI 내장 |
| Order Service | Application Level | Unit 1 Repository 사용 |
| Menu Service | Application Level | Unit 1 Repository 사용 |
| Validation Service (BE) | Application Level | Unit 1 Repository 사용 |
| Order Number Generator | Application Level | Unit 1 Repository 사용 |

**결론**: Unit 2는 Unit 1의 인프라를 100% 재사용하며, 추가 인프라 구성이 불필요합니다.

---

## Next Steps

Unit 2는 Unit 1의 인프라를 재사용하므로 별도의 질문이 필요 없습니다. Infrastructure Design 아티팩트를 바로 생성합니다.

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
