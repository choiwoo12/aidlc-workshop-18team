# Unit of Work Story Map - 테이블오더 서비스

## Overview
32개 User Stories를 3개 유닛에 매핑합니다. 각 스토리는 구현 책임이 있는 유닛에 할당되며, 일부 스토리는 여러 유닛에 걸쳐 구현됩니다.

---

## Story Distribution Summary

| Unit | Must Have | Should Have | Could Have | Total |
|------|-----------|-------------|------------|-------|
| **Customer Frontend** | 10 | 0 | 0 | 10 |
| **Admin Frontend** | 12 | 4 | 1 | 17 |
| **Backend** | 27 | 4 | 1 | 32 |

**Note**: 일부 스토리는 여러 유닛에 걸쳐 구현되므로 합계가 32를 초과합니다.

---

## Unit 1: Customer Frontend (10 Stories)

### Feature 1: 인증 및 세션 관리 (1 Story)

#### Story 1.2: 테이블 태블릿 자동 로그인 (Must Have)
- **책임**: 자동 로그인 UI 처리, 세션 정보 로컬 저장소 관리
- **구현 범위**:
  - 앱 시작 시 로컬 저장소에서 세션 정보 로드
  - 세션 유효성 확인 (Backend API 호출)
  - 자동 로그인 성공 시 메뉴 화면으로 리다이렉트
  - 세션 만료 시 관리자 재설정 요청 메시지 표시
- **의존성**: Backend (세션 검증 API)

---

### Feature 2: 메뉴 탐색 및 조회 (2 Stories)

#### Story 2.1: 메뉴 카테고리별 조회 (Must Have)
- **책임**: 메뉴 목록 UI 표시, 카테고리 필터링
- **구현 범위**:
  - MenuPage, MenuList, CategoryTabs, MenuCard 컴포넌트
  - Backend에서 메뉴 데이터 조회 (GET /api/customer/menus)
  - 카테고리별 필터링 로직
  - 터치 친화적 UI (최소 44x44px 버튼)
  - 로딩 상태 및 에러 처리
- **의존성**: Backend (메뉴 조회 API)

#### Story 2.2: 메뉴 상세 정보 확인 (Must Have)
- **책임**: 메뉴 상세 정보 UI 표시
- **구현 범위**:
  - 메뉴 상세 모달 또는 페이지
  - 메뉴명, 가격, 설명, 이미지 표시
  - "장바구니에 추가" 버튼
  - 이미지 로딩 실패 시 기본 이미지 표시
- **의존성**: Backend (메뉴 데이터)


---

### Feature 3: 장바구니 관리 (5 Stories)

#### Story 3.1: 장바구니에 메뉴 추가 (Must Have)
- **책임**: 장바구니 추가 UI 및 로컬 저장소 관리
- **구현 범위**:
  - "장바구니에 추가" 버튼 클릭 처리
  - useCartStore (Zustand) 상태 업데이트
  - localStorage에 장바구니 데이터 저장
  - 장바구니 아이콘 배지 업데이트
- **의존성**: 없음 (로컬 상태 관리)

#### Story 3.2: 장바구니 수량 조절 (Must Have)
- **책임**: 수량 증가/감소 UI 및 상태 관리
- **구현 범위**:
  - CartItem 컴포넌트 (+/- 버튼)
  - useCartStore 수량 업데이트
  - 총 금액 실시간 재계산
  - 수량 0 시 자동 삭제
- **의존성**: 없음 (로컬 상태 관리)

#### Story 3.3: 장바구니에서 메뉴 삭제 (Must Have)
- **책임**: 메뉴 삭제 UI 및 상태 관리
- **구현 범위**:
  - "삭제" 버튼 클릭 처리
  - useCartStore에서 아이템 제거
  - 총 금액 재계산
  - 빈 장바구니 메시지 표시
- **의존성**: 없음 (로컬 상태 관리)

#### Story 3.4: 장바구니 전체 비우기 (Must Have)
- **책임**: 장바구니 전체 비우기 UI 및 상태 관리
- **구현 범위**:
  - "장바구니 비우기" 버튼
  - 확인 팝업
  - useCartStore 전체 초기화
  - localStorage 초기화
- **의존성**: 없음 (로컬 상태 관리)

#### Story 3.5: 장바구니 데이터 지속성 (Must Have)
- **책임**: localStorage 동기화
- **구현 범위**:
  - useCartStore와 localStorage 동기화
  - 페이지 새로고침 시 데이터 복원
  - 데이터 손상 시 초기화 및 알림
- **의존성**: 없음 (로컬 저장소)


---

### Feature 4: 주문 생성 및 관리 (2 Stories)

#### Story 4.1: 주문 생성 (Must Have)
- **책임**: 주문 생성 UI 및 API 호출
- **구현 범위**:
  - "주문하기" 버튼 및 확인 팝업
  - Backend API 호출 (POST /api/customer/orders)
  - 주문 성공 메시지 및 주문 번호 표시
  - 장바구니 자동 비우기
  - 메뉴 화면으로 리다이렉트
  - 에러 처리 (주문 실패 시 장바구니 유지)
- **의존성**: Backend (주문 생성 API)

#### Story 4.2: 주문 내역 조회 (Must Have)
- **책임**: 주문 내역 UI 표시
- **구현 범위**:
  - OrderHistoryPage, OrderHistory 컴포넌트
  - Backend API 호출 (GET /api/customer/orders)
  - 주문 목록 시간 순 표시
  - 주문 번호, 시각, 메뉴, 수량, 금액, 상태 표시
  - 에러 처리
- **의존성**: Backend (주문 조회 API)

#### Story 4.3: 주문 상태 실시간 업데이트 (Must Have)
- **책임**: SSE 연결 및 실시간 업데이트 UI
- **구현 범위**:
  - SSEClient 구현 (EventSource)
  - ORDER_STATUS_CHANGED 이벤트 수신
  - useOrderStore 상태 업데이트
  - 상태 변경 시 시각적 피드백 (색상 변경)
  - SSE 재연결 로직 (3회 시도)
  - 연결 실패 시 알림 및 수동 새로고침 안내
- **의존성**: Backend (SSE 엔드포인트)


---

## Unit 2: Admin Frontend (17 Stories)

### Feature 1: 인증 및 세션 관리 (2 Stories)

#### Story 1.3: 관리자 로그인 (Must Have)
- **책임**: 로그인 UI 및 인증 처리
- **구현 범위**:
  - LoginPage 컴포넌트
  - 로그인 폼 (매장 식별자, 사용자명, 비밀번호)
  - Backend API 호출 (POST /api/auth/login)
  - JWT 토큰 수신 및 저장 (localStorage)
  - useAuthStore 상태 관리
  - 관리자 대시보드로 리다이렉트
  - 에러 처리 (잘못된 인증 정보, 5회 실패 시 잠금)
- **의존성**: Backend (인증 API)

#### Story 1.5: 세션 만료 처리 (Must Have)
- **책임**: 세션 만료 알림 UI 및 처리
- **구현 범위**:
  - 세션 만료 5분 전 경고 팝업
  - "세션 연장" 버튼 (토큰 갱신 API 호출)
  - 세션 만료 시 자동 로그아웃 및 로그인 화면 리다이렉트
  - 에러 처리 (세션 연장 실패)
- **의존성**: Backend (토큰 갱신 API)

---

### Feature 5: 실시간 주문 모니터링 (5 Stories)

#### Story 5.1: 실시간 주문 대시보드 (Must Have)
- **책임**: 주문 모니터링 UI 및 SSE 연결
- **구현 범위**:
  - DashboardPage, OrderDashboard 컴포넌트
  - TableCard 컴포넌트 (테이블별 주문 현황)
  - SSEClient 구현 (NEW_ORDER 이벤트 수신)
  - 신규 주문 시각적 강조 (색상, 애니메이션)
  - 테이블별 총 주문액 표시
  - 최신 주문 3개 미리보기
  - SSE 재연결 로직 (3회 시도)
  - 연결 실패 시 알림 및 수동 새로고침 안내
- **의존성**: Backend (주문 조회 API, SSE 엔드포인트)

#### Story 5.2: 테이블별 주문 상세 보기 (Must Have)
- **책임**: 테이블 주문 상세 UI
- **구성 범위**:
  - 테이블 카드 클릭 시 상세 화면 표시
  - 전체 주문 목록 (메뉴, 수량, 금액, 상태)
  - 시간 순 정렬
  - 에러 처리
- **의존성**: Backend (주문 조회 API)

#### Story 5.3: 주문 상태 변경 (Must Have)
- **책임**: 주문 상태 변경 UI 및 API 호출
- **구현 범위**:
  - StatusDropdown 컴포넌트
  - 상태 변경 버튼 (대기중 → 준비중 → 완료, 취소)
  - Backend API 호출 (PUT /api/admin/orders/{id}/status)
  - 상태 변경 즉시 반영
  - 에러 처리 (상태 변경 실패 시 이전 상태 유지)
- **의존성**: Backend (주문 상태 변경 API)

#### Story 5.4: 테이블별 필터링 (Should Have)
- **책임**: 테이블 필터링 UI
- **구현 범위**:
  - 테이블 번호 필터 드롭다운
  - 필터링 로직 (클라이언트 사이드)
  - 필터 해제 기능
  - 존재하지 않는 테이블 번호 입력 시 알림
- **의존성**: 없음 (클라이언트 사이드 필터링)

#### Story 5.5: 동시 주문 상태 변경 처리 (Should Have)
- **책임**: 동시성 충돌 처리 UI
- **구현 범위**:
  - SSE를 통한 다른 관리자의 상태 변경 실시간 반영
  - 충돌 감지 시 "주문 상태가 이미 변경되었습니다" 메시지
  - 최신 상태로 자동 새로고침
- **의존성**: Backend (SSE 이벤트)


---

### Feature 6: 테이블 관리 (3 Stories)

#### Story 6.1: 주문 삭제 (Must Have)
- **책임**: 주문 삭제 UI 및 API 호출
- **구현 범위**:
  - "삭제" 버튼
  - 확인 팝업
  - Backend API 호출 (DELETE /api/admin/orders/{id})
  - 테이블 총 주문액 재계산
  - 에러 처리
- **의존성**: Backend (주문 삭제 API)

#### Story 6.2: 과거 주문 내역 조회 (Must Have)
- **책임**: 과거 주문 내역 UI
- **구현 범위**:
  - HistoryPage 컴포넌트
  - DataTable 컴포넌트
  - Backend API 호출 (GET /api/admin/history)
  - 주문 번호, 시각, 메뉴, 총 금액, 완료 시각 표시
  - 시간 역순 정렬
  - 에러 처리
- **의존성**: Backend (과거 주문 조회 API)

#### Story 6.3: 날짜별 과거 내역 필터링 (Should Have)
- **책임**: 날짜 필터링 UI
- **구현 범위**:
  - 날짜 범위 선택 (시작 날짜, 종료 날짜)
  - "조회" 버튼
  - 날짜 범위 검증
  - 에러 처리 (종료 날짜가 시작 날짜보다 이전)
- **의존성**: Backend (날짜 필터 파라미터)

---

### Feature 7: 메뉴 관리 (5 Stories)

#### Story 7.1: 메뉴 조회 (Must Have)
- **책임**: 메뉴 목록 UI
- **구현 범위**:
  - MenuManagementPage 컴포넌트
  - DataTable 컴포넌트
  - Backend API 호출 (GET /api/admin/menus)
  - 메뉴 정보 표시 (이름, 가격, 설명, 이미지, 노출 순서)
  - 수정/삭제 버튼
  - 에러 처리
- **의존성**: Backend (메뉴 조회 API)

#### Story 7.2: 메뉴 등록 (Must Have)
- **책임**: 메뉴 등록 UI 및 이미지 업로드
- **구현 범위**:
  - MenuForm 컴포넌트
  - 메뉴 정보 입력 폼 (메뉴명, 가격, 설명, 카테고리)
  - 이미지 업로드 (JPG/PNG, 최대 5MB)
  - 업로드 진행률 표시
  - Backend API 호출 (POST /api/admin/menus, Multipart)
  - 에러 처리 (필수 필드 누락, 파일 형식/크기 초과)
- **의존성**: Backend (메뉴 등록 API)

#### Story 7.3: 메뉴 수정 (Must Have)
- **책임**: 메뉴 수정 UI 및 이미지 업로드
- **구현 범위**:
  - MenuForm 컴포넌트 (수정 모드)
  - 기존 메뉴 정보 로드
  - 이미지 교체 (JPG/PNG, 최대 5MB)
  - 업로드 진행률 표시
  - Backend API 호출 (PUT /api/admin/menus/{id}, Multipart)
  - 에러 처리 (필수 필드 누락, 파일 형식/크기 초과)
- **의존성**: Backend (메뉴 수정 API)

#### Story 7.4: 메뉴 삭제 (Must Have)
- **책임**: 메뉴 삭제 UI
- **구현 범위**:
  - "삭제" 버튼
  - 확인 팝업
  - Backend API 호출 (DELETE /api/admin/menus/{id})
  - 에러 처리
- **의존성**: Backend (메뉴 삭제 API)

#### Story 7.5: 메뉴 노출 순서 조정 (Should Have)
- **책임**: 메뉴 순서 조정 UI
- **구현 범위**:
  - 드래그 앤 드롭 또는 순서 번호 입력
  - Backend API 호출 (PUT /api/admin/menus/{id})
  - 에러 처리 (순서 변경 실패 시 이전 순서 유지)
- **의존성**: Backend (메뉴 수정 API)


---

### Feature 8: 다중 매장 관리 (4 Stories)

#### Story 8.1: 매장 선택 및 전환 (Must Have)
- **책임**: 매장 선택 UI
- **구현 범위**:
  - 매장 선택 드롭다운
  - 매장 전환 시 데이터 새로고침
  - 선택한 매장 정보 세션 저장
  - 에러 처리 (매장 전환 실패)
- **의존성**: Backend (매장 정보 API)

#### Story 8.2: 매장별 메뉴 관리 (Must Have)
- **책임**: 매장별 메뉴 필터링
- **구현 범위**:
  - 선택한 매장의 메뉴만 표시
  - 메뉴 CRUD 작업 시 매장 ID 포함
  - 다른 매장 메뉴에 영향 없음 확인
  - 에러 처리 (매장 선택 없이 메뉴 관리 시도)
- **의존성**: Backend (매장별 메뉴 API)

#### Story 8.3: 매장별 테이블 설정 (Must Have)
- **책임**: 매장별 테이블 필터링
- **구현 범위**:
  - TableManagementPage 컴포넌트
  - 선택한 매장의 테이블만 표시 (최대 10개)
  - 테이블 초기 설정 시 매장 ID 포함
  - 다른 매장 테이블에 영향 없음 확인
  - 에러 처리 (테이블 수 10개 초과)
- **의존성**: Backend (매장별 테이블 API)

#### Story 8.4: 통합 주문 현황 대시보드 (Could Have)
- **책임**: 전체 매장 통합 대시보드 UI
- **구현 범위**:
  - 통합 대시보드 페이지
  - 모든 매장의 주문 현황 표시 (매장별 그룹화)
  - 각 매장의 총 주문 수, 총 매출 표시
  - 특정 매장 클릭 시 상세 화면 이동
  - 에러 처리
- **의존성**: Backend (전체 매장 주문 조회 API)

---

## Unit 3: Backend (32 Stories - All Stories)

### Feature 1: 인증 및 세션 관리 (5 Stories)

#### Story 1.1: 테이블 태블릿 초기 설정 (Must Have)
- **책임**: 테이블 초기 설정 API 및 비즈니스 로직
- **구현 범위**:
  - TableService.setupTable() 메서드
  - TableMapper.insertTable() 또는 updateTable()
  - PIN 생성 및 bcrypt 해싱
  - 세션 ID 생성 (UUID)
  - 16시간 세션 생성
  - 에러 처리 (PIN 4자리 검증)
- **API**: POST /api/admin/tables/setup

#### Story 1.2: 테이블 태블릿 자동 로그인 (Must Have)
- **책임**: 세션 검증 API
- **구현 범위**:
  - TableService.validateSession() 메서드
  - TableMapper.selectTableBySessionId()
  - 세션 만료 확인 (16시간)
  - 에러 처리 (세션 만료)
- **API**: GET /api/customer/session/validate

#### Story 1.3: 관리자 로그인 (Must Have)
- **책임**: 관리자 인증 API 및 JWT 토큰 생성
- **구현 범위**:
  - AuthService.authenticate() 메서드
  - UserMapper.selectUserByUsername()
  - 비밀번호 검증 (bcrypt)
  - JWT 토큰 생성 (JwtTokenProvider)
  - 로그인 시도 횟수 관리 (5회 제한)
  - 에러 처리 (잘못된 인증 정보, 계정 잠금)
- **API**: POST /api/auth/login

#### Story 1.4: 테이블 세션 라이프사이클 관리 (Must Have)
- **책임**: 세션 시작/종료 API 및 비즈니스 로직
- **구현 범위**:
  - TableService.startSession() 메서드
  - TableService.endSession() 메서드
  - OrderMapper.selectOrdersByTableAndSession()
  - OrderHistoryMapper.insertOrderHistory()
  - TableMapper.updateSessionStatus()
  - 테이블 초기화 (주문 목록, 총 주문액 0)
  - 에러 처리 (미결제 주문 경고)
- **API**: POST /api/admin/tables/{id}/start-session, POST /api/admin/tables/{id}/end-session

#### Story 1.5: 세션 만료 처리 (Must Have)
- **책임**: 토큰 갱신 API
- **구현 범위**:
  - AuthService.refreshToken() 메서드
  - JWT 토큰 검증 및 갱신
  - 16시간 연장
  - 에러 처리 (토큰 갱신 실패)
- **API**: POST /api/auth/refresh


---

### Feature 2: 메뉴 탐색 및 조회 (2 Stories)

#### Story 2.1: 메뉴 카테고리별 조회 (Must Have)
- **책임**: 메뉴 조회 API 및 비즈니스 로직
- **구현 범위**:
  - MenuService.getMenus() 메서드
  - MenuMapper.selectMenusByStoreAndCategory()
  - 카테고리별 필터링
  - 노출 순서 정렬
  - 에러 처리
- **API**: GET /api/customer/menus?storeId={storeId}&category={category}

#### Story 2.2: 메뉴 상세 정보 확인 (Must Have)
- **책임**: 메뉴 상세 조회 API
- **구현 범위**:
  - MenuService.getMenuById() 메서드
  - MenuMapper.selectMenuById()
  - 에러 처리 (메뉴 없음)
- **API**: GET /api/customer/menus/{id}

---

### Feature 3: 장바구니 관리 (5 Stories)

**Note**: 장바구니는 프론트엔드에서 로컬 상태로 관리되므로 Backend API 불필요

#### Story 3.1 ~ 3.5: 장바구니 관리 (Must Have)
- **책임**: 없음 (프론트엔드 로컬 상태 관리)
- **구현 범위**: 없음

---

### Feature 4: 주문 생성 및 관리 (3 Stories)

#### Story 4.1: 주문 생성 (Must Have)
- **책임**: 주문 생성 API 및 비즈니스 로직
- **구현 범위**:
  - OrderService.createOrder() 메서드
  - 주문 검증 (메뉴 존재, 테이블 세션 유효성)
  - OrderMapper.insertOrder()
  - OrderMapper.insertOrderItems()
  - 총 금액 계산
  - SSEService.broadcastEventToStore() (NEW_ORDER 이벤트)
  - 트랜잭션 관리
  - 에러 처리 (주문 실패)
- **API**: POST /api/customer/orders

#### Story 4.2: 주문 내역 조회 (Must Have)
- **책임**: 주문 조회 API
- **구현 범위**:
  - OrderService.getOrdersByTableAndSession() 메서드
  - OrderMapper.selectOrdersByTableAndSession()
  - 시간 순 정렬
  - 에러 처리
- **API**: GET /api/customer/orders?tableId={tableId}&sessionId={sessionId}

#### Story 4.3: 주문 상태 실시간 업데이트 (Must Have)
- **책임**: SSE 연결 관리 및 이벤트 전송
- **구현 범위**:
  - SSEController.connectCustomer() 메서드
  - SSEService.registerClient() 메서드
  - SSEService.sendEvent() 메서드 (ORDER_STATUS_CHANGED)
  - 연결 타임아웃 처리
  - 에러 처리 (연결 실패)
- **API**: GET /api/sse/customer?tableId={tableId}&sessionId={sessionId}

---

### Feature 5: 실시간 주문 모니터링 (5 Stories)

#### Story 5.1: 실시간 주문 대시보드 (Must Have)
- **책임**: 주문 조회 API 및 SSE 이벤트 전송
- **구현 범위**:
  - OrderService.getOrdersByStore() 메서드
  - OrderMapper.selectOrdersByStore()
  - SSEController.connectAdmin() 메서드
  - SSEService.broadcastEventToStore() (NEW_ORDER)
  - 에러 처리
- **API**: GET /api/admin/orders?storeId={storeId}, GET /api/sse/admin?storeId={storeId}&token={token}

#### Story 5.2: 테이블별 주문 상세 보기 (Must Have)
- **책임**: 테이블별 주문 조회 API
- **구현 범위**:
  - OrderService.getOrdersByTable() 메서드
  - OrderMapper.selectOrdersByTable()
  - 시간 순 정렬
  - 에러 처리
- **API**: GET /api/admin/orders?storeId={storeId}&tableId={tableId}

#### Story 5.3: 주문 상태 변경 (Must Have)
- **책임**: 주문 상태 변경 API 및 SSE 이벤트 전송
- **구현 범위**:
  - OrderService.updateOrderStatus() 메서드
  - OrderMapper.updateOrderStatus()
  - SSEService.sendEvent() (ORDER_STATUS_CHANGED, 고객 및 관리자)
  - 에러 처리 (상태 변경 실패)
- **API**: PUT /api/admin/orders/{id}/status

#### Story 5.4: 테이블별 필터링 (Should Have)
- **책임**: 없음 (프론트엔드 클라이언트 사이드 필터링)
- **구현 범위**: 없음

#### Story 5.5: 동시 주문 상태 변경 처리 (Should Have)
- **책임**: 낙관적 잠금 및 충돌 감지
- **구현 범위**:
  - OrderMapper에 version 컬럼 추가
  - 낙관적 잠금 (Optimistic Locking)
  - 충돌 감지 시 에러 응답
  - SSE를 통한 최신 상태 브로드캐스트
- **API**: PUT /api/admin/orders/{id}/status (충돌 시 409 Conflict)


---

### Feature 6: 테이블 관리 (3 Stories)

#### Story 6.1: 주문 삭제 (Must Have)
- **책임**: 주문 삭제 API 및 비즈니스 로직
- **구현 범위**:
  - OrderService.deleteOrder() 메서드
  - OrderMapper.deleteOrderItems()
  - OrderMapper.deleteOrder()
  - 테이블 총 주문액 재계산
  - SSEService.broadcastEventToStore() (ORDER_DELETED)
  - 트랜잭션 관리
  - 에러 처리
- **API**: DELETE /api/admin/orders/{id}

#### Story 6.2: 과거 주문 내역 조회 (Must Have)
- **책임**: 과거 주문 조회 API
- **구현 범위**:
  - OrderService.getOrderHistory() 메서드
  - OrderHistoryMapper.selectOrderHistoryByStore()
  - 시간 역순 정렬
  - 최대 1년간 데이터 보관
  - 에러 처리
- **API**: GET /api/admin/history?storeId={storeId}

#### Story 6.3: 날짜별 과거 내역 필터링 (Should Have)
- **책임**: 날짜 필터링 API
- **구현 범위**:
  - OrderHistoryMapper.selectOrderHistoryByDateRange()
  - 날짜 범위 검증
  - 에러 처리 (잘못된 날짜 범위)
- **API**: GET /api/admin/history?storeId={storeId}&startDate={startDate}&endDate={endDate}

---

### Feature 7: 메뉴 관리 (5 Stories)

#### Story 7.1: 메뉴 조회 (Must Have)
- **책임**: 메뉴 조회 API
- **구현 범위**:
  - MenuService.getMenusByStore() 메서드
  - MenuMapper.selectMenusByStore()
  - 카테고리별 그룹화
  - 에러 처리
- **API**: GET /api/admin/menus?storeId={storeId}

#### Story 7.2: 메뉴 등록 (Must Have)
- **책임**: 메뉴 등록 API 및 이미지 업로드
- **구현 범위**:
  - MenuService.createMenu() 메서드
  - 메뉴 정보 검증 (필수 필드, 가격 범위)
  - FileService.saveFile() (이미지 업로드)
  - 파일 검증 (JPG/PNG, 최대 5MB)
  - MenuMapper.insertMenu()
  - 트랜잭션 관리
  - 에러 처리 (필수 필드 누락, 파일 형식/크기 초과)
- **API**: POST /api/admin/menus (Multipart Form Data)

#### Story 7.3: 메뉴 수정 (Must Have)
- **책임**: 메뉴 수정 API 및 이미지 업로드
- **구현 범위**:
  - MenuService.updateMenu() 메서드
  - 메뉴 존재 확인
  - 메뉴 정보 검증
  - FileService.saveFile() (이미지 변경 시)
  - FileService.deleteFile() (기존 이미지 삭제)
  - MenuMapper.updateMenu()
  - 트랜잭션 관리
  - 에러 처리
- **API**: PUT /api/admin/menus/{id} (Multipart Form Data)

#### Story 7.4: 메뉴 삭제 (Must Have)
- **책임**: 메뉴 삭제 API
- **구현 범위**:
  - MenuService.deleteMenu() 메서드
  - 메뉴 존재 확인
  - 활성 주문에 사용 중인지 확인
  - FileService.deleteFile() (이미지 삭제)
  - MenuMapper.deleteMenu()
  - 트랜잭션 관리
  - 에러 처리
- **API**: DELETE /api/admin/menus/{id}

#### Story 7.5: 메뉴 노출 순서 조정 (Should Have)
- **책임**: 메뉴 순서 변경 API
- **구현 범위**:
  - MenuService.updateMenuOrder() 메서드
  - MenuMapper.updateMenu() (displayOrder 필드)
  - 에러 처리
- **API**: PUT /api/admin/menus/{id} (displayOrder 필드 업데이트)

---

### Feature 8: 다중 매장 관리 (4 Stories)

#### Story 8.1: 매장 선택 및 전환 (Must Have)
- **책임**: 매장 정보 조회 API
- **구현 범위**:
  - StoreService.getStores() 메서드 (신규)
  - StoreMapper.selectStores() (신규)
  - 에러 처리
- **API**: GET /api/admin/stores

#### Story 8.2: 매장별 메뉴 관리 (Must Have)
- **책임**: 매장 ID 기반 메뉴 필터링
- **구현 범위**:
  - 모든 메뉴 API에 storeId 파라미터 포함
  - MenuMapper에서 storeId 조건 추가
  - 다른 매장 메뉴 격리 보장
  - 에러 처리
- **API**: 기존 메뉴 API에 storeId 파라미터 추가

#### Story 8.3: 매장별 테이블 설정 (Must Have)
- **책임**: 매장 ID 기반 테이블 필터링
- **구현 범위**:
  - 모든 테이블 API에 storeId 파라미터 포함
  - TableMapper에서 storeId 조건 추가
  - 테이블 수 10개 제한 검증
  - 다른 매장 테이블 격리 보장
  - 에러 처리
- **API**: 기존 테이블 API에 storeId 파라미터 추가

#### Story 8.4: 통합 주문 현황 대시보드 (Could Have)
- **책임**: 전체 매장 주문 조회 API
- **구현 범위**:
  - OrderService.getAllStoresOrders() 메서드
  - OrderMapper.selectOrdersAllStores()
  - 매장별 그룹화
  - 총 주문 수, 총 매출 계산
  - 에러 처리
- **API**: GET /api/admin/orders/all-stores

---

## Cross-Unit Stories

일부 스토리는 여러 유닛에 걸쳐 구현됩니다:

### Story 1.2: 테이블 태블릿 자동 로그인
- **Customer Frontend**: 자동 로그인 UI 및 로컬 저장소 관리
- **Backend**: 세션 검증 API

### Story 1.5: 세션 만료 처리
- **Customer Frontend**: 세션 만료 알림 (고객용)
- **Admin Frontend**: 세션 만료 알림 (관리자용)
- **Backend**: 토큰 갱신 API

### Story 4.3: 주문 상태 실시간 업데이트
- **Customer Frontend**: SSE 연결 및 실시간 업데이트 UI
- **Backend**: SSE 엔드포인트 및 이벤트 전송

### Story 5.1: 실시간 주문 대시보드
- **Admin Frontend**: 주문 모니터링 UI 및 SSE 연결
- **Backend**: 주문 조회 API 및 SSE 이벤트 전송

### Story 5.5: 동시 주문 상태 변경 처리
- **Admin Frontend**: 충돌 처리 UI
- **Backend**: 낙관적 잠금 및 충돌 감지


---

## Story Assignment Validation

### All Stories Assigned
- [x] 모든 32개 스토리가 유닛에 할당됨
- [x] Customer Frontend: 10개 스토리
- [x] Admin Frontend: 17개 스토리
- [x] Backend: 32개 스토리 (모든 스토리의 백엔드 부분)

### Cross-Unit Stories Identified
- [x] 5개 크로스 유닛 스토리 식별됨
- [x] 각 크로스 유닛 스토리의 책임이 명확히 분리됨

### No Orphan Stories
- [x] 할당되지 않은 스토리 없음
- [x] 모든 Must Have 스토리 할당됨
- [x] 모든 Should Have 스토리 할당됨
- [x] 모든 Could Have 스토리 할당됨

---

## Implementation Priority by Unit

### Backend (Unit 3) - Priority 1
**Reason**: 프론트엔드가 의존하는 API 제공

**Phase 1 - Core Infrastructure**:
- Story 1.1, 1.2, 1.3, 1.4, 1.5 (인증 및 세션)
- Story 2.1, 2.2 (메뉴 조회)

**Phase 2 - Order Management**:
- Story 4.1, 4.2, 4.3 (주문 생성 및 조회)
- Story 5.1, 5.2, 5.3 (주문 모니터링 및 상태 변경)

**Phase 3 - Advanced Features**:
- Story 6.1, 6.2, 6.3 (테이블 관리)
- Story 7.1, 7.2, 7.3, 7.4, 7.5 (메뉴 관리)
- Story 8.1, 8.2, 8.3, 8.4 (다중 매장)
- Story 5.4, 5.5 (Should Have)

---

### Customer Frontend (Unit 1) - Priority 2
**Reason**: 고객 여정이 핵심 비즈니스 가치

**Phase 1 - Menu Browsing**:
- Story 1.2 (자동 로그인)
- Story 2.1, 2.2 (메뉴 조회)

**Phase 2 - Cart & Order**:
- Story 3.1, 3.2, 3.3, 3.4, 3.5 (장바구니)
- Story 4.1, 4.2 (주문 생성 및 조회)

**Phase 3 - Real-time Updates**:
- Story 4.3 (실시간 업데이트)

---

### Admin Frontend (Unit 2) - Priority 3
**Reason**: 관리 기능은 고객 기능 이후 필요

**Phase 1 - Authentication & Monitoring**:
- Story 1.3, 1.5 (로그인 및 세션)
- Story 5.1, 5.2, 5.3 (주문 모니터링)

**Phase 2 - Order & Table Management**:
- Story 6.1, 6.2 (주문 삭제, 과거 내역)

**Phase 3 - Menu Management**:
- Story 7.1, 7.2, 7.3, 7.4 (메뉴 CRUD)

**Phase 4 - Advanced Features**:
- Story 8.1, 8.2, 8.3 (다중 매장)
- Story 5.4, 5.5, 6.3, 7.5, 8.4 (Should Have, Could Have)

---

## Notes

- Backend는 모든 스토리의 API 및 비즈니스 로직을 담당
- Customer Frontend는 고객 관련 10개 스토리 담당
- Admin Frontend는 관리자 관련 17개 스토리 담당
- 장바구니 관련 5개 스토리는 프론트엔드 로컬 상태로만 관리 (Backend API 불필요)
- 크로스 유닛 스토리는 각 유닛의 책임이 명확히 분리됨
- 개발 순서는 Backend → Customer Frontend → Admin Frontend 권장
- Must Have 스토리 우선 구현, Should Have 및 Could Have는 이후 추가

