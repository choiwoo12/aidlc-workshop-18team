# Business Logic Model - Backend

## Overview
Backend 유닛의 비즈니스 로직 워크플로우를 정의합니다. 각 워크플로우는 비즈니스 프로세스를 단계별로 설명하며, 데이터 흐름과 의사결정 로직을 포함합니다.

---

## Workflow 1: 주문 생성 (Order Creation)

### 목적
고객이 장바구니의 메뉴를 주문으로 확정하는 프로세스

### 입력
- `CreateOrderRequest`:
  - storeId: Long
  - tableId: Long
  - sessionId: String (UUID)
  - items: List<OrderItemRequest>
    - menuId: Long
    - quantity: Integer

### 출력
- `OrderResponse`:
  - id: Long
  - orderNumber: String
  - orderTime: LocalDateTime
  - totalAmount: Integer
  - status: String
  - items: List<OrderItemResponse>

### 워크플로우 단계

**Step 1: 입력 검증**
1. storeId, tableId, sessionId 필수 값 확인
2. items 리스트가 비어있지 않은지 확인
3. 각 item의 menuId, quantity 필수 값 확인

**Step 2: 테이블 세션 검증**
1. Table 조회 (tableId)
2. Table.storeId == request.storeId 확인
3. Table.sessionId == request.sessionId 확인
4. Table.sessionStatus == 'ACTIVE' 확인
5. 검증 실패 시 예외 발생: `InvalidSessionException`

**Step 3: 메뉴 검증**
1. 각 item의 menuId로 Menu 조회
2. Menu.storeId == request.storeId 확인
3. Menu.deleted == false 확인 (활성 메뉴만)
4. 검증 실패 시 예외 발생: `MenuNotFoundException` 또는 `MenuNotActiveException`

**Step 4: 주문 번호 생성**
1. 현재 날짜 가져오기 (YYYYMMDD)
2. 해당 날짜의 주문 개수 조회
3. 순번 계산 (개수 + 1, 4자리 패딩)
4. 주문 번호 생성: `ORD-{YYYYMMDD}-{NNNN}`
5. 예: ORD-20260209-0001

**Step 5: 총 주문 금액 계산**
1. 각 item에 대해:
   - Menu.price 조회
   - itemAmount = Menu.price * item.quantity
2. totalAmount = sum(itemAmount)

**Step 6: Order 엔티티 생성 및 저장**
1. Order 객체 생성:
   - orderNumber: 생성된 주문 번호
   - storeId, tableId, sessionId: 요청 값
   - orderTime: 현재 시각
   - totalAmount: 계산된 총액
   - status: '대기중'
   - version: 0
   - deleted: false
2. Order 저장 (OrderMapper.insertOrder)
3. 생성된 Order.id 반환

**Step 7: OrderItem 엔티티 생성 및 저장**
1. 각 item에 대해:
   - OrderItem 객체 생성:
     - orderId: 생성된 Order.id
     - menuId: item.menuId
     - menuName: Menu.name (스냅샷)
     - quantity: item.quantity
     - unitPrice: Menu.price (주문 시점 가격)
   - OrderItem 저장 (OrderMapper.insertOrderItem)

**Step 8: SSE 이벤트 전송**
1. NEW_ORDER 이벤트 생성:
   - orderId: Order.id
   - tableId: Order.tableId
   - totalAmount: Order.totalAmount
   - timestamp: 현재 시각
2. 해당 매장의 모든 관리자에게 브로드캐스트
3. SSEService.broadcastEventToStore(storeId, event)

**Step 9: 응답 생성**
1. Order와 OrderItem 데이터를 OrderResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 6 ~ Step 7: 단일 트랜잭션
- Step 8: 트랜잭션 외부 (비동기)

### 예외 처리
- `InvalidSessionException`: 세션 검증 실패
- `MenuNotFoundException`: 메뉴 없음
- `MenuNotActiveException`: 비활성 메뉴
- `DataIntegrityException`: 데이터 무결성 위반

---

## Workflow 2: 주문 상태 변경 (Order Status Update)

### 목적
관리자가 주문 상태를 변경하는 프로세스

### 입력
- orderId: Long
- newStatus: String ('대기중', '준비중', '완료', '취소')

### 출력
- `OrderResponse`: 업데이트된 주문 정보

### 워크플로우 단계

**Step 1: 주문 조회**
1. Order 조회 (orderId)
2. Order.deleted == false 확인
3. 조회 실패 시 예외 발생: `OrderNotFoundException`

**Step 2: 상태 전이 검증**
1. 현재 상태 확인 (Order.status)
2. 상태 전이 규칙 적용:
   - 현재 상태 == '완료' → 변경 불가 (예외 발생)
   - 현재 상태 != '완료' → 모든 상태로 변경 가능
3. 검증 실패 시 예외 발생: `InvalidStatusTransitionException`

**Step 3: 낙관적 잠금 확인**
1. 요청에 포함된 version과 Order.version 비교
2. version 불일치 시 예외 발생: `OptimisticLockException` (409 Conflict)

**Step 4: 주문 상태 업데이트**
1. Order.status = newStatus
2. Order.version = Order.version + 1
3. Order.updatedAt = 현재 시각
4. Order 업데이트 (OrderMapper.updateOrderStatus)
5. 업데이트 실패 시 (affected rows = 0) 예외 발생: `OptimisticLockException`

**Step 5: SSE 이벤트 전송**
1. ORDER_STATUS_CHANGED 이벤트 생성:
   - orderId: Order.id
   - status: newStatus
   - timestamp: 현재 시각
2. 해당 테이블의 고객에게 전송
   - SSEService.sendEventToClient(tableId, sessionId, event)
3. 해당 매장의 모든 관리자에게 브로드캐스트
   - SSEService.broadcastEventToStore(storeId, event)

**Step 6: 응답 생성**
1. 업데이트된 Order를 OrderResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 4: 단일 트랜잭션
- Step 5: 트랜잭션 외부 (비동기)

### 예외 처리
- `OrderNotFoundException`: 주문 없음
- `InvalidStatusTransitionException`: 잘못된 상태 전이
- `OptimisticLockException`: 동시성 충돌

---

## Workflow 3: 메뉴 등록 (Menu Creation)

### 목적
관리자가 새로운 메뉴를 등록하는 프로세스

### 입력
- `CreateMenuRequest`:
  - storeId: Long
  - name: String
  - price: Integer
  - description: String (optional)
  - category: String
  - image: MultipartFile (optional)

### 출력
- `MenuResponse`: 생성된 메뉴 정보

### 워크플로우 단계

**Step 1: 입력 검증**
1. storeId, name, price, category 필수 값 확인
2. price >= 0 확인
3. 검증 실패 시 예외 발생: `ValidationException`

**Step 2: 이미지 파일 검증 (이미지 있는 경우)**
1. 파일 형식 확인 (JPG, PNG만 허용)
2. 파일 크기 확인 (최대 5MB)
3. 검증 실패 시 예외 발생: `InvalidFileException`

**Step 3: 이미지 파일 업로드 (이미지 있는 경우)**
1. 파일명 생성: `{timestamp}.{extension}`
   - 예: 1707465600000.jpg
2. 파일 저장 경로: `uploads/menus/{filename}`
3. 파일 저장 (FileService.saveFile)
4. 저장된 파일 경로 반환

**Step 4: Menu 엔티티 생성 및 저장**
1. Menu 객체 생성:
   - storeId, name, price, description, category: 요청 값
   - imagePath: 업로드된 파일 경로 (또는 NULL)
   - displayOrder: 0 (기본값)
   - deleted: false
2. Menu 저장 (MenuMapper.insertMenu)
3. 생성된 Menu.id 반환

**Step 5: 응답 생성**
1. Menu를 MenuResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 3 ~ Step 4: 단일 트랜잭션
- 이미지 업로드 실패 시 롤백

### 예외 처리
- `ValidationException`: 입력 검증 실패
- `InvalidFileException`: 파일 검증 실패
- `FileUploadException`: 파일 업로드 실패


---

## Workflow 4: 메뉴 수정 (Menu Update)

### 목적
관리자가 기존 메뉴 정보를 수정하는 프로세스

### 입력
- menuId: Long
- `UpdateMenuRequest`:
  - name: String (optional)
  - price: Integer (optional)
  - description: String (optional)
  - category: String (optional)
  - image: MultipartFile (optional)

### 출력
- `MenuResponse`: 업데이트된 메뉴 정보

### 워크플로우 단계

**Step 1: 메뉴 조회**
1. Menu 조회 (menuId)
2. Menu.deleted == false 확인
3. 조회 실패 시 예외 발생: `MenuNotFoundException`

**Step 2: 입력 검증**
1. price가 제공된 경우 price >= 0 확인
2. 검증 실패 시 예외 발생: `ValidationException`

**Step 3: 이미지 파일 처리 (이미지 변경 시)**
1. 새 이미지 파일 검증 (형식, 크기)
2. 새 이미지 파일 업로드
3. 기존 이미지 파일 삭제 (FileService.deleteFile)
4. 새 파일 경로 저장

**Step 4: Menu 엔티티 업데이트**
1. 제공된 필드만 업데이트:
   - name, price, description, category, imagePath
2. updatedAt = 현재 시각
3. Menu 업데이트 (MenuMapper.updateMenu)

**Step 5: 응답 생성**
1. 업데이트된 Menu를 MenuResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 3 ~ Step 4: 단일 트랜잭션

### 예외 처리
- `MenuNotFoundException`: 메뉴 없음
- `ValidationException`: 입력 검증 실패
- `InvalidFileException`: 파일 검증 실패
- `FileUploadException`: 파일 업로드 실패

---

## Workflow 5: 메뉴 삭제 (Menu Deletion)

### 목적
관리자가 메뉴를 논리적으로 삭제하는 프로세스

### 입력
- menuId: Long

### 출력
- 204 No Content

### 워크플로우 단계

**Step 1: 메뉴 조회**
1. Menu 조회 (menuId)
2. Menu.deleted == false 확인
3. 조회 실패 시 예외 발생: `MenuNotFoundException`

**Step 2: 논리적 삭제**
1. Menu.deleted = true
2. Menu.updatedAt = 현재 시각
3. Menu 업데이트 (MenuMapper.updateMenu)

**Step 3: 응답**
1. 204 No Content 반환

### 트랜잭션 경계
- Step 2: 단일 트랜잭션

### 예외 처리
- `MenuNotFoundException`: 메뉴 없음

### 참고
- 물리적 삭제는 하지 않음 (감사 추적)
- 기존 주문의 OrderItem은 영향받지 않음 (unitPrice, menuName 저장됨)

---

## Workflow 6: 테이블 세션 시작 (Table Session Start)

### 목적
새로운 고객 그룹이 테이블에 착석하여 세션을 시작하는 프로세스

### 입력
- tableId: Long

### 출력
- `TableResponse`: 세션 정보 포함

### 워크플로우 단계

**Step 1: 테이블 조회**
1. Table 조회 (tableId)
2. 조회 실패 시 예외 발생: `TableNotFoundException`

**Step 2: 세션 ID 생성**
1. UUID 생성
2. sessionId = UUID.randomUUID().toString()

**Step 3: 테이블 세션 업데이트**
1. Table.sessionId = 생성된 sessionId
2. Table.sessionStatus = 'ACTIVE'
3. Table.sessionStartTime = 현재 시각
4. Table.updatedAt = 현재 시각
5. Table 업데이트 (TableMapper.updateTable)

**Step 4: 응답 생성**
1. Table을 TableResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 3: 단일 트랜잭션

### 예외 처리
- `TableNotFoundException`: 테이블 없음

---

## Workflow 7: 테이블 세션 종료 (Table Session End)

### 목적
고객 그룹이 퇴장하여 세션을 종료하고 주문을 이력으로 이동하는 프로세스

### 입력
- tableId: Long

### 출력
- `TableResponse`: 초기화된 테이블 정보

### 워크플로우 단계

**Step 1: 테이블 조회**
1. Table 조회 (tableId)
2. Table.sessionStatus == 'ACTIVE' 확인
3. 조회 실패 시 예외 발생: `TableNotFoundException` 또는 `InvalidSessionException`

**Step 2: 현재 세션의 주문 조회**
1. Order 조회 (tableId, sessionId)
2. deleted == false인 주문만 조회
3. OrderItem도 함께 조회 (JOIN)

**Step 3: 주문 이력 생성**
1. 각 Order에 대해:
   - OrderHistory 객체 생성:
     - orderId: Order.id
     - orderNumber, storeId, tableId, sessionId: Order 값 복사
     - orderTime, totalAmount, status: Order 값 복사
     - completedTime: 현재 시각
     - archivedTime: 현재 시각
   - OrderHistory 저장 (OrderHistoryMapper.insertOrderHistory)
   
2. 각 OrderItem에 대해:
   - OrderHistoryItem 객체 생성:
     - orderHistoryId: 생성된 OrderHistory.id
     - menuId, menuName, quantity, unitPrice: OrderItem 값 복사
   - OrderHistoryItem 저장 (OrderHistoryMapper.insertOrderHistoryItem)

**Step 4: 테이블 세션 초기화**
1. Table.sessionId = NULL
2. Table.sessionStatus = 'INACTIVE'
3. Table.sessionStartTime = NULL
4. Table.updatedAt = 현재 시각
5. Table 업데이트 (TableMapper.updateTable)

**Step 5: 응답 생성**
1. Table을 TableResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 3 ~ Step 4: 단일 트랜잭션

### 예외 처리
- `TableNotFoundException`: 테이블 없음
- `InvalidSessionException`: 세션 상태 오류

### 참고
- 원본 Order는 삭제하지 않음 (논리적 삭제도 하지 않음)
- Order는 그대로 유지되며, 조회 시 sessionId로 필터링

---

## Workflow 8: 관리자 로그인 (Admin Login)

### 목적
관리자가 시스템에 로그인하여 JWT 토큰을 발급받는 프로세스

### 입력
- `LoginRequest`:
  - storeId: Long
  - username: String
  - password: String

### 출력
- `LoginResponse`:
  - token: String (JWT)
  - user: UserResponse

### 워크플로우 단계

**Step 1: 입력 검증**
1. storeId, username, password 필수 값 확인
2. 검증 실패 시 예외 발생: `ValidationException`

**Step 2: 사용자 조회**
1. User 조회 (username)
2. User.storeId == request.storeId 확인
3. 조회 실패 시 예외 발생: `InvalidCredentialsException`

**Step 3: 계정 잠금 확인**
1. User.lockedUntil 확인
2. lockedUntil != NULL && lockedUntil > 현재시각 → 계정 잠금 상태
3. 잠금 상태이면 예외 발생: `AccountLockedException`

**Step 4: 비밀번호 검증**
1. bcrypt로 password 검증
2. BCryptPasswordEncoder.matches(request.password, User.password)
3. 검증 실패 시:
   - User.loginAttempts += 1
   - loginAttempts >= 5이면:
     - User.lockedUntil = 현재시각 + 30분
   - User 업데이트
   - 예외 발생: `InvalidCredentialsException`

**Step 5: 로그인 성공 처리**
1. User.loginAttempts = 0
2. User.lockedUntil = NULL
3. User.updatedAt = 현재 시각
4. User 업데이트

**Step 6: JWT 토큰 생성**
1. Claims 생성:
   - userId: User.id
   - username: User.username
   - storeId: User.storeId
   - role: User.role
2. 만료 시간: 현재시각 + 16시간
3. JWT 토큰 생성 (JwtTokenProvider.generateToken)

**Step 7: 응답 생성**
1. LoginResponse 생성:
   - token: 생성된 JWT
   - user: User를 UserResponse로 변환
2. 클라이언트에 반환

### 트랜잭션 경계
- Step 4 ~ Step 5: 단일 트랜잭션

### 예외 처리
- `ValidationException`: 입력 검증 실패
- `InvalidCredentialsException`: 인증 실패
- `AccountLockedException`: 계정 잠금

---

## Workflow 9: 주문 삭제 (Order Deletion)

### 목적
관리자가 주문을 논리적으로 삭제하는 프로세스

### 입력
- orderId: Long

### 출력
- 204 No Content

### 워크플로우 단계

**Step 1: 주문 조회**
1. Order 조회 (orderId)
2. Order.deleted == false 확인
3. 조회 실패 시 예외 발생: `OrderNotFoundException`

**Step 2: 논리적 삭제**
1. Order.deleted = true
2. Order.updatedAt = 현재 시각
3. Order 업데이트 (OrderMapper.updateOrder)

**Step 3: SSE 이벤트 전송**
1. ORDER_DELETED 이벤트 생성:
   - orderId: Order.id
   - timestamp: 현재 시각
2. 해당 매장의 모든 관리자에게 브로드캐스트
3. SSEService.broadcastEventToStore(storeId, event)

**Step 4: 응답**
1. 204 No Content 반환

### 트랜잭션 경계
- Step 2: 단일 트랜잭션
- Step 3: 트랜잭션 외부 (비동기)

### 예외 처리
- `OrderNotFoundException`: 주문 없음

### 참고
- OrderItem은 Order의 논리적 삭제에 따라 함께 처리 (Cascade)
- 물리적 삭제는 하지 않음 (감사 추적)

---

## Workflow 10: SSE 이벤트 전송 (SSE Event Broadcasting)

### 목적
실시간 이벤트를 클라이언트에 전송하는 프로세스

### SSE 연결 관리

**연결 등록**:
1. 클라이언트가 SSE 엔드포인트에 연결
2. clientId 생성 (고객: tableId-sessionId, 관리자: storeId-userId)
3. SseEmitter 생성 (타임아웃: 30초)
4. ConcurrentHashMap에 저장: clientId → SseEmitter
5. 연결 성공 메시지 전송

**연결 해제**:
1. 타임아웃 또는 클라이언트 종료 시
2. ConcurrentHashMap에서 제거
3. SseEmitter.complete() 호출

### 이벤트 전송 방식

**특정 클라이언트에게 전송**:
1. clientId로 SseEmitter 조회
2. SseEmitter.send(event) 호출
3. 전송 실패 시 연결 제거

**매장별 브로드캐스트** (관리자 전용):
1. storeId로 시작하는 모든 clientId 조회
2. 각 SseEmitter에 이벤트 전송
3. 전송 실패한 연결 제거

### 이벤트 타입

**NEW_ORDER**:
- 대상: 관리자
- 데이터: orderId, tableId, totalAmount, timestamp

**ORDER_STATUS_CHANGED**:
- 대상: 고객 + 관리자
- 데이터: orderId, status, timestamp

**ORDER_DELETED**:
- 대상: 관리자
- 데이터: orderId, timestamp

---

## Data Flow Summary

### 주문 생성 플로우
```
Customer Frontend
  → POST /api/customer/orders
  → OrderService.createOrder()
  → OrderMapper.insertOrder()
  → OrderMapper.insertOrderItems()
  → SSEService.broadcastEventToStore() (NEW_ORDER)
  → Admin Frontend (실시간 알림)
```

### 주문 상태 변경 플로우
```
Admin Frontend
  → PUT /api/admin/orders/{id}/status
  → OrderService.updateOrderStatus()
  → OrderMapper.updateOrderStatus() (낙관적 잠금)
  → SSEService.sendEvent() (ORDER_STATUS_CHANGED)
  → Customer Frontend + Admin Frontend (실시간 업데이트)
```

### 세션 종료 플로우
```
Admin Frontend
  → POST /api/admin/tables/{id}/end-session
  → TableService.endSession()
  → OrderMapper.selectOrdersByTableAndSession()
  → OrderHistoryMapper.insertOrderHistory()
  → OrderHistoryMapper.insertOrderHistoryItems()
  → TableMapper.updateTable() (세션 초기화)
```

---

## Notes

- 모든 워크플로우는 트랜잭션 경계가 명확히 정의됨
- SSE 이벤트 전송은 트랜잭션 외부에서 비동기로 처리
- 낙관적 잠금은 Order 상태 변경 시에만 적용
- 논리적 삭제는 Menu, Order에만 적용
- 주문 시점 가격은 OrderItem.unitPrice에 저장하여 불변 유지
- 세션 종료 시 Order는 OrderHistory로 복사되며 원본은 유지

