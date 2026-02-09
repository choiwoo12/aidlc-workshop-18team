# 테이블오더 서비스 (Table Order Service)

소규모 매장을 위한 테이블 주문 관리 시스템입니다.

## 프로젝트 개요

- **목적**: 고객이 테이블에서 직접 주문하고, 관리자가 실시간으로 주문을 관리할 수 있는 시스템
- **대상**: 소규모 매장 (10개 테이블 미만)
- **환경**: 로컬 개발 환경 (Docker Compose)

## 주요 기능

### 고객 기능
- 테이블 번호로 자동 로그인
- 메뉴 조회 (카테고리별)
- 장바구니 관리
- 주문 생성
- 주문 내역 조회

### 관리자 기능
- 관리자 로그인
- 실시간 주문 모니터링 (SSE)
- 주문 상태 관리
- 테이블 관리 (초기 설정, 세션 종료)
- 메뉴 관리 (CRUD)
- 과거 주문 내역 조회

## 기술 스택

### Backend
- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Database**: SQLite (파일 기반)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: JWT (PyJWT)
- **Password**: bcrypt
- **Real-time**: Server-Sent Events (SSE)

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite 5+
- **Styling**: Tailwind CSS 3.4+
- **HTTP Client**: Axios 1.6+
- **State Management**: React Context API
- **Storage**: LocalStorage (Admin), SessionStorage (Customer)

### Infrastructure
- **Containerization**: Docker Compose
- **Database Storage**: Volume mount (./data)
- **File Storage**: Volume mount (./uploads)
- **Logging**: Volume mount (./logs)

## 시작하기

### 사전 요구사항

- Docker Desktop 설치
- Git 설치

### 설치 및 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd aidlc-workshop-18team
```

2. **환경 변수 설정**
```bash
cp .env.example .env
# .env 파일을 열어서 JWT_SECRET_KEY 설정
```

3. **볼륨 디렉토리 생성**
```bash
mkdir -p data logs uploads/menu-images
```

4. **Docker Compose 실행**
```bash
docker-compose up --build
```

5. **서비스 접속**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 개발 모드

개발 모드에서는 Hot Reload가 활성화되어 있습니다.

**Backend 개발**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend 개발**:
```bash
cd frontend
npm install
npm run dev
```

## 프로젝트 구조

```
aidlc-workshop-18team/
├── backend/                 # Python 백엔드
│   ├── app/
│   │   ├── main.py         # FastAPI 애플리케이션
│   │   ├── config.py       # 설정
│   │   ├── models/         # SQLAlchemy 모델
│   │   ├── repositories/   # 데이터 접근 레이어
│   │   ├── services/       # 비즈니스 로직
│   │   ├── api/            # API 컨트롤러
│   │   ├── middleware/     # 미들웨어
│   │   └── utils/          # 유틸리티
│   ├── tests/              # 테스트
│   ├── requirements.txt    # Python 의존성
│   └── Dockerfile
│
├── frontend/               # React 프론트엔드
│   ├── src/
│   │   ├── main.jsx       # 엔트리 포인트
│   │   ├── App.jsx        # 앱 컴포넌트
│   │   ├── components/    # 공통 컴포넌트
│   │   ├── pages/         # 페이지 컴포넌트
│   │   ├── contexts/      # React Context
│   │   ├── services/      # API 서비스
│   │   └── utils/         # 유틸리티
│   ├── public/            # 정적 파일
│   ├── package.json       # Node 의존성
│   └── Dockerfile
│
├── data/                  # 데이터베이스 파일 (gitignored)
├── logs/                  # 로그 파일 (gitignored)
├── uploads/               # 업로드 파일 (gitignored)
├── aidlc-docs/           # 설계 문서
├── docker-compose.yml    # Docker Compose 설정
├── .gitignore
└── README.md
```

## API 문서

FastAPI는 자동으로 API 문서를 생성합니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 테스트

### Backend 테스트
```bash
cd backend
pytest
```

### Frontend 테스트
```bash
cd frontend
npm test
```

## 배포

현재 이 프로젝트는 로컬 개발 환경만 지원합니다. 프로덕션 배포는 지원하지 않습니다.

## 백업 및 복구

### 백업
```bash
docker-compose down
tar -czf backup-$(date +%Y%m%d).tar.gz data/ uploads/
```

### 복구
```bash
docker-compose down
tar -xzf backup-YYYYMMDD.tar.gz
docker-compose up -d
```

## 문제 해결

### 포트가 이미 사용 중인 경우
```bash
# 포트 사용 확인
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# 프로세스 종료 또는 docker-compose.yml에서 포트 변경
```

### 데이터베이스 파일 잠금
```bash
docker-compose down
rm data/app.db
docker-compose up
```

### 볼륨 마운트 권한 오류
```bash
chmod -R 755 data logs uploads
```

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 문의

프로젝트 관련 문의사항은 이슈를 등록해주세요.
