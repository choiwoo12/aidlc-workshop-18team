# Infrastructure Design - Backend

## Overview
Backend 유닛의 논리적 컴포넌트를 실제 인프라 서비스에 매핑하고 배포 환경을 정의합니다.

---

## 1. Deployment Environment (배포 환경)

### 1.1 Server Environment

**선택**: 전용 개발 서버 (팀 공유)

**구성**:
- **서버 타입**: 물리 서버 또는 VM
- **용도**: 팀 공유 개발/테스트 환경
- **접근 방식**: SSH 접근, 팀원 공유

**장점**:
- 일관된 개발 환경
- 팀원 간 통합 테스트 용이
- 로컬 머신 리소스 절약

**제약사항**:
- 동시 배포 시 충돌 가능성
- 서버 다운 시 전체 팀 영향

### 1.2 Operating System

**선택**: Linux (Ubuntu 20.04 LTS 또는 CentOS 8)

**권장**: Ubuntu 20.04 LTS

**이유**:
- 안정성 및 장기 지원
- 풍부한 패키지 생태계
- Java 및 Spring Boot 호환성 우수
- 커뮤니티 지원 활발

**필수 패키지**:
- OpenJDK 17
- Maven 3.x
- Git
- Nginx (리버스 프록시)

---

## 2. Compute Infrastructure (컴퓨팅 인프라)

### 2.1 Application Runtime

**선택**: Embedded Tomcat (Executable JAR)

**실행 방식**:
```bash
java -jar -Xmx1g table-order-backend.jar
```


**장점**:
- 간단한 배포 (단일 JAR 파일)
- 외부 Tomcat 설정 불필요
- 빠른 시작 시간
- Spring Boot 기본 방식

**포트**: 8080 (기본)

### 2.2 JVM Configuration

**메모리 설정**: 표준 설정 (Xmx1g)

**JVM 옵션**:
```bash
-Xms512m          # 초기 힙 크기
-Xmx1g            # 최대 힙 크기
-XX:MetaspaceSize=128m
-XX:MaxMetaspaceSize=256m
-XX:+UseG1GC      # G1 Garbage Collector
```

**근거**:
- 중규모 확장성 (50명 동시 접속)
- H2 In-Memory DB 사용 (메모리 소비)
- SSE 연결 관리 (메모리 소비)
- 여유 있는 메모리 확보

**모니터링**:
- JVM 메모리 사용량 모니터링 (선택적)
- OutOfMemoryError 발생 시 힙 덤프 생성

### 2.3 Server Specifications

**권장 사양**:
- CPU: 2 Core 이상
- RAM: 2GB 이상 (JVM 1GB + OS 1GB)
- Disk: 10GB 이상 (애플리케이션 + 로그 + 이미지)

---

## 3. Storage Infrastructure (스토리지 인프라)

### 3.1 Database Storage

**선택**: H2 In-Memory Database (완전 In-Memory)

**연결 URL**:
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:tableorder
    driver-class-name: org.h2.Driver
    username: sa
    password:
```

**특징**:
- 파일 저장 없음 (메모리만 사용)
- 애플리케이션 재시작 시 데이터 초기화
- 빠른 성능
- 개발/테스트 환경에 적합

**H2 Console**:
- 활성화: `spring.h2.console.enabled=true`
- 접근 경로: `http://localhost:8080/h2-console`

**제약사항**:
- 데이터 영속성 없음
- 서버 재시작 시 모든 데이터 손실
- 프로덕션 환경 부적합

### 3.2 File Storage

**선택**: 로컬 파일 시스템 (애플리케이션 외부 절대 경로)

**저장 경로**: `/var/uploads/table-order/menus/`

**디렉토리 구조**:
```
/var/uploads/table-order/
└── menus/
    ├── 1707465600000.jpg
    ├── 1707465601000.png
    └── ...
```

**파일명 형식**: `{timestamp}.{extension}`

**용량 제한**: 애플리케이션 레벨 제한 (최대 100개 파일)

**설정**:
```yaml
file:
  upload:
    dir: /var/uploads/table-order/menus/
    max-files: 100
    max-size: 5MB
    allowed-extensions: jpg,jpeg,png
```

**권한 설정**:
```bash
sudo mkdir -p /var/uploads/table-order/menus
sudo chown -R appuser:appuser /var/uploads/table-order
sudo chmod -R 755 /var/uploads/table-order
```

**용량 관리**:
- 파일 개수 제한: 100개
- 개수 초과 시 가장 오래된 파일 삭제 (FIFO)
- 애플리케이션 시작 시 파일 개수 확인

**백업**:
- 수동 백업 (필요 시)
- 디렉토리 전체 복사

---

## 4. Networking Infrastructure (네트워킹 인프라)

### 4.1 Application Port

**선택**: 기본 포트 (8080)

**설정**:
```yaml
server:
  port: 8080
```

**접근 URL**:
- Backend API: `http://localhost:8080/api/`
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- H2 Console: `http://localhost:8080/h2-console`

### 4.2 CORS Configuration

**선택**: 모든 Origin 허용 (*) - 개발 환경만

**설정**:
```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsFilter corsFilter() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(Arrays.asList("*")); // 개발 환경
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(Arrays.asList("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        
        return new CorsFilter(source);
    }
}
```

**주의사항**:
- 개발 환경에서만 사용
- 프로덕션 환경에서는 특정 Origin만 허용
- 보안 위험 인지

**프로덕션 권장 설정**:
```java
config.setAllowedOrigins(Arrays.asList(
    "http://customer-frontend.example.com",
    "http://admin-frontend.example.com"
));
```

### 4.3 Reverse Proxy (Nginx)

**선택**: Nginx 사용

**목적**:
- 정적 파일 서빙 (프론트엔드)
- 리버스 프록시 (백엔드 API)
- SSL/TLS 종료 (향후 HTTPS)
- 로드 밸런싱 (향후 확장)

**Nginx 설정** (`/etc/nginx/sites-available/table-order`):
```nginx
server {
    listen 80;
    server_name dev.tableorder.local;

    # Customer Frontend
    location / {
        root /var/www/table-order/customer-frontend;
        try_files $uri $uri/ /index.html;
    }

    # Admin Frontend
    location /admin {
        alias /var/www/table-order/admin-frontend;
        try_files $uri $uri/ /admin/index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SSE Endpoint
    location /sse/ {
        proxy_pass http://localhost:8080/sse/;
        proxy_set_header Connection '';
        proxy_http_version 1.1;
        chunked_transfer_encoding off;
        proxy_buffering off;
        proxy_cache off;
    }

    # Swagger UI
    location /swagger-ui.html {
        proxy_pass http://localhost:8080/swagger-ui.html;
    }

    # H2 Console
    location /h2-console {
        proxy_pass http://localhost:8080/h2-console;
    }
}
```

**Nginx 활성화**:
```bash
sudo ln -s /etc/nginx/sites-available/table-order /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**장점**:
- 프론트엔드와 백엔드 통합 접근
- 정적 파일 캐싱
- SSL/TLS 지원 (향후)
- 로드 밸런싱 (향후)

---

## 5. Monitoring & Logging Infrastructure (모니터링 및 로깅 인프라)

### 5.1 Logging

**로그 파일 위치**: 시스템 로그 디렉토리 (`/var/log/table-order/`)

**디렉토리 구조**:
```
/var/log/table-order/
├── application.log
├── error.log
└── access.log (선택적)
```

**Logback 설정** (`logback-spring.xml`):
```xml
<configuration>
    <property name="LOG_PATH" value="/var/log/table-order"/>
    
    <!-- Console Appender -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <!-- File Appender -->
    <appender name="FILE" class="ch.qos.logback.core.FileAppender">
        <file>${LOG_PATH}/application.log</file>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <!-- Error File Appender -->
    <appender name="ERROR_FILE" class="ch.qos.logback.core.FileAppender">
        <file>${LOG_PATH}/error.log</file>
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>ERROR</level>
        </filter>
        <encoder>
            <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="CONSOLE" />
        <appender-ref ref="FILE" />
        <appender-ref ref="ERROR_FILE" />
    </root>
</configuration>
```

**로그 로테이션**: 로테이션 없음 (단일 파일)

**근거**:
- 개발 환경으로 로그 양 적음
- 수동 관리 가능
- 필요 시 수동 삭제

**프로덕션 권장**:
- 일별 로테이션 (RollingFileAppender)
- 최대 30일 보관
- 압축 저장

**권한 설정**:
```bash
sudo mkdir -p /var/log/table-order
sudo chown -R appuser:appuser /var/log/table-order
sudo chmod -R 755 /var/log/table-order
```

### 5.2 Monitoring

**선택**: 모니터링 없음 (개발 환경)

**근거**:
- 개발/테스트 환경
- 수동 확인으로 충분
- 인프라 비용 절감

**수동 모니터링 방법**:
- 로그 파일 확인 (`tail -f /var/log/table-order/application.log`)
- JVM 메모리 확인 (`jps -lvm`)
- 프로세스 상태 확인 (`ps aux | grep java`)

**향후 프로덕션 환경**:
- Spring Boot Actuator 활성화
- Prometheus + Grafana (선택적)
- 알림 설정 (이메일, Slack)

---

## 6. Security Infrastructure (보안 인프라)

### 6.1 JWT Token Management

**구현**: JwtTokenProvider 컴포넌트

**토큰 저장**:
- 클라이언트: localStorage (프론트엔드)
- 서버: Stateless (저장 안 함)

**토큰 검증**:
- JwtAuthenticationFilter에서 검증
- 서명 검증 (HS256)
- 만료 시간 확인

**Secret Key 관리**:
```yaml
jwt:
  secret: ${JWT_SECRET:default-secret-key-change-in-production}
  expiration: 57600000  # 16시간 (밀리초)
```

**환경 변수 설정**:
```bash
export JWT_SECRET="your-secure-secret-key-here"
```

**주의사항**:
- Secret Key는 환경 변수로 관리
- 코드에 하드코딩 금지
- 프로덕션에서는 강력한 키 사용 (최소 256비트)

### 6.2 HTTPS/TLS

**현재**: HTTP만 사용 (개발 환경)

**향후 프로덕션**:
- Let's Encrypt SSL 인증서
- Nginx에서 SSL/TLS 종료
- HTTP → HTTPS 리다이렉트

**Nginx SSL 설정** (향후):
```nginx
server {
    listen 443 ssl http2;
    server_name tableorder.example.com;

    ssl_certificate /etc/letsencrypt/live/tableorder.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tableorder.example.com/privkey.pem;
    
    # ... 나머지 설정
}
```

### 6.3 Firewall Configuration

**권장 설정** (UFW):
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (Nginx)
sudo ufw allow 443/tcp   # HTTPS (향후)
sudo ufw enable
```

**포트 8080**: 외부 접근 차단 (Nginx를 통해서만 접근)

---

## 7. Deployment & CI/CD Infrastructure (배포 및 CI/CD 인프라)

### 7.1 CI/CD Tool

**선택**: Jenkins

**Jenkins 설정**:
- Jenkins 서버: 별도 서버 또는 동일 서버
- Jenkins 플러그인: Git, Maven, SSH
- 빌드 트리거: Git Push 또는 수동

**Jenkins Pipeline** (Jenkinsfile):
```groovy
pipeline {
    agent any
    
    tools {
        maven 'Maven 3.8'
        jdk 'JDK 17'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-org/table-order-backend.git'
            }
        }
        
        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }
        
        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    scp target/table-order-backend.jar appuser@dev-server:/opt/table-order/
                    ssh appuser@dev-server "sudo systemctl restart table-order"
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
```

**장점**:
- 강력한 플러그인 생태계
- 유연한 파이프라인 설정
- 팀 내 Jenkins 경험 활용

### 7.2 Build Artifact

**선택**: Executable JAR (java -jar)

**빌드 명령**:
```bash
mvn clean package -DskipTests
```

**아티팩트 위치**:
```
target/table-order-backend-1.0.0.jar
```

**배포 위치**:
```
/opt/table-order/table-order-backend.jar
```

**버전 관리**:
- 파일명에 버전 포함 (선택적)
- Git 태그로 버전 관리

### 7.3 Application Restart

**선택**: 수동 재시작 (java -jar 재실행)

**재시작 스크립트** (`/opt/table-order/restart.sh`):
```bash
#!/bin/bash

APP_NAME="table-order-backend"
APP_JAR="/opt/table-order/table-order-backend.jar"
PID_FILE="/var/run/table-order.pid"

# Stop existing process
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "Stopping $APP_NAME (PID: $PID)..."
        kill $PID
        sleep 5
    fi
    rm -f "$PID_FILE"
fi

# Start new process
echo "Starting $APP_NAME..."
nohup java -jar -Xmx1g "$APP_JAR" > /var/log/table-order/application.log 2>&1 &
echo $! > "$PID_FILE"

echo "$APP_NAME started (PID: $(cat $PID_FILE))"
```

**권한 설정**:
```bash
chmod +x /opt/table-order/restart.sh
```

**Jenkins에서 실행**:
```bash
ssh appuser@dev-server "/opt/table-order/restart.sh"
```

**향후 개선** (systemd):
```ini
[Unit]
Description=Table Order Backend
After=network.target

[Service]
Type=simple
User=appuser
ExecStart=/usr/bin/java -jar -Xmx1g /opt/table-order/table-order-backend.jar
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## 8. Component-to-Infrastructure Mapping (컴포넌트-인프라 매핑)

### 8.1 Application Layer

| 논리적 컴포넌트 | 인프라 서비스 | 위치 |
|----------------|--------------|------|
| Spring Boot Application | Embedded Tomcat | Linux Server (8080) |
| Controller Layer | Spring MVC | Embedded Tomcat |
| Service Layer | Spring Bean | JVM Heap |
| Mapper Layer (MyBatis) | MyBatis Framework | JVM Heap |

### 8.2 Data Layer

| 논리적 컴포넌트 | 인프라 서비스 | 위치 |
|----------------|--------------|------|
| H2 Database | In-Memory Database | JVM Heap |
| File Storage | Local Filesystem | /var/uploads/table-order/ |
| Cache (Caffeine) | In-Memory Cache | JVM Heap |

### 8.3 Infrastructure Layer

| 논리적 컴포넌트 | 인프라 서비스 | 위치 |
|----------------|--------------|------|
| SSE Service | Spring WebFlux | Embedded Tomcat |
| JWT Provider | JJWT Library | JVM Heap |
| File Service | Java NIO | Linux Filesystem |
| Logging | Logback | /var/log/table-order/ |

### 8.4 Network Layer

| 논리적 컴포넌트 | 인프라 서비스 | 위치 |
|----------------|--------------|------|
| Reverse Proxy | Nginx | Linux Server (80) |
| CORS Filter | Spring Security | Embedded Tomcat |
| SSL/TLS | Nginx (향후) | Linux Server (443) |

### 8.5 Deployment Layer

| 논리적 컴포넌트 | 인프라 서비스 | 위치 |
|----------------|--------------|------|
| CI/CD Pipeline | Jenkins | Jenkins Server |
| Build Tool | Maven | Jenkins Agent |
| Artifact Repository | Filesystem | /opt/table-order/ |

---

## 9. Infrastructure Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                            │
│  Customer Frontend (React)    Admin Frontend (React)            │
│  http://dev.tableorder.local  http://dev.tableorder.local/admin │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP (80)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx (Reverse Proxy)                      │
│  - Static File Serving (Frontend)                               │
│  - Reverse Proxy (Backend API)                                  │
│  - SSL/TLS Termination (향후)                                   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTP (8080)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              Spring Boot Application (Embedded Tomcat)          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Controller Layer (REST API)                            │   │
│  │  - OrderController, MenuController, TableController     │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │  Service Layer (Business Logic)                         │   │
│  │  - OrderService, MenuService, TableService, AuthService │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │  Mapper Layer (Data Access)                             │   │
│  │  - OrderMapper, MenuMapper, TableMapper (MyBatis)       │   │
│  └────────────────────┬────────────────────────────────────┘   │
│                       │                                         │
│  ┌────────────────────▼────────────────────────────────────┐   │
│  │  Infrastructure Components                              │   │
│  │  - SSEService, FileService, JwtTokenProvider            │   │
│  │  - CacheManager (Caffeine), GlobalExceptionHandler      │   │
│  └─────────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ H2 Database │  │ File Storage│  │   Logging   │
│ (In-Memory) │  │ /var/uploads│  │  /var/log   │
│  JVM Heap   │  │  Filesystem │  │  Filesystem │
└─────────────┘  └─────────────┘  └─────────────┘
```

---

## 10. Environment Configuration (환경 설정)

### 10.1 Application Properties

**파일**: `application.yml`

```yaml
server:
  port: 8080

spring:
  application:
    name: table-order-backend
  
  datasource:
    url: jdbc:h2:mem:tableorder
    driver-class-name: org.h2.Driver
    username: sa
    password:
  
  h2:
    console:
      enabled: true
      path: /h2-console
  
  servlet:
    multipart:
      max-file-size: 5MB
      max-request-size: 5MB
  
  cache:
    type: caffeine
    caffeine:
      spec: maximumSize=500,expireAfterWrite=10m

mybatis:
  mapper-locations: classpath:mybatis/mapper/**/*.xml
  type-aliases-package: com.tableorder.domain
  configuration:
    map-underscore-to-camel-case: true

jwt:
  secret: ${JWT_SECRET:default-secret-key-change-in-production}
  expiration: 57600000  # 16시간

file:
  upload:
    dir: /var/uploads/table-order/menus/
    max-files: 100
    max-size: 5242880  # 5MB

logging:
  level:
    root: INFO
    com.tableorder: INFO
  file:
    path: /var/log/table-order
    name: /var/log/table-order/application.log
```

### 10.2 Environment Variables

**필수 환경 변수**:
```bash
export JWT_SECRET="your-secure-secret-key-here"
export SPRING_PROFILES_ACTIVE="dev"
```

**선택적 환경 변수**:
```bash
export SERVER_PORT=8080
export LOG_PATH=/var/log/table-order
export UPLOAD_DIR=/var/uploads/table-order/menus
```

### 10.3 Profile Configuration

**개발 환경** (`application-dev.yml`):
```yaml
spring:
  h2:
    console:
      enabled: true
  
logging:
  level:
    com.tableorder: DEBUG
```

**테스트 환경** (`application-test.yml`):
```yaml
spring:
  h2:
    console:
      enabled: false

logging:
  level:
    com.tableorder: INFO
```

---

## 11. Scaling Strategy (확장 전략)

### 11.1 Current Architecture

**타입**: 단일 서버 (Monolithic)

**제약사항**:
- 수직 확장만 가능 (CPU, RAM 증설)
- 단일 장애점 (SPOF)
- In-Memory 데이터 공유 불가

### 11.2 Vertical Scaling (수직 확장)

**현재 → 향후**:
- CPU: 2 Core → 4 Core
- RAM: 2GB → 4GB
- JVM Heap: 1GB → 2GB

**적용 시점**:
- 동시 접속자 50명 → 100명
- 매장 수 5개 → 10개

### 11.3 Horizontal Scaling (수평 확장) - 향후

**필요 조건**:
- 데이터베이스: H2 → MySQL/PostgreSQL
- 캐시: Caffeine → Redis
- 세션: Stateless (JWT 유지)
- 파일 저장소: Local → S3/NFS

**아키텍처**:
```
Load Balancer (Nginx)
  ├── Backend Instance 1
  ├── Backend Instance 2
  └── Backend Instance 3
       ↓
  Shared Database (MySQL)
  Shared Cache (Redis)
  Shared Storage (S3/NFS)
```

---

## 12. Disaster Recovery (재해 복구)

### 12.1 Backup Strategy

**데이터베이스**: 백업 불필요 (In-Memory, 영속성 없음)

**파일 저장소**: 수동 백업
```bash
# 백업
tar -czf /backup/table-order-uploads-$(date +%Y%m%d).tar.gz /var/uploads/table-order/

# 복원
tar -xzf /backup/table-order-uploads-20260209.tar.gz -C /
```

**애플리케이션**: Git 저장소 (소스 코드)

### 12.2 Recovery Procedure

**서버 장애 시**:
1. 서버 재시작
2. 애플리케이션 재배포 (Jenkins 또는 수동)
3. 파일 저장소 복원 (필요 시)
4. 서비스 정상화 확인

**예상 복구 시간**: 30분 이내

---

## 13. Security Considerations (보안 고려사항)

### 13.1 Network Security

- Firewall 설정 (UFW)
- 불필요한 포트 차단
- SSH 키 기반 인증

### 13.2 Application Security

- JWT Secret Key 환경 변수 관리
- CORS 설정 (개발 환경: *, 프로덕션: 특정 Origin)
- 입력 검증 (Controller + Service)
- SQL Injection 방지 (MyBatis Prepared Statement)

### 13.3 Data Security

- 비밀번호 해싱 (bcrypt)
- PIN 해싱 (SHA-256)
- HTTPS 사용 (향후 프로덕션)

---

## Notes

- 현재 인프라 설계는 개발/테스트 환경에 최적화됨
- 프로덕션 환경으로 전환 시 다음 항목 재검토 필요:
  - 데이터베이스: H2 → MySQL/PostgreSQL
  - 캐시: Caffeine → Redis
  - 파일 저장소: Local → S3/NFS
  - 모니터링: 없음 → Actuator + Prometheus + Grafana
  - 로그 로테이션: 없음 → 일별 로테이션
  - HTTPS: 없음 → Let's Encrypt SSL
  - 수평 확장: 단일 서버 → 로드 밸런서 + 다중 인스턴스
- 모든 인프라 설정은 NFR 요구사항과 일치함

