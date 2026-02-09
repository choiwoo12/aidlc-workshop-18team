# Build Instructions - 테이블오더 서비스

## Overview
Backend와 Customer Frontend의 빌드 지침.

---

## Backend Build

### Prerequisites
- Java 17 이상
- Maven 3.6 이상

### Build Commands

#### 1. Clean Build
```bash
cd backend
mvn clean compile
```

#### 2. Package (JAR 생성)
```bash
mvn clean package -DskipTests
```

#### 3. Package with Tests
```bash
mvn clean package
```

### Build Output
```
backend/target/
└── table-order-backend-1.0.0.jar
```

### Build Verification
```bash
# JAR 파일 확인
ls -lh backend/target/*.jar

# JAR 실행 테스트
java -jar backend/target/table-order-backend-1.0.0.jar --spring.profiles.active=test
```

---

## Customer Frontend Build

### Prerequisites
- Node.js 18 이상
- npm 9 이상

### Build Commands

#### 1. Install Dependencies
```bash
cd frontend/customer
npm install
```

#### 2. Type Check
```bash
npm run type-check
```

#### 3. Lint
```bash
npm run lint
```

#### 4. Build
```bash
npm run build
```

### Build Output
```
frontend/customer/dist/
├── index.html
├── assets/
│   ├── js/
│   │   ├── main-[hash].js
│   │   ├── react-vendor-[hash].js
│   │   └── zustand-vendor-[hash].js
│   └── css/
│       └── main-[hash].css
```

### Build Verification
```bash
# 빌드 파일 확인
ls -lh frontend/customer/dist/

# 번들 크기 확인
du -sh frontend/customer/dist/

# Preview 서버 실행
npm run preview
```

---

## Full System Build

### Build Script
```bash
#!/bin/bash

echo "🏗️  Building Table Order System..."

# Backend
echo "📦 Building Backend..."
cd backend
mvn clean package -DskipTests
if [ $? -ne 0 ]; then
  echo "❌ Backend build failed"
  exit 1
fi
echo "✅ Backend build complete"

# Customer Frontend
echo "📦 Building Customer Frontend..."
cd ../frontend/customer
npm install
npm run build
if [ $? -ne 0 ]; then
  echo "❌ Frontend build failed"
  exit 1
fi
echo "✅ Frontend build complete"

echo "🎉 All builds complete!"
```

### Save as `scripts/build-all.sh`
```bash
chmod +x scripts/build-all.sh
./scripts/build-all.sh
```

---

## Build Optimization

### Backend
- Maven 병렬 빌드: `mvn -T 4 clean package`
- 오프라인 모드: `mvn -o package`
- 의존성 캐시 활용

### Frontend
- npm ci 사용 (CI 환경)
- 캐시 활용: `npm ci --cache .npm`
- 병렬 빌드: `npm-run-all --parallel`

---

## Troubleshooting

### Backend Build Issues

#### Maven 의존성 문제
```bash
# 의존성 재다운로드
mvn dependency:purge-local-repository
mvn clean install
```

#### Java 버전 문제
```bash
# Java 버전 확인
java -version
mvn -version

# JAVA_HOME 설정
export JAVA_HOME=/path/to/java17
```

### Frontend Build Issues

#### Node 버전 문제
```bash
# Node 버전 확인
node -v
npm -v

# nvm 사용 (권장)
nvm use 18
```

#### 의존성 문제
```bash
# node_modules 삭제 후 재설치
rm -rf node_modules package-lock.json
npm install
```

#### 메모리 부족
```bash
# Node 메모리 증가
export NODE_OPTIONS="--max-old-space-size=4096"
npm run build
```

---

## CI/CD Build

### GitHub Actions Example
```yaml
name: Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
      - name: Build with Maven
        run: |
          cd backend
          mvn clean package -DskipTests

  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Build Frontend
        run: |
          cd frontend/customer
          npm ci
          npm run build
```

---

## Build Artifacts

### Backend
- **JAR**: `backend/target/table-order-backend-1.0.0.jar`
- **Size**: ~50MB
- **Type**: Executable JAR (Spring Boot)

### Frontend
- **Directory**: `frontend/customer/dist/`
- **Size**: ~500KB (gzipped)
- **Type**: Static files

---

## Notes

- Backend 빌드는 약 30초 소요
- Frontend 빌드는 약 20초 소요
- CI/CD 환경에서는 캐시 활용 권장
- 프로덕션 빌드 전 테스트 필수
