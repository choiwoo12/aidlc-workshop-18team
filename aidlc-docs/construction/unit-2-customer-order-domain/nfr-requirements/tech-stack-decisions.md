# Tech Stack Decisions - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 기술 스택 결정입니다. Unit 1의 기술 스택을 상속하고 Unit 2 특화 기술을 추가합니다.

---

## Inherited Technology Stack (from Unit 1)

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLite (파일 기반)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: PyJWT (HS256)
- **Password Hashing**: bcrypt
- **Logging**: Python 내장 logging

### Frontend
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.0+
- **Styling**: Tailwind CSS 3.4+
- **HTTP Client**: Axios 1.6+
- **State Management**: React Context API
- **Routing**: React Router DOM 6.21+

### Infrastructure
- **Deployment**: Docker Compose
- **Database Storage**: 로컬 파일 시스템 (볼륨 마운트)
- **File Storage**: 로컬 파일 시스템 (볼륨 마운트)
- **Logging Storage**: 로컬 파일 시스템 (볼륨 마운트)

---

## Unit 2 Specific Technology Decisions

### 1. Real-time Communication

#### 1.1 SSE (Server-Sent Events)

**Decision**: FastAPI의 `StreamingResponse` 사용

**Rationale**:
- FastAPI 내장 기능으로 추가 라이브러리 불필요
- 단방향 통신으로 주문 상태 업데이트에 적합
- WebSocket 대비 단순한 구현
- HTTP/1.1 기반으로 방화벽 문제 없음

**Implementation**:
```python
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

@app.get("/api/sse/orders/{table_id}")
async def sse_orders(table_id: int):
    return EventSourceResponse(event_generator(table_id))
```

**Alternative Considered**:
- WebSocket: 양방향 통신 불필요, 복잡도 증가
- Polling: 서버 부하 증가, 실시간성 저하

---

#### 1.2 SSE Client (Frontend)

**Decision**: 브라우저 내장 `EventSource` API 사용

**Rationale**:
- 브라우저 표준 API로 추가 라이브러리 불필요
- 자동 재연결 기능 내장
- 간단한 이벤트 리스너 구조

**Implementation**:
```javascript
const eventSource = new EventSource(`/api/sse/orders/${tableId}`);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // 주문 상태 업데이트
};

eventSource.onerror = (error) => {
  // 재연결 로직
};
```

**Alternative Considered**:
- `eventsource` npm 패키지: 브라우저 API로 충분
- WebSocket 클라이언트: 복잡도 증가

---

### 2. State Management

#### 2.1 Cart State Management

**Decision**: React Context API + SessionStorage

**Rationale**:
- React Context API로 전역 상태 관리 (Unit 1 상속)
- SessionStorage로 브라우저 새로고침 시 복원
- 추가 라이브러리 불필요 (Redux, Zustand 등)
- 단순한 상태 구조로 Context API로 충분

**Implementation**:
```javascript
// CartContext.jsx
const CartContext = createContext();

export function CartProvider({ children }) {
  const [cart, setCart] = useState(() => {
    // SessionStorage에서 복원
    const saved = sessionStorage.getItem('cart');
    return saved ? JSON.parse(saved) : { items: [], total: 0 };
  });

  useEffect(() => {
    // SessionStorage에 저장
    sessionStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  return (
    <CartContext.Provider value={{ cart, setCart }}>
      {children}
    </CartContext.Provider>
  );
}
```

**Alternative Considered**:
- Redux: 과도한 복잡도
- Zustand: 추가 라이브러리 불필요
- LocalStorage: 세션 개념과 맞지 않음

---

#### 2.2 Order State Management

**Decision**: React Context API (실시간 업데이트용)

**Rationale**:
- SSE 이벤트 수신 시 전역 상태 업데이트
- 주문 내역 화면에서 실시간 반영
- Context API로 충분한 복잡도

**Implementation**:
```javascript
// OrderContext.jsx
const OrderContext = createContext();

export function OrderProvider({ children }) {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    // SSE 연결 및 이벤트 리스너
    const eventSource = new EventSource(`/api/sse/orders/${tableId}`);
    
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // 주문 상태 업데이트
      setOrders(prev => 
        prev.map(order => 
          order.id === data.order_id 
            ? { ...order, status: data.new_status }
            : order
        )
      );
    };

    return () => eventSource.close();
  }, [tableId]);

  return (
    <OrderContext.Provider value={{ orders, setOrders }}>
      {children}
    </OrderContext.Provider>
  );
}
```

---

### 3. Image Handling

#### 3.1 Image Storage

**Decision**: 로컬 파일 시스템 (Unit 1 상속)

**Rationale**:
- Unit 1의 FileStorage 재사용
- 추가 인프라 불필요
- MVP 범위에서 충분

**Path**: `uploads/menus/{menu_id}/{filename}`

---

#### 3.2 Image Optimization

**Decision**: 최적화 없음 (원본 이미지 사용)

**Rationale**:
- MVP 범위에서 최적화 불필요
- 소규모 매장으로 이미지 개수 제한적
- 개발 시간 단축

**Future Enhancement**:
- 이미지 리사이징 (Pillow 라이브러리)
- WebP 변환
- Lazy Loading

---

### 4. Caching Strategy

#### 4.1 Menu Query Caching

**Decision**: 캐싱 없음 (매번 서버 조회)

**Rationale**:
- 메뉴 변경이 즉시 반영되어야 함
- 소규모 매장으로 메뉴 개수 제한적
- 1초 응답 시간 목표 달성 가능

**Database Optimization**:
- 인덱스 활용 (store_id, is_available)
- 필요한 컬럼만 조회

**Future Enhancement**:
- 인메모리 캐싱 (5분 TTL)
- 수동 무효화 (메뉴 변경 시)

---

### 5. Data Validation

#### 5.1 Client-side Validation

**Decision**: 커스텀 ValidationService

**Rationale**:
- 빠른 피드백으로 사용자 경험 향상
- 서버 부하 감소
- 재사용 가능한 유틸리티

**Implementation**:
```javascript
// ValidationService.js
export const ValidationService = {
  validateRequiredOptions(menu, selectedOptions) {
    const errors = [];
    menu.options.option_groups.forEach(group => {
      if (group.required) {
        const hasSelection = selectedOptions.some(
          opt => opt.group_id === group.id
        );
        if (!hasSelection) {
          errors.push(`${group.name}을(를) 선택해주세요.`);
        }
      }
    });
    return { valid: errors.length === 0, errors };
  },

  validateCart(cart) {
    if (cart.items.length === 0) {
      return { valid: false, errors: ['장바구니가 비어있습니다.'] };
    }
    return { valid: true, errors: [] };
  }
};
```

---

#### 5.2 Server-side Validation

**Decision**: Pydantic 모델 + 커스텀 검증 로직

**Rationale**:
- Pydantic으로 타입 및 기본 검증
- 커스텀 로직으로 비즈니스 규칙 검증
- FastAPI와 완벽한 통합

**Implementation**:
```python
from pydantic import BaseModel, validator

class OrderCreateRequest(BaseModel):
    table_id: int
    cart_items: List[CartItemRequest]

    @validator('cart_items')
    def validate_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError('장바구니가 비어있습니다.')
        return v

# 서비스 레이어에서 추가 검증
def validate_order_items(cart_items):
    for item in cart_items:
        menu = menu_repository.get_by_id(item.menu_id)
        if not menu.is_available:
            raise ValidationError(f'{menu.name}은(는) 현재 판매하지 않습니다.')
        if item.menu_price_snapshot != menu.price:
            raise ValidationError('메뉴 가격이 변경되었습니다.')
```

---

### 6. Error Handling

#### 6.1 Frontend Error Handling

**Decision**: Axios 인터셉터 + 커스텀 에러 핸들러

**Rationale**:
- 중앙 집중식 에러 처리
- 일관된 에러 메시지
- Unit 1의 패턴 재사용

**Implementation**:
```javascript
// axios.js (Unit 1에서 확장)
axios.interceptors.response.use(
  response => response,
  error => {
    // 기본 에러 메시지
    const message = '주문 생성에 실패했습니다. 다시 시도해주세요.';
    
    // 에러 토스트 표시
    showErrorToast(message);
    
    return Promise.reject(error);
  }
);
```

---

#### 6.2 Backend Error Handling

**Decision**: FastAPI 예외 핸들러 (Unit 1 상속)

**Rationale**:
- 중앙 집중식 에러 처리
- 일관된 에러 응답 형식
- 에러 로깅 자동화

**Implementation**:
```python
# Unit 1의 error_middleware.py 재사용
@app.exception_handler(ValidationError)
async def validation_error_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
```

---

### 7. Logging

#### 7.1 Backend Logging

**Decision**: Python 내장 logging (Unit 1 상속) + Unit 2 전용 로거

**Rationale**:
- Unit 1의 로깅 설정 재사용
- Unit 2 전용 로그 파일로 분리
- 파일 로깅으로 영구 기록

**Configuration**:
```python
# logging_config.py (Unit 1 확장)
LOGGING_CONFIG = {
    'loggers': {
        'unit2': {
            'handlers': ['unit2_file'],
            'level': 'INFO',
        }
    },
    'handlers': {
        'unit2_file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'logs/unit2.log',
            'when': 'midnight',
            'backupCount': 30,
        }
    }
}
```

---

### 8. Testing Libraries

#### 8.1 Backend Testing

**Decision**: pytest + pytest-asyncio (Unit 1 상속)

**Rationale**:
- FastAPI 공식 권장 테스트 프레임워크
- 비동기 테스트 지원
- 풍부한 플러그인 생태계

**Additional Libraries**:
- `httpx`: FastAPI 테스트 클라이언트
- `pytest-cov`: 코드 커버리지

---

#### 8.2 Frontend Testing

**Decision**: Vitest + React Testing Library (Unit 1 상속)

**Rationale**:
- Vite와 완벽한 통합
- 빠른 테스트 실행
- React Testing Library로 사용자 중심 테스트

**Additional Libraries**:
- `@testing-library/react`: React 컴포넌트 테스트
- `@testing-library/user-event`: 사용자 이벤트 시뮬레이션

---

## Technology Stack Summary

### Backend
| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Framework | FastAPI | 0.104+ | API 서버 |
| Database | SQLite | 3.x | 데이터 저장 |
| ORM | SQLAlchemy | 2.0+ | 데이터베이스 ORM |
| Real-time | SSE (StreamingResponse) | Built-in | 실시간 통신 |
| Authentication | PyJWT | 2.8+ | JWT 토큰 |
| Password | bcrypt | 4.1+ | 비밀번호 해싱 |
| Validation | Pydantic | 2.5+ | 데이터 검증 |
| Logging | logging | Built-in | 로깅 |
| Testing | pytest | 7.4+ | 테스트 |

### Frontend
| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Framework | React | 18.2+ | UI 프레임워크 |
| Build Tool | Vite | 5.0+ | 빌드 도구 |
| Styling | Tailwind CSS | 3.4+ | CSS 프레임워크 |
| HTTP Client | Axios | 1.6+ | HTTP 요청 |
| Real-time | EventSource | Built-in | SSE 클라이언트 |
| State Management | React Context API | Built-in | 상태 관리 |
| Routing | React Router DOM | 6.21+ | 라우팅 |
| Storage | SessionStorage | Built-in | 클라이언트 저장소 |
| Testing | Vitest | 1.0+ | 테스트 |

### Infrastructure
| Category | Technology | Purpose |
|----------|-----------|---------|
| Deployment | Docker Compose | 컨테이너 오케스트레이션 |
| Database Storage | 로컬 파일 시스템 | 데이터 영속성 |
| File Storage | 로컬 파일 시스템 | 이미지 저장 |
| Logging Storage | 로컬 파일 시스템 | 로그 저장 |

---

## Dependencies

### Backend (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.2
pydantic-settings==2.1.0
pyjwt==2.8.0
bcrypt==4.1.1
python-multipart==0.0.6
sse-starlette==1.8.2
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
pytest-cov==4.1.0
```

### Frontend (package.json)
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "vitest": "^1.0.4",
    "@testing-library/react": "^14.1.2",
    "@testing-library/user-event": "^14.5.1",
    "eslint": "^8.56.0"
  }
}
```

---

## Decision Rationale Summary

### Why SSE over WebSocket?
- 단방향 통신으로 충분 (주문 상태 업데이트만 필요)
- 단순한 구현 및 유지보수
- HTTP/1.1 기반으로 방화벽 문제 없음
- 브라우저 내장 API 사용 가능

### Why No Caching?
- 메뉴 변경이 즉시 반영되어야 함
- 소규모 매장으로 성능 문제 없음
- 단순한 구현

### Why SessionStorage?
- 브라우저 탭별 독립적인 세션 관리
- 브라우저 종료 시 자동 삭제 (세션 개념과 일치)
- 추가 서버 저장소 불필요

### Why No Image Optimization?
- MVP 범위에서 불필요
- 소규모 매장으로 이미지 개수 제한적
- 개발 시간 단축

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
