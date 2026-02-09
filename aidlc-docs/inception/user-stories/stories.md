# User Stories

## 스토리 요약

**총 스토리 수**: 20개
- 고객(Customer) 스토리: 8개
- 관리자(Admin) 스토리: 9개
- 비기능 요구사항(NFR) 스토리: 3개

**구조화 방식**: User Journey-Based (사용자 여정 순서)

**우선순위 분포**:
- MVP: 17개 (핵심 기능)
- P1: 3개 (중요 기능)

---

## Customer Journey: 고객 주문 여정

### US-C-001: 테이블 태블릿 자동 로그인

**As a** 고객 (김민수)  
**I want to** 테이블 태블릿이 자동으로 로그인되어 있기를  
**So that** 별도 로그인 절차 없이 즉시 메뉴를 볼 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: None

**Acceptance Criteria**:
- **Given** 관리자가 테이블 태블릿을 사전 설정했을 때
- **When** 고객이 태블릿 화면을 터치하면
- **Then** 자동으로 로그인되어 메뉴 화면이 표시된다

- **Given** 태블릿이 자동 로그인된 상태일 때
- **When** 페이지를 새로고침하면
- **Then** SessionStorage에 저장된 정보로 다시 자동 로그인된다

**Technical Notes**:
- SessionStorage 사용
- 16시간 세션 유지

---

### US-C-002: 메뉴 카테고리별 조회

**As a** 고객 (김민수)  
**I want to** 메뉴를 카테고리별로 탐색하기를  
**So that** 원하는 메뉴를 빠르게 찾을 수 있다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: US-C-001

**Acceptance Criteria**:
- **Given** 메뉴 화면이 표시되었을 때
- **When** 카테고리 탭을 선택하면
- **Then** 해당 카테고리의 메뉴 목록이 카드 형태로 표시된다

- **Given** 메뉴 목록이 표시되었을 때
- **When** 각 메뉴 카드를 확인하면
- **Then** 메뉴명, 가격, 설명, 이미지가 표시된다

- **Given** 메뉴 화면이 표시되었을 때
- **When** 다른 카테고리로 이동하면
- **Then** 1초 이내에 해당 카테고리 메뉴가 로드된다

**Technical Notes**:
- 터치 친화적 UI (최소 버튼 크기 44x44px)
- 카드 레이아웃

---

### US-C-003: 장바구니에 메뉴 추가

**As a** 고객 (김민수)  
**I want to** 선택한 메뉴를 장바구니에 추가하기를  
**So that** 여러 메뉴를 한 번에 주문할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-C-002

**Acceptance Criteria**:
- **Given** 메뉴 목록이 표시되었을 때
- **When** 메뉴 카드의 "추가" 버튼을 클릭하면
- **Then** 해당 메뉴가 장바구니에 추가되고 시각적 피드백이 표시된다

- **Given** 메뉴가 장바구니에 추가되었을 때
- **When** 장바구니 아이콘을 확인하면
- **Then** 장바구니에 담긴 메뉴 개수가 표시된다

- **Given** 장바구니에 메뉴가 추가되었을 때
- **When** 페이지를 새로고침하면
- **Then** SessionStorage에 저장된 장바구니 내용이 유지된다

**Technical Notes**:
- SessionStorage 사용
- 실시간 총 금액 계산

---

### US-C-004: 장바구니 수량 조절

**As a** 고객 (김민수)  
**I want to** 장바구니에 담긴 메뉴의 수량을 조절하기를  
**So that** 원하는 만큼 주문할 수 있다

**Priority**: MVP  
**Story Points**: 2  
**Dependencies**: US-C-003

**Acceptance Criteria**:
- **Given** 장바구니에 메뉴가 담겨 있을 때
- **When** 수량 증가 버튼을 클릭하면
- **Then** 해당 메뉴의 수량이 1 증가하고 총 금액이 재계산된다

- **Given** 장바구니에 메뉴가 담겨 있을 때
- **When** 수량 감소 버튼을 클릭하면
- **Then** 해당 메뉴의 수량이 1 감소하고 총 금액이 재계산된다

- **Given** 메뉴 수량이 1일 때
- **When** 수량 감소 버튼을 클릭하면
- **Then** 해당 메뉴가 장바구니에서 제거된다

**Technical Notes**:
- 실시간 금액 계산
- 최소 수량 1

---

### US-C-005: 주문 생성

**As a** 고객 (김민수)  
**I want to** 장바구니의 메뉴를 주문하기를  
**So that** 음식을 받을 수 있다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: US-C-003, US-C-004

**Acceptance Criteria**:
- **Given** 장바구니에 메뉴가 담겨 있을 때
- **When** "주문하기" 버튼을 클릭하면
- **Then** 주문 확인 화면이 표시된다

- **Given** 주문 확인 화면이 표시되었을 때
- **When** "확정" 버튼을 클릭하면
- **Then** 주문이 서버로 전송되고 2초 이내에 응답을 받는다

- **Given** 주문이 성공했을 때
- **When** 응답을 받으면
- **Then** 주문 번호가 5초간 표시되고 장바구니가 비워지며 메뉴 화면으로 자동 리다이렉트된다

**Technical Notes**:
- 주문 생성 응답 시간 < 2초
- 주문 정보: 매장 ID, 테이블 ID, 세션 ID, 메뉴 목록, 총 금액

---

### US-C-006: 주문 내역 조회

**As a** 고객 (김민수)  
**I want to** 내가 주문한 내역을 확인하기를  
**So that** 무엇을 주문했는지 알 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-C-005

**Acceptance Criteria**:
- **Given** 주문을 생성했을 때
- **When** "주문 내역" 버튼을 클릭하면
- **Then** 현재 테이블 세션의 주문 목록이 시간 순으로 표시된다

- **Given** 주문 내역이 표시되었을 때
- **When** 각 주문을 확인하면
- **Then** 주문 번호, 주문 시각, 메뉴 목록, 금액, 상태가 표시된다

- **Given** 주문 내역이 표시되었을 때
- **When** 관리자가 주문 상태를 변경하면
- **Then** 실시간으로 상태가 업데이트된다 (선택사항)

**Technical Notes**:
- 현재 세션 주문만 표시
- 페이지네이션 또는 무한 스크롤

---

### US-C-007: 주문 실패 처리

**As a** 고객 (김민수)  
**I want to** 주문 실패 시 명확한 에러 메시지를 받기를  
**So that** 무엇이 잘못되었는지 알고 다시 시도할 수 있다

**Priority**: MVP  
**Story Points**: 2  
**Dependencies**: US-C-005

**Acceptance Criteria**:
- **Given** 주문 확정 버튼을 클릭했을 때
- **When** 서버에서 에러 응답을 받으면
- **Then** 사용자 친화적인 에러 메시지가 표시된다

- **Given** 주문 실패 메시지가 표시되었을 때
- **When** 에러를 확인하면
- **Then** 장바구니 내용이 유지되어 다시 시도할 수 있다

**Technical Notes**:
- 네트워크 에러, 서버 에러, 유효성 검증 에러 구분

---

### US-C-008: 빈 장바구니 주문 방지

**As a** 고객 (김민수)  
**I want to** 장바구니가 비어있을 때 주문 버튼이 비활성화되기를  
**So that** 실수로 빈 주문을 하지 않는다

**Priority**: MVP  
**Story Points**: 1  
**Dependencies**: US-C-003

**Acceptance Criteria**:
- **Given** 장바구니가 비어있을 때
- **When** 장바구니 화면을 확인하면
- **Then** "주문하기" 버튼이 비활성화되어 있다

- **Given** 장바구니에 메뉴가 추가되었을 때
- **When** 장바구니 화면을 확인하면
- **Then** "주문하기" 버튼이 활성화된다

**Technical Notes**:
- 클라이언트 측 유효성 검증

---

## Admin Journey: 관리자 운영 여정

### US-A-001: 관리자 로그인

**As a** 관리자 (박지영)  
**I want to** 매장 관리 시스템에 로그인하기를  
**So that** 주문을 관리할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: None

**Acceptance Criteria**:
- **Given** 로그인 화면이 표시되었을 때
- **When** 매장 식별자, 사용자명, 비밀번호를 입력하고 로그인 버튼을 클릭하면
- **Then** JWT 토큰이 발급되고 LocalStorage에 저장되며 대시보드로 이동한다

- **Given** 로그인에 성공했을 때
- **When** 브라우저를 새로고침하면
- **Then** LocalStorage의 JWT 토큰으로 자동 로그인되어 세션이 유지된다

- **Given** 로그인한 지 16시간이 지났을 때
- **When** API 요청을 하면
- **Then** 자동으로 로그아웃되고 로그인 화면으로 리다이렉트된다

**Technical Notes**:
- JWT 토큰 기반 인증
- bcrypt 비밀번호 해싱
- 16시간 세션 유지

---


### US-A-002: 실시간 주문 모니터링

**As a** 관리자 (박지영)  
**I want to** 들어오는 주문을 실시간으로 확인하기를  
**So that** 빠르게 주문을 처리할 수 있다

**Priority**: MVP  
**Story Points**: 8  
**Dependencies**: US-A-001

**Acceptance Criteria**:
- **Given** 대시보드에 로그인했을 때
- **When** 고객이 주문을 생성하면
- **Then** 2초 이내에 대시보드에 새 주문이 표시된다

- **Given** 대시보드가 표시되었을 때
- **When** 주문 목록을 확인하면
- **Then** 테이블별 카드 형태로 그리드 레이아웃이 표시된다

- **Given** 테이블 카드가 표시되었을 때
- **When** 각 카드를 확인하면
- **Then** 테이블 번호, 총 주문액, 최신 주문 n개 미리보기가 표시된다

- **Given** 신규 주문이 들어왔을 때
- **When** 대시보드를 확인하면
- **Then** 해당 주문이 시각적으로 강조 표시된다 (색상 변경, 애니메이션)

**Technical Notes**:
- Server-Sent Events (SSE) 사용
- 실시간 업데이트 지연 < 2초

---

### US-A-003: 주문 상세 보기

**As a** 관리자 (박지영)  
**I want to** 주문의 전체 메뉴 목록을 상세히 보기를  
**So that** 정확한 주문 내용을 확인할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-A-002

**Acceptance Criteria**:
- **Given** 대시보드에 주문 카드가 표시되었을 때
- **When** 주문 카드를 클릭하면
- **Then** 모달 또는 상세 화면에 전체 메뉴 목록이 표시된다

- **Given** 주문 상세 화면이 표시되었을 때
- **When** 내용을 확인하면
- **Then** 주문 번호, 시각, 테이블 번호, 각 메뉴의 이름/수량/가격, 총 금액이 표시된다

**Technical Notes**:
- 모달 또는 사이드 패널 UI

---

### US-A-004: 주문 상태 변경

**As a** 관리자 (박지영)  
**I want to** 주문 상태를 변경하기를  
**So that** 주문 진행 상황을 추적할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-A-002

**Acceptance Criteria**:
- **Given** 주문이 표시되었을 때
- **When** 상태 변경 버튼을 클릭하면
- **Then** 주문 상태가 "대기중" → "준비중" → "완료"로 변경된다

- **Given** 주문 상태가 변경되었을 때
- **When** 고객이 주문 내역을 확인하면
- **Then** 변경된 상태가 실시간으로 반영된다 (선택사항)

**Technical Notes**:
- 관리자만 상태 변경 가능
- 상태: 대기중, 준비중, 완료

---

### US-A-005: 주문 삭제 (직권 수정)

**As a** 관리자 (박지영)  
**I want to** 잘못된 주문을 삭제하기를  
**So that** 주문 내역을 정확하게 유지할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-A-002

**Acceptance Criteria**:
- **Given** 주문이 표시되었을 때
- **When** 주문 삭제 버튼을 클릭하면
- **Then** 확인 팝업이 표시된다

- **Given** 확인 팝업이 표시되었을 때
- **When** "확인" 버튼을 클릭하면
- **Then** 주문이 즉시 삭제되고 테이블 총 주문액이 재계산된다

- **Given** 주문이 삭제되었을 때
- **When** 결과를 확인하면
- **Then** 성공 또는 실패 피드백이 표시된다

**Technical Notes**:
- 확인 팝업 필수
- 삭제 후 총 주문액 재계산

---

### US-A-006: 테이블 세션 종료 (이용 완료)

**As a** 관리자 (박지영)  
**I want to** 고객이 식사를 마치고 떠날 때 테이블 세션을 종료하기를  
**So that** 다음 고객이 깨끗한 상태로 시작할 수 있다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: US-A-002

**Acceptance Criteria**:
- **Given** 테이블에 주문 내역이 있을 때
- **When** "이용 완료" 버튼을 클릭하면
- **Then** 확인 팝업이 표시된다

- **Given** 확인 팝업이 표시되었을 때
- **When** "확인" 버튼을 클릭하면
- **Then** 해당 세션의 주문 내역이 과거 이력으로 이동하고 테이블 현재 주문 목록 및 총 주문액이 0으로 리셋된다

- **Given** 테이블 세션이 종료되었을 때
- **When** 새 고객이 해당 테이블에서 주문하면
- **Then** 이전 주문 내역 없이 새로운 세션으로 시작된다

**Technical Notes**:
- 주문 이력 OrderHistory 테이블에 저장
- 세션 ID로 주문 그룹화
- 완료 시각 기록

---

### US-A-007: 과거 주문 내역 조회

**As a** 관리자 (박지영)  
**I want to** 과거 주문 내역을 조회하기를  
**So that** 매출 분석 및 이력 관리를 할 수 있다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: US-A-006

**Acceptance Criteria**:
- **Given** 대시보드가 표시되었을 때
- **When** "과거 내역" 버튼을 클릭하면
- **Then** 과거 주문 내역 화면이 표시된다

- **Given** 과거 내역 화면이 표시되었을 때
- **When** 테이블을 선택하면
- **Then** 해당 테이블의 과거 주문 목록이 시간 역순으로 표시된다

- **Given** 과거 주문 목록이 표시되었을 때
- **When** 각 주문을 확인하면
- **Then** 주문 번호, 시각, 메뉴 목록, 총 금액, 매장 이용 완료 시각이 표시된다

- **Given** 과거 내역 화면이 표시되었을 때
- **When** 날짜 필터를 적용하면
- **Then** 해당 기간의 주문만 표시된다

**Technical Notes**:
- 보관 기간: 1년 후 삭제
- 날짜 필터링 기능

---

### US-A-008: 메뉴 관리 (CRUD)

**As a** 관리자 (박지영)  
**I want to** 메뉴를 등록, 수정, 삭제하기를  
**So that** 메뉴를 최신 상태로 유지할 수 있다

**Priority**: MVP  
**Story Points**: 8  
**Dependencies**: US-A-001

**Acceptance Criteria**:
- **Given** 메뉴 관리 화면이 표시되었을 때
- **When** "메뉴 등록" 버튼을 클릭하면
- **Then** 메뉴 등록 폼이 표시된다 (메뉴명, 가격, 설명, 카테고리, 이미지 업로드)

- **Given** 메뉴 등록 폼이 표시되었을 때
- **When** 필수 필드를 입력하고 저장하면
- **Then** 메뉴가 등록되고 메뉴 목록에 표시된다

- **Given** 메뉴 목록이 표시되었을 때
- **When** 메뉴 수정 버튼을 클릭하면
- **Then** 기존 정보가 채워진 수정 폼이 표시된다

- **Given** 메뉴 목록이 표시되었을 때
- **When** 메뉴 삭제 버튼을 클릭하면
- **Then** 확인 팝업 후 메뉴가 삭제된다

- **Given** 메뉴 목록이 표시되었을 때
- **When** 드래그 앤 드롭으로 순서를 변경하면
- **Then** 메뉴 노출 순서가 변경된다

**Technical Notes**:
- 이미지 서버 업로드 및 저장
- 필수 필드 검증
- 가격 범위 검증

---

### US-A-009: 테이블 태블릿 초기 설정

**As a** 관리자 (박지영)  
**I want to** 테이블 태블릿을 초기 설정하기를  
**So that** 고객이 자동 로그인으로 주문할 수 있다

**Priority**: MVP  
**Story Points**: 3  
**Dependencies**: US-A-001

**Acceptance Criteria**:
- **Given** 관리자 대시보드가 표시되었을 때
- **When** "테이블 설정" 버튼을 클릭하면
- **Then** 테이블 설정 화면이 표시된다

- **Given** 테이블 설정 화면이 표시되었을 때
- **When** 테이블 번호와 비밀번호를 입력하고 저장하면
- **Then** 16시간 세션이 생성되고 설정 정보가 저장된다

- **Given** 테이블 설정이 완료되었을 때
- **When** 해당 테이블 태블릿에서 접속하면
- **Then** 자동 로그인이 활성화된다

**Technical Notes**:
- 테이블 번호: 숫자만
- 16시간 세션 생성

---

## Non-Functional Requirements Stories

### US-NFR-001: 성능 요구사항

**As a** 시스템  
**I want to** 빠른 응답 시간을 제공하기를  
**So that** 사용자가 원활하게 서비스를 이용할 수 있다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: All functional stories

**Acceptance Criteria**:
- **Given** 고객이 주문을 생성할 때
- **When** 주문 확정 버튼을 클릭하면
- **Then** 2초 이내에 응답을 받는다

- **Given** 고객이 메뉴를 조회할 때
- **When** 카테고리를 선택하면
- **Then** 1초 이내에 메뉴 목록이 로드된다

- **Given** 관리자가 대시보드를 확인할 때
- **When** 새 주문이 생성되면
- **Then** 2초 이내에 대시보드에 표시된다

- **Given** 시스템이 운영 중일 때
- **When** 동시에 10개 테이블 미만이 접속하면
- **Then** 성능 저하 없이 정상 작동한다

**Technical Notes**:
- 주문 생성 응답 시간 < 2초
- 메뉴 조회 응답 시간 < 1초
- 실시간 업데이트 지연 < 2초
- 동시 접속 지원: 10개 테이블 미만

---

### US-NFR-002: 보안 요구사항

**As a** 시스템  
**I want to** 안전한 인증 및 데이터 보호를 제공하기를  
**So that** 사용자 정보와 주문 데이터가 보호된다

**Priority**: MVP  
**Story Points**: 5  
**Dependencies**: US-A-001, US-C-001

**Acceptance Criteria**:
- **Given** 관리자가 비밀번호를 설정할 때
- **When** 비밀번호가 저장되면
- **Then** bcrypt 해싱으로 안전하게 저장된다

- **Given** 관리자가 로그인할 때
- **When** 인증에 성공하면
- **Then** JWT 토큰이 발급되고 모든 API 요청에 사용된다

- **Given** 관리자가 로그인을 시도할 때
- **When** 연속으로 실패하면
- **Then** 로그인 시도가 제한된다

- **Given** 시스템이 운영 중일 때
- **When** API 통신이 발생하면
- **Then** HTTPS 프로토콜을 사용한다 (프로덕션 환경)

**Technical Notes**:
- bcrypt 비밀번호 해싱
- JWT 토큰 기반 인증
- 로그인 시도 제한
- HTTPS 통신 (프로덕션)

---

### US-NFR-003: 사용성 및 신뢰성 요구사항

**As a** 시스템  
**I want to** 사용하기 쉽고 안정적인 인터페이스를 제공하기를  
**So that** 사용자가 편리하게 서비스를 이용할 수 있다

**Priority**: P1  
**Story Points**: 3  
**Dependencies**: All functional stories

**Acceptance Criteria**:
- **Given** 고객이 태블릿을 사용할 때
- **When** UI 요소를 터치하면
- **Then** 최소 44x44px 크기의 터치 친화적 버튼이 제공된다

- **Given** 사용자가 작업을 수행할 때
- **When** 로딩, 성공, 에러가 발생하면
- **Then** 명확한 시각적 피드백이 표시된다

- **Given** 에러가 발생했을 때
- **When** 사용자가 에러 메시지를 확인하면
- **Then** 사용자 친화적인 에러 메시지가 표시된다

- **Given** 고객이 장바구니에 메뉴를 추가했을 때
- **When** 페이지를 새로고침하면
- **Then** SessionStorage에 저장된 데이터가 유지된다

**Technical Notes**:
- 터치 친화적 UI (최소 44x44px)
- 명확한 시각적 피드백
- 사용자 친화적 에러 메시지
- SessionStorage 데이터 영속성

---

## 스토리 매핑

### 고객(Customer) 페르소나 - 김민수
- US-C-001: 테이블 태블릿 자동 로그인
- US-C-002: 메뉴 카테고리별 조회
- US-C-003: 장바구니에 메뉴 추가
- US-C-004: 장바구니 수량 조절
- US-C-005: 주문 생성
- US-C-006: 주문 내역 조회
- US-C-007: 주문 실패 처리
- US-C-008: 빈 장바구니 주문 방지

### 관리자(Admin) 페르소나 - 박지영
- US-A-001: 관리자 로그인
- US-A-002: 실시간 주문 모니터링
- US-A-003: 주문 상세 보기
- US-A-004: 주문 상태 변경
- US-A-005: 주문 삭제 (직권 수정)
- US-A-006: 테이블 세션 종료 (이용 완료)
- US-A-007: 과거 주문 내역 조회
- US-A-008: 메뉴 관리 (CRUD)
- US-A-009: 테이블 태블릿 초기 설정
- US-NFR-001: 성능 요구사항
- US-NFR-002: 보안 요구사항
- US-NFR-003: 사용성 및 신뢰성 요구사항

---

## INVEST 기준 검증

모든 User Stories는 다음 INVEST 기준을 충족합니다:

- **Independent (독립적)**: 각 스토리는 독립적으로 구현 가능 (의존성은 명시됨)
- **Negotiable (협상 가능)**: 구현 방법은 개발팀과 협의 가능
- **Valuable (가치 있음)**: 각 스토리는 사용자에게 명확한 가치 제공
- **Estimable (추정 가능)**: Story Points로 작업량 추정 가능
- **Small (작음)**: 각 스토리는 중간 단위로 적절한 크기
- **Testable (테스트 가능)**: Given-When-Then 형식의 명확한 Acceptance Criteria

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 승인 대기
