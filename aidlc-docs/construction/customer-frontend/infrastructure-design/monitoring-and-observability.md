# Customer Frontend - Monitoring and Observability

## Overview
프론트엔드 모니터링 및 관찰성 전략. 성능, 에러, 사용자 행동 추적.

---

## Performance Monitoring

### Web Vitals
```typescript
// src/utils/performance.ts
import { onCLS, onFID, onLCP, onFCP, onTTFB } from 'web-vitals';

export function initPerformanceMonitoring() {
  // Core Web Vitals
  onCLS((metric) => {
    sendToAnalytics('CLS', metric.value);
  });

  onFID((metric) => {
    sendToAnalytics('FID', metric.value);
  });

  onLCP((metric) => {
    sendToAnalytics('LCP', metric.value);
  });

  // Additional metrics
  onFCP((metric) => {
    sendToAnalytics('FCP', metric.value);
  });

  onTTFB((metric) => {
    sendToAnalytics('TTFB', metric.value);
  });
}

function sendToAnalytics(metric: string, value: number) {
  if (import.meta.env.PROD) {
    // Send to monitoring service
    console.log(`${metric}: ${value}`);
  }
}
```

---

### Custom Performance Metrics
```typescript
// src/utils/customMetrics.ts
export const measureApiCall = async <T>(
  name: string,
  apiCall: () => Promise<T>
): Promise<T> => {
  const start = performance.now();
  
  try {
    const result = await apiCall();
    const duration = performance.now() - start;
    
    sendToAnalytics('api_call', {
      name,
      duration,
      status: 'success',
    });
    
    return result;
  } catch (error) {
    const duration = performance.now() - start;
    
    sendToAnalytics('api_call', {
      name,
      duration,
      status: 'error',
    });
    
    throw error;
  }
};
```

---

## Error Tracking

### Error Boundary with Logging
```typescript
// src/components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    // Log to monitoring service
    logError({
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
      timestamp: new Date().toISOString(),
    });
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-page">
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

---

### Global Error Handler
```typescript
// src/utils/errorLogger.ts
export function initErrorLogging() {
  // Unhandled errors
  window.addEventListener('error', (event) => {
    logError({
      type: 'unhandled_error',
      message: event.message,
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
      stack: event.error?.stack,
    });
  });

  // Unhandled promise rejections
  window.addEventListener('unhandledrejection', (event) => {
    logError({
      type: 'unhandled_rejection',
      reason: event.reason,
      promise: event.promise,
    });
  });
}

function logError(error: any) {
  if (import.meta.env.PROD) {
    // Send to error tracking service (e.g., Sentry)
    console.error('Error logged:', error);
  } else {
    console.error('Development error:', error);
  }
}
```

---

## User Analytics

### Page View Tracking
```typescript
// src/utils/analytics.ts
export function trackPageView(path: string) {
  if (import.meta.env.PROD) {
    // Google Analytics
    if (window.gtag) {
      window.gtag('config', 'GA_MEASUREMENT_ID', {
        page_path: path,
      });
    }
  }
}

// Usage in App.tsx
function App() {
  const location = useLocation();

  useEffect(() => {
    trackPageView(location.pathname);
  }, [location]);

  return <Routes>{/* ... */}</Routes>;
}
```

---

### Event Tracking
```typescript
// src/utils/analytics.ts
export function trackEvent(
  category: string,
  action: string,
  label?: string,
  value?: number
) {
  if (import.meta.env.PROD) {
    if (window.gtag) {
      window.gtag('event', action, {
        event_category: category,
        event_label: label,
        value: value,
      });
    }
  }
}

// Usage examples
trackEvent('Cart', 'add_item', menu.name);
trackEvent('Order', 'create', orderNumber);
trackEvent('Menu', 'view', menu.name);
```

---

## API Monitoring

### API Call Tracking
```typescript
// src/services/apiClient.ts
apiClient.interceptors.request.use((config) => {
  config.metadata = { startTime: Date.now() };
  return config;
});

apiClient.interceptors.response.use(
  (response) => {
    const duration = Date.now() - response.config.metadata.startTime;
    
    logApiCall({
      url: response.config.url,
      method: response.config.method,
      status: response.status,
      duration,
    });
    
    return response;
  },
  (error) => {
    const duration = Date.now() - error.config.metadata.startTime;
    
    logApiCall({
      url: error.config.url,
      method: error.config.method,
      status: error.response?.status || 0,
      duration,
      error: error.message,
    });
    
    return Promise.reject(error);
  }
);
```

---

## Real User Monitoring (RUM)

### Session Recording
```typescript
// src/utils/sessionRecording.ts
export function initSessionRecording() {
  if (import.meta.env.PROD) {
    // Initialize session recording (e.g., Hotjar, FullStory)
    // This is a placeholder - actual implementation depends on service
  }
}
```

---

### User Journey Tracking
```typescript
// src/utils/journeyTracking.ts
export function trackUserJourney(step: string, data?: any) {
  const journey = JSON.parse(localStorage.getItem('user_journey') || '[]');
  
  journey.push({
    step,
    data,
    timestamp: new Date().toISOString(),
  });
  
  localStorage.setItem('user_journey', JSON.stringify(journey));
  
  // Send to analytics
  trackEvent('Journey', step, JSON.stringify(data));
}

// Usage
trackUserJourney('menu_viewed');
trackUserJourney('item_added_to_cart', { menuId: 1, quantity: 2 });
trackUserJourney('order_created', { orderNumber: 'ORD-001' });
```

---

## Dashboard Metrics

### Key Metrics to Track

#### Performance
- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)
- Page Load Time
- API Response Time

#### Errors
- JavaScript Errors
- API Errors
- Network Errors
- Error Rate

#### Usage
- Page Views
- Unique Users
- Session Duration
- Bounce Rate

#### Business
- Orders Created
- Cart Abandonment Rate
- Average Order Value
- Conversion Rate

---

## Alerting

### Alert Rules
```yaml
# alerts.yml
alerts:
  - name: High Error Rate
    condition: error_rate > 5%
    duration: 5m
    severity: critical
    
  - name: Slow Page Load
    condition: lcp > 3s
    duration: 10m
    severity: warning
    
  - name: API Failure
    condition: api_error_rate > 10%
    duration: 5m
    severity: critical
```

---

## Logging

### Structured Logging
```typescript
// src/utils/logger.ts
export const logger = {
  info: (message: string, data?: any) => {
    if (import.meta.env.DEV) {
      console.log(`[INFO] ${message}`, data);
    }
  },
  
  warn: (message: string, data?: any) => {
    console.warn(`[WARN] ${message}`, data);
  },
  
  error: (message: string, error?: any) => {
    console.error(`[ERROR] ${message}`, error);
    
    if (import.meta.env.PROD) {
      // Send to error tracking
      logError({ message, error });
    }
  },
};
```

---

## Notes

- 성능 모니터링으로 사용자 경험 개선
- 에러 추적으로 빠른 문제 해결
- 사용자 분석으로 제품 개선
- 실시간 알림으로 장애 대응
- 데이터 기반 의사결정
