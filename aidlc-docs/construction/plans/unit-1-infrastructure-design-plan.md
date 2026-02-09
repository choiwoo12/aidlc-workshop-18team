# Infrastructure Design Plan - Unit 1: Shared Foundation

## Overview

Unit 1의 논리적 컴포넌트를 실제 인프라 서비스와 매핑하는 계획입니다.

---

## Execution Plan

### Phase 1: Design Artifacts Analysis
- [x] Functional Design 문서 분석 완료
- [x] NFR Design 문서 분석 완료
- [x] 논리적 컴포넌트 식별 완료

### Phase 2: Infrastructure Mapping
- [x] 데이터베이스 인프라 매핑
- [x] 파일 저장소 인프라 매핑
- [x] 로깅 인프라 매핑
- [x] 컨테이너화 전략 정의

### Phase 3: Deployment Architecture
- [x] 로컬 개발 환경 아키텍처 정의
- [x] Docker Compose 구성 정의
- [x] 네트워크 구성 정의
- [x] 볼륨 마운트 전략 정의

### Phase 4: Documentation
- [x] Infrastructure Design 문서 생성
- [x] Deployment Architecture 문서 생성

---

## Context Analysis

**프로젝트 특성**:
- 로컬 개발 환경만 사용 (프로덕션 배포 없음)
- Docker Compose로 배포
- 클라우드 서비스 불필요
- 소규모 환경 (10개 테이블 미만)

**논리적 컴포넌트** (NFR Design에서 정의됨):
1. Database Connection Manager → SQLite 파일 기반
2. Authentication Manager → 애플리케이션 레벨 (인프라 불필요)
3. Cache Manager → 인메모리 (Python dict)
4. Logging Manager → 로컬 파일 시스템
5. SSE Manager → 애플리케이션 레벨 (인프라 불필요)
6. File Storage Manager → 로컬 파일 시스템

**기술 스택** (NFR Requirements에서 결정됨):
- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: React + Vite
- Deployment: Docker Compose

---

## Context-Specific Questions

Unit 1의 인프라 요구사항은 이미 명확하게 정의되어 있습니다 (로컬 개발 환경, Docker Compose). 다음 사항들을 확인하고자 합니다:

### Q1: Docker Compose 서비스 구성
**Context**: 백엔드와 프론트엔드를 Docker Compose로 배포합니다.

**Question**: Docker Compose 서비스 구성을 어떻게 하시겠습니까?

**Options**:
A) 2개 서비스 (backend, frontend) - 간단함
B) 3개 서비스 (backend, frontend, nginx) - nginx를 리버스 프록시로 사용
C) 1개 서비스 (monolithic) - 백엔드가 프론트엔드 정적 파일 서빙

[Answer]: A

**Rationale**: 로컬 개발 환경이므로 간단한 구성이 적합합니다.

---

### Q2: 데이터베이스 파일 위치
**Context**: SQLite 파일 기반 데이터베이스를 사용합니다.

**Question**: 데이터베이스 파일을 어디에 저장하시겠습니까?

**Options**:
A) 컨테이너 내부 (재시작 시 데이터 유지 안 됨)
B) Docker 볼륨 마운트 (호스트 디렉토리와 동기화)
C) Docker Named Volume (Docker가 관리)

[Answer]: B

**Rationale**: 호스트 디렉토리와 동기화하여 데이터 백업 및 관리가 용이합니다.

---

### Q3: 로그 파일 위치
**Context**: 로그를 날짜별 파일로 저장합니다.

**Question**: 로그 파일을 어디에 저장하시겠습니까?

**Options**:
A) 컨테이너 내부 (재시작 시 로그 손실)
B) Docker 볼륨 마운트 (호스트 디렉토리와 동기화)
C) Docker Named Volume (Docker가 관리)
D) stdout/stderr (Docker 로그로 수집)

[Answer]: B

**Rationale**: 호스트 디렉토리와 동기화하여 로그 분석 및 보관이 용이합니다.

---

### Q4: 업로드 파일 위치
**Context**: 메뉴 이미지를 로컬 파일 시스템에 저장합니다.

**Question**: 업로드 파일을 어디에 저장하시겠습니까?

**Options**:
A) 컨테이너 내부 (재시작 시 파일 손실)
B) Docker 볼륨 마운트 (호스트 디렉토리와 동기화)
C) Docker Named Volume (Docker가 관리)

[Answer]: B

**Rationale**: 호스트 디렉토리와 동기화하여 파일 백업 및 관리가 용이합니다.

---

### Q5: 포트 매핑
**Context**: 백엔드와 프론트엔드가 각각 포트를 사용합니다.

**Question**: 포트 매핑을 어떻게 하시겠습니까?

**Options**:
A) Backend: 8000, Frontend: 3000 (기본 포트)
B) Backend: 8080, Frontend: 8081 (8000번대 통일)
C) Backend: 5000, Frontend: 5001 (5000번대 통일)
D) 사용자 지정 포트

[Answer]: A

**Rationale**: FastAPI 기본 포트 8000, Vite 기본 포트 3000을 사용하여 혼란 방지.

---

## Next Steps

1. 모든 질문에 [Answer]: 태그로 답변해주세요
2. 답변 완료 후 "완료했습니다"라고 알려주세요
3. 답변이 모두 수집되면 Infrastructure Design 아티팩트를 생성합니다

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 질문 대기중
