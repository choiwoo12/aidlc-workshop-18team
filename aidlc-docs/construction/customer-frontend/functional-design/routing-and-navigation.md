# Customer Frontend - Routing and Navigation

## Overview
React Router를 사용한 클라이언트 사이드 라우팅 구조. 단순하고 직관적인 네비게이션.

---

## Route Structure

```
/                    → MenuPage (메뉴 조회)
/cart                → CartPage (장바구니)
/orders              → OrderHistoryPage (주문 내역)
```

---

## Route Definitions

### Root Route (/)
```typescript
{
  path: '/',
  element: <MenuPage />,
}
```

**기능**:
- 메뉴 목록 표시
- 장바구니 담기
- 기본 랜딩 페이지

**Query Parameters**: 없음 (storeId=1 고정)

---

### Cart Route (/cart)
```typescript
{
  path: '/cart',
  element: <CartPage />,
}
```

**기능**:
- 장바구니 항목 표시
- 수량 조절
- 주문 생성

**State**: CartStore에서 관리

---

### Orders Route (/orders)
```typescript
{
  path: '/orders',
  element: <OrderHistoryPage />,
}
```

**기능**:
- 주문 내역 조회
- 주문 상세 보기
- 실시간 상태 업데이트

**Query Parameters**: 없음 (sessionId는 localStorage에서 관리)

---

## Navigation Methods

### Programmatic Navigation
```typescript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();

// 장바구니로 이동
navigate('/cart');

// 뒤로가기
navigate(-1);
```

---

### Link Component
```typescript
import { Link } from 'react-router-dom';

<Link to="/cart">장바구니</Link>
<Link to="/orders">주문내역</Link>
```

---

## Bottom Navigation

### BottomNavigation Component
```typescript
interface NavItem {
  path: string;
  label: string;
  icon: React.ReactNode;
  badge?: number;
}

const navItems: NavItem[] = [
  { path: '/', label: '메뉴', icon: <MenuIcon /> },
  { path: '/cart', label: '장바구니', icon: <CartIcon />, badge: cartItemCount },
  { path: '/orders', label: '주문내역', icon: <OrderIcon /> },
];
```

**기능**:
- 현재 경로 하이라이트
- 장바구니 배지 (아이템 수)
- 탭 클릭으로 페이지 이동

---

## Session Management

### Session ID
```typescript
// localStorage에 저장
const SESSION_KEY = 'tableorder_session_id';

// 세션 ID 생성 (최초 접속 시)
const generateSessionId = (): string => {
  return `session-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

// 세션 ID 가져오기
const getSessionId = (): string => {
  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem(SESSION_KEY, sessionId);
  }
  return sessionId;
};
```

**용도**:
- 주문 생성 시 sessionId 전달
- 주문 내역 조회 시 sessionId 사용
- SSE 구독 시 sessionId 사용

---

### Table ID
```typescript
// URL Query Parameter 또는 고정값
const TABLE_ID = 1; // 데모용 고정값

// 실제 배포 시:
// const tableId = new URLSearchParams(window.location.search).get('tableId');
```

**용도**:
- 주문 생성 시 tableId 전달
- QR 코드 스캔 시 tableId 전달 (향후)

---

### Store ID
```typescript
// 고정값 (단일 매장)
const STORE_ID = 1;
```

**용도**:
- 메뉴 조회 시 storeId 전달

---

## Route Guards

### No Authentication Required
- Customer Frontend는 인증 불필요
- 세션 ID만으로 주문 관리

---

## Navigation Flow

### 메뉴 조회 → 주문 생성
```
1. MenuPage (/)
   ↓ 메뉴 선택, 장바구니 담기
2. CartPage (/cart)
   ↓ 주문하기 버튼 클릭
3. 주문 생성 API 호출
   ↓ 성공 시
4. OrderHistoryPage (/orders) 자동 이동
```

---

### 주문 내역 조회
```
1. OrderHistoryPage (/orders)
   ↓ 주문 카드 클릭
2. OrderDetail 모달 표시
   ↓ SSE로 실시간 업데이트
3. 상태 변경 시 자동 반영
```

---

## Error Handling

### 404 Not Found
```typescript
{
  path: '*',
  element: <NotFoundPage />,
}
```

**표시**:
- "페이지를 찾을 수 없습니다"
- 홈으로 돌아가기 버튼

---

### API Error
- 에러 발생 시 Toast 메시지 표시
- 네트워크 에러 시 재시도 버튼

---

## Browser History

### History Mode
- `BrowserRouter` 사용 (HTML5 History API)
- 깔끔한 URL (해시 없음)

### Back Button
- 브라우저 뒤로가기 지원
- MainLayout의 뒤로가기 버튼과 동일 동작

---

## Deep Linking

### QR Code Scan (향후)
```
https://tableorder.com/?tableId=5&storeId=1
```

**처리**:
1. Query Parameter에서 tableId, storeId 추출
2. localStorage에 저장
3. MenuPage로 리다이렉트

---

## Notes

- 단순한 3개 페이지 구조
- 인증 불필요 (세션 ID만 사용)
- Bottom Navigation으로 빠른 이동
- 모바일 최적화 (터치 친화적)
