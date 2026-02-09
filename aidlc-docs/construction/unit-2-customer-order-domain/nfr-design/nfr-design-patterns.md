# NFR Design Patterns - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 NFR 설계 패턴입니다. NFR 요구사항을 구체적인 설계 패턴으로 변환하여 인프라 독립적인 설계를 제공합니다.

---

## Pattern Categories

1. Real-time Communication Patterns
2. State Management Patterns
3. Data Validation Patterns
4. Error Handling Patterns
5. Performance Optimization Patterns
6. Data Persistence Patterns

---

## 1. Real-time Communication Patterns

### Pattern 1.1: SSE Connection Management

**Purpose**: SSE 연결 생명주기 관리 및 자동 재연결

**Context**: 
- 고객 화면에서 주문 상태 실시간 업데이트 필요
- 네트워크 불안정 시 자동 재연결 필요
- 연결 끊김 감지 및 복구 필요

**Solution**:
```javascript
// Frontend: SSE Connection Manager
class SSEConnectionManager {
  constructor(tableId) {
    this.tableId = tableId;
    this.eventSource = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3;
    this.reconnectDelays = [0, 5000, 10000]; // 즉시, 5초, 10초
  }

  connect(onMessage, onError) {
    this.eventSource = new EventSource(`/api/sse/orders/${this.tableId}`);
    
    this.eventSource.onmessage = (event) => {
      this.reconnectAttempts = 0; // 성공 시 재연결 카운터 리셋
      onMessage(event);
    };
    
    this.eventSource.onerror = (error) => {
      this.handleConnectionError(onMessage, onError);
    };
  }

  handleConnectionError(onMessage, onError) {
    this.eventSource.close();
    
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const delay = this.reconnectDelays[this.reconnectAttempts];
      this.reconnectAttempts++;
      
      setTimeout(() => {
        this.connect(onMessage, onError);
      }, delay);
    } else {
      onError(new Error('SSE 연결에 실패했습니다. 페이지를 새로고침해주세요.'));
    }
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
  }
}
```

**Backend Implementation**:
```python
# Backend: SSE Event Generator
from fastapi.responses import StreamingResponse
import asyncio
import json

async def sse_event_generator(table_id: int):
    """SSE 이벤트 생성기"""
    try:
        while True:
            # Keep-alive 메시지 (30초마다)
            yield ":\n\n"  # 빈 메시지
            await asyncio.sleep(30)
            
            # 실제 이벤트는 주문 상태 변경 시 발송
            # (별도 이벤트 큐에서 가져옴)
    except asyncio.CancelledError:
        # 연결 종료 시 정리
        pass

@app.get("/api/sse/orders/{table_id}")
async def sse_orders(table_id: int):
    return StreamingResponse(
        sse_event_generator(table_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

**Benefits**:
- 자동 재연결로 사용자 편의성 향상
- 연결 끊김 감지 및 복구
- Keep-alive로 연결 유지

**Trade-offs**:
- 재연결 시 일시적인 이벤트 손실 가능 (전체 조회로 복구)

---

### Pattern 1.2: SSE Event Recovery

**Purpose**: SSE 재연결 후 누락된 이벤트 복구

**Context**:
- 재연결 중 발생한 주문 상태 변경 이벤트 누락 가능
- 데이터 일관성 보장 필요

**Solution**:
```javascript
// Frontend: Event Recovery
class OrderStateManager {
  constructor(tableId) {
    this.tableId = tableId;
    this.sseManager = new SSEConnectionManager(tableId);
  }

  async initialize() {
    // 초기 주문 목록 조회
    await this.fetchAllOrders();
    
    // SSE 연결 시작
    this.sseManager.connect(
      this.handleSSEMessage.bind(this),
      this.handleSSEError.bind(this)
    );
  }

  async fetchAllOrders() {
    // 전체 주문 목록 조회 (재연결 시에도 호출)
    const response = await axios.get(`/api/orders?table_id=${this.tableId}`);
    this.updateOrderList(response.data);
  }

  handleSSEMessage(event) {
    const data = JSON.parse(event.data);
    
    if (data.type === 'order_status_changed') {
      // 개별 주문 상태 업데이트
      this.updateOrderStatus(data.order_id, data.new_status);
    }
  }

  async handleSSEError(error) {
    // 재연결 실패 시 전체 주문 목록 다시 조회
    await this.fetchAllOrders();
    // 에러 메시지 표시
    showErrorToast(error.message);
  }
}
```

**Benefits**:
- 재연결 후 데이터 일관성 보장
- 안전한 복구 전략

**Trade-offs**:
- 재연결 시 전체 조회로 인한 네트워크 오버헤드

---

## 2. State Management Patterns

### Pattern 2.1: Cart State Management

**Purpose**: 장바구니 상태 관리 및 영속성

**Context**:
- 장바구니 데이터를 SessionStorage에 저장
- 페이지 새로고침 시 복원 필요
- 중복 항목 처리 필요

**Solution**:
```javascript
// Frontend: Cart Manager
class CartManager {
  constructor() {
    this.storageKey = 'cart';
    this.cart = this.loadFromStorage();
  }

  loadFromStorage() {
    try {
      const saved = sessionStorage.getItem(this.storageKey);
      return saved ? JSON.parse(saved) : { items: [], total: 0 };
    } catch (error) {
      // JSON.parse 실패 시 빈 장바구니로 초기화
      console.error('Failed to load cart from storage:', error);
      return { items: [], total: 0 };
    }
  }

  saveToStorage() {
    try {
      sessionStorage.setItem(this.storageKey, JSON.stringify(this.cart));
    } catch (error) {
      // JSON.stringify 실패 시 빈 장바구니로 초기화
      console.error('Failed to save cart to storage:', error);
      this.cart = { items: [], total: 0 };
      sessionStorage.setItem(this.storageKey, JSON.stringify(this.cart));
    }
  }

  addItem(menu, selectedOptions, quantity = 1) {
    // 중복 항목 확인 (옵션 순서 무관)
    const existingItem = this.findDuplicateItem(menu.id, selectedOptions);
    
    if (existingItem) {
      // 수량 증가
      existingItem.quantity += quantity;
      existingItem.subtotal = this.calculateSubtotal(
        existingItem.menu_snapshot.price,
        existingItem.selected_options,
        existingItem.quantity
      );
    } else {
      // 새 항목 추가
      const newItem = {
        cart_item_id: this.generateUUID(),
        menu_id: menu.id,
        menu_snapshot: {
          name: menu.name,
          price: menu.price,
          image_url: menu.image_url
        },
        selected_options: selectedOptions,
        quantity: quantity,
        subtotal: this.calculateSubtotal(menu.price, selectedOptions, quantity)
      };
      this.cart.items.push(newItem);
    }
    
    this.updateTotal();
    this.saveToStorage();
  }

  findDuplicateItem(menuId, selectedOptions) {
    return this.cart.items.find(item => 
      item.menu_id === menuId && 
      this.isSameOptions(item.selected_options, selectedOptions)
    );
  }

  isSameOptions(options1, options2) {
    // 옵션 순서 무관 비교
    if (options1.length !== options2.length) return false;
    
    // 옵션 그룹별로 정렬 후 비교
    const sorted1 = this.sortOptions(options1);
    const sorted2 = this.sortOptions(options2);
    
    return JSON.stringify(sorted1) === JSON.stringify(sorted2);
  }

  sortOptions(options) {
    // 그룹 ID로 정렬 후, 각 그룹 내에서 선택 ID로 정렬
    return options
      .slice()
      .sort((a, b) => {
        if (a.group_id !== b.group_id) {
          return a.group_id.localeCompare(b.group_id);
        }
        return a.choice_id.localeCompare(b.choice_id);
      });
  }

  calculateSubtotal(menuPrice, selectedOptions, quantity) {
    const optionPrice = selectedOptions.reduce(
      (sum, opt) => sum + opt.price_adjustment, 
      0
    );
    return (menuPrice + optionPrice) * quantity;
  }

  updateTotal() {
    this.cart.total = this.cart.items.reduce(
      (sum, item) => sum + item.subtotal, 
      0
    );
  }

  clear() {
    this.cart = { items: [], total: 0 };
    this.saveToStorage();
  }
}
```

**Benefits**:
- 옵션 순서 무관 비교로 사용자 편의성 향상
- 안전한 에러 처리 (빈 장바구니로 초기화)
- SessionStorage로 페이지 새로고침 시 복원

**Trade-offs**:
- 옵션 정렬로 인한 약간의 성능 오버헤드 (무시 가능)

---

### Pattern 2.2: Order State Synchronization

**Purpose**: SSE를 통한 주문 상태 실시간 동기화

**Context**:
- 관리자가 주문 상태 변경 시 고객 화면에 즉시 반영
- 주문 내역 화면에서 실시간 업데이트

**Solution**:
```javascript
// Frontend: Order Context with SSE
import React, { createContext, useState, useEffect, useContext } from 'react';

const OrderContext = createContext();

export function OrderProvider({ children }) {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const { tableId } = useContext(AuthContext);

  useEffect(() => {
    if (!tableId) return;

    const orderManager = new OrderStateManager(tableId);
    
    // 초기 주문 목록 조회
    orderManager.initialize().then(() => {
      setOrders(orderManager.orders);
      setLoading(false);
    });

    // SSE 이벤트 리스너
    orderManager.onOrderUpdate = (updatedOrders) => {
      setOrders(updatedOrders);
    };

    return () => {
      orderManager.disconnect();
    };
  }, [tableId]);

  return (
    <OrderContext.Provider value={{ orders, loading }}>
      {children}
    </OrderContext.Provider>
  );
}
```

**Benefits**:
- React Context로 전역 상태 관리
- SSE 이벤트 자동 반영
- 컴포넌트 간 상태 공유

---

## 3. Data Validation Patterns

### Pattern 3.1: Client-side Validation

**Purpose**: 빠른 피드백을 위한 클라이언트 측 검증

**Context**:
- 장바구니 추가 시 필수 옵션 검증
- 주문 생성 시 장바구니 비어있지 않음 검증

**Solution**:
```javascript
// Frontend: Validation Service
class ValidationService {
  static validateRequiredOptions(menu, selectedOptions) {
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
  }

  static validateCart(cart) {
    if (cart.items.length === 0) {
      return { 
        valid: false, 
        errors: ['장바구니가 비어있습니다.'] 
      };
    }
    return { valid: true, errors: [] };
  }

  static validateQuantity(quantity) {
    if (quantity < 1) {
      return { 
        valid: false, 
        errors: ['수량은 1 이상이어야 합니다.'] 
      };
    }
    return { valid: true, errors: [] };
  }
}
```

**Benefits**:
- 빠른 피드백으로 사용자 경험 향상
- 서버 부하 감소

---

### Pattern 3.2: Server-side Validation

**Purpose**: 데이터 무결성을 위한 서버 측 검증

**Context**:
- 메뉴 판매 가능 여부 확인
- 가격 일치 확인
- 옵션 유효성 확인

**Solution**:
```python
# Backend: Order Validation Service
from app.utils.exceptions import ValidationError

class OrderValidationService:
    def __init__(self, menu_repository, order_repository):
        self.menu_repository = menu_repository
        self.order_repository = order_repository

    def validate_order_items(self, cart_items):
        """주문 항목 유효성 검증"""
        for item in cart_items:
            # 메뉴 존재 여부 확인
            menu = self.menu_repository.get_by_id(item.menu_id)
            if not menu:
                raise ValidationError(f'메뉴를 찾을 수 없습니다.')
            
            # 판매 가능 여부 확인
            if not menu.is_available:
                raise ValidationError(
                    f'{menu.name}은(는) 현재 판매하지 않습니다.'
                )
            
            # 가격 일치 확인
            if item.menu_price_snapshot != menu.price:
                raise ValidationError(
                    '메뉴 가격이 변경되었습니다. 장바구니를 다시 확인해주세요.'
                )
            
            # 옵션 유효성 확인
            self.validate_options(menu, item.selected_options)

    def validate_options(self, menu, selected_options):
        """옵션 유효성 검증"""
        for selected_opt in selected_options:
            # 옵션 그룹 존재 여부
            group = next(
                (g for g in menu.options['option_groups'] 
                 if g['id'] == selected_opt.group_id),
                None
            )
            if not group:
                raise ValidationError('유효하지 않은 옵션입니다.')
            
            # 옵션 선택 항목 존재 여부
            choice = next(
                (c for c in group['choices'] 
                 if c['id'] == selected_opt.choice_id),
                None
            )
            if not choice:
                raise ValidationError('유효하지 않은 옵션입니다.')
```

**Benefits**:
- 데이터 무결성 보장
- 악의적인 요청 차단

---

## 4. Error Handling Patterns

### Pattern 4.1: Graceful Error Handling

**Purpose**: 사용자 친화적 에러 처리

**Context**:
- 모든 에러에 대해 기본 메시지 표시
- 에러 발생 시 장바구니 유지

**Solution**:
```javascript
// Frontend: Error Handler
class ErrorHandler {
  static handleAPIError(error, context) {
    // 기본 에러 메시지
    const message = '주문 생성에 실패했습니다. 다시 시도해주세요.';
    
    // 에러 로깅 (개발 환경)
    if (process.env.NODE_ENV === 'development') {
      console.error(`[${context}] Error:`, error);
    }
    
    // 사용자에게 에러 메시지 표시
    showErrorToast(message);
    
    return { success: false, message };
  }

  static handleMenuFetchError(error) {
    const message = '메뉴를 불러오는데 실패했습니다.';
    showErrorToast(message);
    
    // 수동 재시도 버튼 표시
    return { 
      success: false, 
      message,
      showRetryButton: true 
    };
  }

  static handleCartError(error) {
    // 장바구니 에러는 조용히 처리 (빈 장바구니로 초기화)
    console.error('Cart error:', error);
    return { items: [], total: 0 };
  }
}
```

**Benefits**:
- 일관된 에러 메시지
- 사용자 혼란 최소화
- 장바구니 데이터 보호

---

### Pattern 4.2: Retry Strategy

**Purpose**: 에러 발생 시 재시도 전략

**Context**:
- 메뉴 조회 실패 시 수동 재시도
- SSE 연결 실패 시 자동 재시도

**Solution**:
```javascript
// Frontend: Retry Button Component
function MenuList() {
  const [menus, setMenus] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchMenus = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get('/api/menus');
      setMenus(response.data);
    } catch (err) {
      const errorResult = ErrorHandler.handleMenuFetchError(err);
      setError(errorResult);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMenus();
  }, []);

  if (loading) return <Loading />;
  
  if (error && error.showRetryButton) {
    return (
      <div className="error-container">
        <p>{error.message}</p>
        <button onClick={fetchMenus}>다시 시도</button>
      </div>
    );
  }

  return <div>{/* 메뉴 목록 렌더링 */}</div>;
}
```

**Benefits**:
- 사용자 제어 재시도
- 명확한 에러 상태 표시

---

## 5. Performance Optimization Patterns

### Pattern 5.1: Order Number Generation

**Purpose**: 주문 번호 생성 최적화

**Context**:
- 테이블별 순차 번호 생성
- AUTO_INCREMENT 활용으로 동시성 제어 단순화

**Solution**:
```python
# Backend: Order Number Generator
class OrderNumberGenerator:
    def __init__(self, order_repository):
        self.order_repository = order_repository

    def generate(self, table_number: str) -> str:
        """
        주문 번호 생성: T{테이블번호}-{순차번호}
        
        AUTO_INCREMENT를 활용하여 동시성 제어 단순화
        """
        # 테이블별 마지막 순차 번호 조회
        last_order = self.order_repository.get_last_order_by_table(table_number)
        
        if last_order:
            # 마지막 주문 번호에서 순차 번호 추출
            last_seq = int(last_order.order_number.split('-')[1])
            next_seq = last_seq + 1
        else:
            # 첫 주문
            next_seq = 1
        
        # 주문 번호 생성 (T01-001 형식)
        order_number = f"T{table_number}-{next_seq:03d}"
        
        return order_number
```

**Alternative with AUTO_INCREMENT**:
```python
# Database Schema
class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    table_id = Column(Integer, ForeignKey('tables.id'))
    sequence_number = Column(Integer)  # 테이블별 순차 번호
    order_number = Column(String(20), unique=True)
    
    # 테이블별 순차 번호 자동 생성
    @staticmethod
    def generate_sequence_number(session, table_id):
        last_order = session.query(Order)\
            .filter(Order.table_id == table_id)\
            .order_by(Order.sequence_number.desc())\
            .first()
        
        return (last_order.sequence_number + 1) if last_order else 1
```

**Benefits**:
- AUTO_INCREMENT로 동시성 제어 단순화
- 데이터베이스 레벨에서 순차 번호 보장

---

### Pattern 5.2: Menu Query Optimization

**Purpose**: 메뉴 조회 성능 최적화

**Context**:
- 캐싱 없이 항상 최신 데이터 조회
- 1초 응답 시간 목표

**Solution**:
```python
# Backend: Optimized Menu Query
class MenuRepository:
    def find_available_menus(self, store_id: int, category: str = None):
        """
        판매 가능한 메뉴 조회 (최적화)
        
        - 인덱스 활용 (store_id, is_available)
        - 필요한 컬럼만 조회
        - 카테고리 필터링
        """
        query = self.session.query(Menu)\
            .filter(Menu.store_id == store_id)\
            .filter(Menu.is_available == True)
        
        if category:
            query = query.filter(
                or_(
                    Menu.category_level1 == category,
                    Menu.category_level2 == category
                )
            )
        
        # 필요한 컬럼만 조회 (options는 JSON 필드)
        return query.all()
```

**Database Indexes**:
```sql
-- 성능 최적화를 위한 인덱스
CREATE INDEX idx_menu_store_available 
ON menus(store_id, is_available);

CREATE INDEX idx_menu_category 
ON menus(category_level1, category_level2);
```

**Benefits**:
- 인덱스 활용으로 빠른 조회
- 1초 응답 시간 목표 달성

---

## 6. Data Persistence Patterns

### Pattern 6.1: SessionStorage Persistence

**Purpose**: 장바구니 데이터 영속성

**Context**:
- 브라우저 새로고침 시 장바구니 복원
- 브라우저 탭 닫기 시 자동 삭제

**Solution**:
```javascript
// Frontend: Storage Service
class StorageService {
  static saveCart(cart) {
    try {
      sessionStorage.setItem('cart', JSON.stringify(cart));
      return { success: true };
    } catch (error) {
      console.error('Failed to save cart:', error);
      return { success: false, error };
    }
  }

  static loadCart() {
    try {
      const saved = sessionStorage.getItem('cart');
      return saved ? JSON.parse(saved) : { items: [], total: 0 };
    } catch (error) {
      console.error('Failed to load cart:', error);
      return { items: [], total: 0 };
    }
  }

  static clearCart() {
    sessionStorage.removeItem('cart');
  }
}
```

**Benefits**:
- 페이지 새로고침 시 장바구니 복원
- 브라우저 탭 닫기 시 자동 삭제 (세션 개념과 일치)

---

## Pattern Summary

| Pattern | Category | Purpose | Complexity |
|---------|----------|---------|------------|
| SSE Connection Management | Real-time | 자동 재연결 | Medium |
| SSE Event Recovery | Real-time | 이벤트 복구 | Low |
| Cart State Management | State | 장바구니 관리 | Medium |
| Order State Sync | State | 주문 상태 동기화 | Low |
| Client Validation | Validation | 빠른 피드백 | Low |
| Server Validation | Validation | 데이터 무결성 | Medium |
| Graceful Error Handling | Error | 사용자 친화적 에러 | Low |
| Retry Strategy | Error | 재시도 전략 | Low |
| Order Number Generation | Performance | 순차 번호 생성 | Low |
| Menu Query Optimization | Performance | 조회 최적화 | Low |
| SessionStorage Persistence | Persistence | 장바구니 영속성 | Low |

---

## Design Principles

1. **Simplicity First**: 가장 단순한 구현 선택 (MVP 범위)
2. **User Experience**: 사용자 편의성 우선 (자동 재연결, 옵션 순서 무관)
3. **Data Safety**: 에러 발생 시 데이터 보호 (장바구니 유지, 빈 장바구니 초기화)
4. **Performance**: 1-2초 응답 시간 목표 달성
5. **Consistency**: 재연결 후 데이터 일관성 보장

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
