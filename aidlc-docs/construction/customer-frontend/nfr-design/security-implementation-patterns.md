# Customer Frontend - Security Implementation Patterns

## Overview
보안 요구사항을 충족하기 위한 구체적인 구현 패턴 및 방법.

---

## XSS 방어

### React 자동 이스케이프 활용
**패턴**: JSX에서 자동 이스케이프

**구현**:
```typescript
// ✅ Safe: React가 자동으로 이스케이프
function MenuCard({ menu }: MenuCardProps) {
  return (
    <div>
      <h3>{menu.name}</h3>
      <p>{menu.price}원</p>
    </div>
  );
}

// ❌ Dangerous: XSS 취약점
function UnsafeComponent({ html }: { html: string }) {
  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
```

---

### Input Sanitization
**패턴**: 사용자 입력 검증 및 정제

**구현**:
```typescript
// src/utils/sanitize.ts
export const sanitizeInput = (input: string): string => {
  // Remove HTML tags
  return input.replace(/<[^>]*>/g, '');
};

export const validateQuantity = (value: number): boolean => {
  return Number.isInteger(value) && value >= 1 && value <= 99;
};

export const sanitizeMenuName = (name: string): string => {
  // Allow only alphanumeric, Korean, spaces
  return name.replace(/[^a-zA-Z0-9가-힣\s]/g, '');
};
```

**사용**:
```typescript
function MenuCard({ menu }: MenuCardProps) {
  const [quantity, setQuantity] = useState(1);

  const handleQuantityChange = (value: string) => {
    const num = parseInt(value, 10);
    if (validateQuantity(num)) {
      setQuantity(num);
    }
  };

  return (
    <input
      type="number"
      value={quantity}
      onChange={(e) => handleQuantityChange(e.target.value)}
      min={1}
      max={99}
    />
  );
}
```

---

### URL Validation
**패턴**: 외부 URL 검증

**구현**:
```typescript
// src/utils/urlValidator.ts
export const isValidImageUrl = (url: string | null): boolean => {
  if (!url) return false;

  try {
    const parsed = new URL(url);
    // Only allow https and same origin
    return parsed.protocol === 'https:' || parsed.origin === window.location.origin;
  } catch {
    return false;
  }
};
```

**사용**:
```typescript
function Image({ src, alt }: ImageProps) {
  const safeSrc = isValidImageUrl(src) ? src : '/placeholder.png';
  
  return <img src={safeSrc} alt={alt} />;
}
```

---

## CSRF 방어

### SameSite Cookie (Backend)
**패턴**: Backend에서 SameSite 쿠키 설정

**Frontend 대응**:
```typescript
// Axios는 자동으로 쿠키 포함
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true, // 쿠키 포함
});
```

---

### CORS 정책 준수
**패턴**: 허용된 Origin만 요청

**구현**:
```typescript
// src/config/api.ts
export const API_URL = import.meta.env.VITE_API_URL;

// Production에서만 HTTPS 강제
if (import.meta.env.PROD && !API_URL.startsWith('https://')) {
  throw new Error('Production API must use HTTPS');
}
```

---

## 데이터 보호

### Sensitive Data Handling
**패턴**: 민감한 데이터 노출 방지

**구현**:
```typescript
// src/utils/logger.ts
export const logger = {
  log: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.log(message, data);
    }
  },
  
  error: (message: string, error?: any) => {
    if (import.meta.env.DEV) {
      console.error(message, error);
    } else {
      // Production: Send to error tracking service
      // Sentry.captureException(error);
    }
  },
};
```

---

### localStorage Security
**패턴**: localStorage 안전하게 사용

**구현**:
```typescript
// src/utils/storage.ts
const STORAGE_PREFIX = 'tableorder_';

export const storage = {
  set: (key: string, value: any): void => {
    try {
      const serialized = JSON.stringify(value);
      localStorage.setItem(STORAGE_PREFIX + key, serialized);
    } catch (error) {
      logger.error('Storage set error', error);
    }
  },

  get: <T>(key: string): T | null => {
    try {
      const item = localStorage.getItem(STORAGE_PREFIX + key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      logger.error('Storage get error', error);
      return null;
    }
  },

  remove: (key: string): void => {
    localStorage.removeItem(STORAGE_PREFIX + key);
  },

  clear: (): void => {
    Object.keys(localStorage)
      .filter(key => key.startsWith(STORAGE_PREFIX))
      .forEach(key => localStorage.removeItem(key));
  },
};

// ❌ Never store sensitive data
// storage.set('password', userPassword); // BAD
// storage.set('creditCard', cardNumber); // BAD

// ✅ OK to store
storage.set('cart', cartItems); // OK
storage.set('sessionId', sessionId); // OK (temporary session)
```

---

## API 보안

### HTTPS Enforcement
**패턴**: Production에서 HTTPS 강제

**구현**:
```typescript
// src/config/api.ts
export const getApiUrl = (): string => {
  const url = import.meta.env.VITE_API_URL;

  if (import.meta.env.PROD) {
    if (!url.startsWith('https://')) {
      throw new Error('Production API must use HTTPS');
    }
  }

  return url;
};

export const apiClient = axios.create({
  baseURL: getApiUrl(),
});
```

---

### Error Message Filtering
**패턴**: 에러 메시지에서 민감한 정보 제거

**구현**:
```typescript
// src/utils/errorHandler.ts
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const status = error.response?.status;
    
    // Don't expose detailed error messages in production
    if (import.meta.env.PROD) {
      switch (status) {
        case 400:
          return '잘못된 요청입니다';
        case 404:
          return '요청한 리소스를 찾을 수 없습니다';
        case 500:
          return '서버 오류가 발생했습니다';
        default:
          return '요청 처리 중 오류가 발생했습니다';
      }
    }

    // Development: Show detailed error
    return error.response?.data?.error || error.message;
  }

  return '알 수 없는 오류가 발생했습니다';
};
```

---

### Rate Limiting (Client-Side)
**패턴**: 중복 요청 방지

**구현**:
```typescript
// src/utils/debounce.ts
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;

  return function executedFunction(...args: Parameters<T>) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };

    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Usage
const handleSubmit = debounce(async () => {
  await createOrder(request);
}, 1000);
```

---

## 의존성 보안

### Dependency Audit
**패턴**: 정기적인 취약점 검사

**스크립트**:
```json
// package.json
{
  "scripts": {
    "audit": "npm audit",
    "audit:fix": "npm audit fix",
    "audit:check": "npm audit --audit-level=moderate"
  }
}
```

**CI/CD 통합**:
```yaml
# .github/workflows/security.yml
name: Security Audit

on:
  schedule:
    - cron: '0 0 * * 0' # Weekly
  pull_request:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm audit --audit-level=moderate
```

---

### Package Lock
**패턴**: 의존성 버전 고정

**구현**:
```json
// package.json
{
  "dependencies": {
    "react": "^18.2.0",
    "axios": "~1.6.0" // Patch updates only
  }
}
```

---

## Content Security Policy

### CSP Meta Tag
**패턴**: CSP 정책 설정

**구현**:
```html
<!-- index.html -->
<meta
  http-equiv="Content-Security-Policy"
  content="
    default-src 'self';
    script-src 'self';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    connect-src 'self' https://api.tableorder.com;
    font-src 'self';
  "
/>
```

---

### CSP Violation Reporting
**패턴**: CSP 위반 모니터링

**구현**:
```typescript
// src/utils/cspReporter.ts
window.addEventListener('securitypolicyviolation', (e) => {
  const violation = {
    blockedURI: e.blockedURI,
    violatedDirective: e.violatedDirective,
    originalPolicy: e.originalPolicy,
  };

  // Send to monitoring service
  logger.error('CSP Violation', violation);
});
```

---

## Secure Coding Practices

### Type Safety
**패턴**: TypeScript로 타입 안정성 확보

**구현**:
```typescript
// ✅ Good: Type-safe
interface CreateOrderRequest {
  storeId: number;
  tableId: number;
  sessionId: string;
  items: OrderItemRequest[];
}

const createOrder = async (request: CreateOrderRequest): Promise<Order> => {
  // TypeScript ensures all required fields are present
  return await orderApi.createOrder(request);
};

// ❌ Bad: No type safety
const createOrder = async (request: any) => {
  return await orderApi.createOrder(request);
};
```

---

### Null Safety
**패턴**: Null/undefined 체크

**구현**:
```typescript
// ✅ Good: Null-safe
function MenuCard({ menu }: MenuCardProps) {
  const imageUrl = menu.imageUrl ?? '/placeholder.png';
  
  return (
    <div>
      <img src={imageUrl} alt={menu.name} />
      <h3>{menu.name}</h3>
    </div>
  );
}

// ❌ Bad: Potential null reference
function MenuCard({ menu }: MenuCardProps) {
  return <img src={menu.imageUrl} alt={menu.name} />;
}
```

---

### Error Boundaries
**패턴**: 에러 격리

**구현**:
```typescript
// src/components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    logger.error('Error Boundary caught error', { error, errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>문제가 발생했습니다</h2>
          <button onClick={() => window.location.reload()}>
            새로고침
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

**사용**:
```typescript
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

---

## 보안 테스트

### Security Test Cases
**패턴**: 보안 테스트 자동화

**구현**:
```typescript
// src/__tests__/security.test.ts
import { sanitizeInput, validateQuantity } from '@/utils/sanitize';

describe('Security Tests', () => {
  describe('XSS Prevention', () => {
    it('should remove HTML tags', () => {
      const input = '<script>alert("xss")</script>Hello';
      const result = sanitizeInput(input);
      expect(result).toBe('Hello');
    });

    it('should remove event handlers', () => {
      const input = '<img src=x onerror="alert(1)">';
      const result = sanitizeInput(input);
      expect(result).not.toContain('onerror');
    });
  });

  describe('Input Validation', () => {
    it('should reject negative quantity', () => {
      expect(validateQuantity(-1)).toBe(false);
    });

    it('should reject zero quantity', () => {
      expect(validateQuantity(0)).toBe(false);
    });

    it('should accept valid quantity', () => {
      expect(validateQuantity(5)).toBe(true);
    });

    it('should reject quantity over 99', () => {
      expect(validateQuantity(100)).toBe(false);
    });
  });
});
```

---

## 보안 체크리스트

### 개발 시
- [ ] 모든 사용자 입력 검증
- [ ] XSS 방어 (React 자동 이스케이프)
- [ ] Type safety (TypeScript)
- [ ] Null safety 체크
- [ ] Error boundary 적용

### 빌드 시
- [ ] npm audit 실행
- [ ] 취약한 의존성 제거
- [ ] Source map 제거 (production)
- [ ] Console.log 제거 (production)

### 배포 시
- [ ] HTTPS 강제
- [ ] CSP 헤더 설정
- [ ] CORS 정책 확인
- [ ] 환경 변수 검증

### 운영 시
- [ ] 정기적인 의존성 업데이트
- [ ] 보안 패치 즉시 적용
- [ ] 에러 모니터링
- [ ] 보안 감사 (월 1회)

---

## Notes

- React는 기본적으로 XSS 방어 제공
- TypeScript로 타입 안정성 확보
- 의존성 취약점 정기 검사 필수
- Production 환경에서 민감한 정보 노출 금지
- 보안은 지속적인 프로세스
