# Customer Frontend - Component Structure

## Overview
Atomic Design 패턴을 적용한 컴포넌트 계층 구조. 재사용성과 유지보수성을 고려한 설계.

---

## Component Hierarchy

```
src/
├── atoms/              # 최소 단위 컴포넌트
├── molecules/          # Atoms 조합
├── organisms/          # Molecules 조합
├── templates/          # 페이지 레이아웃
└── pages/              # 라우팅 페이지
```

---

## Atoms (원자 컴포넌트)

### Button
```typescript
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  fullWidth?: boolean;
}
```

**용도**: 모든 버튼 UI
**예시**: "주문하기", "장바구니 담기", "취소"

---

### Input
```typescript
interface InputProps {
  type?: 'text' | 'number' | 'password';
  value: string | number;
  onChange: (value: string | number) => void;
  placeholder?: string;
  disabled?: boolean;
  error?: string;
}
```

**용도**: 텍스트/숫자 입력
**예시**: 수량 입력

---

### Card
```typescript
interface CardProps {
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
}
```

**용도**: 카드 형태 컨테이너
**예시**: 메뉴 카드, 주문 카드

---

### Badge
```typescript
interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'danger' | 'info';
}
```

**용도**: 상태 표시
**예시**: "준비중", "완료", "취소됨"

---

### Image
```typescript
interface ImageProps {
  src: string | null;
  alt: string;
  fallback?: string;
  width?: string | number;
  height?: string | number;
}
```

**용도**: 이미지 표시 (fallback 지원)
**예시**: 메뉴 이미지

---

## Molecules (분자 컴포넌트)

### MenuCard
```typescript
interface MenuCardProps {
  menu: Menu;
  onAddToCart: (menu: Menu, quantity: number) => void;
}
```

**구성**:
- Image (메뉴 이미지)
- 메뉴명 (텍스트)
- 가격 (텍스트)
- Input (수량)
- Button (장바구니 담기)

**용도**: 메뉴 항목 표시 및 장바구니 추가

---

### CartItem
```typescript
interface CartItemProps {
  item: CartItem;
  onUpdateQuantity: (menuId: number, quantity: number) => void;
  onRemove: (menuId: number) => void;
}
```

**구성**:
- Image (메뉴 이미지)
- 메뉴명, 가격 (텍스트)
- Input (수량 조절)
- Button (삭제)

**용도**: 장바구니 항목 표시 및 수정

---

### OrderStatusBadge
```typescript
interface OrderStatusBadgeProps {
  status: OrderStatus;
}
```

**구성**:
- Badge (상태별 색상)

**용도**: 주문 상태 표시

**매핑**:
- PENDING → 'warning' (주황)
- CONFIRMED → 'info' (파랑)
- PREPARING → 'info' (파랑)
- READY → 'success' (초록)
- COMPLETED → 'success' (초록)
- CANCELLED → 'danger' (빨강)

---

### OrderCard
```typescript
interface OrderCardProps {
  order: Order;
  onClick?: () => void;
}
```

**구성**:
- Card (컨테이너)
- 주문번호, 시간 (텍스트)
- OrderStatusBadge
- 총 금액 (텍스트)

**용도**: 주문 요약 표시

---

## Organisms (유기체 컴포넌트)

### MenuList
```typescript
interface MenuListProps {
  menus: Menu[];
  onAddToCart: (menu: Menu, quantity: number) => void;
  isLoading?: boolean;
}
```

**구성**:
- MenuCard[] (그리드 레이아웃)
- 로딩 스피너
- 빈 상태 메시지

**용도**: 메뉴 목록 표시

---

### Cart
```typescript
interface CartProps {
  items: CartItem[];
  onUpdateQuantity: (menuId: number, quantity: number) => void;
  onRemove: (menuId: number) => void;
  onCheckout: () => void;
  totalAmount: number;
}
```

**구성**:
- CartItem[] (리스트)
- 총 금액 표시
- Button (주문하기)
- 빈 장바구니 메시지

**용도**: 장바구니 전체 UI

---

### OrderHistory
```typescript
interface OrderHistoryProps {
  orders: Order[];
  onOrderClick?: (order: Order) => void;
  isLoading?: boolean;
}
```

**구성**:
- OrderCard[] (리스트)
- 로딩 스피너
- 빈 상태 메시지

**용도**: 주문 내역 목록 표시

---

### OrderDetail
```typescript
interface OrderDetailProps {
  order: Order;
  onClose: () => void;
}
```

**구성**:
- 주문번호, 시간
- OrderStatusBadge
- OrderItem[] (상세 항목)
- 총 금액
- Button (닫기)

**용도**: 주문 상세 정보 모달

---

## Templates (템플릿)

### MainLayout
```typescript
interface MainLayoutProps {
  children: React.ReactNode;
  title?: string;
  showBackButton?: boolean;
  onBack?: () => void;
}
```

**구성**:
- Header (제목, 뒤로가기)
- Main Content (children)
- Footer (네비게이션)

**용도**: 공통 레이아웃

---

### BottomNavigation
```typescript
interface BottomNavigationProps {
  currentPath: string;
}
```

**구성**:
- 메뉴 탭
- 장바구니 탭 (배지: 아이템 수)
- 주문내역 탭

**용도**: 하단 네비게이션 바

---

## Pages (페이지)

### MenuPage
```typescript
// Path: /
```

**구성**:
- MainLayout
- MenuList

**기능**:
- 메뉴 목록 조회 (storeId=1 고정)
- 장바구니 담기
- 장바구니로 이동

---

### CartPage
```typescript
// Path: /cart
```

**구성**:
- MainLayout
- Cart

**기능**:
- 장바구니 항목 표시
- 수량 조절
- 항목 삭제
- 주문 생성

---

### OrderHistoryPage
```typescript
// Path: /orders
```

**구성**:
- MainLayout
- OrderHistory
- OrderDetail (모달)

**기능**:
- 주문 내역 조회
- 주문 상세 보기
- 실시간 상태 업데이트 (SSE)

---

## Component Communication

### Props Down, Events Up
- 부모 → 자식: Props로 데이터 전달
- 자식 → 부모: Callback 함수로 이벤트 전달

### Global State (Zustand)
- CartStore: 장바구니 상태
- OrderStore: 주문 상태
- MenuStore: 메뉴 상태

### Example Flow
```
MenuPage
  ↓ (menus from MenuStore)
MenuList
  ↓ (menu prop)
MenuCard
  ↓ (onAddToCart callback)
CartStore.addItem()
```

---

## Styling Strategy

### CSS Modules
- 각 컴포넌트마다 `.module.css` 파일
- 클래스명 충돌 방지
- 예: `Button.module.css`, `MenuCard.module.css`

### Responsive Design
- Mobile-first 접근
- Breakpoints:
  - Mobile: < 768px
  - Tablet: 768px ~ 1024px
  - Desktop: > 1024px

---

## Accessibility

### ARIA Labels
- 버튼: `aria-label` 명시
- 이미지: `alt` 텍스트 필수
- 폼: `label` 연결

### Keyboard Navigation
- Tab 순서 논리적 구성
- Enter/Space로 버튼 활성화

### Color Contrast
- WCAG AA 기준 준수
- 텍스트 대비율 4.5:1 이상

---

## Notes

- 모든 컴포넌트는 TypeScript로 작성
- Props는 인터페이스로 명시적 정의
- 재사용 가능한 컴포넌트 우선 설계
- 상태는 최소한으로 유지 (Zustand 활용)
