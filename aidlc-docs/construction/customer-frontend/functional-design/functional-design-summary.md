# Customer Frontend - Functional Design Summary

## Overview
Customer Frontend (Unit 1)의 Functional Design 완료. React + TypeScript + Zustand 기반 SPA 구조.

---

## 설계 문서 목록

1. **data-models.md** - 데이터 모델 및 타입 정의
2. **component-structure.md** - Atomic Design 기반 컴포넌트 계층
3. **routing-and-navigation.md** - 라우팅 및 네비게이션 구조
4. **state-management.md** - Zustand 기반 상태 관리
5. **api-integration.md** - REST API 및 SSE 통합

---

## 핵심 설계 결정

### 기술 스택
- **Framework**: React 18 + TypeScript
- **State Management**: Zustand (persist 미들웨어)
- **HTTP Client**: Axios
- **SSE Client**: EventSource
- **Routing**: React Router v6
- **Styling**: CSS Modules
- **Build Tool**: Vite

---

### 아키텍처 패턴

#### Atomic Design
```
Atoms → Molecules → Organisms → Templates → Pages
```

#### State Management
```
Zustand Stores (Global)
├── CartStore (장바구니)
├── OrderStore (주문)
└── MenuStore (메뉴)
```

#### API Layer
```
Services
├── apiClient (Axios)
├── sseClient (EventSource)
└── api/ (API 함수들)
```

---

## 주요 기능

### 1. 메뉴 조회 및 장바구니
- 메뉴 목록 표시 (Grid 레이아웃)
- 수량 선택 후 장바구니 담기
- 장바구니 상태 localStorage 저장

### 2. 주문 생성
- 장바구니 항목 확인
- 주문 생성 API 호출
- 주문 완료 후 주문내역으로 이동

### 3. 주문 내역 및 실시간 업데이트
- 세션별 주문 내역 조회
- SSE로 실시간 상태 업데이트
- 주문 상세 정보 모달

---

## 컴포넌트 구조

### Pages (3개)
1. **MenuPage** (`/`) - 메뉴 조회
2. **CartPage** (`/cart`) - 장바구니
3. **OrderHistoryPage** (`/orders`) - 주문 내역

### Organisms (4개)
1. **MenuList** - 메뉴 목록
2. **Cart** - 장바구니 전체
3. **OrderHistory** - 주문 내역 목록
4. **OrderDetail** - 주문 상세 모달

### Molecules (4개)
1. **MenuCard** - 메뉴 카드
2. **CartItem** - 장바구니 항목
3. **OrderStatusBadge** - 주문 상태 배지
4. **OrderCard** - 주문 카드

### Atoms (5개)
1. **Button** - 버튼
2. **Input** - 입력 필드
3. **Card** - 카드 컨테이너
4. **Badge** - 배지
5. **Image** - 이미지 (fallback 지원)

---

## 데이터 흐름

### 메뉴 조회 → 주문 생성
```
1. MenuPage 마운트
   ↓
2. MenuStore.fetchMenus(storeId=1)
   ↓
3. GET /api/customer/menus?storeId=1
   ↓
4. MenuList 렌더링
   ↓
5. 사용자가 MenuCard에서 "담기" 클릭
   ↓
6. CartStore.addItem(menu, quantity)
   ↓
7. localStorage에 저장
   ↓
8. CartPage로 이동
   ↓
9. "주문하기" 클릭
   ↓
10. OrderStore.createOrder(request)
    ↓
11. POST /api/customer/orders
    ↓
12. OrderHistoryPage로 이동
```

---

### 실시간 주문 상태 업데이트
```
1. OrderHistoryPage 마운트
   ↓
2. OrderStore.fetchOrders(sessionId)
   ↓
3. GET /api/customer/orders?sessionId=xxx
   ↓
4. OrderStore.subscribeToOrderUpdates(sessionId)
   ↓
5. SSE 연결: /api/sse/subscribe?sessionId=xxx
   ↓
6. ORDER_STATUS_CHANGED 이벤트 수신
   ↓
7. OrderStore.updateOrderStatus(orderId, status)
   ↓
8. UI 자동 업데이트
```

---

## API 엔드포인트

### REST API
1. `GET /api/customer/menus?storeId={storeId}` - 메뉴 조회
2. `POST /api/customer/orders` - 주문 생성
3. `GET /api/customer/orders?sessionId={sessionId}` - 주문 내역 조회

### SSE
1. `/api/sse/subscribe?sessionId={sessionId}` - 실시간 업데이트 구독
   - 이벤트: `ORDER_STATUS_CHANGED`

---

## 상태 관리 전략

### CartStore
- **Persistence**: localStorage (페이지 새로고침 시 유지)
- **Actions**: addItem, removeItem, updateQuantity, clearCart

### OrderStore
- **Persistence**: 없음 (항상 서버에서 최신 데이터)
- **Actions**: fetchOrders, createOrder, subscribeToOrderUpdates

### MenuStore
- **Persistence**: 없음 (항상 서버에서 최신 데이터)
- **Actions**: fetchMenus

---

## 세션 관리

### Session ID
- localStorage에 저장 (`tableorder_session_id`)
- 최초 접속 시 자동 생성
- 주문 생성 및 조회 시 사용

### Table ID
- 고정값 (1) 또는 QR 코드 스캔으로 전달 (향후)

### Store ID
- 고정값 (1) - 단일 매장

---

## 에러 처리

### API 에러
- Toast 메시지로 사용자에게 알림
- 재시도 버튼 제공 (선택)

### SSE 에러
- 연결 실패 시 자동 재연결 (5초 후)
- 사용자에게 알림

### 네트워크 에러
- "네트워크 오류가 발생했습니다" 메시지
- 재시도 버튼

---

## 성능 최적화

### Zustand Selector
```typescript
// ✅ Good: 필요한 부분만 구독
const totalItems = useCartStore(state => state.getTotalItems());
```

### React.memo
- 자주 리렌더링되는 컴포넌트에 적용
- 예: MenuCard, CartItem

### Lazy Loading
- 페이지 컴포넌트 lazy import
- 이미지 lazy loading

---

## 접근성 (Accessibility)

### ARIA Labels
- 버튼: `aria-label` 명시
- 이미지: `alt` 텍스트 필수

### Keyboard Navigation
- Tab 순서 논리적 구성
- Enter/Space로 버튼 활성화

### Color Contrast
- WCAG AA 기준 준수

---

## 반응형 디자인

### Breakpoints
- Mobile: < 768px (기본)
- Tablet: 768px ~ 1024px
- Desktop: > 1024px

### Mobile-First
- 모바일 우선 설계
- 터치 친화적 UI

---

## 다음 단계

### NFR Requirements
- 성능 요구사항 (로딩 시간, 응답 시간)
- 보안 요구사항 (XSS, CSRF 방지)
- UX 요구사항 (접근성, 사용성)

### NFR Design
- 성능 최적화 패턴
- 보안 구현 패턴
- UX 개선 패턴

### Infrastructure Design
- 빌드 설정 (Vite)
- 배포 전략 (정적 파일)
- 환경 변수 관리

### Code Generation
- 실제 코드 생성
- 컴포넌트 구현
- 테스트 코드 작성

---

## 검증 체크리스트

- [x] 데이터 모델 정의 완료
- [x] 컴포넌트 계층 구조 설계 완료
- [x] 라우팅 구조 정의 완료
- [x] 상태 관리 전략 수립 완료
- [x] API 통합 방법 정의 완료
- [x] 에러 처리 전략 수립 완료
- [x] 성능 최적화 방안 수립 완료
- [x] 접근성 고려 완료

---

## Notes

- TypeScript로 타입 안정성 확보
- Atomic Design으로 재사용성 극대화
- Zustand로 간단한 상태 관리
- SSE로 실시간 업데이트 구현
- Mobile-first 반응형 디자인
