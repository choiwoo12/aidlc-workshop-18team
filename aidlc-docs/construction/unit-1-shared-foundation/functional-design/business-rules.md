# Business Rules - Unit 1: Shared Foundation

## Overview

Unit 1의 비즈니스 규칙 정의입니다. 도메인 엔티티의 동작과 제약사항을 기술합니다.

---

## Authentication Business Rules

### AR-001: 관리자 인증

**Rule**: 관리자는 아이디와 비밀번호로 로그인

**Process**:
1. 관리자가 아이디와 비밀번호 입력
2. 시스템이 Store 엔티티에서 admin_username으로 매장 조회
3. 입력된 비밀번호를 해시하여 admin_password_hash와 비교
4. 일치하면 인증 토큰 발급, 불일치하면 인증 실패

**Validation Rules**:
- 아이디: 필수, 최소 4자
- 비밀번호: 필수, 최소 8자, 영문 대소문자 + 숫자 + 특수문자 포함

**Security Rules**:
- 비밀번호는 bcrypt로 해시하여 저장
- 인증 실패 시 구체적인 실패 이유 노출 금지 ("아이디 또는 비밀번호가 일치하지 않습니다")
- 인증 토큰은 JWT 형식 사용
- 토큰 만료 시간: 8시간

**Error Scenarios**:
- 아이디 없음 → "아이디 또는 비밀번호가 일치하지 않습니다"
- 비밀번호 불일치 → "아이디 또는 비밀번호가 일치하지 않습니다"
- 입력 형식 오류 → "입력 형식이 올바르지 않습니다"

---

### AR-002: 테이블 자동 로그인

**Rule**: 고객은 테이블 번호만으로 자동 로그인

**Process**:
1. 고객이 테이블 번호 입력 (숫자만)
2. 시스템이 Table 엔티티에서 table_number로 테이블 조회
3. 테이블이 존재하면 자동 로그인 토큰 발급
4. 테이블 상태를 IN_USE로 변경 (AVAILABLE이었을 경우)

**Validation Rules**:
- 테이블 번호: 필수, 숫자만 허용

**Business Logic**:
- 테이블 번호가 존재하지 않으면 로그인 실패
- 테이블 상태와 무관하게 로그인 가능 (이미 사용중인 테이블도 로그인 가능)
- 로그인 시 테이블 상태가 AVAILABLE이면 IN_USE로 자동 변경
- 로그인 시 current_session_started_at 설정

**Token Rules**:
- 토큰에 table_id 포함
- 토큰 만료 시간: 24시간
- 토큰은 테이블별로 고유 (같은 테이블에 여러 디바이스 접속 가능)

**Error Scenarios**:
- 테이블 번호 없음 → "존재하지 않는 테이블 번호입니다"
- 입력 형식 오류 → "테이블 번호는 숫자만 입력 가능합니다"

---

### AR-003: 인증 토큰 관리

**Rule**: 인증 토큰의 생명주기 관리

**Token Structure** (JWT):
```json
{
  "type": "admin" | "table",
  "store_id": "매장 ID",
  "table_id": "테이블 ID (table 타입만)",
  "issued_at": "발급 시간",
  "expires_at": "만료 시간"
}
```

**Token Validation**:
- 모든 API 요청 시 토큰 검증
- 만료된 토큰은 거부
- 토큰 타입에 따라 접근 권한 제어

**Access Control**:
- Admin 토큰: 모든 관리자 API 접근 가능
- Table 토큰: 해당 테이블의 고객 API만 접근 가능

---

## Order Management Business Rules

### OR-001: 주문 생성

**Rule**: 고객이 장바구니에서 주문 생성

**Preconditions**:
- 고객이 테이블 로그인 완료
- 장바구니에 최소 1개 이상의 메뉴 항목 존재

**Process**:
1. 장바구니 항목 유효성 검증
2. 주문 번호 생성 (매장 내 순차 번호)
3. Order 엔티티 생성 (상태: PENDING)
4. 각 장바구니 항목에 대해 OrderItem 생성
   - menu_name_snapshot, menu_price_snapshot에 현재 메뉴 정보 복사
   - selected_options에 선택된 옵션 정보 복사
   - subtotal 계산
5. Order의 total_amount 계산 (모든 OrderItem의 subtotal 합계)
6. 장바구니 초기화

**Validation Rules**:
- 장바구니가 비어있으면 주문 생성 불가
- 모든 메뉴가 is_available=true여야 함
- 필수 옵션이 모두 선택되어야 함
- 수량은 1 이상이어야 함

**Calculation Rules**:
- OrderItem subtotal = (menu_price + 옵션 가격 합계) × quantity
- Order total_amount = 모든 OrderItem subtotal의 합계

**Error Scenarios**:
- 빈 장바구니 → "장바구니가 비어있습니다"
- 판매 불가 메뉴 → "일부 메뉴를 주문할 수 없습니다"
- 필수 옵션 미선택 → "필수 옵션을 선택해주세요"

---

### OR-002: 주문 상태 전이

**Rule**: 주문 상태는 정해진 순서대로만 전이

**State Transition Flow**:
```
PENDING → CONFIRMED → PREPARING → READY → COMPLETED
```

**Transition Rules**:
- 순방향 전이만 허용 (역방향 불가)
- 상태 건너뛰기 불가
- 관리자만 상태 변경 가능 (고객은 불가)

**Allowed Transitions**:
- PENDING → CONFIRMED: 관리자가 주문 확인
- CONFIRMED → PREPARING: 조리 시작
- PREPARING → READY: 조리 완료, 서빙 대기
- READY → COMPLETED: 서빙 완료

**Forbidden Transitions**:
- 역방향: CONFIRMED → PENDING (불가)
- 건너뛰기: PENDING → PREPARING (불가)
- 고객 변경: 고객은 어떤 상태도 변경 불가

**Error Scenarios**:
- 잘못된 전이 → "잘못된 상태 전이입니다"
- 권한 없음 → "주문 상태를 변경할 권한이 없습니다"

---

### OR-003: 주문 수정

**Rule**: PENDING 상태의 주문만 수정 가능

**Allowed Modifications** (PENDING 상태):
- OrderItem 추가
- OrderItem 삭제
- OrderItem 수량 변경
- OrderItem 옵션 변경

**Forbidden Modifications** (CONFIRMED 이후):
- 모든 수정 불가
- 삭제만 가능 (OR-005 참조)

**Process**:
1. 주문 상태 확인 (PENDING인지)
2. 비관적 잠금 획득 (주문 단위)
3. 수정 작업 수행
4. total_amount 재계산
5. 잠금 해제

**Error Scenarios**:
- PENDING 아님 → "확인된 주문은 수정할 수 없습니다"
- 잠금 실패 → "다른 사용자가 수정 중입니다"

---

### OR-004: 주문 조회

**Rule**: 고객과 관리자의 주문 조회 권한

**Customer Access**:
- 자신의 테이블의 주문만 조회 가능
- 현재 세션의 주문만 조회 (과거 세션 불가)
- 모든 상태의 주문 조회 가능

**Admin Access**:
- 모든 테이블의 주문 조회 가능
- 모든 상태의 주문 조회 가능
- 실시간 주문 모니터링 가능

**Query Filters**:
- 테이블별 조회
- 상태별 조회
- 날짜별 조회 (관리자만)

---

### OR-005: 주문 삭제

**Rule**: 주문 삭제 시 OrderHistory로 이동 후 삭제

**Process**:
1. 관리자 권한 확인
2. 주문 정보를 OrderHistory로 복사
   - order_items_snapshot에 모든 OrderItem 정보 저장
   - status_transitions에 상태 변경 이력 저장
3. Order 및 OrderItem 삭제
4. SSE로 실시간 업데이트 전송

**Business Rules**:
- 관리자만 삭제 가능
- 모든 상태의 주문 삭제 가능
- 삭제 전 확인 필요 (UI에서 ConfirmDialog)
- 삭제된 주문은 OrderHistory에서 조회 가능

**Error Scenarios**:
- 권한 없음 → "주문을 삭제할 권한이 없습니다"
- 주문 없음 → "존재하지 않는 주문입니다"

---

## Table Management Business Rules

### TM-001: 테이블 세션 종료

**Rule**: 관리자가 테이블 세션 종료 시 처리

**Process**:
1. 관리자 권한 확인
2. 테이블의 미완료 주문 확인
3. 미완료 주문이 있으면:
   - 관리자에게 주문별 처리 방법 선택 요청
   - 선택지: "완료 처리", "삭제", "취소"
4. 모든 주문 처리 완료 후:
   - 완료된 주문들을 OrderHistory로 이동
   - 테이블 상태를 AVAILABLE로 변경
   - current_session_started_at 초기화
   - status_history에 이력 추가

**Incomplete Order Handling**:
- 관리자가 주문별로 처리 방법 선택
- "완료 처리": 상태를 COMPLETED로 변경 후 이력 이동
- "삭제": OrderHistory로 이동 후 삭제
- "취소": 세션 종료 취소, 주문 유지

**Error Scenarios**:
- 권한 없음 → "테이블 세션을 종료할 권한이 없습니다"
- 테이블 없음 → "존재하지 않는 테이블입니다"

---

### TM-002: 테이블 초기 설정

**Rule**: 관리자가 새 테이블 생성

**Process**:
1. 관리자 권한 확인
2. 테이블 번호 입력 (숫자만)
3. 테이블 번호 중복 확인
4. Table 엔티티 생성 (상태: AVAILABLE)

**Validation Rules**:
- 테이블 번호: 필수, 숫자만, 매장 내 고유
- 초기 상태: AVAILABLE

**Error Scenarios**:
- 권한 없음 → "테이블을 생성할 권한이 없습니다"
- 중복 번호 → "이미 존재하는 테이블 번호입니다"
- 형식 오류 → "테이블 번호는 숫자만 입력 가능합니다"

---

### TM-003: 과거 주문 내역 조회

**Rule**: 관리자가 테이블의 과거 주문 내역 조회

**Process**:
1. 관리자 권한 확인
2. OrderHistory에서 table_id로 조회
3. 날짜 범위 필터 적용 (선택)
4. 주문 이력 목록 반환

**Query Options**:
- 테이블별 조회
- 날짜 범위 조회
- 정렬: 최신순/오래된순

**Data Retention**:
- 1년 후 자동 삭제 (요구사항 Q13)

**Error Scenarios**:
- 권한 없음 → "과거 주문 내역을 조회할 권한이 없습니다"
- 테이블 없음 → "존재하지 않는 테이블입니다"

---

## Menu Management Business Rules

### MM-001: 메뉴 생성

**Rule**: 관리자가 새 메뉴 생성

**Process**:
1. 관리자 권한 확인
2. 메뉴 정보 입력 (이름, 설명, 가격, 카테고리, 옵션)
3. 이미지 업로드 (선택)
4. Menu 엔티티 생성

**Validation Rules**:
- 메뉴명: 필수, 최대 100자
- 가격: 필수, 양수
- category_level1: 필수
- category_level2: 선택
- 옵션: 선택, JSON 형식 검증

**Error Scenarios**:
- 권한 없음 → "메뉴를 생성할 권한이 없습니다"
- 필수 필드 누락 → "필수 정보를 입력해주세요"
- 가격 오류 → "가격은 0보다 커야 합니다"

---

### MM-002: 메뉴 수정

**Rule**: 관리자가 기존 메뉴 수정

**Process**:
1. 관리자 권한 확인
2. 메뉴 조회
3. 수정 가능한 필드 업데이트
4. 이미지 변경 시 기존 이미지 삭제 후 새 이미지 업로드

**Modifiable Fields**:
- 메뉴명, 설명, 가격, 카테고리, 옵션, 이미지, is_available

**Impact on Existing Orders**:
- 기존 주문에는 영향 없음 (스냅샷 방식)
- 새 주문부터 변경된 정보 적용

**Error Scenarios**:
- 권한 없음 → "메뉴를 수정할 권한이 없습니다"
- 메뉴 없음 → "존재하지 않는 메뉴입니다"

---

### MM-003: 메뉴 삭제

**Rule**: 관리자가 메뉴 삭제

**Process**:
1. 관리자 권한 확인
2. 메뉴 조회
3. 삭제 확인 (UI에서 ConfirmDialog)
4. Menu 엔티티 삭제

**Impact on Existing Orders**:
- 기존 주문에는 영향 없음 (스냅샷 방식)
- OrderItem의 menu_id는 null이 되지만 스냅샷 데이터는 유지

**Error Scenarios**:
- 권한 없음 → "메뉴를 삭제할 권한이 없습니다"
- 메뉴 없음 → "존재하지 않는 메뉴입니다"

---

### MM-004: 메뉴 판매 가능 여부 토글

**Rule**: 관리자가 메뉴 판매 가능 여부 변경

**Process**:
1. 관리자 권한 확인
2. 메뉴 조회
3. is_available 토글 (true ↔ false)

**Business Logic**:
- is_available=false인 메뉴는 고객에게 표시되지 않음
- 고객이 장바구니에 담은 후 is_available=false로 변경되면 주문 생성 시 오류

**Error Scenarios**:
- 권한 없음 → "메뉴 상태를 변경할 권한이 없습니다"
- 메뉴 없음 → "존재하지 않는 메뉴입니다"

---

## File Storage Business Rules

### FS-001: 이미지 업로드

**Rule**: 관리자가 메뉴 이미지 업로드

**Process**:
1. 관리자 권한 확인
2. 파일 유효성 검증
3. 파일 저장 (로컬 파일 시스템)
4. 파일 URL 반환

**Validation Rules**:
- 파일 크기: 최대 5MB
- 파일 형식: 제한 없음 (MVP에서는 간단하게)

**Storage Rules**:
- 파일명: UUID 기반 고유 이름 생성
- 저장 경로: `/uploads/menu-images/{uuid}.{extension}`

**Error Scenarios**:
- 권한 없음 → "이미지를 업로드할 권한이 없습니다"
- 파일 크기 초과 → "파일 크기는 5MB 이하여야 합니다"
- 업로드 실패 → "이미지 업로드에 실패했습니다"

---

### FS-002: 이미지 조회

**Rule**: 모든 사용자가 이미지 조회 가능

**Process**:
1. 이미지 URL로 파일 조회
2. 파일 반환

**Access Control**:
- 인증 불필요 (공개 접근)

---

### FS-003: 이미지 삭제

**Rule**: 메뉴 삭제 또는 이미지 변경 시 기존 이미지 삭제

**Process**:
1. 파일 시스템에서 파일 삭제
2. 삭제 실패 시 로그 기록 (오류 무시)

**Business Logic**:
- 메뉴 삭제 시 자동 삭제
- 메뉴 이미지 변경 시 기존 이미지 자동 삭제

---

## Data Validation Business Rules

### DV-001: 클라이언트 측 검증

**Rule**: 프론트엔드에서 사용자 입력 즉시 검증

**Purpose**:
- 사용자 경험 향상 (즉각적인 피드백)
- 불필요한 서버 요청 감소

**Validation Types**:
- 필수 필드 검증
- 데이터 타입 검증 (숫자, 문자열 등)
- 형식 검증 (이메일, 전화번호 등)
- 길이 제한 검증

---

### DV-002: 서버 측 검증

**Rule**: 백엔드에서 모든 요청 데이터 검증

**Purpose**:
- 보안 (악의적인 요청 차단)
- 데이터 무결성 보장

**Validation Types**:
- 클라이언트 측 검증과 동일한 모든 검증
- 비즈니스 규칙 검증
- 권한 검증
- 데이터베이스 제약사항 검증

**Critical Rule**:
- 클라이언트 측 검증을 신뢰하지 않음
- 모든 데이터를 서버에서 재검증

---

## Concurrency Control Business Rules

### CC-001: 비관적 잠금

**Rule**: 주문 수정 시 비관적 잠금 사용

**Scope**: 주문 단위 (Order 엔티티 전체)

**Process**:
1. 주문 수정 요청
2. 데이터베이스에서 주문 잠금 획득
3. 수정 작업 수행
4. 잠금 해제

**Lock Timeout**: 30초

**Error Scenarios**:
- 잠금 획득 실패 → "다른 사용자가 수정 중입니다. 잠시 후 다시 시도해주세요"
- 타임아웃 → "요청 시간이 초과되었습니다"

---

### CC-002: 주문 번호 생성

**Rule**: 주문 번호는 매장 내에서 순차적으로 증가

**Process**:
1. 매장의 마지막 주문 번호 조회 (잠금)
2. 번호 증가 (예: "001" → "002")
3. 새 주문에 번호 할당
4. 잠금 해제

**Format**: 3자리 숫자 (001, 002, ..., 999)

**Overflow Handling**: 999 이후 001로 순환

---

## Error Handling Business Rules

### EH-001: 에러 응답 형식

**Rule**: 모든 에러는 일관된 형식으로 반환

**Error Response Structure**:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적 메시지",
    "details": {} // 선택적 상세 정보
  }
}
```

**Error Categories**:
- Validation Error: 입력 데이터 오류
- Authentication Error: 인증 실패
- Authorization Error: 권한 없음
- Business Logic Error: 비즈니스 규칙 위반
- System Error: 시스템 오류

---

### EH-002: 에러 로깅

**Rule**: 모든 에러는 로그에 기록

**Log Levels**:
- ERROR: 시스템 오류, 예상치 못한 오류
- WARN: 비즈니스 규칙 위반, 인증/권한 오류
- INFO: 정상 동작 로그

**Log Format**:
```
[TIMESTAMP] [LEVEL] [COMPONENT] [MESSAGE] [DETAILS]
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
