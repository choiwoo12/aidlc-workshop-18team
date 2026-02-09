# Backend Code Summary - Unit 1: Shared Foundation

## Overview

Unit 1 Backend 코드 생성 완료. Python FastAPI 기반 백엔드 애플리케이션.

---

## Generated Files

### Configuration & Setup
- `backend/app/config.py` - 애플리케이션 설정 (Pydantic Settings)
- `backend/app/main.py` - FastAPI 메인 애플리케이션
- `backend/requirements.txt` - Python 의존성
- `backend/Dockerfile` - Docker 이미지 빌드 설정
- `backend/.env.example` - 환경 변수 템플릿

### Database Layer
**Models** (SQLAlchemy ORM):
- `backend/app/models/store.py` - Store 엔티티
- `backend/app/models/table.py` - Table 엔티티
- `backend/app/models/menu.py` - Menu 엔티티
- `backend/app/models/order.py` - Order 엔티티
- `backend/app/models/order_item.py` - OrderItem 엔티티
- `backend/app/models/order_history.py` - OrderHistory 엔티티

**Database Utilities**:
- `backend/app/utils/database.py` - 데이터베이스 연결 관리자

### Repository Layer
- `backend/app/repositories/base_repository.py` - Base Repository (CRUD)
- `backend/app/repositories/store_repository.py` - Store 데이터 접근
- `backend/app/repositories/table_repository.py` - Table 데이터 접근
- `backend/app/repositories/menu_repository.py` - Menu 데이터 접근
- `backend/app/repositories/order_repository.py` - Order 데이터 접근
- `backend/app/repositories/order_item_repository.py` - OrderItem 데이터 접근
- `backend/app/repositories/order_history_repository.py` - OrderHistory 데이터 접근

### Service Layer
- `backend/app/services/admin_auth_service.py` - 관리자 인증 비즈니스 로직
- `backend/app/services/table_auth_service.py` - 테이블 인증 비즈니스 로직

### API Layer
- `backend/app/api/auth_controller.py` - 인증 API 엔드포인트
- `backend/app/api/health_controller.py` - Health Check 엔드포인트

### Middleware
- `backend/app/middleware/auth_middleware.py` - JWT 인증 미들웨어
- `backend/app/middleware/error_middleware.py` - 에러 처리 미들웨어

### Utilities
- `backend/app/utils/auth.py` - 비밀번호 해싱 (bcrypt)
- `backend/app/utils/jwt_manager.py` - JWT 토큰 관리
- `backend/app/utils/cache_manager.py` - 인메모리 캐시 관리
- `backend/app/utils/file_storage.py` - 파일 저장소 관리
- `backend/app/utils/logging_config.py` - 로깅 설정
- `backend/app/utils/exceptions.py` - 커스텀 예외 클래스

### Migration Scripts
- `backend/app/migrations/init_db.py` - 데이터베이스 초기화 및 시드 데이터

---

## Key Features Implemented

### 1. Authentication & Security
- ✅ bcrypt 비밀번호 해싱 (cost factor: 12)
- ✅ JWT 토큰 기반 인증 (HS256)
- ✅ Admin 로그인 (username + password)
- ✅ Table 자동 로그인 (table number)
- ✅ 인증 미들웨어 (Bearer token)

### 2. Database Infrastructure
- ✅ SQLite 파일 기반 데이터베이스
- ✅ SQLAlchemy ORM (6개 모델)
- ✅ Foreign Key 제약조건
- ✅ 자동 타임스탬프 (created_at, updated_at)
- ✅ Repository 패턴 (7개 Repository)

### 3. API Endpoints
- ✅ `POST /api/auth/admin/login` - 관리자 로그인
- ✅ `POST /api/auth/table/login` - 테이블 로그인
- ✅ `GET /health` - Health Check

### 4. Error Handling
- ✅ 중앙 집중식 에러 처리
- ✅ 일관된 에러 응답 형식
- ✅ 커스텀 예외 클래스
- ✅ 에러 로깅

### 5. Logging
- ✅ 파일 기반 로깅 (날짜별)
- ✅ 로그 레벨 설정 (DEBUG, INFO, WARNING, ERROR)
- ✅ 구조화된 로그 형식

### 6. Caching
- ✅ 인메모리 캐시 (Python dict)
- ✅ TTL 지원 (기본 5분)
- ✅ 패턴 기반 삭제

### 7. File Storage
- ✅ 로컬 파일 시스템 저장
- ✅ UUID 기반 파일명
- ✅ 파일 크기 검증 (최대 5MB)
- ✅ MIME 타입 검증 (image/*)

---

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI 0.104+
- **Database**: SQLite (파일 기반)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: PyJWT (HS256)
- **Password**: bcrypt (cost factor: 12)
- **Validation**: Pydantic 2.5+

---

## Running the Backend

### Development Mode
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Mode
```bash
docker-compose up backend
```

### Initialize Database
```bash
python -m app.migrations.init_db
```

---

## API Documentation

FastAPI 자동 생성 문서:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Environment Variables

Required:
- `JWT_SECRET_KEY` - JWT 시크릿 키 (필수)

Optional (기본값 제공):
- `DB_FILE_PATH` - 데이터베이스 파일 경로
- `LOG_LEVEL` - 로그 레벨
- `CORS_ORIGINS` - CORS 허용 Origin

---

## Next Steps (Unit 2 & 3)

Unit 1에서 구현한 기반 위에 다음 기능들이 추가될 예정:
- Unit 2: 고객 주문 도메인 (메뉴 조회, 장바구니, 주문 생성)
- Unit 3: 관리자 운영 도메인 (주문 관리, 테이블 관리, 메뉴 관리)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
