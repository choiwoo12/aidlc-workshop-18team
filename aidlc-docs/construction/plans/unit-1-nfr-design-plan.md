# NFR Design Plan - Unit 1: Shared Foundation

## Overview

Unit 1의 NFR 요구사항을 논리적 컴포넌트와 설계 패턴으로 통합하는 계획입니다.

---

## Execution Plan

### Phase 1: NFR Requirements Analysis
- [x] NFR Requirements 문서 분석 완료
- [x] 기술 스택 결정 문서 분석 완료
- [x] Functional Design과의 통합 포인트 식별 완료

### Phase 2: Design Pattern Selection
- [x] 성능 최적화 패턴 선택
- [x] 보안 패턴 선택
- [x] 에러 처리 패턴 선택
- [x] 캐싱 패턴 선택
- [x] 동시성 제어 패턴 선택

### Phase 3: Logical Component Definition
- [x] 데이터베이스 연결 관리 컴포넌트
- [x] 인증/권한 관리 컴포넌트
- [x] 캐싱 컴포넌트
- [x] 로깅 컴포넌트
- [x] SSE 이벤트 관리 컴포넌트
- [x] 파일 저장소 컴포넌트

### Phase 4: Infrastructure-Independent Design
- [x] 논리적 컴포넌트 간 인터페이스 정의
- [x] 컴포넌트 간 의존성 정의
- [x] 설정 관리 전략 정의

### Phase 5: Documentation
- [x] NFR Design Patterns 문서 생성
- [x] Logical Components 문서 생성

---

## Context-Specific Questions

Unit 1의 NFR 요구사항은 이미 명확하게 정의되어 있으며, 기술 스택도 결정되었습니다. 다음 사항들을 확인하고자 합니다:

### Q1: SSE 연결 관리 전략
**Context**: 실시간 주문 업데이트를 위해 SSE를 사용합니다. 관리자가 여러 디바이스에서 접속할 수 있습니다.

**Question**: SSE 연결 관리 전략을 어떻게 하시겠습니까?

**Options**:
A) 단일 연결만 허용 (새 연결 시 기존 연결 종료)
B) 다중 연결 허용 (모든 연결에 이벤트 브로드캐스트)
C) 연결 풀 관리 (최대 N개 연결 제한)

[Answer]: B

**Rationale**: 관리자가 여러 디바이스(태블릿, PC 등)에서 동시에 모니터링할 수 있어야 합니다.

---

### Q2: 캐시 무효화 전략
**Context**: 메뉴 조회 API를 5분간 캐싱합니다. 메뉴 변경 시 캐시를 무효화해야 합니다.

**Question**: 캐시 무효화 전략을 어떻게 하시겠습니까?

**Options**:
A) 메뉴 변경 시 즉시 캐시 삭제 (동기)
B) 메뉴 변경 시 캐시 만료 시간 0으로 설정 (지연 삭제)
C) 메뉴 변경 시 캐시 버전 증가 (버전 기반)

[Answer]: A

**Rationale**: 메뉴 변경 후 즉시 반영되어야 고객이 최신 정보를 볼 수 있습니다.

---

### Q3: 데이터베이스 연결 풀 크기
**Context**: 동시 접속자 10-12명 (고객 10명 + 관리자 1-2명)을 지원합니다.

**Question**: 데이터베이스 연결 풀 크기를 어떻게 설정하시겠습니까?

**Options**:
A) 최소 5개, 최대 10개 (보수적)
B) 최소 10개, 최대 20개 (균형)
C) 최소 20개, 최대 50개 (여유)
D) 연결 풀 사용 안 함 (단순)

[Answer]: B

**Rationale**: 동시 접속자 수를 고려하여 충분한 연결 풀을 확보하되, 리소스 낭비를 방지합니다.

---

### Q4: 로그 파일 로테이션 전략
**Context**: 로그를 날짜별 파일로 저장합니다 (logs/app-2026-02-09.log).

**Question**: 로그 파일 로테이션 및 보관 전략을 어떻게 하시겠습니까?

**Options**:
A) 날짜별 파일, 30일 후 자동 삭제
B) 날짜별 파일, 90일 후 자동 삭제
C) 날짜별 파일, 수동 삭제
D) 크기 기반 로테이션 (10MB마다)

[Answer]: A

**Rationale**: 개발 환경이므로 30일 보관으로 충분하며, 디스크 공간 절약이 가능합니다.

---

### Q5: 파일 업로드 검증 전략
**Context**: 메뉴 이미지를 로컬 파일 시스템에 저장합니다 (최대 5MB).

**Question**: 파일 업로드 검증을 어떻게 하시겠습니까?

**Options**:
A) 파일 크기만 검증 (간단)
B) 파일 크기 + 확장자 검증 (기본)
C) 파일 크기 + MIME 타입 검증 (권장)
D) 파일 크기 + MIME 타입 + 이미지 내용 검증 (엄격)

[Answer]: C

**Rationale**: MIME 타입 검증으로 악의적인 파일 업로드를 방지하되, MVP 범위에서 적절한 수준입니다.

---

## Next Steps

1. 모든 질문에 [Answer]: 태그로 답변해주세요
2. 답변 완료 후 "완료했습니다"라고 알려주세요
3. 답변이 모두 수집되면 NFR Design 아티팩트를 생성합니다

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 질문 대기중
