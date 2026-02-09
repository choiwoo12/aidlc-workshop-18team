# Backend API Documentation

## Overview
Backend REST API 엔드포인트 명세입니다. 모든 API는 `/api` prefix를 사용합니다.

---

## Base URL
```
http://localhost:8080/api
```

---

## Authentication

### Admin APIs
- **Header**: `Authorization: Bearer {JWT_TOKEN}`
- **Token 획득**: POST `/api/auth/login`

### Customer APIs
- **No Authentication Required** (세션 ID로 검증)

---

## API Endpoints

### 1. Auth APIs

#### 1.1 Admin Login
```
POST /api/auth/login
```

**Request Body**:
```json
{
  "storeId": 1,
  "username": "admin1",
  "password": "admin123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin1",
      "role": "ADMIN",
      "storeId": 1
    }
  },
  "message": "로그인 성공",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

---

### 2. Customer Order APIs

#### 2.1 Create Order
```
POST /api/customer/orders
```

**Request Body**:
```json
{
  "storeId": 1,
  "tableId": 1,
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "items": [
    {
      "menuId": 1,
      "quantity": 2
    },
    {
      "menuId": 2,
      "quantity": 1
    }
  ]
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "orderNumber": "ORD-20260209-0001",
    "storeId": 1,
    "tableId": 1,
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "orderTime": "2026-02-09T15:00:00",
    "totalAmount": 23000,
    "status": "대기중",
    "version": 0,
    "items": [
      {
        "id": 1,
        "menuId": 1,
        "menuName": "김치찌개",
        "quantity": 2,
        "unitPrice": 8000
      },
      {
        "id": 2,
        "menuId": 2,
        "menuName": "된장찌개",
        "quantity": 1,
        "unitPrice": 7000
      }
    ]
  },
  "message": "주문이 생성되었습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 2.2 Get Orders by Session
```
GET /api/customer/orders?tableId=1&sessionId=550e8400-e29b-41d4-a716-446655440000
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "orderNumber": "ORD-20260209-0001",
      "totalAmount": 23000,
      "status": "대기중",
      "orderTime": "2026-02-09T15:00:00",
      "items": [...]
    }
  ],
  "message": null,
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

---

### 3. Customer Menu APIs

#### 3.1 Get Menus by Store
```
GET /api/customer/menus?storeId=1
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "김치찌개",
      "price": 8000,
      "description": "얼큰한 김치찌개",
      "category": "찌개류",
      "imagePath": "/uploads/menus/1707465600000.jpg",
      "displayOrder": 1
    },
    {
      "id": 2,
      "name": "된장찌개",
      "price": 7000,
      "description": "구수한 된장찌개",
      "category": "찌개류",
      "imagePath": null,
      "displayOrder": 2
    }
  ],
  "message": null,
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

---

### 4. Customer SSE APIs

#### 4.1 Connect to SSE
```
GET /api/customer/sse?tableId=1&sessionId=550e8400-e29b-41d4-a716-446655440000
```

**Response**: Server-Sent Events stream

**Event Types**:
- `ORDER_STATUS_CHANGED`: 주문 상태 변경
- `connected`: 연결 성공

---

### 5. Admin Order APIs

#### 5.1 Get All Orders
```
GET /api/admin/orders?storeId=1
Authorization: Bearer {JWT_TOKEN}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "orderNumber": "ORD-20260209-0001",
      "tableId": 1,
      "totalAmount": 23000,
      "status": "대기중",
      "orderTime": "2026-02-09T15:00:00",
      "items": [...]
    }
  ],
  "message": null,
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 5.2 Update Order Status
```
PUT /api/admin/orders/{id}/status
Authorization: Bearer {JWT_TOKEN}
```

**Request Body**:
```json
{
  "status": "준비중",
  "version": 0
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "orderNumber": "ORD-20260209-0001",
    "status": "준비중",
    "version": 1,
    ...
  },
  "message": "주문 상태가 변경되었습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 5.3 Delete Order
```
DELETE /api/admin/orders/{id}
Authorization: Bearer {JWT_TOKEN}
```

**Response** (204 No Content)

---

### 6. Admin Menu APIs

#### 6.1 Create Menu
```
POST /api/admin/menus
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data
```

**Form Data**:
- `storeId`: 1
- `name`: "새로운 메뉴"
- `price`: 10000
- `description`: "맛있는 메뉴"
- `category`: "신메뉴"
- `image`: (file)

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 10,
    "name": "새로운 메뉴",
    "price": 10000,
    "imagePath": "/uploads/menus/1707465600000.jpg",
    ...
  },
  "message": "메뉴가 생성되었습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 6.2 Update Menu
```
PUT /api/admin/menus/{id}
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data
```

**Form Data**: (선택적 필드)
- `name`: "수정된 메뉴"
- `price`: 11000
- `image`: (file)

**Response** (200 OK)

#### 6.3 Delete Menu
```
DELETE /api/admin/menus/{id}
Authorization: Bearer {JWT_TOKEN}
```

**Response** (204 No Content)

#### 6.4 Get All Menus
```
GET /api/admin/menus?storeId=1
Authorization: Bearer {JWT_TOKEN}
```

**Response** (200 OK)

---

### 7. Admin Table APIs

#### 7.1 Get All Tables
```
GET /api/admin/tables?storeId=1
Authorization: Bearer {JWT_TOKEN}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "tableNumber": 1,
      "sessionId": "550e8400-e29b-41d4-a716-446655440000",
      "sessionStatus": "ACTIVE",
      "sessionStartTime": "2026-02-09T14:00:00"
    },
    {
      "id": 2,
      "tableNumber": 2,
      "sessionId": null,
      "sessionStatus": "INACTIVE",
      "sessionStartTime": null
    }
  ],
  "message": null,
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 7.2 Start Session
```
POST /api/admin/tables/{id}/start-session
Authorization: Bearer {JWT_TOKEN}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "tableNumber": 1,
    "sessionId": "550e8400-e29b-41d4-a716-446655440000",
    "sessionStatus": "ACTIVE",
    "sessionStartTime": "2026-02-09T15:00:00"
  },
  "message": "세션이 시작되었습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

#### 7.3 End Session
```
POST /api/admin/tables/{id}/end-session
Authorization: Bearer {JWT_TOKEN}
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "tableNumber": 1,
    "sessionId": null,
    "sessionStatus": "INACTIVE",
    "sessionStartTime": null
  },
  "message": "세션이 종료되었습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

---

### 8. Admin SSE APIs

#### 8.1 Connect to SSE
```
GET /api/admin/sse?storeId=1&userId=1
Authorization: Bearer {JWT_TOKEN}
```

**Response**: Server-Sent Events stream

**Event Types**:
- `NEW_ORDER`: 새 주문 알림
- `ORDER_STATUS_CHANGED`: 주문 상태 변경
- `ORDER_DELETED`: 주문 삭제
- `connected`: 연결 성공

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "data": null,
  "message": "입력 검증 실패",
  "error": {
    "storeId": "매장 ID는 필수입니다",
    "items": "주문 항목은 최소 1개 이상이어야 합니다"
  },
  "timestamp": "2026-02-09T15:00:00"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "data": null,
  "message": "인증이 필요합니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

### 404 Not Found
```json
{
  "success": false,
  "data": null,
  "message": "주문을 찾을 수 없습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

### 409 Conflict (Optimistic Lock)
```json
{
  "success": false,
  "data": null,
  "message": "주문이 다른 사용자에 의해 수정되었습니다. 다시 시도해주세요",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "data": null,
  "message": "시스템 오류가 발생했습니다",
  "error": null,
  "timestamp": "2026-02-09T15:00:00"
}
```

---

## Swagger UI

Interactive API documentation is available at:
```
http://localhost:8080/swagger-ui.html
```

---

## API Testing

### Using curl

**Login**:
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"storeId":1,"username":"admin1","password":"admin123"}'
```

**Create Order**:
```bash
curl -X POST http://localhost:8080/api/customer/orders \
  -H "Content-Type: application/json" \
  -d '{
    "storeId":1,
    "tableId":1,
    "sessionId":"550e8400-e29b-41d4-a716-446655440000",
    "items":[{"menuId":1,"quantity":2}]
  }'
```

**Get Menus**:
```bash
curl http://localhost:8080/api/customer/menus?storeId=1
```

---

## Notes

- 모든 timestamp는 ISO 8601 형식 (YYYY-MM-DDTHH:MM:SS)
- JWT 토큰 만료 시간: 16시간
- SSE 연결 타임아웃: 30초
- 파일 업로드 최대 크기: 5MB
- 허용 이미지 형식: JPG, PNG
