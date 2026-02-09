# Backend Infrastructure Design Plan

## Overview
이 계획은 Backend 유닛의 논리적 컴포넌트를 실제 인프라 서비스에 매핑하고 배포 아키텍처를 정의합니다.

## Context Analysis

### Functional Design Summary
- **Domain Entities**: Store, Table, Menu, Order, OrderItem, OrderHistory, OrderHistoryItem, User
- **Business Workflows**: 10개 워크플로우 (주문 생성, 상태 변경, 메뉴 관리, 세션 관리, 로그인 등)
- **Data Access**: MyBatis 기반 데이터 액세스

### NFR Requirements Summary
- **Database**: H2 In-Memory (개발/테스트 환경)
- **Caching**: Spring Cache + Caffeine (애플리케이션 레벨)
- **File Storage**: 로컬 파일 시스템 (uploads/)
- **Deployment**: CI/CD 파이프라인 (GitHub Actions)
- **Scalability**: 중규모 (50명 동시 접속, 5개 매장)
- **Monitoring**: 없음 (개발 환경)

### NFR Design Summary
- **Logical Components**: 18개 컴포넌트 (Common, Infrastructure, Security, Utility, Configuration)
- **Patterns**: 11개 NFR 패턴 (Resilience, Performance, Security, Scalability, Maintainability)

## Infrastructure Design Questions

아래 질문들에 [Answer]: 태그를 사용하여 답변해주세요.

---

### 1. Deployment Environment (배포 환경)

**Q1: 애플리케이션 서버 환경은 어떻게 구성하시겠습니까?**

현재 요구사항: 로컬 서버 (On-premises), 개발/테스트 환경

선택지:
- A) 단일 서버 (개발자 로컬 머신)
- B) 전용 개발 서버 (팀 공유)
- C) 클라우드 VM (AWS EC2, Azure VM 등)
- D) 기타 (구체적으로 명시)

[Answer]: B

**Q2: 운영 체제는 무엇을 사용하시겠습니까?**

선택지:
- A) Windows Server
- B) Linux (Ubuntu, CentOS 등)
- C) macOS
- D) 개발자 환경에 따라 다름

[Answer]: B

---

### 2. Compute Infrastructure (컴퓨팅 인프라)

**Q3: Spring Boot 애플리케이션 실행 방식은 무엇입니까?**

선택지:
- A) Embedded Tomcat (JAR 실행)
- B) External Tomcat (WAR 배포)
- C) Docker Container
- D) 기타 (구체적으로 명시)

[Answer]: A

**Q4: JVM 메모리 설정은 어떻게 하시겠습니까?**

현재 요구사항: 중규모 확장성 (50명 동시 접속)

선택지:
- A) 최소 설정 (Xmx512m)
- B) 표준 설정 (Xmx1g)
- C) 넉넉한 설정 (Xmx2g)
- D) 기타 (구체적으로 명시)

[Answer]: B

---

### 3. Storage Infrastructure (스토리지 인프라)

**Q5: H2 Database 파일 저장 위치는 어디입니까?**

현재 요구사항: H2 In-Memory (영속성 불필요)

선택지:
- A) 완전 In-Memory (파일 없음, jdbc:h2:mem:)
- B) 파일 기반 (jdbc:h2:file:, 재시작 시 데이터 유지)
- C) 혼합 (In-Memory + 주기적 파일 백업)
- D) 기타 (구체적으로 명시)

[Answer]: A

**Q6: 메뉴 이미지 파일 저장소 위치는 어디입니까?**

현재 요구사항: 로컬 파일 시스템 (uploads/)

선택지:
- A) 애플리케이션 디렉토리 내부 (src/main/resources/uploads/)
- B) 애플리케이션 외부 절대 경로 (/var/uploads/, C:\uploads\ 등)
- C) 사용자 홈 디렉토리 (~/uploads/)
- D) 기타 (구체적으로 명시)

[Answer]: B

**Q7: 파일 저장소 용량 제한은 어떻게 관리하시겠습니까?**

선택지:
- A) 제한 없음 (개발 환경)
- B) 애플리케이션 레벨 제한 (예: 최대 100개 파일)
- C) 파일 시스템 쿼터 설정
- D) 기타 (구체적으로 명시)

[Answer]: B

---

### 4. Networking Infrastructure (네트워킹 인프라)

**Q8: 애플리케이션 포트 설정은 어떻게 하시겠습니까?**

선택지:
- A) 기본 포트 (8080)
- B) 커스텀 포트 (예: 9090, 3000)
- C) 환경 변수로 설정 (PORT)
- D) 기타 (구체적으로 명시)

[Answer]: A

**Q9: CORS 허용 Origin 설정은 어떻게 하시겠습니까?**

현재 요구사항: Customer Frontend (localhost:3000), Admin Frontend (localhost:3001)

선택지:
- A) 고정 설정 (localhost:3000, localhost:3001)
- B) 환경 변수로 설정 (CORS_ALLOWED_ORIGINS)
- C) 모든 Origin 허용 (*) - 개발 환경만
- D) 기타 (구체적으로 명시)

[Answer]: C

**Q10: 로드 밸런서 또는 리버스 프록시를 사용하시겠습니까?**

현재 요구사항: 단일 서버, 개발 환경

선택지:
- A) 사용 안 함 (직접 접근)
- B) Nginx 사용
- C) Apache HTTP Server 사용
- D) 기타 (구체적으로 명시)

[Answer]: B

---

### 5. Monitoring & Logging Infrastructure (모니터링 및 로깅 인프라)

**Q11: 로그 파일 저장 위치는 어디입니까?**

현재 요구사항: 표준 로깅 (INFO, WARN, ERROR)

선택지:
- A) 콘솔 출력만 (파일 저장 안 함)
- B) 애플리케이션 디렉토리 내부 (logs/)
- C) 시스템 로그 디렉토리 (/var/log/, C:\logs\ 등)
- D) 기타 (구체적으로 명시)

[Answer]: C

**Q12: 로그 파일 로테이션 정책은 어떻게 하시겠습니까?**

선택지:
- A) 로테이션 없음 (단일 파일)
- B) 일별 로테이션 (application-YYYY-MM-DD.log)
- C) 크기 기반 로테이션 (10MB 초과 시)
- D) 기타 (구체적으로 명시)

[Answer]: A

---

### 6. Deployment & CI/CD Infrastructure (배포 및 CI/CD 인프라)

**Q13: CI/CD 파이프라인 도구는 무엇을 사용하시겠습니까?**

현재 요구사항: CI/CD 파이프라인 (GitHub Actions 권장)

선택지:
- A) GitHub Actions
- B) Jenkins
- C) GitLab CI
- D) 수동 배포 (CI/CD 없음)

[Answer]: B

**Q14: 배포 아티팩트 형식은 무엇입니까?**

선택지:
- A) Executable JAR (java -jar)
- B) WAR (Tomcat 배포)
- C) Docker Image
- D) 기타 (구체적으로 명시)

[Answer]: A

**Q15: 배포 후 애플리케이션 재시작 방식은 무엇입니까?**

선택지:
- A) 수동 재시작 (java -jar 재실행)
- B) 스크립트 자동 재시작 (systemd, init.d)
- C) Docker Container 재시작
- D) 기타 (구체적으로 명시)

[Answer]: A

---

## Execution Plan

### Phase 1: Analyze Answers
- [x] Review all user answers
- [x] Identify ambiguities or missing information
- [x] Create follow-up questions if needed

### Phase 2: Generate Infrastructure Design
- [x] Create `infrastructure-design.md`
  - [x] Map logical components to infrastructure services
  - [x] Define compute infrastructure (JVM, server)
  - [x] Define storage infrastructure (database, files)
  - [x] Define networking infrastructure (ports, CORS, load balancer)
  - [x] Define monitoring infrastructure (logging, metrics)
  - [x] Define security infrastructure (JWT, HTTPS)

### Phase 3: Generate Deployment Architecture
- [x] Create `deployment-architecture.md`
  - [x] Define deployment topology (single server, multi-tier)
  - [x] Define deployment process (build, test, deploy)
  - [x] Define CI/CD pipeline (Jenkins workflow)
  - [x] Define environment configuration (dev, test, prod)
  - [x] Define scaling strategy (vertical, horizontal)
  - [x] Define disaster recovery plan (backup, restore)

### Phase 4: Update Plan Checkboxes
- [x] Mark all completed steps with [x]
- [x] Update aidlc-state.md with Infrastructure Design completion

### Phase 5: Present Completion Message
- [x] Display completion announcement
- [x] Provide AI summary of infrastructure design
- [x] Present formatted workflow message with 2 options

---

## Notes

- 이 계획은 Backend 유닛의 인프라 설계에 초점을 맞춥니다
- 개발/테스트 환경을 기준으로 질문이 생성되었습니다
- 프로덕션 환경으로 전환 시 인프라 재검토가 필요합니다
- 모든 답변은 NFR 요구사항과 일치해야 합니다

