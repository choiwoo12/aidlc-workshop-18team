# Test Instructions - 테이블오더 서비스

## Overview
Backend와 Customer Frontend의 테스트 실행 지침.

---

## Backend Tests

### Test Types
1. **Unit Tests**: 개별 클래스/메서드 테스트
2. **Integration Tests**: 컴포넌트 간 통합 테스트
3. **API Tests**: REST API 엔드포인트 테스트

### Test Commands

#### 모든 테스트 실행
```bash
cd backend
mvn test
```

#### 특정 테스트 클래스 실행
```bash
mvn test -Dtest=OrderServiceTest
```

#### 특정 테스트 메서드 실행
```bash
mvn test -Dtest=OrderServiceTest#testCreateOrder
```

#### 테스트 커버리지
```bash
mvn test jacoco:report
```

커버리지 리포트: `backend/target/site/jacoco/index.html`

---

## Customer Frontend Tests

### Test Types
1. **Unit Tests**: 함수/유틸리티 테스트
2. **Component Tests**: React 컴포넌트 테스트
3. **Integration Tests**: Store + API 통합 테스트

### Test Commands

#### 모든 테스트 실행
```bash
cd frontend/customer
npm test
```

#### Watch 모드
```bash
npm test -- --watch
```

#### 특정 테스트 파일 실행
```bash
npm test -- storage.test.ts
```

#### 테스트 커버리지
```bash
npm test -- --coverage
```

커버리지 리포트: `frontend/customer/coverage/index.html`

---

## Integration Tests (E2E)

### 전체 시스템 통합 테스트

#### 1. Backend 서버 시작
```bash
cd backend
java -jar target/table-order-backend-1.0.0.jar &
BACKEND_PID=$!
```

#### 2. Frontend 개발 서버 시작
```bash
cd frontend/customer
npm run dev &
FRONTEND_PID=$!
```

#### 3. API 테스트
```bash
# 메뉴 조회
curl http://localhost:8080/api/customer/menus?storeId=1

# 주문 생성
curl -X POST http://localhost:8080/api/customer/orders \
  -H "Content-Type: application/json" \
  -d '{
    "storeId": 1,
    "tableId": 1,
    "sessionId": "test-session-001",
    "items": [
      {"menuId": 1, "quantity": 2}
    ]
  }'
```

#### 4. 서버 종료
```bash
kill $BACKEND_PID
kill $FRONTEND_PID
```

---

## Test Coverage Goals

### Backend
- **Unit Tests**: 80% 이상
- **Integration Tests**: 70% 이상
- **Overall**: 75% 이상

### Frontend
- **Unit Tests**: 80% 이상
- **Component Tests**: 70% 이상
- **Overall**: 75% 이상

---

## Test Data

### Backend Test Data
`backend/src/main/resources/data.sql`에 정의:
- Stores: 2개
- Tables: 5개
- Menus: 8개
- Users: 2개 (admin)

### Frontend Test Data
Mock 데이터 사용:
```typescript
const mockMenu = {
  id: 1,
  storeId: 1,
  name: '김치찌개',
  price: 8000,
  imageUrl: null,
  createdAt: '2024-01-01T00:00:00Z',
};
```

---

## Automated Testing

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash

echo "Running tests..."

# Backend tests
cd backend
mvn test -q
if [ $? -ne 0 ]; then
  echo "❌ Backend tests failed"
  exit 1
fi

# Frontend tests
cd ../frontend/customer
npm test -- --run
if [ $? -ne 0 ]; then
  echo "❌ Frontend tests failed"
  exit 1
fi

echo "✅ All tests passed"
```

### CI/CD Testing
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
      - name: Run Backend Tests
        run: |
          cd backend
          mvn test

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Run Frontend Tests
        run: |
          cd frontend/customer
          npm ci
          npm test -- --run
```

---

## Test Reports

### Backend
- **JUnit XML**: `backend/target/surefire-reports/`
- **Jacoco HTML**: `backend/target/site/jacoco/index.html`

### Frontend
- **Vitest JSON**: `frontend/customer/coverage/coverage-final.json`
- **HTML Report**: `frontend/customer/coverage/index.html`

---

## Troubleshooting

### Backend Test Issues

#### H2 Database 문제
```bash
# 테스트 DB 초기화
mvn clean test
```

#### 포트 충돌
```bash
# 랜덤 포트 사용
mvn test -Dserver.port=0
```

### Frontend Test Issues

#### jsdom 문제
```bash
# jsdom 재설치
npm install -D jsdom
```

#### 비동기 테스트 타임아웃
```typescript
// 타임아웃 증가
it('async test', async () => {
  // ...
}, 10000); // 10초
```

---

## Performance Testing

### Backend Load Test (Apache Bench)
```bash
# 메뉴 조회 부하 테스트
ab -n 1000 -c 10 http://localhost:8080/api/customer/menus?storeId=1

# 주문 생성 부하 테스트
ab -n 100 -c 5 -p order.json -T application/json \
  http://localhost:8080/api/customer/orders
```

### Frontend Performance Test
```bash
# Lighthouse CI
npm install -g @lhci/cli
lhci autorun --collect.url=http://localhost:5173
```

---

## Test Best Practices

### Backend
1. 각 테스트는 독립적이어야 함
2. @Transactional로 테스트 격리
3. Mock 사용 최소화 (실제 DB 사용)
4. 테스트 이름은 명확하게

### Frontend
1. 사용자 관점에서 테스트
2. Implementation details 테스트 지양
3. Mock은 필요한 경우만 사용
4. 비동기 처리 주의

---

## Notes

- 모든 PR은 테스트 통과 필수
- 테스트 커버리지 75% 이상 유지
- 실패하는 테스트는 즉시 수정
- 테스트 실행 시간 모니터링
