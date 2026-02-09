# Docker Compose 빠른 시작 가이드

## 📋 사전 요구사항

- **Docker Desktop** 설치 (Windows/Mac)
  - Windows: https://docs.docker.com/desktop/install/windows-install/
  - Mac: https://docs.docker.com/desktop/install/mac-install/
- 또는 **Docker Engine + Docker Compose** (Linux)
  - https://docs.docker.com/engine/install/

### 설치 확인

```bash
docker --version
docker-compose --version
```

---

## 🚀 3분 안에 실행하기

### 1단계: 환경 변수 설정

```bash
# 1. .env 파일 생성
copy .env.example .env

# 2. .env 파일 편집 (필수)
# JWT_SECRET_KEY 설정 (아무 문자열이나 입력)
```

**최소 설정 예시** (`.env` 파일):
```env
JWT_SECRET_KEY=my-super-secret-key-for-development-only
```

### 2단계: 볼륨 디렉토리 생성

```bash
# Windows (PowerShell)
New-Item -ItemType Directory -Force -Path data, logs, uploads\menu-images

# Windows (CMD)
mkdir data logs uploads\menu-images

# Mac/Linux
mkdir -p data logs uploads/menu-images
```

### 3단계: Docker Compose 실행

```bash
# 빌드 및 실행 (첫 실행 시)
docker-compose up --build

# 또는 백그라운드 실행
docker-compose up --build -d
```

**실행 확인**:
- Backend: http://localhost:8000/docs (Swagger UI)
- Frontend: http://localhost:5173 (로그인 화면)

### 4단계: 데이터베이스 초기화

```bash
# 새 터미널 열기 (또는 백그라운드 실행 시)
docker-compose exec backend python -m app.migrations.init_db
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

---

## 🎮 서비스 사용하기

### 1. 브라우저에서 접속
http://localhost:5173

### 2. 테이블 로그인 (고객)
- "고객 로그인" 탭 선택
- 테이블 번호: `1` 입력
- 로그인 클릭

### 3. 메뉴 조회 및 주문
- 메뉴 목록 확인
- 메뉴 클릭 → 옵션 선택 → 장바구니 추가
- 장바구니 → 주문하기

### 4. 주문 내역 확인
- 실시간 주문 상태 업데이트 (SSE)

---

## 🔧 Docker Compose 명령어

### 기본 명령어

```bash
# 서비스 시작 (포그라운드)
docker-compose up

# 서비스 시작 (백그라운드)
docker-compose up -d

# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart

# 특정 서비스만 재시작
docker-compose restart backend
docker-compose restart frontend
```

### 로그 확인

```bash
# 모든 서비스 로그 (실시간)
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f backend
docker-compose logs -f frontend

# 최근 100줄만 보기
docker-compose logs --tail=100 backend
```

### 컨테이너 접속

```bash
# Backend 컨테이너 접속
docker-compose exec backend bash

# Frontend 컨테이너 접속
docker-compose exec frontend sh

# 데이터베이스 확인
docker-compose exec backend python -c "from app.utils.database import SessionLocal; print(SessionLocal())"
```

### 빌드 및 재빌드

```bash
# 이미지 재빌드
docker-compose build

# 캐시 없이 재빌드
docker-compose build --no-cache

# 특정 서비스만 재빌드
docker-compose build backend
docker-compose build frontend

# 재빌드 후 실행
docker-compose up --build
```

### 정리 명령어

```bash
# 컨테이너 중지 및 삭제
docker-compose down

# 컨테이너 + 볼륨 삭제
docker-compose down -v

# 컨테이너 + 볼륨 + 이미지 삭제
docker-compose down -v --rmi all

# 사용하지 않는 Docker 리소스 정리
docker system prune -a
```

---

## 📊 서비스 상태 확인

### 컨테이너 상태

```bash
# 실행 중인 컨테이너 확인
docker-compose ps

# 상세 정보
docker-compose ps -a
```

**출력 예시**:
```
NAME                    STATUS              PORTS
tableorder-backend      Up 5 minutes        0.0.0.0:8000->8000/tcp
tableorder-frontend     Up 5 minutes        0.0.0.0:5173->5173/tcp
```

### Health Check

```bash
# Backend health check
curl http://localhost:8000/api/health

# 또는 브라우저에서
http://localhost:8000/api/health
```

**응답 예시**:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-09T10:00:00"
}
```

---

## 🔄 개발 워크플로우

### 코드 변경 시 (Hot Reload)

**Backend**:
- `backend/app/` 디렉토리의 파일 수정
- 자동으로 서버 재시작 (uvicorn --reload)
- 로그 확인: `docker-compose logs -f backend`

**Frontend**:
- `frontend/src/` 디렉토리의 파일 수정
- 자동으로 브라우저 새로고침 (Vite HMR)
- 로그 확인: `docker-compose logs -f frontend`

### 의존성 추가 시

**Backend** (`requirements.txt` 수정):
```bash
# 1. requirements.txt 수정
# 2. 이미지 재빌드
docker-compose build backend
# 3. 서비스 재시작
docker-compose up -d backend
```

**Frontend** (`package.json` 수정):
```bash
# 1. package.json 수정
# 2. 이미지 재빌드
docker-compose build frontend
# 3. 서비스 재시작
docker-compose up -d frontend
```

### 데이터베이스 초기화

```bash
# 1. 서비스 중지
docker-compose down

# 2. 데이터베이스 파일 삭제
rm data/app.db

# 3. 서비스 재시작
docker-compose up -d

# 4. 데이터베이스 초기화
docker-compose exec backend python -m app.migrations.init_db
```

---

## 🐛 문제 해결

### 1. 포트가 이미 사용 중

**증상**:
```
Error: bind: address already in use
```

**해결**:
```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :5173

# Mac/Linux
lsof -i :8000
lsof -i :5173

# 프로세스 종료 또는 docker-compose.yml에서 포트 변경
```

### 2. 볼륨 마운트 권한 오류

**증상**:
```
Permission denied: '/app/data/app.db'
```

**해결**:
```bash
# Windows: Docker Desktop 설정에서 드라이브 공유 확인
# Mac/Linux: 권한 수정
chmod -R 755 data logs uploads
```

### 3. 컨테이너가 계속 재시작됨

**확인**:
```bash
# 로그 확인
docker-compose logs backend
docker-compose logs frontend

# Health check 상태 확인
docker-compose ps
```

**일반적인 원인**:
- Backend: 데이터베이스 연결 실패, 환경 변수 누락
- Frontend: 빌드 오류, 의존성 설치 실패

### 4. Frontend가 Backend에 연결 안 됨

**확인 사항**:
1. Backend가 정상 실행 중인지 확인
   ```bash
   curl http://localhost:8000/api/health
   ```

2. CORS 설정 확인 (backend `.env`)
   ```env
   CORS_ORIGINS=http://localhost:5173
   ```

3. Frontend 환경 변수 확인
   ```env
   VITE_API_URL=http://localhost:8000
   ```

4. 네트워크 연결 확인
   ```bash
   docker-compose exec frontend ping backend
   ```

### 5. 이미지 빌드 실패

**해결**:
```bash
# 캐시 없이 재빌드
docker-compose build --no-cache

# 또는 Docker 캐시 전체 삭제
docker system prune -a
docker-compose build
```

### 6. 데이터베이스 파일 잠김

**증상**:
```
database is locked
```

**해결**:
```bash
# 1. 모든 컨테이너 중지
docker-compose down

# 2. 데이터베이스 파일 삭제
rm data/app.db

# 3. 재시작 및 초기화
docker-compose up -d
docker-compose exec backend python -m app.migrations.init_db
```

---

## 📁 디렉토리 구조

```
aidlc-workshop/
├── docker-compose.yml          # Docker Compose 설정
├── .env                        # 환경 변수 (gitignored)
├── .env.example                # 환경 변수 템플릿
├── .dockerignore               # Docker 빌드 제외 파일
│
├── backend/
│   ├── Dockerfile              # Backend 이미지 정의
│   ├── .dockerignore
│   ├── requirements.txt
│   └── app/                    # 소스 코드 (볼륨 마운트)
│
├── frontend/
│   ├── Dockerfile              # Frontend 이미지 정의
│   ├── .dockerignore
│   ├── package.json
│   └── src/                    # 소스 코드 (볼륨 마운트)
│
├── data/                       # SQLite DB (볼륨 마운트, gitignored)
├── logs/                       # 로그 파일 (볼륨 마운트, gitignored)
└── uploads/                    # 업로드 파일 (볼륨 마운트, gitignored)
```

---

## 🔐 보안 고려사항

### 개발 환경

1. **JWT_SECRET_KEY 설정**
   - `.env` 파일에 강력한 키 설정
   - 절대 Git에 커밋하지 않기

2. **기본 계정 변경**
   - 관리자 비밀번호 변경 (admin1234 → 강력한 비밀번호)

3. **포트 노출 최소화**
   - 필요한 포트만 외부 노출
   - 프로덕션에서는 reverse proxy 사용

### 프로덕션 배포 시 (향후)

1. **HTTPS 사용** (nginx + Let's Encrypt)
2. **환경 변수 관리** (AWS Secrets Manager)
3. **데이터베이스 변경** (PostgreSQL, MySQL)
4. **파일 스토리지** (S3, GCS)
5. **모니터링 추가** (Prometheus, CloudWatch)

---

## 📊 성능 최적화

### 개발 환경

- **Hot Reload**: 코드 변경 시 자동 재시작
- **볼륨 마운트**: 빠른 개발 사이클
- **Layer Caching**: 의존성 변경 시에만 재설치

### 프로덕션 빌드 (향후)

```bash
# Frontend 프로덕션 빌드
docker-compose -f docker-compose.prod.yml build frontend

# Multi-stage build로 이미지 크기 최소화
# nginx로 정적 파일 서빙
```

---

## 🔄 백업 및 복구

### 백업

```bash
# 1. 서비스 중지
docker-compose down

# 2. 데이터 백업
tar -czf backup-$(date +%Y%m%d).tar.gz data/ uploads/

# 3. 서비스 재시작
docker-compose up -d
```

### 복구

```bash
# 1. 서비스 중지
docker-compose down

# 2. 백업 복원
tar -xzf backup-YYYYMMDD.tar.gz

# 3. 서비스 재시작
docker-compose up -d
```

---

## 📝 체크리스트

### 초기 설정

- [ ] Docker Desktop 설치 및 실행
- [ ] `.env` 파일 생성 및 `JWT_SECRET_KEY` 설정
- [ ] 볼륨 디렉토리 생성 (`data`, `logs`, `uploads`)
- [ ] `docker-compose up --build` 실행
- [ ] 데이터베이스 초기화 (`init_db.py`)
- [ ] Backend health check 확인 (http://localhost:8000/api/health)
- [ ] Frontend 접속 확인 (http://localhost:5173)

### 일상 사용

- [ ] `docker-compose up -d` (서비스 시작)
- [ ] 코드 수정 (자동 Hot Reload)
- [ ] `docker-compose logs -f` (로그 확인)
- [ ] `docker-compose down` (서비스 중지)

### 문제 발생 시

- [ ] `docker-compose logs` (로그 확인)
- [ ] `docker-compose ps` (컨테이너 상태 확인)
- [ ] `docker-compose restart` (서비스 재시작)
- [ ] `docker-compose down -v` (완전 초기화)
- [ ] `docker-compose up --build` (재빌드 및 실행)

---

## 🎯 다음 단계

1. **서비스 실행 및 테스트**
   - 테이블 로그인
   - 메뉴 조회 및 주문
   - 주문 내역 확인

2. **Unit 3 개발**
   - Admin Operations Domain
   - 주문 관리, 메뉴 관리

3. **프로덕션 배포 준비**
   - docker-compose.prod.yml 작성
   - nginx reverse proxy 설정
   - HTTPS 설정

---

## 📞 추가 도움말

### 공식 문서

- Docker: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- FastAPI: https://fastapi.tiangolo.com/
- Vite: https://vitejs.dev/

### 커뮤니티

- Docker Community: https://forums.docker.com/
- Stack Overflow: https://stackoverflow.com/

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: Unit 1, Unit 2 완료
