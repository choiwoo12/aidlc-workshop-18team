# Business Rules - Backend

## Overview
Backend 유닛의 비즈니스 규칙을 정의합니다. 각 규칙은 검증 로직, 제약조건, 비즈니스 정책을 포함합니다.

---

## Category 1: 주문 검증 규칙 (Order Validation Rules)

### Rule 1.1: 주문 생성 필수 필드 검증
**규칙**: 주문 생성 시 모든 필수 필드가 제공되어야 함

**검증 항목**:
- storeId: NOT NULL
- tableId: NOT NULL
- sessionId: NOT NULL, UUID 형식
- items: NOT NULL, NOT EMPTY
- items[].menuId: NOT NULL
- items[].quantity: NOT NULL, > 0

**위반 시 처리**:
- 예외: `ValidationException`
- HTTP 상태: 400 Bad Request
- 메시지: "필수 필드가 누락되었습니다: {fieldName}"

---

### Rule 1.2: 테이블 세션 유효성 검증
**규칙**: 주문 생성 시 테이블 세션이 유효해야 함

**검증 항목**:
1. Table 존재 여부
2. Table.storeId == request.storeId
3. Table.sessionId == request.sessionId
4. Table.sessionStatus == 'ACTIVE'

**위반 시 처리**:
- 예외: `InvalidSessionException`
- HTTP 상태: 400 Bad Request
- 메시지: "유효하지 않은 테이블 세션입니다"

---

### Rule 1.3: 메뉴 존재 및 활성 상태 검증
**규칙**: 주문 생성 시 모든 메뉴가 존재하고 활성 상태여야 함

**검증 항목**:
1. Menu 존재 여부 (menuId)
2. Menu.storeId == request.storeId
3. Menu.deleted == false

**위반 시 처리**:
- 예외: `MenuNotFoundException` 또는 `MenuNotActiveException`
- HTTP 상태: 404 Not Found 또는 400 Bad Request
- 메시지: "메뉴를 찾을 수 없거나 비활성 상태입니다: {menuId}"

---

### Rule 1.4: 주문 총액 일관성 검증
**규칙**: 주문 조회 시 저장된 총액과 계산된 총액이 일치해야 함

**검증 로직**:
1. Order.totalAmount 조회
2. OrderItem의 (unitPrice * quantity) 합계 계산
3. 두 값 비교

**불일치 시 처리**:
- 로그 경고: "주문 총액 불일치 감지: orderId={}, stored={}, calculated={}"
- 계산된 값 반환 (데이터 무결성 우선)
- 관리자에게 알림 (선택적)

---

### Rule 1.5: 주문 상태 전이 규칙
**규칙**: 주문 상태 변경 시 허용된 전이만 가능

**허용된 전이**:
- '대기중' → '준비중', '완료', '취소'
- '준비중' → '대기중', '완료', '취소'
- '완료' → 변경 불가
- '취소' → 변경 불가

**위반 시 처리**:
- 예외: `InvalidStatusTransitionException`
- HTTP 상태: 400 Bad Request
- 메시지: "허용되지 않은 상태 전이입니다: {currentStatus} → {newStatus}"

---

## Category 2: 메뉴 검증 규칙 (Menu Validation Rules)

### Rule 2.1: 메뉴 필수 필드 검증
**규칙**: 메뉴 생성/수정 시 필수 필드가 제공되어야 함

**검증 항목** (생성 시):
- storeId: NOT NULL
- name: NOT NULL, 최대 100자
- price: NOT NULL, >= 0
- category: NOT NULL, 최대 50자

**검증 항목** (수정 시):
- 제공된 필드만 검증
- price가 제공된 경우: >= 0

**위반 시 처리**:
- 예외: `ValidationException`
- HTTP 상태: 400 Bad Request
- 메시지: "필수 필드가 누락되었거나 유효하지 않습니다: {fieldName}"

---

### Rule 2.2: 메뉴 가격 범위 검증
**규칙**: 메뉴 가격은 0 이상이어야 함

**검증 로직**:
- price >= 0

**위반 시 처리**:
- 예외: `ValidationException`
- HTTP 상태: 400 Bad Request
- 메시지: "메뉴 가격은 0 이상이어야 합니다"

---

### Rule 2.3: 메뉴 이미지 파일 검증
**규칙**: 메뉴 이미지는 허용된 형식과 크기여야 함

**검증 항목**:
- 파일 형식: JPG, PNG만 허용
- 파일 크기: 최대 5MB
- MIME 타입: image/jpeg, image/png

**위반 시 처리**:
- 예외: `InvalidFileException`
- HTTP 상태: 400 Bad Request
- 메시지: "지원하지 않는 파일 형식이거나 크기가 초과되었습니다"

---

### Rule 2.4: 메뉴 논리적 삭제 규칙
**규칙**: 메뉴 삭제 시 논리적 삭제만 수행

**처리 로직**:
1. Menu.deleted = true 설정
2. 물리적 삭제는 하지 않음
3. 기존 주문의 OrderItem은 영향받지 않음

**조회 시 처리**:
- deleted == false인 메뉴만 반환
- 관리자는 deleted == true인 메뉴도 조회 가능 (선택적)

---

## Category 3: 테이블 세션 규칙 (Table Session Rules)

### Rule 3.1: 테이블 번호 고유성 규칙
**규칙**: 같은 매장 내 테이블 번호는 고유해야 함

**검증 로직**:
- UNIQUE 제약조건: (storeId, tableNumber)

**위반 시 처리**:
- 예외: `DuplicateTableNumberException`
- HTTP 상태: 409 Conflict
- 메시지: "이미 존재하는 테이블 번호입니다: {tableNumber}"

---

### Rule 3.2: 테이블 수 제한 규칙
**규칙**: 매장당 테이블 수는 최대 10개

**검증 로직**:
1. 해당 매장의 테이블 개수 조회
2. 개수 < 10 확인

**위반 시 처리**:
- 예외: `TableLimitExceededException`
- HTTP 상태: 400 Bad Request
- 메시지: "매장당 최대 10개의 테이블만 생성할 수 있습니다"

---

### Rule 3.3: 테이블 PIN 저장 규칙
**규칙**: 테이블 PIN은 SHA-256으로 해싱하여 저장

**처리 로직**:
1. 4자리 PIN 입력 받음
2. SHA-256 해싱 수행
3. 해시값 저장 (64자)

**검증 로직**:
- PIN 길이 == 4
- PIN은 숫자만 허용

**위반 시 처리**:
- 예외: `ValidationException`
- HTTP 상태: 400 Bad Request
- 메시지: "PIN은 4자리 숫자여야 합니다"

---

### Rule 3.4: 세션 ID 생성 규칙
**규칙**: 세션 ID는 UUID 형식으로 생성

**생성 로직**:
- UUID.randomUUID().toString()
- 형식: 550e8400-e29b-41d4-a716-446655440000

**검증 로직**:
- UUID 형식 검증 (36자, 하이픈 포함)

---

### Rule 3.5: 세션 종료 시 주문 이력 이동 규칙
**규칙**: 세션 종료 시 모든 주문을 OrderHistory로 복사

**처리 로직**:
1. 현재 세션의 모든 Order 조회 (deleted == false)
2. 각 Order를 OrderHistory로 복사
3. 각 OrderItem을 OrderHistoryItem으로 복사
4. 원본 Order는 유지 (삭제하지 않음)
5. Table 세션 초기화

**데이터 보관 기간**:
- OrderHistory: 최대 1년

---

## Category 4: 인증 규칙 (Authentication Rules)

### Rule 4.1: 비밀번호 해싱 규칙
**규칙**: 사용자 비밀번호는 bcrypt로 해싱하여 저장

**처리 로직**:
1. 평문 비밀번호 입력 받음
2. bcrypt 해싱 수행 (strength: 10)
3. 해시값 저장 (60자)

**검증 로직**:
- BCryptPasswordEncoder.matches(plainPassword, hashedPassword)

---

### Rule 4.2: 로그인 시도 제한 규칙
**규칙**: 로그인 5회 실패 시 계정 잠금

**처리 로직**:
1. 로그인 실패 시 loginAttempts += 1
2. loginAttempts >= 5이면:
   - lockedUntil = 현재시각 + 30분
3. 로그인 성공 시:
   - loginAttempts = 0
   - lockedUntil = NULL

**잠금 확인**:
- lockedUntil != NULL && lockedUntil > 현재시각 → 잠금 상태

**위반 시 처리**:
- 예외: `AccountLockedException`
- HTTP 상태: 423 Locked
- 메시지: "계정이 잠겼습니다. {unlockTime}에 해제됩니다"

---

### Rule 4.3: JWT 토큰 만료 규칙
**규칙**: JWT 토큰은 16시간 후 만료

**토큰 생성**:
- 만료 시간: 현재시각 + 16시간
- Claims: userId, username, storeId, role

**토큰 검증**:
1. 서명 검증
2. 만료 시간 확인
3. Claims 추출

**만료 시 처리**:
- 예외: `TokenExpiredException`
- HTTP 상태: 401 Unauthorized
- 메시지: "토큰이 만료되었습니다. 다시 로그인해주세요"

---

## Category 5: 파일 업로드 규칙 (File Upload Rules)

### Rule 5.1: 파일 형식 제한 규칙
**규칙**: 메뉴 이미지는 JPG, PNG만 허용

**검증 로직**:
1. 파일 확장자 확인 (.jpg, .jpeg, .png)
2. MIME 타입 확인 (image/jpeg, image/png)

**위반 시 처리**:
- 예외: `InvalidFileException`
- HTTP 상태: 400 Bad Request
- 메시지: "지원하지 않는 파일 형식입니다. JPG 또는 PNG 파일만 업로드 가능합니다"

---

### Rule 5.2: 파일 크기 제한 규칙
**규칙**: 메뉴 이미지는 최대 5MB

**검증 로직**:
- 파일 크기 <= 5MB (5,242,880 bytes)

**위반 시 처리**:
- 예외: `FileSizeExceededException`
- HTTP 상태: 413 Payload Too Large
- 메시지: "파일 크기가 5MB를 초과합니다"

---

### Rule 5.3: 파일명 생성 규칙
**규칙**: 업로드된 파일명은 Timestamp + 확장자 형식

**생성 로직**:
1. 현재 타임스탬프 가져오기 (밀리초)
2. 원본 파일 확장자 추출
3. 파일명 생성: `{timestamp}.{extension}`
4. 예: 1707465600000.jpg

**저장 경로**:
- `uploads/menus/{filename}`

---

## Category 6: 데이터 무결성 규칙 (Data Integrity Rules)

### Rule 6.1: 매장별 데이터 격리 규칙
**규칙**: 모든 데이터는 매장별로 격리되어야 함

**격리 전략**:
- 계층적 격리: Store → Table → Order
- Table.storeId로 매장 식별
- Order.tableId로 테이블 식별
- Menu.storeId로 매장 식별
- User.storeId로 매장 식별

**검증 로직**:
- 주문 생성 시: Table.storeId == Menu.storeId 확인
- 데이터 조회 시: 현재 사용자의 storeId로 필터링

**위반 시 처리**:
- 예외: `DataIntegrityException`
- HTTP 상태: 400 Bad Request
- 메시지: "매장 데이터 불일치가 감지되었습니다"

---

### Rule 6.2: 외래 키 무결성 규칙
**규칙**: 모든 외래 키는 유효한 참조를 가져야 함

**외래 키 목록**:
- Table.storeId → Store.id
- Menu.storeId → Store.id
- Order.storeId → Store.id
- Order.tableId → Table.id
- OrderItem.orderId → Order.id
- OrderItem.menuId → Menu.id
- User.storeId → Store.id

**위반 시 처리**:
- 예외: `ForeignKeyViolationException`
- HTTP 상태: 400 Bad Request
- 메시지: "참조하는 데이터가 존재하지 않습니다"

---

### Rule 6.3: 주문 번호 고유성 규칙
**규칙**: 주문 번호는 전체 시스템에서 고유해야 함

**생성 로직**:
1. 현재 날짜 (YYYYMMDD)
2. 해당 날짜의 주문 개수 조회
3. 순번 = 개수 + 1 (4자리 패딩)
4. 주문 번호 = ORD-{YYYYMMDD}-{NNNN}

**동시성 처리**:
- 주문 번호 생성 시 동기화 (synchronized 또는 DB lock)
- 중복 발생 시 재시도

**위반 시 처리**:
- 예외: `DuplicateOrderNumberException`
- HTTP 상태: 409 Conflict
- 재시도 로직 수행

---

## Category 7: 동시성 제어 규칙 (Concurrency Control Rules)

### Rule 7.1: 주문 상태 변경 낙관적 잠금 규칙
**규칙**: 주문 상태 변경 시 낙관적 잠금 사용

**처리 로직**:
1. Order 조회 (version 포함)
2. 상태 변경
3. version += 1
4. UPDATE ... WHERE id = ? AND version = ?
5. affected rows == 0이면 충돌 발생

**충돌 시 처리**:
- 예외: `OptimisticLockException`
- HTTP 상태: 409 Conflict
- 메시지: "주문 상태가 이미 변경되었습니다. 최신 정보를 확인해주세요"

---

### Rule 7.2: SSE 연결 동시성 규칙
**규칙**: SSE 연결은 ConcurrentHashMap으로 관리

**처리 로직**:
- ConcurrentHashMap<String, SseEmitter> 사용
- clientId를 키로 사용
- 스레드 안전성 보장

**연결 제거**:
- 타임아웃 또는 에러 발생 시 자동 제거
- 명시적 연결 해제 시 제거

---

## Category 8: 에러 처리 규칙 (Error Handling Rules)

### Rule 8.1: 비즈니스 예외 계층 구조
**규칙**: 모든 비즈니스 예외는 계층 구조를 따름

**예외 계층**:
```
BusinessException (추상 클래스)
├── ValidationException
├── NotFoundException
│   ├── OrderNotFoundException
│   ├── MenuNotFoundException
│   └── TableNotFoundException
├── InvalidStateException
│   ├── InvalidSessionException
│   ├── InvalidStatusTransitionException
│   └── AccountLockedException
├── ConflictException
│   ├── OptimisticLockException
│   ├── DuplicateOrderNumberException
│   └── DuplicateTableNumberException
└── FileException
    ├── InvalidFileException
    ├── FileSizeExceededException
    └── FileUploadException
```

---

### Rule 8.2: HTTP 상태 코드 매핑 규칙
**규칙**: 예외 타입에 따라 적절한 HTTP 상태 코드 반환

**매핑 테이블**:
| 예외 타입 | HTTP 상태 | 설명 |
|-----------|-----------|------|
| ValidationException | 400 Bad Request | 입력 검증 실패 |
| NotFoundException | 404 Not Found | 리소스 없음 |
| InvalidStateException | 400 Bad Request | 잘못된 상태 |
| OptimisticLockException | 409 Conflict | 동시성 충돌 |
| DuplicateException | 409 Conflict | 중복 데이터 |
| AccountLockedException | 423 Locked | 계정 잠금 |
| FileException | 400 Bad Request | 파일 처리 오류 |
| FileSizeExceededException | 413 Payload Too Large | 파일 크기 초과 |

---

### Rule 8.3: 에러 응답 형식 규칙
**규칙**: 모든 에러 응답은 표준 형식을 따름

**응답 형식**:
```json
{
  "timestamp": "2026-02-09T14:30:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "필수 필드가 누락되었습니다: storeId",
  "path": "/api/customer/orders"
}
```

**필드 설명**:
- timestamp: 에러 발생 시각 (ISO 8601)
- status: HTTP 상태 코드
- error: HTTP 상태 메시지
- message: 상세 에러 메시지
- path: 요청 경로

---

## Notes

- 모든 비즈니스 규칙은 Service 레이어에서 검증
- 데이터베이스 제약조건은 최후의 방어선
- 예외 메시지는 사용자 친화적이고 명확해야 함
- 보안 관련 에러는 상세 정보 노출 금지
- 모든 규칙 위반은 감사 로그에 기록

