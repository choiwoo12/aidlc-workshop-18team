# Deployment Architecture - Backend

## Overview
Backend 유닛의 배포 아키텍처, 배포 프로세스, CI/CD 파이프라인을 정의합니다.

---

## 1. Deployment Topology (배포 토폴로지)

### 1.1 Architecture Overview

**배포 타입**: 단일 서버 (Single Server)

**서버 구성**:
```
┌─────────────────────────────────────────────────────────────┐
│                    Development Server                       │
│  (Ubuntu 20.04 LTS, 2 Core, 2GB RAM, 10GB Disk)           │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Nginx (Port 80)                                    │   │
│  │  - Reverse Proxy                                    │   │
│  │  - Static File Serving                              │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                     │
│  ┌────────────────────▼────────────────────────────────┐   │
│  │  Spring Boot Application (Port 8080)                │   │
│  │  - Embedded Tomcat                                  │   │
│  │  - JVM (Xmx1g)                                      │   │
│  └────────────────────┬────────────────────────────────┘   │
│                       │                                     │
│  ┌────────────────────▼────────────────────────────────┐   │
│  │  Storage                                            │   │
│  │  - H2 In-Memory Database (JVM Heap)                │   │
│  │  - File Storage (/var/uploads/)                    │   │
│  │  - Logs (/var/log/table-order/)                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Network Topology

**외부 접근**:
```
Internet
  │
  │ HTTP (80)
  ▼
Nginx (Reverse Proxy)
  │
  ├─ /                → Customer Frontend (Static Files)
  ├─ /admin           → Admin Frontend (Static Files)
  ├─ /api/*           → Backend API (Proxy to 8080)
  ├─ /sse/*           → SSE Endpoint (Proxy to 8080)
  ├─ /swagger-ui.html → Swagger UI (Proxy to 8080)
  └─ /h2-console      → H2 Console (Proxy to 8080)
```

**내부 통신**:
```
Nginx (80) ←→ Spring Boot (8080)
```


### 1.3 Directory Structure

**서버 디렉토리 구조**:
```
/opt/table-order/
├── table-order-backend.jar       # 애플리케이션 JAR
├── restart.sh                     # 재시작 스크립트
└── application.yml                # 설정 파일 (선택적)

/var/uploads/table-order/
└── menus/                         # 메뉴 이미지 파일
    ├── 1707465600000.jpg
    └── ...

/var/log/table-order/
├── application.log                # 애플리케이션 로그
└── error.log                      # 에러 로그

/var/www/table-order/
├── customer-frontend/             # Customer Frontend 정적 파일
│   ├── index.html
│   ├── static/
│   └── ...
└── admin-frontend/                # Admin Frontend 정적 파일
    ├── index.html
    ├── static/
    └── ...

/etc/nginx/sites-available/
└── table-order                    # Nginx 설정 파일
```

---

## 2. Deployment Process (배포 프로세스)

### 2.1 Build Process

**Step 1: Source Code Checkout**
```bash
git clone https://github.com/your-org/table-order-backend.git
cd table-order-backend
git checkout main
```

**Step 2: Build with Maven**
```bash
mvn clean package -DskipTests
```

**Output**:
```
target/table-order-backend-1.0.0.jar
```

**Step 3: Run Tests (Optional)**
```bash
mvn test
```

### 2.2 Deployment Process

**Step 1: Stop Existing Application**
```bash
ssh appuser@dev-server "/opt/table-order/restart.sh stop"
```

**Step 2: Upload JAR File**
```bash
scp target/table-order-backend-1.0.0.jar appuser@dev-server:/opt/table-order/table-order-backend.jar
```

**Step 3: Start Application**
```bash
ssh appuser@dev-server "/opt/table-order/restart.sh start"
```

**Step 4: Verify Deployment**
```bash
# Check application status
curl http://dev-server:8080/actuator/health

# Check logs
ssh appuser@dev-server "tail -f /var/log/table-order/application.log"
```

### 2.3 Rollback Process

**Step 1: Keep Previous Version**
```bash
# Before deployment, backup current JAR
ssh appuser@dev-server "cp /opt/table-order/table-order-backend.jar /opt/table-order/table-order-backend.jar.backup"
```

**Step 2: Rollback**
```bash
# Stop current version
ssh appuser@dev-server "/opt/table-order/restart.sh stop"

# Restore previous version
ssh appuser@dev-server "cp /opt/table-order/table-order-backend.jar.backup /opt/table-order/table-order-backend.jar"

# Start previous version
ssh appuser@dev-server "/opt/table-order/restart.sh start"
```

---

## 3. CI/CD Pipeline (Jenkins)

### 3.1 Jenkins Configuration

**Jenkins 설치**:
```bash
# Install Java
sudo apt update
sudo apt install openjdk-17-jdk -y

# Install Jenkins
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

**Jenkins 접근**:
- URL: `http://jenkins-server:8080`
- 초기 비밀번호: `/var/lib/jenkins/secrets/initialAdminPassword`

**필수 플러그인**:
- Git Plugin
- Maven Integration Plugin
- SSH Agent Plugin
- Pipeline Plugin

### 3.2 Jenkins Pipeline

**Jenkinsfile** (프로젝트 루트):
```groovy
pipeline {
    agent any
    
    tools {
        maven 'Maven 3.8'
        jdk 'JDK 17'
    }
    
    environment {
        APP_NAME = 'table-order-backend'
        DEPLOY_SERVER = 'appuser@dev-server'
        DEPLOY_PATH = '/opt/table-order'
        JAR_NAME = 'table-order-backend.jar'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                git branch: 'main', 
                    url: 'https://github.com/your-org/table-order-backend.git',
                    credentialsId: 'github-credentials'
            }
        }
        
        stage('Build') {
            steps {
                echo 'Building application...'
                sh 'mvn clean package -DskipTests'
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'mvn test'
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        
        stage('Backup') {
            steps {
                echo 'Backing up current version...'
                sshagent(['ssh-credentials']) {
                    sh """
                        ssh ${DEPLOY_SERVER} '
                            if [ -f ${DEPLOY_PATH}/${JAR_NAME} ]; then
                                cp ${DEPLOY_PATH}/${JAR_NAME} ${DEPLOY_PATH}/${JAR_NAME}.backup
                            fi
                        '
                    """
                }
            }
        }
        
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sshagent(['ssh-credentials']) {
                    sh """
                        # Upload JAR
                        scp target/${APP_NAME}-*.jar ${DEPLOY_SERVER}:${DEPLOY_PATH}/${JAR_NAME}
                        
                        # Restart application
                        ssh ${DEPLOY_SERVER} '${DEPLOY_PATH}/restart.sh'
                    """
                }
            }
        }
        
        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                script {
                    sleep(time: 10, unit: 'SECONDS')
                    def response = sh(
                        script: "curl -s -o /dev/null -w '%{http_code}' http://dev-server:8080/actuator/health",
                        returnStdout: true
                    ).trim()
                    
                    if (response != '200') {
                        error("Deployment verification failed. HTTP status: ${response}")
                    }
                }
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
            // 알림 전송 (이메일, Slack 등)
        }
        failure {
            echo 'Deployment failed!'
            // 알림 전송 및 롤백 고려
        }
        always {
            cleanWs()
        }
    }
}
```

### 3.3 Jenkins Job Configuration

**Job 생성**:
1. Jenkins 대시보드 → "New Item"
2. Job 이름: "table-order-backend-deploy"
3. 타입: "Pipeline"
4. Pipeline 설정:
   - Definition: "Pipeline script from SCM"
   - SCM: Git
   - Repository URL: `https://github.com/your-org/table-order-backend.git`
   - Script Path: `Jenkinsfile`

**빌드 트리거**:
- Poll SCM: `H/5 * * * *` (5분마다 Git 변경 확인)
- 또는 GitHub Webhook 설정

**Credentials 설정**:
- GitHub Credentials: Username + Personal Access Token
- SSH Credentials: Private Key (dev-server 접근용)

### 3.4 Deployment Script

**restart.sh** (`/opt/table-order/restart.sh`):
```bash
#!/bin/bash

APP_NAME="table-order-backend"
APP_JAR="/opt/table-order/table-order-backend.jar"
PID_FILE="/var/run/table-order.pid"
LOG_FILE="/var/log/table-order/application.log"

# Function to stop application
stop_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "Stopping $APP_NAME (PID: $PID)..."
            kill $PID
            
            # Wait for graceful shutdown (max 30 seconds)
            for i in {1..30}; do
                if ! ps -p $PID > /dev/null 2>&1; then
                    echo "$APP_NAME stopped successfully"
                    break
                fi
                sleep 1
            done
            
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                echo "Force killing $APP_NAME..."
                kill -9 $PID
            fi
        fi
        rm -f "$PID_FILE"
    else
        echo "$APP_NAME is not running"
    fi
}

# Function to start application
start_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "$APP_NAME is already running (PID: $PID)"
            exit 1
        fi
    fi
    
    echo "Starting $APP_NAME..."
    
    # Set environment variables
    export JWT_SECRET="${JWT_SECRET:-default-secret-key-change-in-production}"
    export SPRING_PROFILES_ACTIVE="dev"
    
    # Start application
    nohup java -jar \
        -Xms512m \
        -Xmx1g \
        -XX:MetaspaceSize=128m \
        -XX:MaxMetaspaceSize=256m \
        -XX:+UseG1GC \
        "$APP_JAR" \
        > "$LOG_FILE" 2>&1 &
    
    echo $! > "$PID_FILE"
    
    echo "$APP_NAME started (PID: $(cat $PID_FILE))"
    echo "Logs: tail -f $LOG_FILE"
}

# Function to check status
status_app() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "$APP_NAME is running (PID: $PID)"
        else
            echo "$APP_NAME is not running (stale PID file)"
        fi
    else
        echo "$APP_NAME is not running"
    fi
}

# Main script
case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        stop_app
        sleep 2
        start_app
        ;;
    status)
        status_app
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
```

**권한 설정**:
```bash
chmod +x /opt/table-order/restart.sh
chown appuser:appuser /opt/table-order/restart.sh
```

---

## 4. Environment Configuration (환경 설정)

### 4.1 Development Environment

**환경 변수** (`/etc/environment` 또는 `~/.bashrc`):
```bash
# JWT Secret
export JWT_SECRET="dev-secret-key-change-in-production"

# Spring Profile
export SPRING_PROFILES_ACTIVE="dev"

# Log Path
export LOG_PATH="/var/log/table-order"

# Upload Directory
export UPLOAD_DIR="/var/uploads/table-order/menus"
```

**application-dev.yml**:
```yaml
spring:
  h2:
    console:
      enabled: true
  
  datasource:
    url: jdbc:h2:mem:tableorder
  
logging:
  level:
    root: INFO
    com.tableorder: DEBUG
    org.springframework: INFO
    org.mybatis: DEBUG

server:
  port: 8080
```

### 4.2 Test Environment

**환경 변수**:
```bash
export JWT_SECRET="test-secret-key"
export SPRING_PROFILES_ACTIVE="test"
```

**application-test.yml**:
```yaml
spring:
  h2:
    console:
      enabled: false
  
  datasource:
    url: jdbc:h2:mem:testdb

logging:
  level:
    root: INFO
    com.tableorder: INFO
```

### 4.3 Production Environment (향후)

**환경 변수**:
```bash
export JWT_SECRET="$(openssl rand -base64 32)"
export SPRING_PROFILES_ACTIVE="prod"
export DATABASE_URL="jdbc:mysql://prod-db:3306/tableorder"
export DATABASE_USERNAME="tableorder_user"
export DATABASE_PASSWORD="secure-password"
```

**application-prod.yml**:
```yaml
spring:
  h2:
    console:
      enabled: false
  
  datasource:
    url: ${DATABASE_URL}
    username: ${DATABASE_USERNAME}
    password: ${DATABASE_PASSWORD}

logging:
  level:
    root: WARN
    com.tableorder: INFO
```

---

## 5. Deployment Checklist (배포 체크리스트)

### 5.1 Pre-Deployment

- [ ] 소스 코드 최신 버전 확인 (Git pull)
- [ ] 단위 테스트 통과 확인 (`mvn test`)
- [ ] 통합 테스트 통과 확인 (선택적)
- [ ] 빌드 성공 확인 (`mvn clean package`)
- [ ] 환경 변수 설정 확인 (JWT_SECRET 등)
- [ ] 디렉토리 권한 확인 (/var/uploads, /var/log)
- [ ] 현재 버전 백업 (JAR 파일)

### 5.2 Deployment

- [ ] 기존 애플리케이션 중지
- [ ] 새 JAR 파일 업로드
- [ ] 애플리케이션 시작
- [ ] 프로세스 실행 확인 (`ps aux | grep java`)
- [ ] 로그 확인 (에러 없는지)
- [ ] Health Check 확인 (`/actuator/health`)

### 5.3 Post-Deployment

- [ ] API 엔드포인트 테스트 (Swagger UI)
- [ ] 주요 기능 테스트 (주문 생성, 메뉴 조회 등)
- [ ] SSE 연결 테스트
- [ ] 프론트엔드 연동 테스트
- [ ] 로그 모니터링 (10분간)
- [ ] 성능 확인 (응답 시간)

### 5.4 Rollback Criteria

다음 상황 발생 시 롤백:
- [ ] 애플리케이션 시작 실패
- [ ] Health Check 실패 (5분 이상)
- [ ] 주요 API 엔드포인트 오류 (500 에러)
- [ ] 데이터베이스 연결 실패
- [ ] 심각한 로그 에러 발생

---

## 6. Monitoring & Health Check (모니터링 및 헬스 체크)

### 6.1 Health Check Endpoint

**Spring Boot Actuator 설정**:
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info
  endpoint:
    health:
      show-details: always
```

**Health Check URL**:
```
http://dev-server:8080/actuator/health
```

**응답 예시**:
```json
{
  "status": "UP",
  "components": {
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 10737418240,
        "free": 5368709120,
        "threshold": 10485760
      }
    },
    "db": {
      "status": "UP",
      "details": {
        "database": "H2",
        "validationQuery": "isValid()"
      }
    }
  }
}
```

### 6.2 Manual Monitoring

**프로세스 확인**:
```bash
ps aux | grep java
```

**로그 확인**:
```bash
tail -f /var/log/table-order/application.log
tail -f /var/log/table-order/error.log
```

**메모리 사용량 확인**:
```bash
jps -lvm
```

**디스크 사용량 확인**:
```bash
df -h
du -sh /var/uploads/table-order/
du -sh /var/log/table-order/
```

### 6.3 Automated Monitoring (향후)

**Prometheus + Grafana**:
- Spring Boot Actuator metrics 수집
- JVM 메모리, CPU, 스레드 모니터링
- API 응답 시간 모니터링
- 알림 설정 (이메일, Slack)

---

## 7. Disaster Recovery Plan (재해 복구 계획)

### 7.1 Backup Strategy

**애플리케이션 코드**:
- Git 저장소 (GitHub)
- 자동 백업 (Git push)

**설정 파일**:
- `/opt/table-order/application.yml` (수동 백업)
- `/etc/nginx/sites-available/table-order` (수동 백업)

**파일 저장소**:
- `/var/uploads/table-order/` (수동 백업)
- 백업 스크립트:
```bash
#!/bin/bash
BACKUP_DIR="/backup/table-order"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/uploads-$DATE.tar.gz /var/uploads/table-order/
```

**데이터베이스**:
- H2 In-Memory (백업 불필요, 영속성 없음)

### 7.2 Recovery Procedure

**서버 장애 시**:
1. 서버 재시작
2. 필수 서비스 확인 (Nginx, Java)
3. 애플리케이션 재시작 (`/opt/table-order/restart.sh start`)
4. Health Check 확인
5. 로그 확인

**애플리케이션 장애 시**:
1. 로그 확인 (에러 원인 파악)
2. 롤백 결정 (필요 시)
3. 이전 버전으로 롤백
4. 또는 핫픽스 배포

**파일 저장소 손실 시**:
1. 백업에서 복원
```bash
tar -xzf /backup/table-order/uploads-20260209.tar.gz -C /
```
2. 권한 확인
```bash
chown -R appuser:appuser /var/uploads/table-order
chmod -R 755 /var/uploads/table-order
```

**예상 복구 시간**: 30분 이내

---

## 8. Scaling Plan (확장 계획)

### 8.1 Current Capacity

**현재 용량**:
- 동시 접속: 50명
- 매장 수: 5개
- 일일 주문: 500건

**리소스 사용률**:
- CPU: ~30%
- RAM: ~50% (JVM 1GB + OS)
- Disk: ~20%

### 8.2 Vertical Scaling (수직 확장)

**확장 시점**: 동시 접속 50명 → 100명

**확장 방법**:
1. 서버 리소스 증설
   - CPU: 2 Core → 4 Core
   - RAM: 2GB → 4GB
2. JVM 메모리 증설
   - Xmx: 1GB → 2GB
3. 연결 풀 증설
   - HikariCP: 10 → 20

**예상 용량**:
- 동시 접속: 100명
- 매장 수: 10개
- 일일 주문: 1,000건

### 8.3 Horizontal Scaling (수평 확장) - 향후

**확장 시점**: 동시 접속 100명 초과

**필요 변경사항**:
1. 데이터베이스: H2 → MySQL/PostgreSQL (공유 DB)
2. 캐시: Caffeine → Redis (공유 캐시)
3. 세션: Stateless 유지 (JWT)
4. 파일 저장소: Local → S3/NFS (공유 스토리지)
5. 로드 밸런서: Nginx (다중 백엔드 인스턴스)

**아키텍처**:
```
Nginx Load Balancer
  ├── Backend Instance 1 (8080)
  ├── Backend Instance 2 (8081)
  └── Backend Instance 3 (8082)
       ↓
  MySQL Database (공유)
  Redis Cache (공유)
  S3/NFS Storage (공유)
```

---

## 9. Security Considerations (보안 고려사항)

### 9.1 Network Security

**Firewall 설정** (UFW):
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (Nginx)
sudo ufw deny 8080/tcp   # Block direct access to Spring Boot
sudo ufw enable
```

**SSH 보안**:
- 키 기반 인증만 허용
- 비밀번호 인증 비활성화
- Root 로그인 비활성화

### 9.2 Application Security

**환경 변수 보안**:
- JWT Secret은 환경 변수로 관리
- 코드에 하드코딩 금지
- `.env` 파일은 Git에 커밋 금지

**CORS 보안**:
- 개발 환경: 모든 Origin 허용 (*)
- 프로덕션: 특정 Origin만 허용

**HTTPS** (향후 프로덕션):
- Let's Encrypt SSL 인증서
- Nginx에서 SSL/TLS 종료
- HTTP → HTTPS 리다이렉트

### 9.3 Access Control

**서버 접근**:
- SSH 키 기반 인증
- 특정 IP만 SSH 접근 허용 (선택적)

**애플리케이션 접근**:
- JWT 토큰 기반 인증
- 역할 기반 권한 관리 (RBAC)

---

## 10. Deployment Timeline (배포 일정)

### 10.1 Initial Deployment

**Phase 1: 인프라 준비** (1일)
- [ ] 서버 프로비저닝
- [ ] OS 설치 및 설정 (Ubuntu 20.04)
- [ ] 필수 패키지 설치 (Java, Maven, Nginx)
- [ ] 디렉토리 생성 및 권한 설정
- [ ] Firewall 설정

**Phase 2: CI/CD 설정** (1일)
- [ ] Jenkins 설치 및 설정
- [ ] Jenkins Job 생성
- [ ] Git 연동
- [ ] SSH Credentials 설정
- [ ] Pipeline 테스트

**Phase 3: 애플리케이션 배포** (0.5일)
- [ ] 첫 배포 (수동)
- [ ] Health Check 확인
- [ ] 로그 확인
- [ ] API 테스트

**Phase 4: 프론트엔드 배포** (0.5일)
- [ ] Nginx 설정
- [ ] 정적 파일 업로드
- [ ] 프론트엔드-백엔드 연동 테스트

**총 소요 시간**: 3일

### 10.2 Regular Deployment

**빈도**: 주 1~2회 (개발 진행에 따라)

**배포 시간**: 10~15분
- 빌드: 3분
- 테스트: 2분
- 배포: 5분
- 검증: 5분

**배포 시간대**: 업무 시간 외 (저녁 또는 주말)

---

## Notes

- 현재 배포 아키텍처는 개발/테스트 환경에 최적화됨
- 단일 서버 구성으로 간단하고 관리 용이
- Jenkins를 사용한 CI/CD 파이프라인으로 자동화
- 프로덕션 환경으로 전환 시 다음 항목 고려:
  - 로드 밸런서 추가
  - 다중 인스턴스 배포
  - 공유 데이터베이스 (MySQL/PostgreSQL)
  - 공유 캐시 (Redis)
  - 공유 스토리지 (S3/NFS)
  - HTTPS/SSL 적용
  - 자동 모니터링 및 알림
- 모든 배포 프로세스는 롤백 가능하도록 설계됨

