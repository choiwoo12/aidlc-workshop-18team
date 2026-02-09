# NFR Requirements Clarification Questions - Unit 1

## Overview

초기 답변을 검토한 결과, 일부 답변에서 추가 명확화가 필요합니다.

---

## Clarification Questions

### CQ1: SQLite In-Memory Mode - 데이터 영속성 (Q2 관련)
Q2에서 "SQLite in-memory mode (완전 메모리, 재시작 시 데이터 손실)" (C)를 선택하셨습니다.

**중요**: 이 선택은 서버 재시작 시 모든 데이터(매장, 테이블, 메뉴, 주문)가 손실됩니다.

**예시**:
- 관리자가 메뉴 10개 등록
- 서버 재시작
- 모든 메뉴 데이터 손실 → 다시 등록 필요

이것이 의도한 동작인가요?

A) 네, 의도한 것입니다 (개발/테스트용으로 충분)
B) 아니요, 파일 기반 SQLite로 변경 (재시작 후에도 데이터 유지)
C) 아니요, 하이브리드 방식 (메뉴는 파일, 주문은 메모리)
D) Other (설명해주세요)

[Answer]: B (수정됨: 원래 C였으나 사용자 요청으로 B로 변경)

**Rationale**: 
- 파일 기반 SQLite로 모든 데이터 영속성 보장
- 서버 재시작 시에도 메뉴, 주문 데이터 유지
- 단일 DB 연결로 복잡도 감소
- MVP 범위에서 성능 충분

---

### CQ2: 데이터베이스 인덱스 - Primary Key만 (Q10 관련)
Q10에서 "Primary Key만 (최소한)" (A)를 선택하셨습니다.

**잠재적 문제**:
- Foreign Key에 인덱스가 없으면 JOIN 성능 저하
- 자주 조회되는 필드(예: table_number, order_status)에 인덱스가 없으면 조회 성능 저하

**예시**:
- 테이블 번호로 주문 조회: `SELECT * FROM orders WHERE table_id = ?`
- table_id에 인덱스가 없으면 Full Table Scan 발생

다시 한번 확인해주세요. 어떤 필드에 인덱스를 생성할까요?

A) Primary Key만 (최소한) - **성능 저하 가능**
B) Foreign Key + 자주 조회되는 필드 (균형) - **권장**
C) 모든 조회 필드 (성능 최우선)
D) Other (설명해주세요)

[Answer]: B

**Rationale**: 인덱스는 조회 성능에 직접적인 영향을 미칩니다.

---

### CQ3: 프론트엔드 번들 최적화 - 최적화 없음 (Q12 관련)
Q12에서 "최적화 없음 (개발 속도 우선)" (A)를 선택하셨습니다.

**잠재적 문제**:
- 초기 로딩 시간 증가 (모든 코드를 한 번에 다운로드)
- 사용하지 않는 코드도 번들에 포함

**예시**:
- 관리자 코드가 고객 페이지에도 포함됨
- 초기 로딩 시간: 5-10초 (최적화 시 1-2초)

다시 한번 확인해주세요. 프론트엔드 번들을 어떻게 최적화할까요?

A) 최적화 없음 (개발 속도 우선) - **로딩 시간 증가**
B) 기본 최적화 (Code splitting, Tree shaking) - **권장**
C) 고급 최적화 (Lazy loading, Dynamic imports)
D) Other (설명해주세요)

[Answer]: B

**Rationale**: 번들 최적화는 사용자 경험(로딩 속도)에 영향을 미칩니다.

---

### CQ4: JWT 토큰 저장 - LocalStorage (Q14 관련)
Q14에서 "LocalStorage (간단함, XSS 취약)" (A)를 선택하셨습니다.

**보안 위험**:
- XSS (Cross-Site Scripting) 공격에 취약
- 악의적인 스크립트가 토큰을 탈취할 수 있음

**하지만**:
- Requirements Analysis에서 이미 LocalStorage 사용 결정됨
- 로컬 개발 환경만 사용 (프로덕션 배포 없음)
- MVP 범위에서는 허용 가능

이 선택을 유지하시겠습니까?

A) 네, LocalStorage 유지 (MVP에 적합, 간단함)
B) 아니요, HttpOnly Cookie로 변경 (보안 강화)
C) 아니요, Memory only로 변경 (가장 안전)
D) Other (설명해주세요)

[Answer]: A

**Rationale**: 보안과 사용자 경험의 균형을 고려해야 합니다.

---

## Next Steps

1. 모든 명확화 질문에 [Answer]: 태그로 답변해주세요
2. 답변 완료 후 "완료했습니다"라고 알려주세요
3. 모든 답변이 명확해지면 NFR Requirements 아티팩트를 생성합니다

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 명확화 질문 대기중
