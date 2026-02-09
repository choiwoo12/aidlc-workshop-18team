# Domain Entities - Unit 1: Shared Foundation

## Overview

Unit 1의 도메인 엔티티 정의입니다. 기술 스택 독립적이며, 순수한 비즈니스 개념과 규칙만을 포함합니다.

---

## Entity Definitions

### 1. Store (매장)

**Purpose**: 매장 기본 정보 관리

**Attributes**:
- `id`: 매장 고유 식별자 (Primary Key)
- `name`: 매장명 (필수, 최대 100자)
- `admin_username`: 관리자 계정 아이디 (필수, 고유, 최소 4자)
- `admin_password_hash`: 관리자 비밀번호 해시 (필수)
- `created_at`: 생성 일시 (자동 생성)
- `updated_at`: 수정 일시 (자동 갱신)

**Business Rules**:
- 매장명은 비어있을 수 없음
- 관리자 계정은 매장당 1개만 존재
- 관리자 비밀번호는 해시 형태로만 저장 (평문 저장 금지)

**Relationships**:
- 1:N with Table (한 매장은 여러 테이블을 가짐)
- 1:N with Menu (한 매장은 여러 메뉴를 가짐)

---

### 2. Table (테이블)

**Purpose**: 테이블 정보 및 상태 관리

**Attributes**:
- `id`: 테이블 고유 식별자 (Primary Key)
- `store_id`: 매장 ID (Foreign Key, 필수)
- `table_number`: 테이블 번호 (필수, 매장 내 고유, 숫자만)
- `status`: 현재 상태 (필수, enum: AVAILABLE, IN_USE)
- `status_changed_at`: 상태 변경 일시 (자동 갱신)
- `status_history`: 상태 변경 이력 배열 (구조: [{status, timestamp, changed_by}])
- `current_session_started_at`: 현재 세션 시작 일시 (IN_USE일 때만)
- `created_at`: 생성 일시 (자동 생성)
- `updated_at`: 수정 일시 (자동 갱신)

**Status Values**:
- `AVAILABLE`: 비어있음 (사용 가능)
- `IN_USE`: 사용중 (고객이 착석)

**Business Rules**:
- 테이블 번호는 매장 내에서 고유해야 함
- 테이블 번호는 숫자만 허용 (1, 2, 3, ...)
- 상태 변경 시 status_history에 이력 자동 추가
- 상태 변경 시 status_changed_at 자동 갱신
- IN_USE 상태로 변경 시 current_session_started_at 설정
- AVAILABLE 상태로 변경 시 current_session_started_at 초기화

**Relationships**:
- N:1 with Store (여러 테이블은 한 매장에 속함)
- 1:N with Order (한 테이블은 여러 주문을 가짐)

**State History Structure**:
```
status_history: [
  {
    status: "IN_USE",
    timestamp: "2026-02-09T10:00:00Z",
    changed_by: "admin" or "system"
  },
  {
    status: "AVAILABLE",
    timestamp: "2026-02-09T12:00:00Z",
    changed_by: "admin"
  }
]
```

---

### 3. Menu (메뉴)

**Purpose**: 메뉴 정보 및 옵션 관리

**Attributes**:
- `id`: 메뉴 고유 식별자 (Primary Key)
- `store_id`: 매장 ID (Foreign Key, 필수)
- `name`: 메뉴명 (필수, 최대 100자)
- `description`: 메뉴 설명 (선택, 최대 500자)
- `price`: 기본 가격 (필수, 양수)
- `category_level1`: 1단계 카테고리 (필수, 예: "음료", "식사", "디저트")
- `category_level2`: 2단계 카테고리 (선택, 예: "커피", "주스", "에이드")
- `image_url`: 메뉴 이미지 URL (선택)
- `is_available`: 판매 가능 여부 (필수, 기본값: true)
- `options`: 메뉴 옵션 JSON (선택, 구조화된 옵션 정의)
- `created_at`: 생성 일시 (자동 생성)
- `updated_at`: 수정 일시 (자동 갱신)

**Category Structure**:
- Level 1 (필수): 대분류 (예: "음료", "식사", "디저트")
- Level 2 (선택): 중분류 (예: "커피", "주스", "에이드")

**Options Structure** (JSON):
```json
{
  "option_groups": [
    {
      "id": "size",
      "name": "사이즈",
      "required": true,
      "allow_multiple": false,
      "choices": [
        {
          "id": "regular",
          "name": "레귤러",
          "price_adjustment": 0
        },
        {
          "id": "large",
          "name": "라지",
          "price_adjustment": 500
        }
      ]
    },
    {
      "id": "topping",
      "name": "토핑",
      "required": false,
      "allow_multiple": true,
      "choices": [
        {
          "id": "whipped_cream",
          "name": "휘핑크림",
          "price_adjustment": 500
        },
        {
          "id": "shot",
          "name": "샷 추가",
          "price_adjustment": 500
        }
      ]
    }
  ]
}
```

**Business Rules**:
- 메뉴명은 비어있을 수 없음
- 가격은 0보다 커야 함
- category_level1은 필수, category_level2는 선택
- 옵션 그룹의 required가 true면 고객은 반드시 선택해야 함
- 옵션 그룹의 allow_multiple이 false면 단일 선택만 가능
- 옵션 선택 시 price_adjustment가 최종 가격에 반영됨

**Relationships**:
- N:1 with Store (여러 메뉴는 한 매장에 속함)
- 1:N with OrderItem (한 메뉴는 여러 주문 항목에 참조됨)

---

### 4. Order (주문)

**Purpose**: 고객 주문 정보 및 상태 관리

**Attributes**:
- `id`: 주문 고유 식별자 (Primary Key)
- `store_id`: 매장 ID (Foreign Key, 필수)
- `table_id`: 테이블 ID (Foreign Key, 필수)
- `order_number`: 주문 번호 (필수, 사람이 읽을 수 있는 형식, 예: "001", "002")
- `status`: 주문 상태 (필수, enum)
- `total_amount`: 총 금액 (필수, 양수, 계산됨)
- `created_at`: 주문 생성 일시 (자동 생성)
- `updated_at`: 수정 일시 (자동 갱신)
- `lock_version`: 비관적 잠금용 버전 번호 (자동 관리)

**Status Values** (순서대로 전이):
1. `PENDING`: 대기중 (주문 생성 직후)
2. `CONFIRMED`: 확인됨 (관리자가 확인)
3. `PREPARING`: 준비중 (조리 시작)
4. `READY`: 서빙 대기 (조리 완료)
5. `COMPLETED`: 완료 (서빙 완료)

**Status Transition Rules**:
- 순방향 전이만 허용 (역방향 불가)
- PENDING → CONFIRMED → PREPARING → READY → COMPLETED
- 상태 건너뛰기 불가 (예: PENDING → PREPARING 불가)

**Business Rules**:
- 주문 번호는 매장 내에서 고유하며 순차적으로 증가
- 총 금액은 주문 항목들의 합계로 자동 계산
- 주문 수정은 PENDING 상태일 때만 가능
- 주문 항목이 없는 주문은 생성 불가
- 비관적 잠금: 주문 수정 시 전체 주문 잠금

**Relationships**:
- N:1 with Store (여러 주문은 한 매장에 속함)
- N:1 with Table (여러 주문은 한 테이블에 속함)
- 1:N with OrderItem (한 주문은 여러 주문 항목을 가짐)

---

### 5. OrderItem (주문 항목)

**Purpose**: 주문 내 개별 메뉴 항목 정보

**Attributes**:
- `id`: 주문 항목 고유 식별자 (Primary Key)
- `order_id`: 주문 ID (Foreign Key, 필수)
- `menu_id`: 메뉴 ID (Foreign Key, 필수, 참조용)
- `menu_name_snapshot`: 주문 시점 메뉴명 (필수, 스냅샷)
- `menu_price_snapshot`: 주문 시점 기본 가격 (필수, 스냅샷)
- `selected_options`: 선택된 옵션 JSON (선택, 스냅샷)
- `quantity`: 수량 (필수, 양수)
- `subtotal`: 소계 (필수, 양수, 계산됨)
- `created_at`: 생성 일시 (자동 생성)

**Selected Options Structure** (JSON):
```json
{
  "options": [
    {
      "group_id": "size",
      "group_name": "사이즈",
      "choice_id": "large",
      "choice_name": "라지",
      "price_adjustment": 500
    },
    {
      "group_id": "topping",
      "group_name": "토핑",
      "choice_id": "whipped_cream",
      "choice_name": "휘핑크림",
      "price_adjustment": 500
    }
  ]
}
```

**Business Rules**:
- 주문 생성 시 menu_name_snapshot과 menu_price_snapshot에 현재 메뉴 정보 복사
- 주문 생성 시 selected_options에 선택된 옵션 정보 복사
- 소계 = (menu_price_snapshot + 옵션 가격 합계) × quantity
- 수량은 1 이상이어야 함
- 메뉴 정보 변경 시에도 스냅샷은 변경되지 않음 (과거 데이터 보존)

**Relationships**:
- N:1 with Order (여러 주문 항목은 한 주문에 속함)
- N:1 with Menu (여러 주문 항목은 한 메뉴를 참조, 스냅샷 방식)

**Snapshot Rationale**:
- Menu ID는 참조 관계 유지용
- 스냅샷 필드들은 과거 주문 데이터 정확성 보장용
- 메뉴 가격/이름 변경 시에도 과거 주문은 주문 당시 정보 유지

---

### 6. OrderHistory (주문 이력)

**Purpose**: 완료된 주문의 이력 보관 및 분석

**Attributes**:
- `id`: 이력 고유 식별자 (Primary Key)
- `store_id`: 매장 ID (Foreign Key, 필수)
- `table_id`: 테이블 ID (Foreign Key, 필수)
- `original_order_id`: 원본 주문 ID (참조용)
- `order_number`: 주문 번호 (필수)
- `order_items_snapshot`: 주문 항목 스냅샷 JSON (필수)
- `total_amount`: 총 금액 (필수)
- `status_transitions`: 상태 변경 이력 JSON (필수)
- `session_started_at`: 테이블 세션 시작 일시 (필수)
- `session_ended_at`: 테이블 세션 종료 일시 (필수)
- `created_at`: 이력 생성 일시 (자동 생성)

**Order Items Snapshot Structure** (JSON):
```json
{
  "items": [
    {
      "menu_name": "아메리카노",
      "menu_price": 3000,
      "selected_options": [...],
      "quantity": 2,
      "subtotal": 6000
    }
  ]
}
```

**Status Transitions Structure** (JSON):
```json
{
  "transitions": [
    {
      "from_status": null,
      "to_status": "PENDING",
      "timestamp": "2026-02-09T10:00:00Z",
      "changed_by": "customer"
    },
    {
      "from_status": "PENDING",
      "to_status": "CONFIRMED",
      "timestamp": "2026-02-09T10:01:00Z",
      "changed_by": "admin"
    },
    {
      "from_status": "CONFIRMED",
      "to_status": "PREPARING",
      "timestamp": "2026-02-09T10:05:00Z",
      "changed_by": "admin"
    },
    {
      "from_status": "PREPARING",
      "to_status": "READY",
      "timestamp": "2026-02-09T10:15:00Z",
      "changed_by": "admin"
    },
    {
      "from_status": "READY",
      "to_status": "COMPLETED",
      "timestamp": "2026-02-09T10:20:00Z",
      "changed_by": "admin"
    }
  ]
}
```

**Business Rules**:
- 테이블 세션 종료 시 해당 세션의 모든 완료된 주문을 OrderHistory로 이동
- order_items_snapshot에 주문 항목 전체 정보 저장
- status_transitions에 모든 상태 변경 이력 저장
- 이력 데이터는 수정 불가 (읽기 전용)
- 1년 후 자동 삭제 (요구사항 Q13 참조)

**Relationships**:
- N:1 with Store (여러 이력은 한 매장에 속함)
- N:1 with Table (여러 이력은 한 테이블에 속함)

---

## Entity Relationship Diagram

```
Store (1) ----< (N) Table
  |                  |
  |                  |
  |                  |
(1)                (1)
  |                  |
  v                  v
Menu (N) ----< (N) Order (1) ----< (N) OrderItem
                     |
                     |
                    (1)
                     |
                     v
                OrderHistory
```

**Relationships Summary**:
- Store → Table: 1:N
- Store → Menu: 1:N
- Store → Order: 1:N
- Store → OrderHistory: 1:N
- Table → Order: 1:N
- Table → OrderHistory: 1:N
- Menu → OrderItem: 1:N (참조 관계, 스냅샷 방식)
- Order → OrderItem: 1:N

---

## Data Integrity Constraints

### Referential Integrity
- 모든 Foreign Key는 참조 무결성 유지
- 삭제 시 Cascade 규칙:
  - Store 삭제 → 관련 Table, Menu, Order, OrderHistory 모두 삭제
  - Table 삭제 → 관련 Order, OrderHistory 모두 삭제
  - Order 삭제 → 관련 OrderItem 모두 삭제
  - Menu 삭제 → OrderItem은 유지 (스냅샷 방식이므로)

### Business Constraints
- 주문 생성 시 최소 1개 이상의 OrderItem 필요
- 주문 총액은 OrderItem 소계의 합과 일치해야 함
- 테이블 상태가 IN_USE일 때만 주문 생성 가능
- 주문 번호는 매장 내에서 고유하고 순차적

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
