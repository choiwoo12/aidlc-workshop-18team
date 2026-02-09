# Customer Frontend - Performance Optimization Patterns

## Overview
성능 요구사항을 충족하기 위한 구체적인 최적화 패턴 및 구현 방법.

---

## Code Splitting

### Route-Based Splitting
**목적**: 페이지별로 번들 분리하여 초기 로딩 시간 단축

**구현**:
```typescript
// src/App.tsx
import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

// Lazy load pages
const MenuPage = lazy(() => import('@/pages/MenuPage'));
const CartPage = lazy(() => import('@/pages/CartPage'));
const OrderHistoryPage = lazy(() => import('@/pages/OrderHistoryPage'));

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/" element={<MenuPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/orders" element={<OrderHistoryPage />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  );
}
```

**효과**: 초기 번들 크기 30-40% 감소

---

### Component-Based Splitting
**목적**: 큰 컴포넌트 lazy loading

**구현**:
```typescript
// 큰 모달 컴포넌트
const OrderDetailModal = lazy(() => import('@/organisms/OrderDetail'));

function OrderHistoryPage() {
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  return (
    <div>
      {/* ... */}
      {selectedOrder && (
        <Suspense fallback={<div>로딩 중...</div>}>
          <OrderDetailModal
            order={selectedOrder}
            onClose={() => setSelectedOrder(null)}
          />
        </Suspense>
      )}
    </div>
  );
}
```

---

## Image Optimization

### Lazy Loading
**목적**: 뷰포트에 보이는 이미지만 로드

**구현**:
```typescript
// src/atoms/Image.tsx
import { useState, useEffect, useRef } from 'react';

interface ImageProps {
  src: string | null;
  alt: string;
  fallback?: string;
  className?: string;
}

export function Image({ src, alt, fallback = '/placeholder.png', className }: ImageProps) {
  const [imageSrc, setImageSrc] = useState(fallback);
  const [isLoading, setIsLoading] = useState(true);
  const imgRef = useRef<HTMLImageElement>(null);

  useEffect(() => {
    if (!src) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setImageSrc(src);
            observer.disconnect();
          }
        });
      },
      { rootMargin: '50px' }
    );

    if (imgRef.current) {
      observer.observe(imgRef.current);
    }

    return () => observer.disconnect();
  }, [src]);

  return (
    <img
      ref={imgRef}
      src={imageSrc}
      alt={alt}
      className={className}
      onLoad={() => setIsLoading(false)}
      onError={() => setImageSrc(fallback)}
      style={{ opacity: isLoading ? 0.5 : 1, transition: 'opacity 0.3s' }}
    />
  );
}
```

---

### WebP Format
**목적**: 이미지 파일 크기 30-50% 감소

**구현**:
```html
<picture>
  <source srcset="menu.webp" type="image/webp" />
  <source srcset="menu.jpg" type="image/jpeg" />
  <img src="menu.jpg" alt="메뉴" />
</picture>
```

---

## React Performance

### React.memo
**목적**: 불필요한 리렌더링 방지

**구현**:
```typescript
// src/molecules/MenuCard.tsx
import { memo } from 'react';

interface MenuCardProps {
  menu: Menu;
  onAddToCart: (menu: Menu, quantity: number) => void;
}

export const MenuCard = memo(({ menu, onAddToCart }: MenuCardProps) => {
  // ...
}, (prevProps, nextProps) => {
  // Custom comparison
  return prevProps.menu.id === nextProps.menu.id;
});
```

---

### useMemo & useCallback
**목적**: 계산 비용이 큰 작업 메모이제이션

**구현**:
```typescript
import { useMemo, useCallback } from 'react';

function Cart() {
  const items = useCartStore(state => state.items);

  // Expensive calculation
  const totalAmount = useMemo(() => {
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }, [items]);

  // Callback memoization
  const handleUpdateQuantity = useCallback((menuId: number, quantity: number) => {
    updateQuantity(menuId, quantity);
  }, []);

  return (
    <div>
      {items.map(item => (
        <CartItem
          key={item.menuId}
          item={item}
          onUpdateQuantity={handleUpdateQuantity}
        />
      ))}
      <div>총액: {totalAmount}원</div>
    </div>
  );
}
```

---

### Virtual Scrolling (선택)
**목적**: 긴 리스트 렌더링 최적화

**구현** (react-window):
```typescript
import { FixedSizeList } from 'react-window';

function MenuList({ menus }: MenuListProps) {
  const Row = ({ index, style }: any) => (
    <div style={style}>
      <MenuCard menu={menus[index]} />
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={menus.length}
      itemSize={200}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

---

## Bundle Optimization

### Tree Shaking
**목적**: 사용하지 않는 코드 제거

**Vite 설정**:
```typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'zustand-vendor': ['zustand'],
          'axios-vendor': ['axios'],
        },
      },
    },
  },
});
```

---

### Dynamic Imports
**목적**: 필요할 때만 모듈 로드

**구현**:
```typescript
// Toast 라이브러리 동적 로드
const showToast = async (message: string) => {
  const { toast } = await import('react-toastify');
  toast.success(message);
};
```

---

## API Optimization

### Request Deduplication
**목적**: 중복 API 호출 방지

**구현**:
```typescript
// src/services/apiClient.ts
const pendingRequests = new Map<string, Promise<any>>();

export const apiClient = {
  async get<T>(url: string): Promise<T> {
    // Check if request is already pending
    if (pendingRequests.has(url)) {
      return pendingRequests.get(url)!;
    }

    // Create new request
    const request = axios.get<T>(url).finally(() => {
      pendingRequests.delete(url);
    });

    pendingRequests.set(url, request);
    return request;
  },
};
```

---

### Debounce
**목적**: API 호출 빈도 제한

**구현**:
```typescript
import { debounce } from 'lodash-es';

const debouncedSearch = debounce(async (query: string) => {
  const results = await searchMenus(query);
  setSearchResults(results);
}, 300);
```

---

### Caching Strategy
**목적**: 불필요한 API 호출 제거

**구현**:
```typescript
// Zustand store with cache
export const useMenuStore = create<MenuState>((set, get) => ({
  menus: [],
  lastFetchTime: null,
  cacheTimeout: 5 * 60 * 1000, // 5 minutes

  fetchMenus: async (storeId) => {
    const now = Date.now();
    const { lastFetchTime, cacheTimeout } = get();

    // Use cache if valid
    if (lastFetchTime && now - lastFetchTime < cacheTimeout) {
      return;
    }

    const menus = await menuApi.getMenus(storeId);
    set({ menus, lastFetchTime: now });
  },
}));
```

---

## Loading Optimization

### Skeleton UI
**목적**: 로딩 중 구조 표시로 체감 성능 향상

**구현**:
```typescript
// src/components/SkeletonCard.tsx
export function SkeletonCard() {
  return (
    <div className="skeleton-card">
      <div className="skeleton-image" />
      <div className="skeleton-text skeleton-title" />
      <div className="skeleton-text skeleton-price" />
      <div className="skeleton-button" />
    </div>
  );
}

// CSS
.skeleton-card {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}
```

---

### Progressive Loading
**목적**: 중요한 콘텐츠 먼저 로드

**구현**:
```typescript
function MenuPage() {
  const [menus, setMenus] = useState<Menu[]>([]);
  const [isLoadingMore, setIsLoadingMore] = useState(false);

  useEffect(() => {
    // Load first 10 items immediately
    loadMenus(0, 10);
  }, []);

  const loadMore = async () => {
    setIsLoadingMore(true);
    await loadMenus(menus.length, 10);
    setIsLoadingMore(false);
  };

  return (
    <div>
      <MenuList menus={menus} />
      {isLoadingMore && <LoadingSpinner />}
      <button onClick={loadMore}>더 보기</button>
    </div>
  );
}
```

---

## SSE Optimization

### Connection Pooling
**목적**: SSE 연결 재사용

**구현**:
```typescript
// src/services/sseClient.ts
class SSEClient {
  private static instance: SSEClient;
  private eventSource: EventSource | null = null;

  static getInstance(): SSEClient {
    if (!SSEClient.instance) {
      SSEClient.instance = new SSEClient();
    }
    return SSEClient.instance;
  }

  connect(sessionId: string, handlers: SSEEventHandlers): void {
    // Reuse existing connection if same sessionId
    if (this.eventSource && this.eventSource.url.includes(sessionId)) {
      return;
    }

    this.disconnect();
    this.eventSource = new EventSource(`/api/sse/subscribe?sessionId=${sessionId}`);
    // ...
  }
}
```

---

### Heartbeat
**목적**: 연결 유지 및 재연결

**구현**:
```typescript
connect(sessionId: string, handlers: SSEEventHandlers): void {
  this.eventSource = new EventSource(url);

  // Heartbeat check
  let heartbeatTimer: NodeJS.Timeout;

  this.eventSource.addEventListener('heartbeat', () => {
    clearTimeout(heartbeatTimer);
    heartbeatTimer = setTimeout(() => {
      console.warn('Heartbeat timeout, reconnecting...');
      this.reconnect(sessionId, handlers);
    }, 30000); // 30 seconds
  });
}
```

---

## Monitoring

### Performance Metrics
**목적**: 실시간 성능 모니터링

**구현**:
```typescript
// src/utils/performance.ts
import { onCLS, onFID, onLCP } from 'web-vitals';

export function initPerformanceMonitoring() {
  onCLS(console.log);
  onFID(console.log);
  onLCP(console.log);

  // Custom metrics
  if (window.performance) {
    window.addEventListener('load', () => {
      const perfData = window.performance.timing;
      const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
      console.log('Page Load Time:', pageLoadTime);
    });
  }
}
```

---

## Build Optimization

### Vite Configuration
**목적**: 최적화된 프로덕션 빌드

**구현**:
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    target: 'es2015',
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'zustand-vendor': ['zustand'],
        },
      },
    },
    chunkSizeWarningLimit: 500,
  },
  optimizeDeps: {
    include: ['react', 'react-dom', 'zustand'],
  },
});
```

---

## 성능 체크리스트

### 빌드 시
- [ ] Code splitting 적용
- [ ] Tree shaking 활성화
- [ ] 번들 크기 < 200KB (gzipped)
- [ ] Source map 제거 (production)

### 런타임
- [ ] React.memo 적용
- [ ] useMemo/useCallback 사용
- [ ] 이미지 lazy loading
- [ ] API 중복 호출 방지

### 모니터링
- [ ] Lighthouse 점수 > 90
- [ ] LCP < 2.5초
- [ ] FID < 100ms
- [ ] CLS < 0.1

---

## Notes

- 성능 최적화는 측정 후 진행
- 과도한 최적화는 코드 복잡도 증가
- 사용자 경험에 영향 큰 부분 우선
- 정기적인 성능 감사 필요
