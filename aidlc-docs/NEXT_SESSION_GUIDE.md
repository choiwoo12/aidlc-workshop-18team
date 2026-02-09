# Next Session Guide - Unit 2 Code Generation (In Progress)

## 현재 상태

**Date**: 2026-02-09  
**Current Phase**: CONSTRUCTION  
**Current Unit**: Unit 2 (Customer Order Domain)  
**Current Stage**: Code Generation (Part 2: Generation) - **진행 중** ⏳

---

## 완료된 작업

### Unit 1 (Shared Foundation) - 완전 완료 ✅
모든 설계 및 코드 생성 완료 (약 60개 파일)

### Unit 2 (Customer Order Domain) - 설계 완료, 코드 생성 진행 중 🔄

**설계 단계 (완료)**:
1. **Functional Design** ✅
   - business-rules.md (10개 비즈니스 규칙)
   - business-logic-model.md (6개 비즈니스 플로우)
   - service-methods.md (6개 서비스)

2. **NFR Requirements** ✅
   - nfr-requirements.md (10개 Unit 2 특화 NFR)
   - tech-stack-decisions.md (SSE, 상태 관리 등)

3. **NFR Design** ✅
   - nfr-design-patterns.md (11개 설계 패턴)
   - logical-components.md (11개 컴포넌트)

4. **Infrastructure Design** ✅
   - infrastructure-design.md (Unit 1 인프라 100% 재사용)

**코드 생성 단계 (진행 중)** ⏳:
- **완료**: 4/23 단계
- **남은 작업**: 19/23 단계

---

## 코드 생성 진행 상황

### 완료된 단계 (4/23) ✅

**Backend Service Layer**:
1. ✅ MenuService (`backend/app/services/menu_service.py`)
   - 메뉴 조회, 카테고리 필터링
   
2. ✅ OrderNumberGenerator (`backend/app/utils/order_number_generator.py`)
   - 주문 번호 생성 (T01-001 형식)
   
3. ✅ OrderValidationService (`backend/app/services/order_validation_service.py`)
   - 서버 측 주문 데이터 검증
   
4. ✅ OrderService (`backend/app/services/order_service.py`)
   - 주문 생성, 주문 내역 조회

---

## 남은 작업 (19/23 단계)

### Backend (6단계 남음)
- [ ] Step 5: SSEService - SSE 이벤트 생성 및 브로드캐스트
- [ ] Step 6: MenuController - `/api/menus` 엔드포인트
- [ ] Step 7: OrderController - `/api/orders` 엔드포인트
- [ ] Step 8: SSEController - `/api/sse/orders/{table_id}` 엔드포인트
- [ ] Step 9: Main App Integration - 라우트 추가
- [ ] Step 10: Backend Summary Documentation

### Frontend (12단계 남음)
- [ ] Step 11: MenuService - 메뉴 API 호출
- [ ] Step 12: OrderService - 주문 API 호출
- [ ] Step 13: SSEService - SSE 연결 관리
- [ ] Step 14: CartService - 장바구니 관리
- [ ] Step 15: ValidationService - 클라이언트 검증
- [ ] Step 16: CartContext - 장바구니 전역 상태
- [ ] Step 17: OrderContext - 주문 전역 상태
- [ ] Step 18: MenuPage - 메뉴 목록 화면
- [ ] Step 19: CartPage - 장바구니 화면
- [ ] Step 20: OrderHistoryPage - 주문 내역 화면
- [ ] Step 21: App Integration - 라우트 추가
- [ ] Step 22: Frontend Summary Documentation

### Documentation (1단계 남음)
- [ ] Step 23: Code Summary Documentation

---

## 다음 세션 시작 방법

### 1. 상태 확인
다음 세션 시작 시 다음 명령으로 시작하세요:

```
"이전 세션을 계속하고 싶습니다. Unit 2 Code Generation을 이어서 진행해주세요."
```

### 2. 자동 로드될 파일
- `aidlc-docs/aidlc-state.md` - 현재 워크플로우 상태
- `aidlc-docs/audit.md` - 모든 사용자 입력 및 AI 응답 로그
- `aidlc-docs/construction/plans/unit-2-code-generation-plan.md` - 코드 생성 계획 (체크박스 업데이트됨)

### 3. 다음 단계: Backend 나머지 구현

**Step 5부터 시작**: SSEService 구현

**참조할 문서**:
- Unit 2 NFR Design: `aidlc-docs/construction/unit-2-customer-order-domain/nfr-design/*`
- Unit 2 Functional Design: `aidlc-docs/construction/unit-2-customer-order-domain/functional-design/*`
- Code Generation Plan: `aidlc-docs/construction/plans/unit-2-code-generation-plan.md`

---

## 주요 설계 결정 (참조용)

### Backend 구현
- **SSE**: FastAPI StreamingResponse, Keep-alive 30초
- **주문 번호**: T{테이블번호}-{순차번호} (AUTO_INCREMENT 활용)
- **검증**: 서버 측 상세 검증 (메뉴 판매 가능, 가격 일치, 옵션 유효성)

### Frontend 구현
- **SSE 연결**: 브라우저 EventSource API, 자동 재연결 (최대 3회)
- **장바구니**: SessionStorage, 옵션 순서 무관 비교
- **상태 관리**: React Context API
- **에러 처리**: 기본 메시지, 사용자 친화적

---

## 예상 남은 작업 시간

- **Backend 나머지**: 6단계 (약 30-40분)
- **Frontend 전체**: 12단계 (약 60-80분)
- **Documentation**: 1단계 (약 10분)

**총 예상 시간**: 약 100-130분

---

## 파일 위치 참조

### 생성된 파일 (4개)
- `backend/app/services/menu_service.py`
- `backend/app/utils/order_number_generator.py`
- `backend/app/services/order_validation_service.py`
- `backend/app/services/order_service.py`

### 생성될 파일 위치
- **Backend**: `backend/app/services/`, `backend/app/api/`
- **Frontend**: `frontend/src/services/`, `frontend/src/context/`, `frontend/src/pages/`
- **Documentation**: `aidlc-docs/construction/unit-2-customer-order-domain/code/`

---

## 중요 참고사항

1. **언어**: 한국어로 응답 (기술 용어는 영어)
2. **코드 위치**: 애플리케이션 코드는 workspace root (aidlc-docs/ 제외)
3. **Unit 1 재사용**: Repository, Middleware, Database, 공통 컴포넌트 재사용
4. **체크박스 업데이트**: 각 단계 완료 시 즉시 계획 파일 업데이트

---

**문서 버전**: 2.0  
**작성일**: 2026-02-09  
**다음 세션 시작 시**: 이 파일을 참조하여 Step 5부터 진행
