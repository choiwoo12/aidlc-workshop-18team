# Customer Frontend - NFR Design Summary

## Overview
Customer Frontend의 NFR Design 완료. 성능, 보안, UX 요구사항을 충족하기 위한 구체적인 구현 패턴 정의.

---

## 문서 목록

1. **performance-optimization-patterns.md** - 성능 최적화 패턴
2. **security-implementation-patterns.md** - 보안 구현 패턴
3. **ux-implementation-patterns.md** - UX 구현 패턴

---

## 핵심 구현 패턴

### 성능 최적화

#### Code Splitting
- Route-based splitting (페이지별)
- Component-based splitting (큰 컴포넌트)
- Dynamic imports

```typescript
const MenuPage = lazy(() => import('@/pages/MenuPage'));
```

#### Image Optimization
- Lazy loading (Intersection Observer)
- WebP 포맷
- Responsive images

#### React Performance
- React.memo
- useMemo & useCallback
- Virtual scrolling (선택)

#### Bundle Optimization
- Tree shaking
- Manual chunks (vendor 분리)
- Terser minification

---

### 보안 구현

#### XSS 방어
- React 자동 이스케이프
- Input sanitization
- URL validation

```typescript
export const sanitizeInput = (input: string): string => {
  return input.replace(/<[^>]*>/g, '');
};
```

#### CSRF 방어
- SameSite 쿠키 (Backend)
- CORS 정책 준수
- withCredentials 설정

#### 데이터 보호
- localStorage 안전 사용
- Production 로깅 비활성화
- 에러 메시지 필터링

#### 의존성 보안
- npm audit 정기 실행
- Dependabot 활용
- 패키지 버전 고정

---

### UX 구현

#### 피드백 시스템
- Toast notifications
- Loading spinners
- Skeleton UI

```typescript
toast.success('장바구니에 담았습니다');
```

#### 접근성
- Keyboard navigation
- ARIA labels
- Focus management
- Semantic HTML

#### 반응형 디자인
- Mobile-first
- Responsive grid
- Touch-friendly UI (44x44px)

#### 에러 처리
- Error states
- Empty states
- Retry 버튼

#### 애니메이션
- Page transitions
- Button feedback
- Loading animations (60 FPS)

---

## 기술 스택 및 라이브러리

### Core
- React 18
- TypeScript
- Vite

### State Management
- Zustand
- zustand/middleware (persist)

### HTTP & SSE
- Axios
- EventSource

### Routing
- React Router v6

### UI/UX
- react-toastify (Toast)
- CSS Modules
- Intersection Observer (Lazy loading)

### Development
- ESLint
- Prettier
- Vitest (Testing)

---

## 디렉토리 구조

```
frontend/customer/
├── public/
│   └── placeholder.png
├── src/
│   ├── atoms/              # Button, Input, Card, Badge, Image
│   ├── molecules/          # MenuCard, CartItem, OrderStatusBadge
│   ├── organisms/          # MenuList, Cart, OrderHistory
│   ├── templates/          # MainLayout, BottomNavigation
│   ├── pages/              # MenuPage, CartPage, OrderHistoryPage
│   ├── stores/             # useCartStore, useOrderStore, useMenuStore
│   ├── services/           # apiClient, sseClient, api/
│   ├── hooks/              # useNetworkStatus, useDebounce
│   ├── utils/              # sanitize, logger, storage, errorHandler
│   ├── styles/             # colors.css, typography.css, spacing.css
│   ├── components/         # ErrorBoundary, LoadingSpinner, EmptyState
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── vite.config.ts
├── tsconfig.json
└── .env.development
```

---

## 환경 변수

### .env.development
```env
VITE_API_URL=http://localhost:8080
```

### .env.production
```env
VITE_API_URL=https://api.tableorder.com
```

---

## Vite 설정

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
          'axios-vendor': ['axios'],
        },
      },
    },
  },
});
```

---

## 성능 목표

### 로딩 성능
- Initial Load: < 3초
- FCP: < 1.5초
- LCP: < 2.5초
- Bundle Size: < 200KB (gzipped)

### 런타임 성능
- 60 FPS 애니메이션
- Memory: < 50MB
- API 응답: < 1초

---

## 보안 목표

### 방어 메커니즘
- XSS 방어: React 자동 이스케이프
- CSRF 방어: SameSite 쿠키
- HTTPS: Production 필수
- 의존성 취약점: 0개

---

## UX 목표

### 사용성
- 3-Click Rule 준수
- 즉각적인 피드백
- 명확한 에러 메시지

### 접근성
- WCAG 2.1 AA 준수
- 키보드 네비게이션
- 스크린 리더 호환

### 반응형
- Mobile-First
- Touch-Friendly
- Flexible layouts

---

## 구현 우선순위

### Phase 1: Core (Critical)
1. 기본 컴포넌트 (Atoms, Molecules)
2. 페이지 구조 (Pages, Templates)
3. 상태 관리 (Zustand stores)
4. API 통신 (Axios, SSE)
5. 라우팅 (React Router)

### Phase 2: Optimization (High)
1. Code splitting
2. Image lazy loading
3. React.memo 적용
4. Bundle optimization

### Phase 3: Enhancement (Medium)
1. 애니메이션
2. 오프라인 지원
3. 에러 경계
4. 성능 모니터링

---

## 테스트 전략

### Unit Tests
- 컴포넌트 렌더링
- Store 로직
- Utility 함수

### Integration Tests
- API 통합
- SSE 연결
- 페이지 플로우

### E2E Tests
- 메뉴 조회 → 주문 생성
- 주문 내역 조회
- 실시간 업데이트

---

## 다음 단계

### Infrastructure Design
빌드 및 배포 인프라 설계:
1. **빌드 설정**
   - Vite 설정 최적화
   - 환경 변수 관리
   - TypeScript 설정

2. **배포 전략**
   - 정적 파일 호스팅
   - CDN 설정
   - CI/CD 파이프라인

3. **모니터링**
   - 성능 모니터링
   - 에러 추적
   - 사용자 분석

---

## 검증 체크리스트

- [x] 성능 최적화 패턴 정의 완료
- [x] 보안 구현 패턴 정의 완료
- [x] UX 구현 패턴 정의 완료
- [x] 기술 스택 선정 완료
- [x] 디렉토리 구조 정의 완료
- [x] 환경 설정 정의 완료
- [x] 우선순위 설정 완료

---

## Notes

- 모든 패턴은 실제 코드로 구현 가능
- 성능, 보안, UX의 균형 유지
- 측정 가능한 목표 설정
- 지속적인 개선 프로세스
- 사용자 피드백 반영
