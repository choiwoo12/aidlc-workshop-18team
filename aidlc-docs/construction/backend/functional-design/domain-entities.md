# Domain Entities - Backend

## Overview
테이블오더 서비스의 도메인 엔티티를 정의합니다. 각 엔티티는 비즈니스 개념을 표현하며, 속성과 제약조건을 포함합니다.

---

## Entity Relationship Diagram

```
Store (매장)
  |
  +-- Table (테이블) [1:N]
  |     |
  |     +-- Order (주문) [1:N]
  |           |
  |           +-- OrderItem (주문 항목) [1:N]
  |                 |
  |                 +-- Menu (메뉴) [N:1]
  |
  +-- Menu (메뉴) [1:N]
  |
  +-- User (사용자) [1:N]
  |
  +-- OrderHistory (주문 이력) [1:N]
        |
        +-- OrderHistoryItem (주문 이력 항목) [1:N]
```

**관계 설명**:
- Store는 여러 Table, Menu, User, OrderHistory를 가짐
- Table은 여러 Order를 가짐 (현재 세션 + 과거 세션)
- Order는 여러 OrderItem을 가짐
- OrderItem은 하나의 Menu를 참조
- OrderHistory는 세션 종료 시 Order 데이터를 복사하여 저장
- OrderHistoryItem은 OrderHistory의 항목

---

## Entity 1: Store (매장)

### 책임
- 매장 정보 관리
- 다중 매장 환경에서 데이터 격리의 최상위 엔티티

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 매장 고유 식별자 | PK, Auto-increment |
| name | String | Y | 매장명 | NOT NULL, 최대 100자 |
| address | String | N | 매장 주소 | 최대 200자 |
| phone | String | N | 매장 전화번호 | 최대 20자 |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |
| updatedAt | LocalDateTime | Y | 수정 시각 | NOT NULL, 자동 갱신 |

### 비즈니스 규칙
- 매장명은 중복 가능 (다른 지점)
- 매장 삭제 시 하위 데이터(Table, Menu, User) 확인 필요

---

## Entity 2: Table (테이블)

### 책임
- 테이블 정보 관리
- 테이블 세션 관리
- 테이블 초기 설정 정보 저장

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 테이블 고유 식별자 | PK, Auto-increment |
| storeId | Long | Y | 매장 ID | FK → Store.id, NOT NULL |
| tableNumber | Integer | Y | 테이블 번호 | NOT NULL, 1~10 |
| pin | String | Y | 4자리 PIN (SHA-256 해싱) | NOT NULL, 64자 (해시값) |
| sessionId | String | N | 현재 세션 ID (UUID) | 36자, NULL 가능 |
| sessionStatus | String | Y | 세션 상태 | ENUM: 'ACTIVE', 'INACTIVE' |
| sessionStartTime | LocalDateTime | N | 세션 시작 시각 | NULL 가능 |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |
| updatedAt | LocalDateTime | Y | 수정 시각 | NOT NULL, 자동 갱신 |

### 비즈니스 규칙
- 같은 매장 내 테이블 번호는 중복 불가 (UNIQUE: storeId + tableNumber)
- 테이블 수는 매장당 최대 10개
- PIN은 SHA-256으로 해싱하여 저장
- sessionId는 UUID 형식
- 세션 시작 시 sessionId 생성, sessionStatus = 'ACTIVE'
- 세션 종료 시 sessionId = NULL, sessionStatus = 'INACTIVE'

---

## Entity 3: Menu (메뉴)

### 책임
- 메뉴 정보 관리
- 메뉴 이미지 경로 저장
- 메뉴 노출 순서 관리

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 메뉴 고유 식별자 | PK, Auto-increment |
| storeId | Long | Y | 매장 ID | FK → Store.id, NOT NULL |
| name | String | Y | 메뉴명 | NOT NULL, 최대 100자 |
| price | Integer | Y | 가격 (원) | NOT NULL, >= 0 |
| description | String | N | 메뉴 설명 | 최대 500자 |
| category | String | Y | 카테고리 | NOT NULL, 최대 50자 |
| imagePath | String | N | 이미지 파일 경로 | 최대 255자 |
| displayOrder | Integer | Y | 노출 순서 | NOT NULL, 기본값 0 |
| deleted | Boolean | Y | 논리적 삭제 플래그 | NOT NULL, 기본값 false |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |
| updatedAt | LocalDateTime | Y | 수정 시각 | NOT NULL, 자동 갱신 |

### 비즈니스 규칙
- 가격은 0 이상
- 이미지 파일명은 Timestamp + 확장자 (예: 1707465600000.jpg)
- 논리적 삭제 시 deleted = true 설정
- 조회 시 deleted = false인 메뉴만 반환
- displayOrder가 작을수록 먼저 표시

---

## Entity 4: Order (주문)

### 책임
- 주문 정보 관리
- 주문 상태 관리
- 주문 총액 저장

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 주문 고유 식별자 | PK, Auto-increment |
| orderNumber | String | Y | 주문 번호 | UNIQUE, NOT NULL, 형식: ORD-YYYYMMDD-NNNN |
| storeId | Long | Y | 매장 ID | FK → Store.id, NOT NULL |
| tableId | Long | Y | 테이블 ID | FK → Table.id, NOT NULL |
| sessionId | String | Y | 세션 ID | NOT NULL, 36자 (UUID) |
| orderTime | LocalDateTime | Y | 주문 시각 | NOT NULL, 자동 설정 |
| totalAmount | Integer | Y | 총 주문 금액 (원) | NOT NULL, >= 0 |
| status | String | Y | 주문 상태 | ENUM: '대기중', '준비중', '완료', '취소' |
| version | Integer | Y | 낙관적 잠금 버전 | NOT NULL, 기본값 0 |
| deleted | Boolean | Y | 논리적 삭제 플래그 | NOT NULL, 기본값 false |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |
| updatedAt | LocalDateTime | Y | 수정 시각 | NOT NULL, 자동 갱신 |

### 비즈니스 규칙
- orderNumber 형식: ORD-YYYYMMDD-NNNN (예: ORD-20260209-0001)
- totalAmount는 OrderItem의 (unitPrice * quantity) 합계
- 주문 생성 시 totalAmount 계산 및 저장
- 주문 조회 시 totalAmount 재계산하여 검증
- 상태 전이 규칙: 완료 상태에서는 다른 상태로 변경 불가
- version 컬럼으로 낙관적 잠금 구현
- 논리적 삭제 시 deleted = true 설정
- 조회 시 deleted = false인 주문만 반환

---

## Entity 5: OrderItem (주문 항목)

### 책임
- 주문 항목 정보 관리
- 주문 시점의 메뉴 가격 저장 (불변)

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 주문 항목 고유 식별자 | PK, Auto-increment |
| orderId | Long | Y | 주문 ID | FK → Order.id, NOT NULL |
| menuId | Long | Y | 메뉴 ID | FK → Menu.id, NOT NULL |
| menuName | String | Y | 메뉴명 (스냅샷) | NOT NULL, 최대 100자 |
| quantity | Integer | Y | 수량 | NOT NULL, > 0 |
| unitPrice | Integer | Y | 단가 (주문 시점 가격) | NOT NULL, >= 0 |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |

### 비즈니스 규칙
- unitPrice는 주문 생성 시점의 Menu.price를 저장 (불변)
- menuName은 주문 생성 시점의 Menu.name을 저장 (스냅샷)
- quantity는 1 이상
- Order 논리적 삭제 시 OrderItem도 함께 처리 (Cascade)
- 물리적 삭제는 하지 않음 (감사 추적)

---

## Entity 6: OrderHistory (주문 이력)

### 책임
- 세션 종료 시 주문 데이터 보관
- 과거 주문 내역 조회

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 주문 이력 고유 식별자 | PK, Auto-increment |
| orderId | Long | Y | 원본 주문 ID | NOT NULL |
| orderNumber | String | Y | 주문 번호 | NOT NULL |
| storeId | Long | Y | 매장 ID | NOT NULL |
| tableId | Long | Y | 테이블 ID | NOT NULL |
| sessionId | String | Y | 세션 ID | NOT NULL |
| orderTime | LocalDateTime | Y | 주문 시각 | NOT NULL |
| totalAmount | Integer | Y | 총 주문 금액 | NOT NULL |
| status | String | Y | 최종 주문 상태 | NOT NULL |
| completedTime | LocalDateTime | Y | 완료 시각 | NOT NULL |
| archivedTime | LocalDateTime | Y | 이력 이동 시각 | NOT NULL, 자동 설정 |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |

### 비즈니스 규칙
- 세션 종료 시 Order 데이터를 복사하여 생성
- orderId는 원본 Order.id 참조 (FK 아님, 단순 참조)
- 최대 1년간 데이터 보관
- 조회 전용 (수정/삭제 불가)

---

## Entity 7: OrderHistoryItem (주문 이력 항목)

### 책임
- 주문 이력의 항목 정보 보관

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 주문 이력 항목 고유 식별자 | PK, Auto-increment |
| orderHistoryId | Long | Y | 주문 이력 ID | FK → OrderHistory.id, NOT NULL |
| menuId | Long | Y | 메뉴 ID | NOT NULL |
| menuName | String | Y | 메뉴명 | NOT NULL |
| quantity | Integer | Y | 수량 | NOT NULL |
| unitPrice | Integer | Y | 단가 | NOT NULL |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |

### 비즈니스 규칙
- 세션 종료 시 OrderItem 데이터를 복사하여 생성
- 조회 전용 (수정/삭제 불가)

---

## Entity 8: User (사용자)

### 책임
- 관리자 사용자 정보 관리
- 인증 정보 저장

### 속성

| 속성명 | 타입 | 필수 | 설명 | 제약조건 |
|--------|------|------|------|----------|
| id | Long | Y | 사용자 고유 식별자 | PK, Auto-increment |
| storeId | Long | Y | 매장 ID | FK → Store.id, NOT NULL |
| username | String | Y | 사용자명 | UNIQUE, NOT NULL, 최대 50자 |
| password | String | Y | 비밀번호 (bcrypt 해싱) | NOT NULL, 60자 (해시값) |
| role | String | Y | 역할 | ENUM: 'ADMIN', 'MANAGER' |
| loginAttempts | Integer | Y | 로그인 시도 횟수 | NOT NULL, 기본값 0 |
| lockedUntil | LocalDateTime | N | 계정 잠금 해제 시각 | NULL 가능 |
| createdAt | LocalDateTime | Y | 생성 시각 | NOT NULL, 자동 설정 |
| updatedAt | LocalDateTime | Y | 수정 시각 | NOT NULL, 자동 갱신 |

### 비즈니스 규칙
- username은 전체 시스템에서 고유
- password는 bcrypt로 해싱하여 저장
- 로그인 실패 시 loginAttempts 증가
- loginAttempts >= 5이면 계정 잠금 (lockedUntil = 현재시각 + 30분)
- 로그인 성공 시 loginAttempts = 0, lockedUntil = NULL

---

## Data Type Mapping

### Java → Database (H2)

| Java Type | H2 Type | 설명 |
|-----------|---------|------|
| Long | BIGINT | 64-bit 정수 |
| Integer | INT | 32-bit 정수 |
| String | VARCHAR | 가변 길이 문자열 |
| Boolean | BOOLEAN | true/false |
| LocalDateTime | TIMESTAMP | 날짜 + 시간 |

---

## Constraints Summary

### Primary Keys
- 모든 엔티티: id (Auto-increment)

### Foreign Keys
- Table.storeId → Store.id
- Menu.storeId → Store.id
- Order.storeId → Store.id
- Order.tableId → Table.id
- OrderItem.orderId → Order.id
- OrderItem.menuId → Menu.id
- OrderHistoryItem.orderHistoryId → OrderHistory.id
- User.storeId → Store.id

### Unique Constraints
- Table: (storeId, tableNumber)
- Order: orderNumber
- User: username

### Check Constraints
- Menu.price >= 0
- Order.totalAmount >= 0
- OrderItem.quantity > 0
- OrderItem.unitPrice >= 0
- Table.tableNumber BETWEEN 1 AND 10

---

## Indexes

성능 최적화를 위한 인덱스:

### Table
- IDX_table_store_session: (storeId, sessionId)

### Menu
- IDX_menu_store_category: (storeId, category, displayOrder)
- IDX_menu_deleted: (deleted)

### Order
- IDX_order_table_session: (tableId, sessionId)
- IDX_order_store_time: (storeId, orderTime)
- IDX_order_deleted: (deleted)

### OrderHistory
- IDX_order_history_store_time: (storeId, archivedTime)

### User
- IDX_user_store: (storeId)

---

## Notes

- 모든 엔티티는 createdAt, updatedAt 타임스탬프 포함
- 논리적 삭제는 Menu, Order만 적용 (deleted 플래그)
- OrderItem은 Order의 논리적 삭제에 따라 함께 처리 (Cascade)
- OrderHistory는 세션 종료 시 Order 데이터를 복사하여 생성
- 낙관적 잠금은 Order 엔티티만 적용 (version 컬럼)
- 계층적 데이터 격리: Store → Table → Order

