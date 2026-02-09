# Integration Test Guide - 테이블오더 서비스

## Overview
Backend와 Customer Frontend 간 통합 테스트 가이드.

---

## Test Scenarios

### Scenario 1: 메뉴 조회 → 주문 생성

#### 1. Backend 서버 시작
```bash
cd backend
java -jar target/table-order-backend-1.0.0.jar
```

서버 시작 확인:
```
Started TableOrderApplication in X.XXX seconds
```

#### 2. 메뉴 조회 테스트
```bash
curl -X GET "http://localhost:8080/api/customer/menus?storeId=1"
```

**Expected Response**:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "storeId": 1,
      "name": "김치찌개",
      "price": 8000,
      "imageUrl": null,
      "createdAt": "2026-02-09T..."
    }
  ],
  "message": null,
  "error": null,
  "timestamp": "2026-02-09T..."
}
```

#### 3. 주문 생성 테스트
```bash
curl -X POST "http://localhost:8080/api/customer/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "storeId": 1,
    "tableId": 1,
    "sessionId": "test-session-001",
    "items": [
      {
        "menuId": 1,
        "quantity": 2
      },
      {
        "menuId": 3,
        "quantity": 1
      }
    ]
  }'
```

**Expected Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "orderNumber": "ORD-20260209-0001",
    "tableId": 1,
    "sessionId": "test-session-001",
    "status": "PENDING",
    "totalAmount": 25000,
    "items": [
      {
        "id": 1,
        "menuId": 1,
        "menuName": "김치찌개",
        "quantity": 2,
        "unitPrice": 8000,
        "subtotal": 16000
      },
      {
        "id": 2,
        "menuId": 3,
        "menuName": "비빔밥",
        "quantity": 1,
        "unitPrice": 9000,
        "subtotal": 9000
      }
    ],
    "createdAt": "2026-02-09T..."
  }
}
```

#### 4. 주문 내역 조회 테스트
```bash
curl -X GET "http://localhost:8080/api/customer/orders?sessionId=test-session-001"
```

---

### Scenario 2: Frontend + Backend 통합

#### 1. Backend 서버 시작
```bash
cd backend
java -jar target/table-order-backend-1.0.0.jar &
```

#### 2. Frontend 개발 서버 시작
```bash
cd frontend/customer
npm run dev
```

#### 3. 브라우저 테스트
1. http://localhost:5173 접속
2. 메뉴 목록 확인
3. 장바구니에 메뉴 추가
4. 주문 생성
5. 주문 내역 확인

#### 4. 브라우저 콘솔 확인
```
[API Request] GET /api/customer/menus?storeId=1
[API Response] /api/customer/menus {...}
[API Request] POST /api/customer/orders
[API Response] /api/customer/orders {...}
```

---

## API Endpoint Tests

### 1. Health Check
```bash
curl http://localhost:8080/actuator/health
```

### 2. Swagger UI
브라우저에서 접속:
```
http://localhost:8080/swagger-ui/index.html
```

### 3. H2 Console
브라우저에서 접속:
```
http://localhost:8080/h2-console
```

**Connection Info**:
- JDBC URL: `jdbc:h2:mem:tableorder`
- User: `SA`
- Password: (empty)

---

## Error Scenarios

### 1. 잘못된 요청
```bash
curl -X POST "http://localhost:8080/api/customer/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "storeId": 1,
    "tableId": 1,
    "sessionId": "invalid-session",
    "items": []
  }'
```

**Expected**: 400 Bad Request

### 2. 존재하지 않는 메뉴
```bash
curl -X GET "http://localhost:8080/api/customer/menus?storeId=999"
```

**Expected**: 200 OK with empty array

### 3. 비활성 세션
```bash
curl -X POST "http://localhost:8080/api/customer/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "storeId": 1,
    "tableId": 2,
    "sessionId": "inactive-session",
    "items": [{"menuId": 1, "quantity": 1}]
  }'
```

**Expected**: 400 Bad Request - "Table session is not active"

---

## Performance Tests

### 1. 동시 요청 테스트
```bash
# 10개 동시 요청
for i in {1..10}; do
  curl -X GET "http://localhost:8080/api/customer/menus?storeId=1" &
done
wait
```

### 2. 부하 테스트 (Apache Bench)
```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8080/api/customer/menus?storeId=1
```

**Expected**:
- Requests per second: > 100
- Time per request: < 100ms
- Failed requests: 0

---

## Database Verification

### 1. H2 Console 접속
```
http://localhost:8080/h2-console
```

### 2. 데이터 확인
```sql
-- 메뉴 확인
SELECT * FROM menu;

-- 주문 확인
SELECT * FROM `order`;

-- 주문 항목 확인
SELECT * FROM order_item;

-- 테이블 확인
SELECT * FROM `table`;
```

---

## Automated Integration Tests

### Bash Script
```bash
#!/bin/bash

echo "🧪 Running Integration Tests..."

# Start Backend
cd backend
java -jar target/table-order-backend-1.0.0.jar > /dev/null 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

# Wait for backend to start
sleep 10

# Test 1: Menu API
echo "Testing Menu API..."
RESPONSE=$(curl -s http://localhost:8080/api/customer/menus?storeId=1)
if echo "$RESPONSE" | grep -q "success"; then
  echo "✅ Menu API test passed"
else
  echo "❌ Menu API test failed"
  kill $BACKEND_PID
  exit 1
fi

# Test 2: Order API
echo "Testing Order API..."
RESPONSE=$(curl -s -X POST http://localhost:8080/api/customer/orders \
  -H "Content-Type: application/json" \
  -d '{
    "storeId": 1,
    "tableId": 1,
    "sessionId": "test-session-001",
    "items": [{"menuId": 1, "quantity": 2}]
  }')
if echo "$RESPONSE" | grep -q "orderNumber"; then
  echo "✅ Order API test passed"
else
  echo "❌ Order API test failed"
  kill $BACKEND_PID
  exit 1
fi

# Cleanup
kill $BACKEND_PID
echo "✅ All integration tests passed!"
```

---

## Test Checklist

### Backend
- [ ] 서버 정상 시작
- [ ] H2 Console 접속 가능
- [ ] Swagger UI 접속 가능
- [ ] 메뉴 조회 API 동작
- [ ] 주문 생성 API 동작
- [ ] 주문 조회 API 동작
- [ ] 에러 처리 정상

### Frontend
- [ ] 개발 서버 정상 시작
- [ ] 메뉴 페이지 렌더링
- [ ] 장바구니 기능 동작
- [ ] 주문 생성 기능 동작
- [ ] Toast 메시지 표시
- [ ] 라우팅 정상 동작

### Integration
- [ ] Frontend → Backend API 통신
- [ ] CORS 정상 동작
- [ ] 에러 처리 정상
- [ ] 데이터 일관성 유지

---

## Troubleshooting

### Backend 서버 시작 실패
```bash
# 포트 사용 확인
lsof -i :8080

# 프로세스 종료
kill -9 <PID>
```

### Frontend 서버 시작 실패
```bash
# 포트 사용 확인
lsof -i :5173

# 프로세스 종료
kill -9 <PID>
```

### CORS 에러
Backend SecurityConfig 확인:
```java
configuration.setAllowedOrigins(Arrays.asList("http://localhost:5173"));
```

---

## Notes

- 통합 테스트는 실제 환경과 유사하게 구성
- 테스트 데이터는 data.sql에서 관리
- 테스트 후 서버 정리 필수
- CI/CD에서 자동화 권장
