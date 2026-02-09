# NFR Design Plan - Unit 2: Customer Order Domain

## Overview

Unit 2의 NFR 요구사항을 논리적 컴포넌트와 설계 패턴으로 통합하는 계획입니다.

---

## Execution Plan

### Phase 1: NFR Requirements Analysis
- [x] NFR Requirements 문서 분석
- [x] 기술 스택 결정 문서 분석
- [x] Functional Design과의 통합 포인트 식별

### Phase 2: Design Pattern Selection
- [x] SSE 연결 관리 패턴 선택
- [x] 장바구니 상태 관리 패턴 선택
- [x] 실시간 업데이트 패턴 선택
- [x] 에러 처리 패턴 선택
- [x] 데이터 검증 패턴 선택

### Phase 3: Logical Component Definition
- [x] SSE 연결 관리 컴포넌트
- [x] 장바구니 관리 컴포넌트
- [x] 주문 관리 컴포넌트
- [x] 메뉴 조회 컴포넌트
- [x] 데이터 검증 컴포넌트

### Phase 4: Infrastructure-Independent Design
- [x] 논리적 컴포넌트 간 인터페이스 정의
- [x] 컴포넌트 간 의존성 정의
- [x] 설정 관리 전략 정의

### Phase 5: Documentation
- [x] NFR Design Patterns 문서 생성
- [x] Logical Components 문서 생성

---

## Context-Specific Questions

Unit 2의 NFR 요구사항은 이미 명확하게 정의되어 있으며, 기술 스택도 결정되었습니다. 다음 사항들을 확인하고자 합니다:

### Q1: SSE 재연결 전략 세부사항
**Context**: SSE 연결이 끊어졌을 때 자동 재연결을 최대 3회 시도합니다.

**Question**: SSE 재연결 시 이전 이벤트 복구 전략을 어떻게 하시겠습니까?

**Options**:
A) 재연결 후 전체 주문 목록 다시 조회 (안전)
B) 재연결 후 마지막 이벤트 ID부터 재전송 (효율적)
C) 재연결 후 복구 없음 (단순)

[Answer]: A

**Rationale**: 

---

### Q2: 장바구니 중복 항목 비교 로직
**Context**: 같은 메뉴 + 같은 옵션 조합일 때 수량을 증가시킵니다.

**Question**: 옵션 비교 시 옵션 순서를 어떻게 처리하시겠습니까?

**Options**:
A) 옵션 순서 무관 (정렬 후 비교)
B) 옵션 순서 고려 (순서대로 비교)
C) 옵션 ID 집합으로 비교 (가장 단순)

[Answer]: A

**Rationale**: 

---

### Q3: 주문 번호 순차 번호 관리
**Context**: 주문 번호는 T{테이블번호}-{순차번호} 형식이며, 테이블별로 관리됩니다.

**Question**: 순차 번호 생성 시 동시성 제어를 어떻게 하시겠습니까?

**Options**:
A) 데이터베이스 트랜잭션 + SELECT FOR UPDATE (안전)
B) 데이터베이스 AUTO_INCREMENT 활용 (단순)
C) 애플리케이션 레벨 락 (복잡)
D) 동시성 제어 없음 (단순, 소규모 환경)

[Answer]: B

**Rationale**: 

---

### Q4: SSE Keep-alive 메시지 형식
**Context**: SSE 연결 유지를 위해 30초마다 Keep-alive 메시지를 전송합니다.

**Question**: Keep-alive 메시지 형식을 어떻게 하시겠습니까?

**Options**:
A) 빈 메시지 (단순)
B) JSON 형식 {"type": "ping"} (명확)
C) 주석 형식 ": keep-alive" (SSE 표준)

[Answer]: A

**Rationale**: 

---

### Q5: 장바구니 데이터 직렬화
**Context**: 장바구니 데이터를 SessionStorage에 저장합니다.

**Question**: 장바구니 데이터 직렬화 시 에러 처리를 어떻게 하시겠습니까?

**Options**:
A) JSON.stringify 실패 시 빈 장바구니로 초기화 (안전)
B) JSON.stringify 실패 시 에러 메시지 표시 (명확)
C) JSON.stringify 실패 시 무시 (단순)

[Answer]: A

**Rationale**: 

---

### Q6: 메뉴 조회 에러 처리
**Context**: 메뉴 조회 실패 시 빈 목록을 표시합니다.

**Question**: 메뉴 조회 실패 시 재시도 전략을 어떻게 하시겠습니까?

**Options**:
A) 자동 재시도 (1회, 5초 후)
B) 수동 재시도 버튼 표시 (사용자 제어)
C) 재시도 없음 (단순)

[Answer]: B

**Rationale**: 

---

### Q7: 주문 생성 시 서버 검증 실패 처리
**Context**: 서버 측 검증 실패 시 장바구니를 유지하고 에러 메시지를 표시합니다.

**Question**: 서버 검증 실패 시 장바구니 항목 하이라이트를 어떻게 하시겠습니까?

**Options**:
A) 문제 있는 항목만 하이라이트 (명확)
B) 전체 장바구니 하이라이트 (단순)
C) 하이라이트 없음 (가장 단순)

[Answer]: C

**Rationale**: 

---

## Next Steps

1. 모든 질문에 [Answer]: 태그로 답변해주세요
2. 답변 완료 후 "완료했습니다"라고 알려주세요
3. 답변이 모두 수집되면 명확화 질문이 필요한지 분석합니다
4. 명확화 질문이 없으면 NFR Design 아티팩트를 생성합니다

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 질문 대기중
