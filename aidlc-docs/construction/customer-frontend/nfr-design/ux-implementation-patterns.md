# Customer Frontend - UX Implementation Patterns

## Overview
사용자 경험 요구사항을 충족하기 위한 구체적인 구현 패턴 및 방법.

---

## 피드백 시스템

### Toast Notifications
**패턴**: 사용자 액션에 즉각적인 피드백

**구현**:
```typescript
// src/utils/toast.ts
import { toast as reactToast, ToastOptions } from 'react-toastify';

const defaultOptions: ToastOptions = {
  position: 'top-center',
  autoClose: 3000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
};

export const toast = {
  success: (message: string) => {
    reactToast.success(message, defaultOptions);
  },

  error: (message: string) => {
    reactToast.error(message, defaultOptions);
  },

  info: (message: string) => {
    reactToast.info(message, defaultOptions);
  },

  warning: (message: string) => {
    reactToast.warning(message, defaultOptions);
  },
};
```

**사용**:
```typescript
// 장바구니 담기
const handleAddToCart = () => {
  addItem(menu, quantity);
  toast.success('장바구니에 담았습니다');
};

// 주문 생성
try {
  await createOrder(request);
  toast.success('주문이 완료되었습니다');
  navigate('/orders');
} catch (error) {
  toast.error('주문 생성에 실패했습니다');
}
```

---

### Loading States
**패턴**: 로딩 중 명확한 표시

**구현**:
```typescript
// src/components/LoadingSpinner.tsx
export function LoadingSpinner({ size = 'medium' }: { size?: 'small' | 'medium' | 'large' }) {
  const sizeClass = {
    small: 'w-4 h-4',
    medium: 'w-8 h-8',
    large: 'w-12 h-12',
  }[size];

  return (
    <div className="flex justify-center items-center">
      <div className={`${sizeClass} border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin`} />
    </div>
  );
}

// src/components/SkeletonLoader.tsx
export function SkeletonLoader() {
  return (
    <div className="animate-pulse">
      <div className="h-48 bg-gray-200 rounded mb-4" />
      <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-200 rounded w-1/2" />
    </div>
  );
}
```

**사용**:
```typescript
function MenuPage() {
  const { menus, isLoading } = useMenuStore();

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 gap-4">
        {[...Array(6)].map((_, i) => (
          <SkeletonLoader key={i} />
        ))}
      </div>
    );
  }

  return <MenuList menus={menus} />;
}
```

---

## 접근성 구현

### Keyboard Navigation
**패턴**: 키보드만으로 모든 기능 사용 가능

**구현**:
```typescript
// src/atoms/Button.tsx
interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  ariaLabel?: string;
}

export function Button({ children, onClick, disabled, ariaLabel }: ButtonProps) {
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick?.();
    }
  };

  return (
    <button
      onClick={onClick}
      onKeyDown={handleKeyDown}
      disabled={disabled}
      aria-label={ariaLabel}
      className="focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      {children}
    </button>
  );
}
```

---

### ARIA Labels
**패턴**: 스크린 리더를 위한 레이블

**구현**:
```typescript
// src/molecules/MenuCard.tsx
export function MenuCard({ menu, onAddToCart }: MenuCardProps) {
  return (
    <article aria-labelledby={`menu-${menu.id}`}>
      <img
        src={menu.imageUrl || '/placeholder.png'}
        alt={`${menu.name} 이미지`}
      />
      <h3 id={`menu-${menu.id}`}>{menu.name}</h3>
      <p aria-label="가격">{menu.price}원</p>
      
      <label htmlFor={`quantity-${menu.id}`} className="sr-only">
        수량
      </label>
      <input
        id={`quantity-${menu.id}`}
        type="number"
        aria-label="수량"
        aria-describedby={`quantity-help-${menu.id}`}
      />
      <span id={`quantity-help-${menu.id}`} className="sr-only">
        1개에서 99개까지 선택 가능합니다
      </span>
      
      <button
        onClick={() => onAddToCart(menu, quantity)}
        aria-label={`${menu.name} 장바구니에 담기`}
      >
        담기
      </button>
    </article>
  );
}
```

---

### Focus Management
**패턴**: 포커스 상태 관리

**구현**:
```typescript
// src/organisms/OrderDetailModal.tsx
import { useEffect, useRef } from 'react';

export function OrderDetailModal({ order, onClose }: OrderDetailModalProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    // Save previous focus
    previousFocusRef.current = document.activeElement as HTMLElement;

    // Focus close button
    closeButtonRef.current?.focus();

    // Trap focus within modal
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      // Restore previous focus
      previousFocusRef.current?.focus();
    };
  }, [onClose]);

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <h2 id="modal-title">주문 상세</h2>
      {/* ... */}
      <button
        ref={closeButtonRef}
        onClick={onClose}
        aria-label="닫기"
      >
        닫기
      </button>
    </div>
  );
}
```

---

## 반응형 디자인

### Responsive Grid
**패턴**: 화면 크기에 따른 그리드 레이아웃

**구현**:
```css
/* src/organisms/MenuList.module.css */
.menuGrid {
  display: grid;
  gap: 1rem;
  
  /* Mobile: 1 column */
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  /* Tablet: 2 columns */
  .menuGrid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  /* Desktop: 3 columns */
  .menuGrid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

### Touch-Friendly UI
**패턴**: 터치 친화적 인터페이스

**구현**:
```css
/* src/atoms/Button.module.css */
.button {
  /* Minimum touch target: 44x44px */
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px;
  
  /* Touch feedback */
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0.1);
  touch-action: manipulation;
}

.button:active {
  transform: scale(0.98);
}
```

---

### Responsive Images
**패턴**: 화면 크기에 맞는 이미지

**구현**:
```typescript
// src/atoms/Image.tsx
export function Image({ src, alt }: ImageProps) {
  return (
    <picture>
      <source
        media="(max-width: 640px)"
        srcSet={`${src}?w=400 1x, ${src}?w=800 2x`}
      />
      <source
        media="(min-width: 641px)"
        srcSet={`${src}?w=800 1x, ${src}?w=1600 2x`}
      />
      <img
        src={src}
        alt={alt}
        loading="lazy"
        className="w-full h-auto"
      />
    </picture>
  );
}
```

---

## 에러 처리

### Error States
**패턴**: 에러 상태 명확히 표시

**구현**:
```typescript
// src/components/ErrorState.tsx
interface ErrorStateProps {
  message: string;
  onRetry?: () => void;
}

export function ErrorState({ message, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8">
      <svg className="w-16 h-16 text-red-500 mb-4" /* ... */>
        {/* Error icon */}
      </svg>
      <p className="text-gray-700 mb-4">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          다시 시도
        </button>
      )}
    </div>
  );
}
```

**사용**:
```typescript
function MenuPage() {
  const { menus, isLoading, error, fetchMenus } = useMenuStore();

  if (error) {
    return (
      <ErrorState
        message={error}
        onRetry={() => fetchMenus(1)}
      />
    );
  }

  // ...
}
```

---

### Empty States
**패턴**: 빈 상태 안내

**구현**:
```typescript
// src/components/EmptyState.tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({ icon, title, description, action }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center">
      {icon && <div className="mb-4">{icon}</div>}
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      {description && <p className="text-gray-600 mb-4">{description}</p>}
      {action && (
        <button
          onClick={action.onClick}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          {action.label}
        </button>
      )}
    </div>
  );
}
```

**사용**:
```typescript
function CartPage() {
  const items = useCartStore(state => state.items);
  const navigate = useNavigate();

  if (items.length === 0) {
    return (
      <EmptyState
        icon={<CartIcon className="w-16 h-16 text-gray-400" />}
        title="장바구니가 비어있습니다"
        description="메뉴를 담아보세요"
        action={{
          label: '메뉴 보러가기',
          onClick: () => navigate('/'),
        }}
      />
    );
  }

  // ...
}
```

---

## 애니메이션

### Page Transitions
**패턴**: 부드러운 페이지 전환

**구현**:
```css
/* src/App.css */
.page-enter {
  opacity: 0;
  transform: translateX(20px);
}

.page-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition: opacity 300ms, transform 300ms;
}

.page-exit {
  opacity: 1;
}

.page-exit-active {
  opacity: 0;
  transition: opacity 300ms;
}
```

```typescript
// src/App.tsx
import { CSSTransition, TransitionGroup } from 'react-transition-group';

function App() {
  const location = useLocation();

  return (
    <TransitionGroup>
      <CSSTransition
        key={location.pathname}
        classNames="page"
        timeout={300}
      >
        <Routes location={location}>
          {/* routes */}
        </Routes>
      </CSSTransition>
    </TransitionGroup>
  );
}
```

---

### Button Feedback
**패턴**: 버튼 클릭 피드백

**구현**:
```css
/* src/atoms/Button.module.css */
.button {
  transition: all 150ms ease-in-out;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}
```

---

### Loading Animations
**패턴**: 로딩 애니메이션

**구현**:
```css
/* src/components/LoadingSpinner.module.css */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.skeleton {
  animation: pulse 1.5s ease-in-out infinite;
}
```

---

## 오프라인 지원

### Network Status Detection
**패턴**: 네트워크 상태 감지

**구현**:
```typescript
// src/hooks/useNetworkStatus.ts
import { useState, useEffect } from 'react';

export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => {
      setIsOnline(true);
      toast.success('인터넷 연결이 복구되었습니다');
    };

    const handleOffline = () => {
      setIsOnline(false);
      toast.warning('인터넷 연결이 끊어졌습니다');
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}
```

**사용**:
```typescript
function App() {
  const isOnline = useNetworkStatus();

  return (
    <div>
      {!isOnline && (
        <div className="bg-yellow-100 p-2 text-center">
          오프라인 상태입니다
        </div>
      )}
      {/* ... */}
    </div>
  );
}
```

---

## 디자인 시스템

### Color Palette
**패턴**: 일관된 색상 사용

**구현**:
```css
/* src/styles/colors.css */
:root {
  --color-primary: #007bff;
  --color-primary-dark: #0056b3;
  --color-success: #28a745;
  --color-warning: #ffc107;
  --color-danger: #dc3545;
  --color-gray-100: #f8f9fa;
  --color-gray-500: #6c757d;
  --color-gray-900: #212529;
}
```

---

### Typography
**패턴**: 일관된 타이포그래피

**구현**:
```css
/* src/styles/typography.css */
:root {
  --font-size-xs: 0.75rem;    /* 12px */
  --font-size-sm: 0.875rem;   /* 14px */
  --font-size-base: 1rem;     /* 16px */
  --font-size-lg: 1.125rem;   /* 18px */
  --font-size-xl: 1.25rem;    /* 20px */
  --font-size-2xl: 1.5rem;    /* 24px */
  
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-bold: 700;
}

h1 {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
}

h2 {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
}

p {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
}
```

---

### Spacing
**패턴**: 일관된 간격

**구현**:
```css
/* src/styles/spacing.css */
:root {
  --spacing-xs: 0.25rem;   /* 4px */
  --spacing-sm: 0.5rem;    /* 8px */
  --spacing-md: 1rem;      /* 16px */
  --spacing-lg: 1.5rem;    /* 24px */
  --spacing-xl: 2rem;      /* 32px */
}
```

---

## UX 체크리스트

### 사용성
- [ ] 3-Click Rule 준수
- [ ] 명확한 피드백 (Toast)
- [ ] 로딩 상태 표시
- [ ] 에러 복구 방법 제공
- [ ] 빈 상태 안내

### 접근성
- [ ] 키보드 네비게이션
- [ ] ARIA 레이블
- [ ] 포커스 관리
- [ ] 색상 대비 4.5:1
- [ ] Semantic HTML

### 반응형
- [ ] Mobile-First
- [ ] Touch-Friendly (44x44px)
- [ ] Responsive images
- [ ] Flexible layouts

### 애니메이션
- [ ] 60 FPS
- [ ] GPU 가속
- [ ] 부드러운 전환
- [ ] 로딩 애니메이션

---

## Notes

- 사용자 중심 설계
- 일관된 디자인 시스템
- 접근성은 필수
- 성능과 UX의 균형
- 지속적인 개선
