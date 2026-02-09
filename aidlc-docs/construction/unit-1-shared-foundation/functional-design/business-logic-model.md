# Business Logic Model - Unit 1: Shared Foundation

## Overview

Unit 1의 비즈니스 로직 모델입니다. 주요 비즈니스 프로세스와 데이터 흐름을 정의합니다.

---

## Authentication Flows

### AF-001: 관리자 로그인 플로우

**Actors**: 관리자, 시스템

**Preconditions**: 
- 매장이 생성되어 있음
- 관리자 계정이 설정되어 있음

**Main Flow**:
1. 관리자가 로그인 페이지 접속
2. 관리자가 아이디와 비밀번호 입력
3. 시스템이 입력 형식 검증 (클라이언트)
4. 시스템이 로그인 요청 전송 (서버)
5. 시스템이 입력 형식 재검증 (서버)
6. 시스템이 Store 엔티티에서 admin_username으로 매장 조회
7. 시스템이 비밀번호 해시 비교
8. 일치하면 JWT 토큰 발급 (type: admin, 만료: 8시간)
9. 시스템이 토큰을 클라이언트에 반환
10. 클라이언트가 토큰을 LocalStorage에 저장
11. 관리자 대시보드로 리다이렉트

**Alternative Flows**:
- 3a. 입력 형식 오류 → 에러 메시지 표시, 재입력 요청
- 6a. 아이디 없음 → "아이디 또는 비밀번호가 일치하지 않습니다" 표시
- 7a. 비밀번호 불일치 → "아이디 또는 비밀번호가 일치하지 않습니다" 표시

**Postconditions**:
- 관리자가 인증됨
- 토큰이 저장됨
- 관리자 대시보드 접근 가능

---

### AF-002: 테이블 자동 로그인 플로우

**Actors**: 고객, 시스템

**Preconditions**:
- 테이블이 생성되어 있음

**Main Flow**:
1. 고객이 테이블 태블릿에서 앱 실행
2. 시스템이 테이블 번호 입력 화면 표시
3. 고객이 테이블 번호 입력 (숫자만)
4. 시스템이 입력 형식 검증 (클라이언트)
5. 시스템이 로그인 요청 전송 (서버)
6. 시스템이 입력 형식 재검증 (서버)
7. 시스템이 Table 엔티티에서 table_number로 테이블 조회
8. 테이블이 존재하면 JWT 토큰 발급 (type: table, 만료: 24시간)
9. 테이블 상태가 AVAILABLE이면 IN_USE로 변경
10. current_session_started_at 설정
11. status_history에 이력 추가
12. 시스템이 토큰을 클라이언트에 반환
13. 클라이언트가 토큰을 SessionStorage에 저장
14. 고객 메뉴 페이지로 리다이렉트

**Alternative Flows**:
- 3a. 입력 형식 오류 → 에러 메시지 표시, 재입력 요청
- 7a. 테이블 번호 없음 → "존재하지 않는 테이블 번호입니다" 표시

**Postconditions**:
- 고객이 인증됨
- 토큰이 저장됨
- 테이블 상태가 IN_USE (이전에 AVAILABLE이었을 경우)
- 고객 메뉴 페이지 접근 가능

---

## Order Management Flows

### OM-001: 주문 생성 플로우

**Actors**: 고객, 시스템

**Preconditions**:
- 고객이 테이블 로그인 완료
- 장바구니에 최소 1개 이상의 메뉴 항목 존재

**Main Flow**:
1. 고객이 장바구니 페이지에서 "주문하기" 버튼 클릭
2. 시스템이 장바구니 유효성 검증 (클라이언트)
   - 장바구니가 비어있지 않은지
   - 모든 필수 옵션이 선택되었는지
3. 시스템이 주문 생성 요청 전송 (서버)
4. 시스템이 장바구니 유효성 재검증 (서버)
5. 시스템이 모든 메뉴의 is_available 확인
6. 시스템이 주문 번호 생성 (매장 내 순차 번호, 잠금 사용)
7. 시스템이 Order 엔티티 생성 (상태: PENDING)
8. 각 장바구니 항목에 대해:
   - OrderItem 엔티티 생성
   - menu_name_snapshot에 현재 메뉴명 복사
   - menu_price_snapshot에 현재 메뉴 가격 복사
   - selected_options에 선택된 옵션 정보 복사
   - subtotal 계산: (menu_price + 옵션 가격 합계) × quantity
9. Order의 total_amount 계산 (모든 OrderItem subtotal 합계)
10. 시스템이 주문 정보를 클라이언트에 반환
11. 클라이언트가 장바구니 초기화 (SessionStorage)
12. SSE를 통해 관리자에게 실시간 알림 전송
13. 주문 완료 페이지로 리다이렉트

**Alternative Flows**:
- 2a. 장바구니 비어있음 → "장바구니가 비어있습니다" 표시
- 2b. 필수 옵션 미선택 → "필수 옵션을 선택해주세요" 표시
- 5a. 판매 불가 메뉴 존재 → "일부 메뉴를 주문할 수 없습니다" 표시

**Postconditions**:
- Order 엔티티 생성됨 (상태: PENDING)
- OrderItem 엔티티들 생성됨
- 장바구니 초기화됨
- 관리자가 실시간 알림 수신

---

### OM-002: 주문 상태 변경 플로우

**Actors**: 관리자, 시스템

**Preconditions**:
- 관리자가 로그인 완료
- 주문이 존재함

**Main Flow**:
1. 관리자가 대시보드에서 주문 선택
2. 관리자가 상태 변경 버튼 클릭 (예: "확인" 버튼)
3. 시스템이 상태 전이 유효성 검증 (클라이언트)
4. 시스템이 상태 변경 요청 전송 (서버)
5. 시스템이 관리자 권한 확인
6. 시스템이 비관적 잠금 획득 (주문 단위)
7. 시스템이 상태 전이 유효성 재검증 (서버)
8. 시스템이 Order의 status 업데이트
9. 시스템이 잠금 해제
10. SSE를 통해 고객과 다른 관리자에게 실시간 업데이트 전송
11. 대시보드 UI 갱신

**Alternative Flows**:
- 5a. 권한 없음 → "주문 상태를 변경할 권한이 없습니다" 표시
- 6a. 잠금 획득 실패 → "다른 사용자가 수정 중입니다" 표시
- 7a. 잘못된 전이 → "잘못된 상태 전이입니다" 표시

**Postconditions**:
- 주문 상태가 변경됨
- 모든 사용자가 실시간 업데이트 수신

---

### OM-003: 주문 삭제 플로우

**Actors**: 관리자, 시스템

**Preconditions**:
- 관리자가 로그인 완료
- 주문이 존재함

**Main Flow**:
1. 관리자가 대시보드에서 주문 선택
2. 관리자가 "삭제" 버튼 클릭
3. 시스템이 확인 다이얼로그 표시 ("정말 삭제하시겠습니까?")
4. 관리자가 "확인" 클릭
5. 시스템이 삭제 요청 전송 (서버)
6. 시스템이 관리자 권한 확인
7. 시스템이 OrderHistory 엔티티 생성
   - order_items_snapshot에 모든 OrderItem 정보 저장
   - status_transitions에 상태 변경 이력 저장
8. 시스템이 Order 및 OrderItem 삭제
9. SSE를 통해 고객과 다른 관리자에게 실시간 업데이트 전송
10. 대시보드 UI 갱신

**Alternative Flows**:
- 4a. 관리자가 "취소" 클릭 → 삭제 취소
- 6a. 권한 없음 → "주문을 삭제할 권한이 없습니다" 표시

**Postconditions**:
- Order 및 OrderItem 삭제됨
- OrderHistory에 이력 보관됨
- 모든 사용자가 실시간 업데이트 수신

---

## Table Management Flows

### TM-001: 테이블 세션 종료 플로우

**Actors**: 관리자, 시스템

**Preconditions**:
- 관리자가 로그인 완료
- 테이블이 존재함

**Main Flow**:
1. 관리자가 테이블 관리 페이지에서 테이블 선택
2. 관리자가 "세션 종료" 버튼 클릭
3. 시스템이 테이블의 미완료 주문 조회
4. 미완료 주문이 있으면:
   - 시스템이 주문 목록과 처리 옵션 표시
   - 각 주문별로 선택지: "완료 처리", "삭제", "취소"
   - 관리자가 각 주문의 처리 방법 선택
5. 관리자가 "세션 종료" 확인
6. 시스템이 세션 종료 요청 전송 (서버)
7. 시스템이 관리자 권한 확인
8. 각 주문에 대해 선택된 처리 수행:
   - "완료 처리": 상태를 COMPLETED로 변경
   - "삭제": OrderHistory로 이동 후 삭제
9. 모든 완료된 주문을 OrderHistory로 이동
10. 테이블 상태를 AVAILABLE로 변경
11. current_session_started_at 초기화
12. status_history에 이력 추가
13. 테이블 관리 페이지 UI 갱신

**Alternative Flows**:
- 4a. 미완료 주문 없음 → 바로 세션 종료 진행
- 4b. 관리자가 "취소" 선택 → 세션 종료 취소
- 7a. 권한 없음 → "테이블 세션을 종료할 권한이 없습니다" 표시

**Postconditions**:
- 테이블 상태가 AVAILABLE
- 완료된 주문들이 OrderHistory로 이동
- 테이블 세션 정보 초기화

---

## Menu Management Flows

### MM-001: 메뉴 생성 플로우

**Actors**: 관리자, 시스템

**Preconditions**:
- 관리자가 로그인 완료

**Main Flow**:
1. 관리자가 메뉴 관리 페이지에서 "메뉴 추가" 버튼 클릭
2. 시스템이 메뉴 생성 폼 표시
3. 관리자가 메뉴 정보 입력:
   - 메뉴명, 설명, 가격
   - 1단계 카테고리, 2단계 카테고리 (선택)
   - 옵션 그룹 및 선택지 (선택)
   - 이미지 업로드 (선택)
4. 시스템이 입력 유효성 검증 (클라이언트)
5. 관리자가 "저장" 버튼 클릭
6. 이미지가 있으면:
   - 시스템이 이미지 업로드 요청 전송
   - 시스템이 이미지 저장 후 URL 반환
7. 시스템이 메뉴 생성 요청 전송 (서버)
8. 시스템이 관리자 권한 확인
9. 시스템이 입력 유효성 재검증 (서버)
10. 시스템이 Menu 엔티티 생성
11. 메뉴 관리 페이지 UI 갱신

**Alternative Flows**:
- 4a. 필수 필드 누락 → "필수 정보를 입력해주세요" 표시
- 4b. 가격 오류 → "가격은 0보다 커야 합니다" 표시
- 6a. 이미지 업로드 실패 → "이미지 업로드에 실패했습니다" 표시
- 8a. 권한 없음 → "메뉴를 생성할 권한이 없습니다" 표시

**Postconditions**:
- Menu 엔티티 생성됨
- 이미지가 저장됨 (있을 경우)
- 고객이 새 메뉴 조회 가능

---

## Data Flow Diagrams

### DF-001: 주문 생성 데이터 흐름

```
Customer → CartContext (SessionStorage)
           ↓
CartContext → OrderService (API Request)
           ↓
OrderService → Validation (Client + Server)
           ↓
OrderService → Order Entity (Create, status: PENDING)
           ↓
OrderService → OrderItem Entities (Create with snapshots)
           ↓
OrderService → Calculate total_amount
           ↓
OrderService → SSEService (Notify admin)
           ↓
OrderService → Response to Customer
           ↓
Customer → Clear CartContext
```

---

### DF-002: 주문 상태 변경 데이터 흐름

```
Admin → DashboardPage (Select order)
        ↓
DashboardPage → OrderService (Change status request)
        ↓
OrderService → Pessimistic Lock (Order level)
        ↓
OrderService → Validate state transition
        ↓
OrderService → Update Order.status
        ↓
OrderService → Release Lock
        ↓
OrderService → SSEService (Notify all users)
        ↓
SSEService → Customer (Real-time update)
SSEService → Other Admins (Real-time update)
```

---

### DF-003: 테이블 세션 종료 데이터 흐름

```
Admin → TableManagementPage (End session)
        ↓
TableManagementPage → Check incomplete orders
        ↓
Admin → Select action for each order
        ↓
TableService → Process each order
        ↓
TableService → Move completed orders to OrderHistory
        ↓
TableService → Update Table.status to AVAILABLE
        ↓
TableService → Clear current_session_started_at
        ↓
TableService → Add to status_history
        ↓
TableManagementPage → UI refresh
```

---

## Calculation Logic

### CL-001: OrderItem Subtotal 계산

**Formula**:
```
subtotal = (menu_price_snapshot + sum(option_price_adjustments)) × quantity
```

**Example**:
- 메뉴: 아메리카노 (3,000원)
- 옵션 1: 라지 사이즈 (+500원)
- 옵션 2: 샷 추가 (+500원)
- 수량: 2

```
subtotal = (3000 + 500 + 500) × 2 = 8,000원
```

---

### CL-002: Order Total Amount 계산

**Formula**:
```
total_amount = sum(all OrderItem subtotals)
```

**Example**:
- OrderItem 1: 아메리카노 라지 × 2 = 8,000원
- OrderItem 2: 카페라떼 × 1 = 4,000원

```
total_amount = 8000 + 4000 = 12,000원
```

---

### CL-003: 주문 번호 생성 로직

**Algorithm**:
```
1. 매장의 마지막 주문 번호 조회 (잠금)
2. 번호를 정수로 변환
3. 1 증가
4. 999를 초과하면 1로 리셋
5. 3자리 문자열로 포맷 (예: "001", "002", "999")
6. 잠금 해제
```

**Example**:
```
Last order number: "098"
→ Parse to int: 98
→ Increment: 99
→ Format: "099"

Last order number: "999"
→ Parse to int: 999
→ Increment: 1000
→ Overflow: 1
→ Format: "001"
```

---

## Validation Logic

### VL-001: 메뉴 옵션 유효성 검증

**Rules**:
1. 필수 옵션 그룹은 반드시 1개 선택되어야 함
2. 단일 선택 옵션 그룹은 최대 1개만 선택 가능
3. 다중 선택 옵션 그룹은 여러 개 선택 가능
4. 선택된 옵션은 해당 옵션 그룹에 속해야 함

**Validation Algorithm**:
```
For each option_group in menu.options:
  If option_group.required:
    Check at least one choice is selected
    If not selected: Error "필수 옵션을 선택해주세요"
  
  If not option_group.allow_multiple:
    Check at most one choice is selected
    If multiple selected: Error "하나만 선택 가능합니다"
  
  For each selected_choice:
    Check choice exists in option_group.choices
    If not exists: Error "잘못된 옵션입니다"
```

---

### VL-002: 주문 상태 전이 유효성 검증

**Valid Transitions**:
```
PENDING → CONFIRMED: Valid
CONFIRMED → PREPARING: Valid
PREPARING → READY: Valid
READY → COMPLETED: Valid

All other transitions: Invalid
```

**Validation Algorithm**:
```
current_status = order.status
new_status = requested_status

valid_transitions = {
  "PENDING": ["CONFIRMED"],
  "CONFIRMED": ["PREPARING"],
  "PREPARING": ["READY"],
  "READY": ["COMPLETED"]
}

If new_status not in valid_transitions[current_status]:
  Error "잘못된 상태 전이입니다"
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
