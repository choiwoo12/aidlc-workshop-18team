# 테이블오더 서비스 빠른 시작 가이드

## 📋 사전 요구사항

### Backend
- Python 3.9 이상
- pip (Python 패키지 관리자)

### Frontend
- Node.js 18 이상
- npm 또는 yarn

---

## 🚀 빠른 시작 (5분 안에 실행)

### 1단계: Backend 설정 및 실행

#### 1.1 Backend 디렉토리로 이동
```bash
cd backend
```

#### 1.2 Python 가상환경 생성 및 활성화 (권장)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 1.3 의존성 설치
```bash
pip install -r requirements.txt
```

#### 1.4 환경 변수 설정
```bash
# .env 파일 생성
copy .env.example .env

# .env 파일 편집 (JWT_SECRET_KEY 설정)
# JWT_SECRET_KEY=your-secret-key-here (아무 문자열이나 입력)
```

**간단한 설정 예시** (`.env` 파일):
```env
JWT_SECRET_KEY=my-super-secret-key-for-development
CORS_ORIGINS=http://localhost:5173
```

#### 1.5 데이터베이스 초기화
```bash
python -m app.migrations.init_db
```

**출력 예시**:
```
Initializing database...
Database initialized.

Creating initial data...
Initial data created successfully:
  Store: 테스트 매장
  Admin Username: admin
  Admin Password: admin1234
Done.
```

#### 1.6 Backend 서버 실행
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**서버 실행 확인**:
- 브라우저에서 http://localhost:8000/docs 접속
- Swagger UI가 표시되면 성공!

---

### 2단계: Frontend 설정 및 실행

#### 2.1 새 터미널 열기 (Backend는 계속 실행)

#### 2.2 Frontend 디렉토리로 이동
```bash
cd frontend
```

#### 2.3 의존성 설치
```bash
npm install
```

#### 2.4 환경 변수 설정 (선택사항)
Frontend는 기본적으로 `http://localhost:8000`을 Backend URL로 사용합니다.

변경이 필요한 경우 `.env` 파일 생성:
```env
VITE_API_URL=http://localhost:8000
```

#### 2.5 Frontend 개발 서버 실행
```bash
npm run dev
```

**서버 실행 확인**:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## 🎮 서비스 사용하기

### 1. 브라우저에서 접속
http://localhost:5173 접속

### 2. 테이블 로그인 (고객)
- "고객 로그인" 탭 선택
- 테이블 번호 입력: `1` (또는 1~10 사이 아무 숫자)
- 로그인 클릭

### 3. 메뉴 조회 및 주문
- 메뉴 목록 확인
- 메뉴 클릭 → 옵션 선택 → 수량 선택 → 장바구니 추가
- 장바구니 버튼 클릭
- 주문하기 클릭

### 4. 주문 내역 확인
- 주문 완료 후 자동으로 주문 내역 페이지 이동
- 실시간 주문 상태 업데이트 확인 (SSE 연결)

### 5. 관리자 로그인 (선택사항)
- "관리자 로그인" 탭 선택
- 아이디: `admin`
- 비밀번호: `admin1234`
- 로그인 클릭

**참고**: Unit 3 (Admin Operations Domain)가 아직 구현되지 않아 관리자 기능은 제한적입니다.

---

## 📊 현재 구현된 기능

### ✅ Unit 1: Shared Foundation
- 인증 (JWT)
- 데이터베이스 (SQLite)
- 공통 컴포넌트

### ✅ Unit 2: Customer Order Domain
- 메뉴 조회 (카테고리 필터링)
- 장바구니 관리 (SessionStorage)
- 주문 생성
- 주문 내역 조회
- 실시간 주문 상태 업데이트 (SSE)

### ⏳ Unit 3: Admin Operations Domain (미구현)
- 주문 관리 (상태 변경)
- 메뉴 관리 (CRUD)
- 테이블 관리

---

## 🧪 테스트 시나리오

### 시나리오 1: 기본 주문 플로우
1. 테이블 로그인 (테이블 번호: 1)
2. 메뉴 페이지에서 메뉴 선택
3. 옵션 선택 (있는 경우)
4. 수량 선택
5. 장바구니에 추가
6. 장바구니 페이지로 이동
7. 주문하기
8. 주문 내역 페이지에서 확인

### 시나리오 2: 장바구니 관리
1. 여러 메뉴 장바구니에 추가
2. 동일 메뉴 + 동일 옵션 추가 → 수량 증가 확인
3. 장바구니에서 수량 조절
4. 항목 제거
5. 페이지 새로고침 → 장바구니 유지 확인

### 시나리오 3: 실시간 업데이트 (SSE)
1. 테이블 로그인 후 주문 생성
2. 주문 내역 페이지에서 SSE 연결 상태 확인 (초록색 점)
3. 관리자가 주문 상태 변경 시 실시간 업데이트 확인
   - **참고**: Unit 3 미구현으로 수동 테스트 어려움

---

## 🔧 문제 해결

### Backend 실행 오류

#### 1. `ModuleNotFoundError: No module named 'app'`
```bash
# backend 디렉토리에서 실행하는지 확인
cd backend
python -m app.migrations.init_db
```

#### 2. `ImportError: cannot import name 'SessionLocal'`
```bash
# 의존성 재설치
pip install -r requirements.txt --force-reinstall
```

#### 3. 포트 8000이 이미 사용 중
```bash
# 다른 포트 사용
uvicorn app.main:app --reload --port 8001

# Frontend .env 파일도 수정 필요
VITE_API_URL=http://localhost:8001
```

### Frontend 실행 오류

#### 1. `npm install` 실패
```bash
# 캐시 삭제 후 재시도
npm cache clean --force
npm install
```

#### 2. 포트 5173이 이미 사용 중
```bash
# Vite가 자동으로 다른 포트 할당
# 또는 수동 지정
npm run dev -- --port 3000
```

#### 3. API 연결 오류 (CORS)
- Backend `.env` 파일의 `CORS_ORIGINS` 확인
- Frontend 실행 포트와 일치하는지 확인

---

## 📁 디렉토리 구조

```
aidlc-workshop/
├── backend/
│   ├── app/
│   │   ├── api/              # API Controllers
│   │   ├── models/           # Database Models
│   │   ├── repositories/     # Data Access Layer
│   │   ├── services/         # Business Logic
│   │   ├── middleware/       # Middleware
│   │   ├── utils/            # Utilities
│   │   ├── migrations/       # Database Migrations
│   │   └── main.py           # FastAPI App
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/       # React Components
│   │   ├── pages/            # Page Components
│   │   ├── services/         # API Services
│   │   ├── context/          # React Context
│   │   ├── utils/            # Utilities
│   │   └── App.jsx
│   ├── package.json
│   └── .env
├── data/                     # SQLite Database (자동 생성)
├── uploads/                  # File Uploads (자동 생성)
└── logs/                     # Application Logs (자동 생성)
```

---

## 🔐 기본 계정 정보

### 관리자 계정
- **아이디**: `admin`
- **비밀번호**: `admin1234`

### 테이블 로그인
- **테이블 번호**: 1~10 (아무 숫자나 입력 가능)

---

## 📝 추가 정보

### API 문서
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 데이터베이스
- 위치: `data/app.db` (SQLite)
- 초기화: `python -m app.migrations.init_db`

### 로그
- 위치: `logs/app-{date}.log`
- 레벨: INFO (`.env`에서 변경 가능)

---

## 🎯 다음 단계

1. **Unit 3 구현**: Admin Operations Domain
   - 주문 관리 (상태 변경)
   - 메뉴 관리 (CRUD)
   - 테이블 관리

2. **테스트 작성**: Unit Test, Integration Test

3. **배포 준비**: Docker, CI/CD

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: Unit 1, Unit 2 완료
