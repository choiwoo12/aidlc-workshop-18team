# Deployment Architecture - Unit 1: Shared Foundation

## Overview

Unit 1의 배포 아키텍처입니다. Docker Compose를 사용한 로컬 개발 환경에 최적화되어 있습니다.

---

## Deployment Strategy

### Deployment Type
- **Environment**: Local development only
- **Orchestration**: Docker Compose
- **Services**: 2 services (backend, frontend)
- **Network**: Single bridge network

### Deployment Goals
- 간단한 설정 및 실행
- 개발 편의성 (hot reload)
- 데이터 영속성 (volume mounts)
- 서비스 간 통신 용이

---

## Docker Compose Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: tableorder-backend
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./uploads:/app/uploads
      - ./backend/app:/app/app  # Hot reload
    environment:
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - DB_FILE_PATH=/app/data/app.db
      - UPLOAD_DIR=/app/uploads/menu-images
      - LOG_FILE_PATH=/app/logs/app-{date}.log
      - LOG_LEVEL=INFO
      - PYTHONUNBUFFERED=1
    networks:
      - tableorder-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: tableorder-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src  # Hot reload
      - ./frontend/public:/app/public
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_SSE_URL=http://localhost:8000
    networks:
      - tableorder-network
    depends_on:
      backend:
        condition: service_healthy
    restart: unless-stopped

networks:
  tableorder-network:
    driver: bridge

volumes:
  data:
  logs:
  uploads:
```

---

## Backend Dockerfile

### Dockerfile (Multi-stage build)

```dockerfile
# Stage 1: Base
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Dependencies
FROM base as dependencies

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Application
FROM dependencies as application

# Copy application code
COPY ./app /app/app

# Create directories for volumes
RUN mkdir -p /app/data /app/logs /app/uploads/menu-images

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### requirements.txt

```txt
fastapi==0.104.0
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
sse-starlette==1.8.2
```

---

## Frontend Dockerfile

### Dockerfile

```dockerfile
# Stage 1: Base
FROM node:18-alpine as base

WORKDIR /app

# Stage 2: Dependencies
FROM base as dependencies

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Stage 3: Development
FROM dependencies as development

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

### package.json (relevant scripts)

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

---

## Environment Configuration

### .env File (Development)

```bash
# JWT Secret (REQUIRED - Generate a secure random string)
JWT_SECRET_KEY=your-secret-key-here-change-this-in-production

# Database Configuration
DB_FILE_PATH=/app/data/app.db
DB_POOL_MIN_SIZE=10
DB_POOL_MAX_SIZE=20
DB_CONNECTION_TIMEOUT=30
DB_IDLE_TIMEOUT=300

# File Storage Configuration
UPLOAD_DIR=/app/uploads/menu-images
MAX_FILE_SIZE=5242880  # 5MB in bytes
ALLOWED_MIME_TYPES=image/*

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=/app/logs/app-{date}.log
LOG_RETENTION_DAYS=30

# Cache Configuration
CACHE_TTL=300  # 5 minutes in seconds

# SSE Configuration
SSE_HEARTBEAT_INTERVAL=30  # seconds

# CORS Configuration (Development)
CORS_ORIGINS=http://localhost:3000

# Frontend API URL
VITE_API_URL=http://localhost:8000
VITE_SSE_URL=http://localhost:8000
```

### .env.example (Template)

```bash
# Copy this file to .env and fill in the values

# JWT Secret (REQUIRED)
JWT_SECRET_KEY=

# Database Configuration (Optional - defaults provided)
# DB_FILE_PATH=/app/data/app.db
# DB_POOL_MIN_SIZE=10
# DB_POOL_MAX_SIZE=20

# File Storage Configuration (Optional - defaults provided)
# UPLOAD_DIR=/app/uploads/menu-images
# MAX_FILE_SIZE=5242880

# Logging Configuration (Optional - defaults provided)
# LOG_LEVEL=INFO
# LOG_FILE_PATH=/app/logs/app-{date}.log

# Frontend API URL (Optional - defaults provided)
# VITE_API_URL=http://localhost:8000
```

---

## Directory Structure

### Project Root Structure

```
tableorder-service/
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
├── README.md
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── services/
│   │   ├── api/
│   │   └── utils/
│   └── tests/
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   ├── contexts/
│   │   └── utils/
│   └── public/
│
├── data/              (Volume mount - gitignored)
│   └── app.db
│
├── logs/              (Volume mount - gitignored)
│   └── app-2026-02-09.log
│
├── uploads/           (Volume mount - gitignored)
│   └── menu-images/
│
└── aidlc-docs/        (Documentation)
```

### .gitignore

```gitignore
# Environment variables
.env

# Data directories (volume mounts)
data/
logs/
uploads/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Node
node_modules/
dist/
.vite/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Deployment Commands

### Initial Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd tableorder-service

# 2. Create .env file
cp .env.example .env
# Edit .env and set JWT_SECRET_KEY

# 3. Create volume directories
mkdir -p data logs uploads/menu-images

# 4. Build and start services
docker-compose up --build
```

### Daily Operations

```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Rebuild and restart
docker-compose up --build
```

### Maintenance

```bash
# Remove all containers and volumes
docker-compose down -v

# Remove all containers, volumes, and images
docker-compose down -v --rmi all

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh
```

---

## Service Communication

### Frontend → Backend Communication

**HTTP Requests**:
```javascript
// Frontend (React)
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Example: Get menus
const response = await axios.get(`${API_URL}/api/menus`);
```

**SSE Connection**:
```javascript
// Frontend (React)
const SSE_URL = import.meta.env.VITE_SSE_URL || 'http://localhost:8000';

// Example: Subscribe to order updates
const eventSource = new EventSource(`${SSE_URL}/api/sse/orders`);
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Order update:', data);
};
```

### Backend CORS Configuration

```python
# Backend (FastAPI)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Health Checks

### Backend Health Check Endpoint

```python
# Backend (FastAPI)
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "cache": "active"
        }
    }
```

### Docker Health Check

```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

---

## Troubleshooting

### Common Issues

**Issue 1: Port already in use**
```bash
# Check what's using the port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Kill the process or change port in docker-compose.yml
```

**Issue 2: Database file locked**
```bash
# Stop all containers
docker-compose down

# Remove database file
rm data/app.db

# Restart services
docker-compose up
```

**Issue 3: Volume mount permission denied**
```bash
# Fix permissions
chmod -R 755 data logs uploads

# Or run containers as current user
docker-compose run --user $(id -u):$(id -g) backend
```

**Issue 4: Frontend can't connect to backend**
```bash
# Check CORS configuration in backend
# Check VITE_API_URL in frontend .env
# Check network connectivity
docker-compose exec frontend ping backend
```

---

## Performance Optimization

### Docker Build Optimization

**Use .dockerignore**:
```
# .dockerignore (backend)
__pycache__
*.pyc
.git
.env
tests/
*.md

# .dockerignore (frontend)
node_modules
.git
.env
*.md
```

**Multi-stage builds**: Already implemented in Dockerfiles

**Layer caching**: Dependencies installed before copying source code

### Runtime Optimization

**Backend**:
- Use `--workers` flag for production (not needed for development)
- Enable SQLAlchemy connection pooling (already configured)

**Frontend**:
- Use production build for deployment: `npm run build`
- Serve static files with nginx (future enhancement)

---

## Security Best Practices

### Development Environment

1. **Never commit .env file** (already in .gitignore)
2. **Use strong JWT secret** (generate with `openssl rand -hex 32`)
3. **Keep dependencies updated** (regular `pip install -U` and `npm update`)
4. **Use official base images** (already using python:3.11-slim and node:18-alpine)

### Production Considerations (Future)

1. **Use HTTPS** (nginx with Let's Encrypt)
2. **Use secrets manager** (AWS Secrets Manager, HashiCorp Vault)
3. **Enable security headers** (Helmet.js, FastAPI middleware)
4. **Implement rate limiting** (slowapi, nginx)
5. **Use production database** (PostgreSQL, MySQL)
6. **Use cloud storage** (S3, GCS)
7. **Enable monitoring** (Prometheus, CloudWatch)

---

## Deployment Checklist

### Pre-deployment

- [ ] Create .env file from .env.example
- [ ] Set JWT_SECRET_KEY in .env
- [ ] Create volume directories (data, logs, uploads)
- [ ] Review docker-compose.yml configuration
- [ ] Review Dockerfile configurations

### Deployment

- [ ] Build Docker images: `docker-compose build`
- [ ] Start services: `docker-compose up -d`
- [ ] Check service health: `docker-compose ps`
- [ ] Check logs: `docker-compose logs`
- [ ] Test backend health: `curl http://localhost:8000/health`
- [ ] Test frontend: Open `http://localhost:3000` in browser

### Post-deployment

- [ ] Verify database file created: `ls -la data/`
- [ ] Verify logs created: `ls -la logs/`
- [ ] Test API endpoints
- [ ] Test SSE connection
- [ ] Test file upload
- [ ] Create initial admin account

---

## Backup and Recovery

### Backup Procedure

```bash
# 1. Stop services
docker-compose down

# 2. Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/ uploads/

# 3. Move backup to safe location
mv backup-*.tar.gz /path/to/backup/location/

# 4. Restart services
docker-compose up -d
```

### Recovery Procedure

```bash
# 1. Stop services
docker-compose down

# 2. Restore backup
tar -xzf backup-YYYYMMDD.tar.gz

# 3. Restart services
docker-compose up -d
```

### Automated Backup (Optional)

```bash
# Create backup script: backup.sh
#!/bin/bash
DATE=$(date +%Y%m%d)
docker-compose down
tar -czf backup-$DATE.tar.gz data/ uploads/
docker-compose up -d

# Add to crontab for daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

---

## Monitoring and Logging

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100 backend

# Since specific time
docker-compose logs --since 2026-02-09T10:00:00 backend
```

### Application Logs

```bash
# Backend logs (file-based)
tail -f logs/app-2026-02-09.log

# Frontend logs (stdout)
docker-compose logs -f frontend
```

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
