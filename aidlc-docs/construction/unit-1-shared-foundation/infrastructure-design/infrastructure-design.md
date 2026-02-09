# Infrastructure Design - Unit 1: Shared Foundation

## Overview

Unit 1의 논리적 컴포넌트를 실제 인프라 서비스와 매핑한 설계입니다. 로컬 개발 환경에 최적화되어 있습니다.

---

## Infrastructure Mapping

### 1. Database Infrastructure

**Logical Component**: Database Connection Manager

**Infrastructure Service**: SQLite (File-based)

**Mapping Details**:
- **Service Type**: File-based relational database
- **Location**: Host directory mounted to container
- **File Path**: `./data/app.db` (host) → `/app/data/app.db` (container)
- **Connection Pool**: SQLAlchemy connection pool (min: 10, max: 20)
- **Backup Strategy**: Host directory backup (manual)

**Configuration**:
```yaml
Database:
  Type: SQLite
  Mode: File-based
  Path: /app/data/app.db
  Connection Pool:
    Min Size: 10
    Max Size: 20
    Timeout: 30s
    Idle Timeout: 300s
```

**Benefits**:
- 데이터 영속성 보장 (호스트 디렉토리 마운트)
- 간단한 설정 및 관리
- 백업 및 복구 용이

**Limitations**:
- 단일 서버만 지원 (수평 확장 불가)
- 동시 쓰기 성능 제한
- 프로덕션 환경에는 부적합

---

### 2. File Storage Infrastructure

**Logical Component**: File Storage Manager

**Infrastructure Service**: Local File System

**Mapping Details**:
- **Service Type**: Local file system
- **Location**: Host directory mounted to container
- **Upload Path**: `./uploads/menu-images` (host) → `/app/uploads/menu-images` (container)
- **File Naming**: UUID-based unique names
- **Max File Size**: 5MB

**Configuration**:
```yaml
File Storage:
  Type: Local File System
  Upload Directory: /app/uploads/menu-images
  Max File Size: 5MB
  Allowed MIME Types: image/*
```

**Benefits**:
- 간단한 구현
- 파일 백업 및 관리 용이
- 추가 서비스 불필요

**Limitations**:
- 단일 서버만 지원
- CDN 없음 (성능 제한)
- 프로덕션 환경에는 클라우드 스토리지 권장 (S3, GCS)

---

### 3. Logging Infrastructure

**Logical Component**: Logging Manager

**Infrastructure Service**: Local File System

**Mapping Details**:
- **Service Type**: File-based logging
- **Location**: Host directory mounted to container
- **Log Path**: `./logs` (host) → `/app/logs` (container)
- **Log Format**: `[timestamp] [level] [component] [message]`
- **Rotation**: Daily, 30-day retention

**Configuration**:
```yaml
Logging:
  Type: File-based
  Log Directory: /app/logs
  Log Level: INFO
  Log Format: "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
  Rotation:
    Type: Daily
    Retention Days: 30
```

**Benefits**:
- 로그 분석 및 보관 용이
- 호스트에서 직접 접근 가능
- 간단한 설정

**Limitations**:
- 중앙 집중식 로그 관리 없음
- 로그 검색 기능 제한
- 프로덕션 환경에는 로그 수집 서비스 권장 (ELK, CloudWatch)

---

### 4. Cache Infrastructure

**Logical Component**: Cache Manager

**Infrastructure Service**: In-memory (Application-level)

**Mapping Details**:
- **Service Type**: In-memory cache (Python dict)
- **Location**: Application memory
- **TTL**: 5 minutes (300 seconds)
- **Eviction Policy**: TTL-based

**Configuration**:
```yaml
Cache:
  Type: In-memory
  TTL: 300s
  Max Size: Unlimited (memory-bound)
```

**Benefits**:
- 간단한 구현
- 추가 서비스 불필요
- 빠른 응답 시간

**Limitations**:
- 서버 재시작 시 캐시 손실
- 다중 서버 환경에서 캐시 동기화 불가
- 프로덕션 환경에는 Redis 권장

---

### 5. Authentication Infrastructure

**Logical Component**: Authentication Manager

**Infrastructure Service**: Application-level (No external service)

**Mapping Details**:
- **Service Type**: Application-level authentication
- **JWT Secret**: Environment variable
- **Password Hashing**: bcrypt (application library)
- **Token Storage**: Client-side (LocalStorage/SessionStorage)

**Configuration**:
```yaml
Authentication:
  Type: Application-level
  JWT:
    Algorithm: HS256
    Secret: ${JWT_SECRET_KEY}
    Admin Expiry: 28800s  # 8 hours
    Table Expiry: 86400s  # 24 hours
  Password:
    Algorithm: bcrypt
    Cost Factor: 12
```

**Benefits**:
- 간단한 구현
- 추가 서비스 불필요
- Stateless 인증

**Limitations**:
- 토큰 무효화 어려움 (블랙리스트 없음)
- 프로덕션 환경에는 인증 서비스 권장 (Auth0, Cognito)

---

### 6. Real-time Communication Infrastructure

**Logical Component**: SSE Manager

**Infrastructure Service**: Application-level (FastAPI SSE)

**Mapping Details**:
- **Service Type**: Server-Sent Events (HTTP-based)
- **Connection Management**: In-memory (Python dict)
- **Event Types**: order_created, order_updated, order_deleted
- **Heartbeat**: 30 seconds

**Configuration**:
```yaml
SSE:
  Type: Server-Sent Events
  Heartbeat Interval: 30s
  Connection Timeout: 300s
```

**Benefits**:
- 간단한 구현
- HTTP 기반 (방화벽 친화적)
- 추가 서비스 불필요

**Limitations**:
- 단방향 통신만 가능
- 다중 서버 환경에서 이벤트 동기화 불가
- 프로덕션 환경에는 메시징 서비스 권장 (Redis Pub/Sub, RabbitMQ)

---

## Infrastructure Summary

| Logical Component | Infrastructure Service | Location | Persistence |
|-------------------|------------------------|----------|-------------|
| Database Connection Manager | SQLite (File-based) | Host volume mount | Persistent |
| File Storage Manager | Local File System | Host volume mount | Persistent |
| Logging Manager | Local File System | Host volume mount | Persistent |
| Cache Manager | In-memory (Python dict) | Application memory | Volatile |
| Authentication Manager | Application-level | Application code | Stateless |
| SSE Manager | Application-level (FastAPI) | Application memory | Volatile |

---

## Environment Variables

### Required Environment Variables
```bash
# JWT Secret (REQUIRED)
JWT_SECRET_KEY=your-secret-key-here

# Database (Optional, defaults provided)
DB_FILE_PATH=data/app.db
DB_POOL_MIN_SIZE=10
DB_POOL_MAX_SIZE=20

# File Storage (Optional, defaults provided)
UPLOAD_DIR=uploads/menu-images
MAX_FILE_SIZE=5242880  # 5MB in bytes

# Logging (Optional, defaults provided)
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/app-{date}.log
LOG_RETENTION_DAYS=30

# Cache (Optional, defaults provided)
CACHE_TTL=300  # 5 minutes in seconds

# SSE (Optional, defaults provided)
SSE_HEARTBEAT_INTERVAL=30  # seconds
```

### Environment Variable Management
- **Development**: `.env` file (not committed to git)
- **Production**: Environment variables or secrets manager

---

## Volume Mounts

### Backend Service Volumes
```yaml
volumes:
  - ./data:/app/data              # Database files
  - ./logs:/app/logs              # Log files
  - ./uploads:/app/uploads        # Uploaded files
```

### Frontend Service Volumes
```yaml
volumes:
  - ./frontend/src:/app/src       # Source code (hot reload)
  - ./frontend/public:/app/public # Static files
```

---

## Network Configuration

### Docker Network
- **Type**: Bridge network (default)
- **Name**: `tableorder-network`
- **Services**: backend, frontend

### Service Communication
- **Frontend → Backend**: HTTP requests to `http://backend:8000`
- **Backend → Frontend**: Not applicable (client-initiated only)

### Port Mapping
- **Backend**: `8000:8000` (host:container)
- **Frontend**: `3000:3000` (host:container)

---

## Security Considerations

### Network Security
- **CORS**: Configured to allow frontend origin
- **HTTPS**: Not required (local development only)
- **Firewall**: Not required (local development only)

### Data Security
- **Database**: File permissions (host OS)
- **Uploaded Files**: File permissions (host OS)
- **Logs**: File permissions (host OS)
- **JWT Secret**: Environment variable (not in code)

### Container Security
- **User**: Run as non-root user (recommended)
- **Image**: Use official base images
- **Vulnerabilities**: Regular image updates

---

## Scalability Considerations

### Current Limitations
- **Single Server**: No horizontal scaling
- **In-memory Cache**: No cache sharing between instances
- **SQLite**: Limited concurrent writes
- **Local File Storage**: No distributed storage

### Future Scalability Options
If scaling is needed in the future:
1. **Database**: Migrate to PostgreSQL or MySQL
2. **Cache**: Migrate to Redis
3. **File Storage**: Migrate to S3 or GCS
4. **Load Balancer**: Add nginx or cloud load balancer
5. **Messaging**: Add RabbitMQ or Redis Pub/Sub for SSE

---

## Monitoring and Observability

### Current Approach
- **Logs**: File-based logs in `./logs` directory
- **Metrics**: None (not required for MVP)
- **Tracing**: None (not required for MVP)
- **Health Checks**: Docker health checks

### Future Monitoring Options
If monitoring is needed in the future:
1. **Logging**: ELK Stack or CloudWatch Logs
2. **Metrics**: Prometheus + Grafana
3. **Tracing**: Jaeger or X-Ray
4. **APM**: New Relic or Datadog

---

## Backup and Recovery

### Backup Strategy
- **Database**: Manual backup of `./data` directory
- **Uploaded Files**: Manual backup of `./uploads` directory
- **Logs**: Manual backup of `./logs` directory (optional)

### Recovery Strategy
1. Stop Docker containers
2. Restore backed-up directories
3. Start Docker containers

### Backup Frequency
- **Recommended**: Daily backups
- **Retention**: 7 days (configurable)

---

## Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Host Machine                          │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Docker Compose Network                     │ │
│  │                                                          │ │
│  │  ┌──────────────────┐      ┌──────────────────┐       │ │
│  │  │  Backend Service │      │ Frontend Service │       │ │
│  │  │   (FastAPI)      │      │    (React)       │       │ │
│  │  │   Port: 8000     │      │   Port: 3000     │       │ │
│  │  └──────────────────┘      └──────────────────┘       │ │
│  │           │                          │                  │ │
│  └───────────┼──────────────────────────┼─────────────────┘ │
│              │                          │                    │
│              ↓                          ↓                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Host File System                          │  │
│  │                                                         │  │
│  │  ./data/          (Database files)                     │  │
│  │  ./logs/          (Log files)                          │  │
│  │  ./uploads/       (Uploaded files)                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
