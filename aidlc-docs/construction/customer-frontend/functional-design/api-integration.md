# Customer Frontend - API Integration

## Overview
Axios 기반 REST API 클라이언트와 EventSource 기반 SSE 클라이언트 구현.

---

## API Client Setup

### Base Configuration
```typescript
// src/services/apiClient.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8080',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config) => {
    // 요청 로깅 (개발 환경)
    if (import.meta.env.DEV) {
      console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    // 응답 로깅 (개발 환경)
    if (import.meta.env.DEV) {
      console.log(`[API Response] ${response.config.url}`, response.data);
    }
    return response;
  },
  (error) => {
    // 에러 처리
    const message = error.response?.data?.error || '네트워크 오류가 발생했습니다';
    console.error('[API Error]', message);
    return Promise.reject(new Error(message));
  }
);

export { apiClient };
```

---

## REST API Endpoints

### 1. 메뉴 조회
```typescript
// GET /api/customer/menus?storeId={storeId}

interface GetMenusParams {
  storeId: number;
}

export const getMenus = async (params: GetMenusParams): Promise<Menu[]> => {
  const response = await apiClient.get<ApiResponse<Menu[]>>(
    '/api/customer/menus',
    { params }
  );
  return response.data.data || [];
};
```

**사용 예시**:
```typescript
const menus = await getMenus({ storeId: 1 });
```

---

### 2. 주문 생성
```typescript
// POST /api/customer/orders

export const createOrder = async (request: CreateOrderRequest): Promise<Order> => {
  const response = await apiClient.post<ApiResponse<Order>>(
    '/api/customer/orders',
    request
  );
  return response.data.data!;
};
```

**사용 예시**:
```typescript
const order = await createOrder({
  storeId: 1,
  tableId: 1,
  sessionId: 'session-123',
  items: [
    { menuId: 1, quantity: 2 },
    { menuId: 3, quantity: 1 },
  ],
});
```

---

### 3. 주문 내역 조회
```typescript
// GET /api/customer/orders?sessionId={sessionId}

interface GetOrdersParams {
  sessionId: string;
}

export const getOrders = async (params: GetOrdersParams): Promise<Order[]> => {
  const response = await apiClient.get<ApiResponse<Order[]>>(
    '/api/customer/orders',
    { params }
  );
  return response.data.data || [];
};
```

**사용 예시**:
```typescript
const orders = await getOrders({ sessionId: 'session-123' });
```

---

## SSE Client

### SSE Connection Setup
```typescript
// src/services/sseClient.ts

export interface SSEEventHandlers {
  onOrderStatusChanged?: (event: OrderStatusChangedEvent) => void;
  onError?: (error: Event) => void;
  onOpen?: () => void;
}

export class SSEClient {
  private eventSource: EventSource | null = null;
  private baseURL: string;

  constructor(baseURL: string = import.meta.env.VITE_API_URL || 'http://localhost:8080') {
    this.baseURL = baseURL;
  }

  connect(sessionId: string, handlers: SSEEventHandlers): void {
    if (this.eventSource) {
      this.disconnect();
    }

    const url = `${this.baseURL}/api/sse/subscribe?sessionId=${sessionId}`;
    this.eventSource = new EventSource(url);

    // Connection opened
    this.eventSource.onopen = () => {
      console.log('[SSE] Connected');
      handlers.onOpen?.();
    };

    // ORDER_STATUS_CHANGED event
    this.eventSource.addEventListener('ORDER_STATUS_CHANGED', (event) => {
      const data: OrderStatusChangedEvent = JSON.parse(event.data);
      console.log('[SSE] ORDER_STATUS_CHANGED', data);
      handlers.onOrderStatusChanged?.(data);
    });

    // Error handling
    this.eventSource.onerror = (error) => {
      console.error('[SSE] Connection error', error);
      handlers.onError?.(error);
      this.disconnect();
    };
  }

  disconnect(): void {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
      console.log('[SSE] Disconnected');
    }
  }

  isConnected(): boolean {
    return this.eventSource !== null && this.eventSource.readyState === EventSource.OPEN;
  }
}

export const sseClient = new SSEClient();
```

---

### SSE Usage Example
```typescript
import { sseClient } from '@/services/sseClient';
import { useOrderStore } from '@/stores/useOrderStore';

function OrderHistoryPage() {
  const updateOrderStatus = useOrderStore(state => state.updateOrderStatus);
  const sessionId = getSessionId();

  useEffect(() => {
    sseClient.connect(sessionId, {
      onOrderStatusChanged: (event) => {
        updateOrderStatus(event.orderId, event.status);
        toast.info(`주문 상태가 변경되었습니다: ${event.status}`);
      },
      onError: () => {
        toast.error('실시간 업데이트 연결에 실패했습니다');
      },
      onOpen: () => {
        console.log('실시간 업데이트 연결됨');
      },
    });

    return () => {
      sseClient.disconnect();
    };
  }, [sessionId]);

  // ...
}
```

---

## Error Handling

### API Error Types
```typescript
interface ApiError {
  message: string;
  status?: number;
  code?: string;
}

export const handleApiError = (error: unknown): ApiError => {
  if (axios.isAxiosError(error)) {
    return {
      message: error.response?.data?.error || error.message,
      status: error.response?.status,
      code: error.code,
    };
  }
  return {
    message: '알 수 없는 오류가 발생했습니다',
  };
};
```

---

### Usage with Toast
```typescript
import { toast } from 'react-toastify';

try {
  await createOrder(request);
  toast.success('주문이 완료되었습니다');
} catch (error) {
  const apiError = handleApiError(error);
  toast.error(apiError.message);
}
```

---

## Request/Response Logging

### Development Mode
```typescript
if (import.meta.env.DEV) {
  console.log('[API Request]', config);
  console.log('[API Response]', response);
}
```

### Production Mode
- 로깅 비활성화
- 에러만 Sentry 등으로 전송 (선택)

---

## Retry Logic

### Automatic Retry (선택)
```typescript
import axiosRetry from 'axios-retry';

axiosRetry(apiClient, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) => {
    return axiosRetry.isNetworkOrIdempotentRequestError(error) ||
           error.response?.status === 500;
  },
});
```

---

## Request Cancellation

### Cancel Token
```typescript
import { CancelToken } from 'axios';

let cancelTokenSource = CancelToken.source();

const fetchMenus = async () => {
  try {
    const response = await apiClient.get('/api/customer/menus', {
      cancelToken: cancelTokenSource.token,
    });
    return response.data;
  } catch (error) {
    if (axios.isCancel(error)) {
      console.log('Request canceled');
    }
  }
};

// Cancel request
cancelTokenSource.cancel('Operation canceled by user');
```

---

## Environment Variables

### .env.development
```env
VITE_API_URL=http://localhost:8080
```

### .env.production
```env
VITE_API_URL=https://api.tableorder.com
```

---

## CORS Configuration

### Backend CORS Setup (참고)
```java
@Configuration
public class SecurityConfig {
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("http://localhost:5173"));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        return source;
    }
}
```

---

## API Service Layer

### Organized API Functions
```typescript
// src/services/api/menuApi.ts
export const menuApi = {
  getMenus: (storeId: number) => getMenus({ storeId }),
};

// src/services/api/orderApi.ts
export const orderApi = {
  createOrder: (request: CreateOrderRequest) => createOrder(request),
  getOrders: (sessionId: string) => getOrders({ sessionId }),
};

// src/services/api/index.ts
export { menuApi } from './menuApi';
export { orderApi } from './orderApi';
```

---

### Usage in Stores
```typescript
import { menuApi } from '@/services/api';

export const useMenuStore = create<MenuState>((set) => ({
  fetchMenus: async (storeId) => {
    set({ isLoading: true });
    try {
      const menus = await menuApi.getMenus(storeId);
      set({ menus, isLoading: false });
    } catch (error) {
      set({ error: handleApiError(error).message, isLoading: false });
    }
  },
}));
```

---

## Testing

### Mock API Client
```typescript
import { vi } from 'vitest';
import { apiClient } from '@/services/apiClient';

vi.mock('@/services/apiClient', () => ({
  apiClient: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

test('메뉴 조회 성공', async () => {
  (apiClient.get as any).mockResolvedValue({
    data: {
      success: true,
      data: [mockMenu1, mockMenu2],
    },
  });

  const menus = await getMenus({ storeId: 1 });
  expect(menus).toHaveLength(2);
});
```

---

## Notes

- Axios interceptor로 공통 에러 처리
- SSE는 컴포넌트 언마운트 시 연결 해제 필수
- 환경 변수로 API URL 관리
- 개발 환경에서만 로깅 활성화
- CORS 설정은 Backend에서 처리
