# Backend Functional Design Plan - 테이블오더 서비스

## Plan Overview
Backend 유닛의 상세 비즈니스 로직, 도메인 모델, 비즈니스 규칙을 설계합니다. 이 설계는 기술 독립적이며 순수한 비즈니스 기능에 집중합니다.

---

## Unit Context

### Backend 유닛 책임
- 비즈니스 로직 처리
- 데이터 저장 및 조회
- 인증 및 권한 관리
- REST API 제공
- SSE 실시간 이벤트 전송
- 파일 업로드 처리

### 할당된 스토리
- 총 32개 스토리 (모든 스토리의 백엔드 부분)
- Must Have: 27개
- Should Have: 4개
- Could Have: 1개

---

## Functional Design Methodology

### 1. Domain Model Design
- [ ] 핵심 도메인 엔티티 정의
- [ ] 엔티티 간 관계 정의
- [ ] 엔티티 속성 및 제약조건 정의
- [ ] 값 객체(Value Object) 식별

### 2. Business Logic Modeling
- [ ] 주문 생성 워크플로우 설계
- [ ] 주문 상태 전이 로직 설계
- [ ] 메뉴 관리 워크플로우 설계
- [ ] 테이블 세션 라이프사이클 설계
- [ ] 인증 및 권한 로직 설계
- [ ] 파일 업로드 처리 로직 설계

### 3. Business Rules Definition
- [ ] 주문 검증 규칙 정의
- [ ] 메뉴 검증 규칙 정의
- [ ] 테이블 세션 규칙 정의
- [ ] 인증 규칙 정의
- [ ] 파일 업로드 규칙 정의
- [ ] 데이터 무결성 규칙 정의

### 4. Data Flow Design
- [ ] 주문 생성 데이터 흐름
- [ ] 주문 상태 변경 데이터 흐름
- [ ] 메뉴 CRUD 데이터 흐름
- [ ] 테이블 세션 데이터 흐름
- [ ] 인증 데이터 흐름

### 5. Error Handling Strategy
- [ ] 비즈니스 예외 정의
- [ ] 검증 실패 처리
- [ ] 동시성 충돌 처리
- [ ] 데이터 무결성 위반 처리

---

## Context-Appropriate Questions

다음 질문들에 답변해주시면 더 정확한 Functional Design을 생성할 수 있습니다.


### Q1: 주문 번호 생성 전략
주문 번호를 어떻게 생성할까요?

A) **Auto-increment ID** - 데이터베이스 자동 증가 ID 사용 (1, 2, 3...)
B) **UUID** - 범용 고유 식별자 사용 (예: 550e8400-e29b-41d4-a716-446655440000)
C) **Custom Format** - 사용자 정의 형식 (예: ORD-20260209-0001, 날짜 + 순번)
D) **Timestamp-based** - 타임스탬프 기반 (예: 1707465600000)

[Answer]: C

**Reasoning**: 주문 번호 생성 전략은 주문 추적, 고유성 보장, 사용자 친화성에 영향을 줍니다.

---

### Q2: 주문 상태 전이 규칙
주문 상태 전이에 제약이 있나요?

A) **순차적 전이만 허용** - 대기중 → 준비중 → 완료 순서만 가능 (역방향 불가)
B) **자유로운 전이** - 모든 상태 간 전이 가능 (대기중 ↔ 준비중 ↔ 완료)
C) **일부 제약** - 완료 상태에서는 다른 상태로 변경 불가, 나머지는 자유
D) **취소 특별 처리** - 취소는 완료 제외한 모든 상태에서 가능

[Answer]: C

**Reasoning**: 상태 전이 규칙은 비즈니스 로직의 복잡도와 오류 방지에 영향을 줍니다.

---

### Q3: 주문 총액 계산 시점
주문 총액을 언제 계산하고 저장할까요?

A) **주문 생성 시 계산 및 저장** - Order 엔티티에 totalAmount 저장
B) **실시간 계산** - 조회 시마다 OrderItem에서 계산 (저장 안 함)
C) **둘 다** - 생성 시 저장하고, 조회 시 재계산하여 검증

[Answer]: C

**Reasoning**: 총액 계산 전략은 데이터 무결성과 성능에 영향을 줍니다.

---

### Q4: 메뉴 가격 변경 시 기존 주문 처리
메뉴 가격이 변경되면 이미 생성된 주문의 가격은 어떻게 처리할까요?

A) **OrderItem에 unitPrice 저장** - 주문 생성 시점의 가격을 OrderItem에 저장하여 불변 유지
B) **Menu 참조만** - OrderItem에 menuId만 저장하고 조회 시 현재 Menu 가격 사용
C) **가격 이력 관리** - MenuPriceHistory 테이블로 가격 변경 이력 관리

[Answer]: B

**Reasoning**: 가격 변경 처리는 주문 데이터의 정확성과 감사 추적에 영향을 줍니다.

---

### Q5: 테이블 세션 ID 생성 및 관리
테이블 세션 ID를 어떻게 생성하고 관리할까요?

A) **UUID** - 범용 고유 식별자 사용
B) **Timestamp + TableId** - 타임스탬프와 테이블 ID 조합 (예: 1707465600000-table5)
C) **Auto-increment** - 데이터베이스 자동 증가 ID
D) **Custom Format** - 사용자 정의 형식 (예: SES-20260209-T05-001)

[Answer]: A

**Reasoning**: 세션 ID 생성 전략은 세션 추적과 고유성 보장에 영향을 줍니다.

---

### Q6: 테이블 세션 종료 시 주문 이력 이동 방식
세션 종료 시 주문을 OrderHistory로 어떻게 이동할까요?

A) **Order 데이터 복사** - Order와 OrderItem을 OrderHistory와 OrderHistoryItem으로 복사 후 원본 삭제
B) **상태 플래그** - Order에 archived 플래그 추가하여 논리적 삭제
C) **별도 테이블 없음** - Order에 sessionStatus 필드만 추가하여 구분
D) **이동 없음** - 세션 종료해도 Order는 그대로 유지, 조회 시 필터링만

[Answer]: D

**Reasoning**: 주문 이력 관리 방식은 데이터 구조와 조회 성능에 영향을 줍니다.

---

### Q7: 동시 주문 상태 변경 충돌 처리
여러 관리자가 동시에 같은 주문의 상태를 변경하려고 할 때 어떻게 처리할까요?

A) **낙관적 잠금 (Optimistic Locking)** - version 컬럼 사용, 충돌 시 409 Conflict 응답
B) **비관적 잠금 (Pessimistic Locking)** - 데이터베이스 row lock 사용
C) **Last Write Wins** - 마지막 요청이 이김, 충돌 무시
D) **충돌 처리 없음** - 동시성 제어 없이 모든 요청 처리

[Answer]: C

**Reasoning**: 동시성 제어 전략은 데이터 무결성과 사용자 경험에 영향을 줍니다.
### Q8: 메뉴 삭제 시 기존 주문 처리
메뉴를 삭제하려고 할 때 해당 메뉴가 포함된 주문이 있으면 어떻게 처리할까요?

A) **삭제 불가** - 활성 주문(대기중, 준비중)에 포함된 메뉴는 삭제 불가, 에러 반환
B) **논리적 삭제** - Menu에 deleted 플래그 추가, 실제 삭제는 안 함
C) **강제 삭제** - 주문과 관계없이 삭제 허용
D) **완료된 주문만 확인** - 완료되지 않은 주문에만 포함되어 있으면 삭제 불가

[Answer]: B

**Reasoning**: 메뉴 삭제 정책은 데이터 무결성과 비즈니스 연속성에 영향을 줍니다.

---

### Q9: 파일 업로드 시 파일명 생성 전략
메뉴 이미지 파일을 업로드할 때 파일명을 어떻게 생성할까요?

A) **UUID + 확장자** - 고유 식별자 사용 (예: 550e8400-e29b-41d4-a716-446655440000.jpg)
B) **Timestamp + 확장자** - 타임스탬프 사용 (예: 1707465600000.jpg)
C) **원본 파일명 유지** - 사용자가 업로드한 원본 파일명 그대로 사용
D) **Custom Format** - 사용자 정의 형식 (예: menu-{menuId}-{timestamp}.jpg)

[Answer]: B

**Reasoning**: 파일명 생성 전략은 파일 고유성과 관리 편의성에 영향을 줍니다.

---

### Q10: JWT 토큰 만료 시간 및 갱신 전략
JWT 토큰의 만료 시간과 갱신 방식을 어떻게 설정할까요?

A) **16시간 만료, 갱신 없음** - 토큰 만료 시 재로그인 필요
B) **16시간 만료, Refresh Token 사용** - Access Token(짧은 만료) + Refresh Token(긴 만료)
C) **16시간 만료, 자동 갱신** - 만료 5분 전 자동으로 새 토큰 발급
D) **16시간 만료, 수동 갱신** - 사용자가 "세션 연장" 버튼 클릭 시 갱신

[Answer]: B

**Reasoning**: 토큰 관리 전략은 보안과 사용자 경험에 영향을 줍니다.

---

### Q11: 매장별 데이터 격리 전략
다중 매장 환경에서 데이터를 어떻게 격리할까요?

A) **모든 엔티티에 storeId** - Store, Table, Menu, Order, User 모두 storeId 컬럼 포함
B) **계층적 격리** - Store → Table → Order 계층 구조로 격리
C) **User 기반 격리** - User에 storeId만 있고, 조회 시 User의 storeId로 필터링
D) **격리 없음** - 모든 매장 데이터 공유, 프론트엔드에서만 필터링

[Answer]: B

**Reasoning**: 데이터 격리 전략은 보안과 데이터 무결성에 영향을 줍니다.

---

### Q12: 주문 생성 시 검증 규칙
주문 생성 시 어떤 검증을 수행할까요?

A) **기본 검증만** - 메뉴 존재 여부, 수량 > 0만 확인
B) **세션 검증 포함** - 기본 검증 + 테이블 세션 유효성 확인
C) **재고 검증 포함** - 기본 검증 + 메뉴 재고 확인 (향후 확장 고려)
D) **전체 검증** - 메뉴 존재, 수량, 세션, 매장 일치, 메뉴 활성 상태 모두 확인

[Answer]: D

**Reasoning**: 검증 규칙은 데이터 품질과 비즈니스 로직 복잡도에 영향을 줍니다.

---

### Q13: 테이블 초기 설정 시 PIN 저장 방식
테이블 초기 설정 시 4자리 PIN을 어떻게 저장할까요?

A) **평문 저장** - PIN을 그대로 저장 (간단한 개발 환경)
B) **bcrypt 해싱** - bcrypt로 해싱하여 저장
C) **SHA-256 해싱** - SHA-256으로 해싱하여 저장
D) **암호화** - AES 등으로 암호화하여 저장 (복호화 가능)

[Answer]: C

**Reasoning**: PIN 저장 방식은 보안 수준에 영향을 줍니다.

---

### Q14: SSE 연결 관리 전략
SSE 연결을 어떻게 관리할까요?

A) **In-Memory Map** - ConcurrentHashMap에 clientId → SseEmitter 저장
B) **Redis 기반** - Redis에 연결 정보 저장 (다중 서버 환경 대비)
C) **Database 기반** - 데이터베이스에 연결 정보 저장
D) **연결 관리 없음** - 매 이벤트마다 새로 연결

[Answer]: A

**Reasoning**: SSE 연결 관리 방식은 확장성과 성능에 영향을 줍니다.

---

### Q15: 주문 삭제 시 OrderItem 처리
주문을 삭제할 때 OrderItem은 어떻게 처리할까요?

A) **Cascade Delete** - Order 삭제 시 OrderItem도 자동 삭제
B) **수동 삭제** - OrderItem 먼저 삭제 후 Order 삭제
C) **논리적 삭제** - Order와 OrderItem 모두 deleted 플래그만 설정
D) **이력 이동** - 삭제 전 OrderHistory로 이동 후 삭제

[Answer]: C

**Reasoning**: OrderItem 처리 방식은 데이터 무결성과 감사 추적에 영향을 줍니다.

---

## Mandatory Functional Design Artifacts

### 1. business-logic-model.md
- [x] 주문 생성 워크플로우
- [x] 주문 상태 전이 로직
- [x] 메뉴 관리 워크플로우
- [x] 테이블 세션 라이프사이클
- [x] 인증 및 권한 로직
- [x] 파일 업로드 처리 로직
- [x] SSE 이벤트 전송 로직

### 2. business-rules.md
- [x] 주문 검증 규칙
- [x] 메뉴 검증 규칙
- [x] 테이블 세션 규칙
- [x] 인증 규칙
- [x] 파일 업로드 규칙
- [x] 데이터 무결성 규칙
- [x] 동시성 제어 규칙

### 3. domain-entities.md
- [x] Store 엔티티
- [x] Table 엔티티
- [x] Menu 엔티티
- [x] Order 엔티티
- [x] OrderItem 엔티티
- [x] OrderHistory 엔티티
- [x] User 엔티티
- [x] 엔티티 간 관계 다이어그램
- [x] 엔티티 속성 및 제약조건

---

## Next Steps After Plan Approval

1. 사용자가 모든 [Answer]: 태그를 채움
2. AI가 답변을 분석하고 모호한 부분 확인
3. 필요시 추가 질문으로 명확화
4. 사용자가 계획 승인
5. 승인된 계획에 따라 Functional Design 아티팩트 생성 시작

---

**참고**: 이 계획은 사용자의 답변에 따라 조정될 수 있습니다. 모든 질문에 답변해주시면 최적의 Functional Design을 생성할 수 있습니다.



---

## Follow-up Questions for Clarification

답변을 검토한 결과, 몇 가지 명확화가 필요한 부분이 있습니다.

### FQ1: Q4 답변 명확화 - 메뉴 가격 변경 처리
Q4에서 "B) Menu 참조만"을 선택하셨는데, 이는 주문 생성 후 메뉴 가격이 변경되면 과거 주문의 금액도 변경된다는 의미입니다. 

**문제점**:
- 고객이 주문 시 10,000원이었던 메뉴가 나중에 15,000원으로 변경되면, 과거 주문 내역도 15,000원으로 표시됨
- 주문 총액이 실제 결제 금액과 달라질 수 있음
- 감사 추적(Audit Trail)이 불가능

**재확인 질문**: 정말로 주문 생성 시점의 가격을 저장하지 않고, 항상 현재 메뉴 가격을 참조하시겠습니까?

A) **예, Menu 참조만** - 과거 주문도 현재 가격으로 표시 (가격 변경 시 과거 주문 금액도 변경)
B) **아니오, OrderItem에 unitPrice 저장** - 주문 생성 시점의 가격을 OrderItem에 저장하여 불변 유지

[Answer]: B

---

### FQ2: Q6 답변 명확화 - 주문 이력 관리
Q6에서 "D) 이동 없음"을 선택하셨는데, 이는 OrderHistory 테이블을 사용하지 않는다는 의미입니다.

**확인 사항**:
- User Story 1.4에서 "주문 내역이 OrderHistory로 이동"이라고 명시되어 있음
- User Story 6.2에서 "과거 주문 내역 조회"가 있음
- Domain Model에 OrderHistory 엔티티가 정의되어 있음

**재확인 질문**: OrderHistory 테이블을 사용하지 않고, Order 테이블에서 sessionStatus 필드로만 구분하시겠습니까?

A) **예, Order 테이블만 사용** - OrderHistory 테이블 없이 Order에 sessionStatus 필드 추가
B) **아니오, OrderHistory 사용** - 세션 종료 시 Order 데이터를 OrderHistory로 복사

[Answer]: B

---

### FQ3: Q7 답변 명확화 - 동시성 제어
Q7에서 "C) Last Write Wins"를 선택하셨는데, 이는 동시성 충돌을 무시한다는 의미입니다.

**문제점**:
- User Story 5.5에 "동시 주문 상태 변경 처리"가 Should Have로 정의되어 있음
- Story에서 "충돌 감지 시 '주문 상태가 이미 변경되었습니다' 메시지 표시" 요구
- Last Write Wins는 충돌을 감지하지 못하므로 Story 요구사항 불충족

**재확인 질문**: User Story 5.5의 요구사항을 구현하지 않고, Last Write Wins 방식을 사용하시겠습니까?

A) **예, Last Write Wins** - Story 5.5 구현 안 함 (Should Have이므로 생략 가능)
B) **아니오, 낙관적 잠금 사용** - Story 5.5 요구사항 충족 (version 컬럼 사용)

[Answer]: B

---

### FQ4: Q8과 Q15 답변 일관성 확인
Q8에서 메뉴 삭제 시 "B) 논리적 삭제"를 선택하셨고, Q15에서 주문 삭제 시 "C) 논리적 삭제"를 선택하셨습니다.

**확인 사항**:
- 모든 엔티티(Menu, Order, OrderItem)에 deleted 플래그를 추가하는 것이 맞나요?
- 논리적 삭제된 데이터는 조회 시 자동으로 필터링되나요, 아니면 명시적으로 제외해야 하나요?

**명확화 질문**: 논리적 삭제 전략을 어떻게 적용할까요?

A) **모든 엔티티에 deleted 플래그** - Menu, Order, OrderItem 모두 deleted 컬럼 추가
B) **일부 엔티티만** - Menu와 Order만 deleted 플래그, OrderItem은 Cascade
C) **조회 시 자동 필터링** - MyBatis에서 deleted=false 조건 자동 추가
D) **명시적 필터링** - 각 쿼리에서 deleted=false 조건 명시적으로 추가

[Answer]: B

---

### FQ5: Q10 답변 명확화 - JWT Refresh Token
Q10에서 "B) Refresh Token 사용"을 선택하셨습니다.

**구현 세부사항 확인**:
- Access Token 만료 시간: 얼마로 설정할까요? (예: 1시간, 2시간)
- Refresh Token 만료 시간: 16시간으로 설정할까요?
- Refresh Token 저장 위치: 데이터베이스에 저장할까요, 아니면 클라이언트만 보관할까요?

**명확화 질문**: Refresh Token 구현 세부사항을 어떻게 설정할까요?

A) **Access Token 1시간, Refresh Token 16시간, DB 저장 안 함**
B) **Access Token 2시간, Refresh Token 16시간, DB 저장 안 함**
C) **Access Token 1시간, Refresh Token 16시간, DB에 저장**
D) **Access Token 16시간, Refresh Token 없음** - 단순화 (Q10 답변 변경)

[Answer]: D

---

**참고**: 위 5개 추가 질문에 답변해주시면 모호한 부분이 해결되고 Functional Design 생성을 진행할 수 있습니다.

