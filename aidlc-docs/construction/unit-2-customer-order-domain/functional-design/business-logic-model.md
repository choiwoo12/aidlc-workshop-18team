# Business Logic Model - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 비즈니스 로직 모델입니다. 고객 주문 프로세스의 플로우, 데이터 흐름, 계산 로직을 정의합니다.

---

## 1. Business Flows

### BF-001: 메뉴 조회 플로우

```
[고객] → [메뉴 페이지 접속]
         ↓
[카테고리 선택 (선택사항)]
         ↓
[MenuService.getMenus(category)]
         ↓
[MenuRepository.findByCategory()]
         ↓
[판매 가능 메뉴 필터링]
         ↓
[메뉴 목록 반환]
         ↓
[메뉴 카드 표시]
```

**주요 단계**:
1. 고객이 메뉴 페이지 접속
2. 카테고리 선택 (선택사항, 기본값: 전체)
3. MenuService가 MenuRepository를 통해 메뉴 조회
4. `is_available = true`인 메뉴만 필터링
5. 메뉴 목록을 카드 형태로 표시

**데이터 흐름**:
- Input: category (Level 1 또는 Level 2, 선택사항)
- Output: Menu[] (이름, 가격, 설명, 이미지, 카테고리)

---

### BF-002: 장바구니 추가 플로우

```
[고객] → [메뉴 카드의 "추가" 버튼 클릭]
         ↓
[옵션이 있는가?]
    ↓ Yes          ↓ No
[옵션 선택 모달]  [즉시 장바구니 추가]
    ↓
[필수 옵션 검증]
    ↓
[장바구니에 추가]
    ↓
[중복 항목 확인]
    ↓ 동일 옵션      ↓ 다른 옵션
[수량 증가]      [별도 항목 추가]
    ↓
[SessionStorage 저장]
    ↓
[시각적 피드백 (토스트)]
    ↓
[장바구니 아이콘 배지 업데이트]
```

**주요 단계**:
1. 고객이 메뉴 카드의 "추가" 버튼 클릭
2. 메뉴에 옵션이 있으면 옵션 선택 모달 표시
3. 필수 옵션 검증 (required = true인 옵션 그룹)
4. 장바구니에 추가 (중복 항목 확인)
5. SessionStorage에 저장
6. 시각적 피드백 표시

**데이터 흐름**:
- Input: Menu, SelectedOptions[]
- Output: CartItem (menu_id, menu_snapshot, selected_options, quantity, subtotal)

---

### BF-003: 장바구니 수량 조절 플로우

```
[고객] → [장바구니 페이지 접속]
         ↓
[장바구니 항목 목록 표시]
         ↓
[수량 증가/감소 버튼 클릭]
         ↓
[수량 = 0인가?]
    ↓ Yes          ↓ No
[항목 제거]      [수량 업데이트]
    ↓
[소계 재계산]
    ↓
[총액 재계산]
    ↓
[SessionStorage 저장]
    ↓
[UI 업데이트]
```

**주요 단계**:
1. 고객이 장바구니 페이지 접속
2. 장바구니 항목 목록 표시
3. 수량 증가/감소 버튼 클릭
4. 수량이 0이면 항목 제거, 아니면 수량 업데이트
5. 소계 및 총액 재계산
6. SessionStorage에 저장

**계산 로직**:
- 소계 = (메뉴 가격 + 옵션 가격 합계) × 수량
- 총액 = 모든 항목의 소계 합계

---

### BF-004: 주문 생성 플로우

```
[고객] → [장바구니 페이지에서 "주문하기" 버튼 클릭]
         ↓
[장바구니 비어있는가?]
    ↓ Yes          ↓ No
[에러 표시]      [주문 확인 화면]
    ↓
[고객이 "확정" 버튼 클릭]
    ↓
[OrderService.createOrder()]
    ↓
[주문 번호 생성 (T{테이블번호}-{순차번호})]
    ↓
[Order 엔티티 생성 (status: PENDING)]
    ↓
[장바구니 항목 → OrderItem 변환]
    ↓
[OrderRepository.save()]
    ↓
[성공?]
    ↓ Yes                    ↓ No
[주문 번호 표시 (5초)]    [에러 메시지 표시]
    ↓                        ↓
[장바구니 비우기]          [장바구니 유지]
    ↓
[메뉴 페이지로 리다이렉트]
```

**주요 단계**:
1. 고객이 "주문하기" 버튼 클릭
2. 장바구니 비어있는지 검증
3. 주문 확인 화면 표시
4. 고객이 "확정" 버튼 클릭
5. OrderService가 주문 생성
6. 주문 번호 생성 (테이블별 순차)
7. Order 및 OrderItem 엔티티 생성
8. 데이터베이스에 저장
9. 성공 시 주문 번호 표시 후 장바구니 비우기
10. 실패 시 에러 메시지 표시, 장바구니 유지

**데이터 흐름**:
- Input: CartItem[]
- Output: Order (order_number, status, total_amount, OrderItem[])

---

### BF-005: 주문 내역 조회 플로우

```
[고객] → ["주문 내역" 버튼 클릭]
         ↓
[OrderService.getOrderHistory(table_id, session_id)]
         ↓
[OrderRepository.findByTableAndSession()]
         ↓
[현재 세션의 주문만 필터링]
         ↓
[주문 목록 반환 (시간 역순)]
         ↓
[주문 내역 화면 표시]
         ↓
[각 주문: 주문 번호, 시각, 메뉴 목록, 금액, 상태]
```

**주요 단계**:
1. 고객이 "주문 내역" 버튼 클릭
2. OrderService가 현재 테이블 세션의 주문 조회
3. 주문 목록을 시간 역순으로 정렬
4. 주문 내역 화면 표시

**데이터 흐름**:
- Input: table_id, session_id
- Output: Order[] (order_number, created_at, OrderItem[], total_amount, status)

---

### BF-006: 실시간 주문 상태 업데이트 플로우

```
[고객 화면 로드]
    ↓
[SSEService.connect(table_id)]
    ↓
[SSE 연결 설정]
    ↓
[Keep-alive 메시지 수신 (30초마다)]
    ↓
[관리자가 주문 상태 변경]
    ↓
[서버에서 SSE 이벤트 발송]
    ↓
[고객 화면에서 이벤트 수신]
    ↓
[주문 상태 업데이트]
    ↓
[UI 업데이트 (주문 내역 화면)]
```

**주요 단계**:
1. 고객 화면 로드 시 SSE 연결 자동 설정
2. Keep-alive 메시지로 연결 유지
3. 관리자가 주문 상태 변경 시 서버에서 SSE 이벤트 발송
4. 고객 화면에서 이벤트 수신
5. 주문 상태 업데이트 및 UI 반영

**이벤트 데이터**:
```json
{
  "event": "order_status_changed",
  "data": {
    "order_id": 123,
    "order_number": "T01-001",
    "old_status": "PENDING",
    "new_status": "CONFIRMED"
  }
}
```

---

## 2. Data Flow Diagrams

### DF-001: 메뉴 조회 데이터 흐름

```
[고객 UI]
    ↓ (category)
[MenuService]
    ↓ (category)
[MenuRepository]
    ↓ (SQL Query)
[Database]
    ↓ (Menu[])
[MenuRepository]
    ↓ (Menu[])
[MenuService] → 필터링 (is_available = true)
    ↓ (Menu[])
[고객 UI] → 메뉴 카드 표시
```

---

### DF-002: 주문 생성 데이터 흐름

```
[고객 UI]
    ↓ (CartItem[])
[OrderService]
    ↓ (주문 번호 생성)
[OrderService] → Order 엔티티 생성
    ↓
[OrderService] → OrderItem 엔티티 생성 (CartItem 변환)
    ↓ (Order, OrderItem[])
[OrderRepository]
    ↓ (SQL Insert)
[Database]
    ↓ (Order ID)
[OrderRepository]
    ↓ (Order)
[OrderService]
    ↓ (Order)
[고객 UI] → 주문 번호 표시
```

---

### DF-003: 실시간 업데이트 데이터 흐름

```
[관리자 UI]
    ↓ (주문 상태 변경)
[AdminController]
    ↓ (order_id, new_status)
[OrderManagementService]
    ↓ (SQL Update)
[Database]
    ↓ (Success)
[OrderManagementService]
    ↓ (SSE 이벤트 발송)
[SSEService]
    ↓ (이벤트 브로드캐스트)
[고객 UI] → 주문 상태 업데이트
```

---

## 3. Calculation Logic

### CL-001: 메뉴 가격 계산

**기본 가격**:
```
menu_price = Menu.price
```

**옵션 가격 계산**:
```
option_price = Σ(selected_option.price_adjustment)
```

**최종 가격**:
```
final_price = menu_price + option_price
```

**예시**:
- 메뉴: 아메리카노 (3000원)
- 옵션 1: 라지 사이즈 (+500원)
- 옵션 2: 샷 추가 (+500원)
- 최종 가격: 3000 + 500 + 500 = 4000원

---

### CL-002: 장바구니 소계 계산

**항목 소계**:
```
item_subtotal = (menu_price + option_price) × quantity
```

**장바구니 총액**:
```
cart_total = Σ(item_subtotal)
```

**예시**:
- 항목 1: 아메리카노 (라지, 샷 추가) × 2 = 4000 × 2 = 8000원
- 항목 2: 카페라떼 (레귤러) × 1 = 3500 × 1 = 3500원
- 장바구니 총액: 8000 + 3500 = 11500원

---

### CL-003: 주문 총액 계산

**주문 총액**:
```
order_total = Σ(OrderItem.subtotal)
```

**OrderItem 소계**:
```
OrderItem.subtotal = (menu_price_snapshot + option_price) × quantity
```

**예시**:
- OrderItem 1: 아메리카노 (4000원) × 2 = 8000원
- OrderItem 2: 카페라떼 (3500원) × 1 = 3500원
- 주문 총액: 8000 + 3500 = 11500원

---

### CL-004: 주문 번호 생성 로직

**주문 번호 형식**:
```
order_number = "T{table_number}-{sequence_number}"
```

**순차 번호 생성**:
```
sequence_number = 테이블별 마지막 주문 번호 + 1
```

**예시**:
- 테이블 1의 첫 주문: T01-001
- 테이블 1의 두 번째 주문: T01-002
- 테이블 2의 첫 주문: T02-001

**순차 번호 리셋**:
- 테이블 세션 종료 시 순차 번호 001로 리셋

---

## 4. Validation Logic

### VL-001: 장바구니 추가 검증

**필수 옵션 검증**:
```python
for option_group in menu.options.option_groups:
    if option_group.required:
        if not has_selected_option(option_group.id):
            raise ValidationError("필수 옵션을 선택해주세요.")
```

**단일/다중 선택 검증**:
```python
for option_group in menu.options.option_groups:
    selected_count = count_selected_options(option_group.id)
    if not option_group.allow_multiple and selected_count > 1:
        raise ValidationError("하나만 선택 가능합니다.")
```

---

### VL-002: 주문 생성 검증

**장바구니 비어있지 않음 검증**:
```python
if len(cart_items) == 0:
    raise ValidationError("장바구니가 비어있습니다.")
```

**서버 측 추가 검증** (서버에서 수행):
```python
# 메뉴 판매 가능 여부
for item in cart_items:
    menu = get_menu(item.menu_id)
    if not menu.is_available:
        raise ValidationError(f"{menu.name}은(는) 현재 판매하지 않습니다.")

# 가격 일치 확인
for item in cart_items:
    menu = get_menu(item.menu_id)
    if item.menu_price_snapshot != menu.price:
        raise ValidationError("메뉴 가격이 변경되었습니다. 장바구니를 다시 확인해주세요.")
```

---

### VL-003: 옵션 비교 로직

**같은 옵션 조합 판단**:
```python
def is_same_options(options1, options2):
    # 옵션 개수가 다르면 다른 옵션
    if len(options1) != len(options2):
        return False
    
    # 각 옵션 그룹별로 선택 항목 비교
    for group_id in get_all_group_ids(options1, options2):
        choices1 = get_choices_by_group(options1, group_id)
        choices2 = get_choices_by_group(options2, group_id)
        
        # 선택 항목이 다르면 다른 옵션
        if set(choices1) != set(choices2):
            return False
    
    return True
```

---

## 5. State Management

### SM-001: 장바구니 상태 (SessionStorage)

**데이터 구조**:
```json
{
  "cart_items": [
    {
      "cart_item_id": "uuid-1",
      "menu_id": 1,
      "menu_snapshot": {
        "name": "아메리카노",
        "price": 3000,
        "image_url": "/images/americano.jpg"
      },
      "selected_options": [
        {
          "group_id": "size",
          "group_name": "사이즈",
          "choice_id": "large",
          "choice_name": "라지",
          "price_adjustment": 500
        }
      ],
      "quantity": 2,
      "subtotal": 7000
    }
  ],
  "total_amount": 7000
}
```

---

### SM-002: 주문 상태 (서버)

**Order 엔티티 상태**:
- PENDING: 대기중 (주문 생성 직후)
- CONFIRMED: 확인됨 (관리자 확인)
- PREPARING: 준비중 (조리 시작)
- READY: 서빙 대기 (조리 완료)
- COMPLETED: 완료 (서빙 완료)

**상태 전이 규칙**:
- 순방향 전이만 허용
- 상태 건너뛰기 불가

---

## 6. Error Handling

### EH-001: 에러 처리 전략

**에러 메시지**:
- 모든 에러: "주문 생성에 실패했습니다. 다시 시도해주세요."
- 에러 타입 구분 없음

**에러 발생 시 동작**:
- 주문 생성 실패: 장바구니 유지, 에러 메시지 표시
- 메뉴 조회 실패: 빈 목록 표시, 에러 메시지 표시
- SSE 연결 실패: 자동 재연결 시도 (최대 3회)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
