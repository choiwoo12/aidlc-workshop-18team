# Backend NFR Requirements Plan - 테이블오더 서비스

## Plan Overview
Backend 유닛의 비기능 요구사항(NFR)을 평가하고 기술 스택을 결정합니다. Functional Design을 기반으로 성능, 확장성, 가용성, 보안 요구사항을 정의합니다.

---

## Functional Design Context

### Backend 유닛 특성
- **비즈니스 로직**: 10개 워크플로우 (주문, 메뉴, 세션, 인증, SSE)
- **도메인 엔티티**: 8개 (Store, Table, Menu, Order, OrderItem, OrderHistory, OrderHistoryItem, User)
- **비즈니스 규칙**: 28개 (검증, 무결성, 동시성 제어)
- **기술 스택**: Spring Boot, MyBatis, H2 (In-Memory), JWT, SSE

### 기존 NFR (Requirements Analysis에서 정의됨)
- **NFR-1 (성능)**: 페이지 로딩 3초 이내, SSE 이벤트 2초 이내 전달
- **NFR-2 (보안)**: JWT 인증, bcrypt 비밀번호 해싱, 로그인 5회 실패 시 잠금
- **NFR-3 (사용성)**: 터치 친화적 UI (최소 44x44px)
- **NFR-4 (신뢰성)**: 주문 실패 시 장바구니 유지, SSE 재연결 3회 시도

---

## NFR Assessment Methodology

### 1. Scalability Requirements
- [x] 동시 사용자 수 예상
- [x] 매장 수 확장 계획
- [x] 데이터 증가율 예상
- [x] 수평/수직 확장 전략

### 2. Performance Requirements
- [x] API 응답 시간 목표
- [x] 데이터베이스 쿼리 성능
- [x] SSE 이벤트 전송 지연
- [x] 파일 업로드 성능

### 3. Availability Requirements
- [x] 시스템 가용성 목표
- [x] 장애 복구 시간
- [x] 백업 및 복구 전략

### 4. Security Requirements
- [x] 데이터 암호화 요구사항
- [x] API 보안 강화
- [x] 감사 로그 요구사항

### 5. Tech Stack Decisions
- [x] 데이터베이스 선택 검증
- [x] 캐싱 전략
- [x] 로깅 및 모니터링
- [x] 배포 전략

---

## Context-Appropriate Questions

다음 질문들에 답변해주시면 Backend 유닛의 NFR을 정확히 정의할 수 있습니다.

### Q1: 동시 접속 사용자 수
예상되는 동시 접속 사용자 수는 얼마인가요?

A) **소규모** - 동시 접속 10명 이하 (1개 매장, 10개 테이블)
B) **중규모** - 동시 접속 50명 이하 (5개 매장, 각 10개 테이블)
C) **대규모** - 동시 접속 100명 이상 (10개 이상 매장)
D) **확장 가능** - 초기 소규모, 향후 대규모 확장 계획

[Answer]: B

**Reasoning**: 동시 접속자 수는 서버 리소스, 데이터베이스 연결 풀, SSE 연결 관리에 영향을 줍니다.

---

### Q2: API 응답 시간 목표
REST API의 평균 응답 시간 목표는 얼마인가요?

A) **매우 빠름** - 100ms 이내
B) **빠름** - 500ms 이내
C) **보통** - 1초 이내
D) **느림** - 3초 이내 (기존 NFR-1)

[Answer]: C

**Reasoning**: 응답 시간 목표는 데이터베이스 최적화, 캐싱 전략, 인덱스 설계에 영향을 줍니다.

---

### Q3: 데이터베이스 선택 재검토
H2 In-Memory DB를 사용하기로 했는데, 이것이 적절한가요?

A) **H2 In-Memory 유지** - 개발/테스트 환경, 데이터 영속성 불필요
B) **H2 File-based** - 데이터 영속성 필요, 단순한 파일 저장
C) **MySQL/PostgreSQL** - 프로덕션 환경, 데이터 영속성 및 확장성 필요
D) **혼합** - 개발은 H2, 프로덕션은 MySQL/PostgreSQL

[Answer]: A

**Reasoning**: 데이터베이스 선택은 데이터 영속성, 성능, 확장성에 영향을 줍니다.

---

### Q4: 캐싱 전략
자주 조회되는 데이터(메뉴, 매장 정보)에 캐싱을 적용할까요?

A) **캐싱 없음** - 단순성 우선, 항상 DB 조회
B) **애플리케이션 캐시** - Spring Cache (Caffeine) 사용
C) **분산 캐시** - Redis 사용 (다중 서버 환경)
D) **HTTP 캐시** - ETag, Cache-Control 헤더 사용

[Answer]: B

**Reasoning**: 캐싱 전략은 성능과 데이터 일관성에 영향을 줍니다.

---

### Q5: 로깅 레벨 및 전략
애플리케이션 로깅을 어떻게 설정할까요?

A) **최소 로깅** - ERROR만 로깅
B) **표준 로깅** - INFO, WARN, ERROR 로깅
C) **상세 로깅** - DEBUG 포함, 모든 요청/응답 로깅
D) **구조화 로깅** - JSON 형식, 중앙 집중식 로그 수집 (ELK, CloudWatch)

[Answer]: B

**Reasoning**: 로깅 전략은 디버깅, 모니터링, 성능에 영향을 줍니다.

---

### Q6: 모니터링 및 알림
시스템 모니터링을 어떻게 구성할까요?

A) **모니터링 없음** - 개발 환경, 수동 확인
B) **기본 모니터링** - Spring Boot Actuator (health, metrics)
C) **고급 모니터링** - Prometheus + Grafana
D) **클라우드 모니터링** - AWS CloudWatch, Azure Monitor

[Answer]: A

**Reasoning**: 모니터링 전략은 장애 감지, 성능 분석, 운영 효율성에 영향을 줍니다.

---

### Q7: 에러 처리 및 재시도 전략
외부 시스템 호출(파일 저장, SSE 전송) 실패 시 어떻게 처리할까요?

A) **즉시 실패** - 재시도 없음, 에러 반환
B) **단순 재시도** - 고정 간격으로 3회 재시도
C) **지수 백오프** - 재시도 간격을 점진적으로 증가 (1초, 2초, 4초)
D) **Circuit Breaker** - 연속 실패 시 일시적으로 호출 중단

[Answer]: B

**Reasoning**: 재시도 전략은 시스템 안정성과 사용자 경험에 영향을 줍니다.

---

### Q8: 데이터베이스 연결 풀 크기
데이터베이스 연결 풀을 어떻게 설정할까요?

A) **최소** - 5개 연결 (소규모 환경)
B) **표준** - 10개 연결 (중규모 환경)
C) **대규모** - 20개 이상 연결 (대규모 환경)
D) **동적** - HikariCP 기본 설정 사용 (자동 조정)

[Answer]: B

**Reasoning**: 연결 풀 크기는 동시 요청 처리 능력과 리소스 사용에 영향을 줍니다.

---

### Q9: SSE 연결 타임아웃
SSE 연결의 타임아웃을 어떻게 설정할까요?

A) **짧음** - 30초 (빠른 재연결)
B) **보통** - 5분 (균형)
C) **길음** - 30분 (연결 유지 우선)
D) **무제한** - 타임아웃 없음 (클라이언트가 연결 유지)

[Answer]: A

**Reasoning**: SSE 타임아웃은 서버 리소스와 실시간성에 영향을 줍니다.

---

### Q10: 파일 저장소 전략
메뉴 이미지 파일을 어디에 저장할까요?

A) **로컬 파일 시스템** - uploads/ 디렉토리
B) **네트워크 스토리지** - NFS, SMB
C) **클라우드 스토리지** - AWS S3, Azure Blob Storage
D) **CDN** - CloudFront, Cloudflare (정적 파일 배포)

[Answer]: A

**Reasoning**: 파일 저장소 선택은 확장성, 가용성, 비용에 영향을 줍니다.

---

### Q11: 트랜잭션 격리 수준
데이터베이스 트랜잭션 격리 수준을 어떻게 설정할까요?

A) **READ_UNCOMMITTED** - 가장 낮은 격리, 최고 성능
B) **READ_COMMITTED** - 커밋된 데이터만 읽기 (기본값)
C) **REPEATABLE_READ** - 반복 읽기 보장
D) **SERIALIZABLE** - 가장 높은 격리, 최저 성능

[Answer]: B

**Reasoning**: 격리 수준은 데이터 일관성과 성능 간 트레이드오프에 영향을 줍니다.

---

### Q12: API 문서화 전략
REST API 문서를 어떻게 생성하고 관리할까요?

A) **문서 없음** - 코드만 참조
B) **수동 문서** - Markdown 파일로 작성
C) **Swagger/OpenAPI** - 자동 생성 및 UI 제공 (기존 요구사항)
D) **Postman Collection** - Postman으로 API 테스트 및 문서화

[Answer]: C

**Reasoning**: API 문서화는 개발 효율성과 협업에 영향을 줍니다.

---

### Q13: 보안 헤더 설정
HTTP 보안 헤더를 어떻게 설정할까요?

A) **기본 설정** - Spring Security 기본값 사용
B) **강화 설정** - HSTS, CSP, X-Frame-Options 등 추가
C) **최소 설정** - CORS만 설정
D) **설정 없음** - 개발 환경, 보안 헤더 불필요

[Answer]: C

**Reasoning**: 보안 헤더는 웹 애플리케이션 보안에 영향을 줍니다.

---

### Q14: 데이터 백업 전략
데이터 백업을 어떻게 수행할까요?

A) **백업 없음** - In-Memory DB, 데이터 영속성 불필요
B) **수동 백업** - 필요 시 수동으로 데이터 내보내기
C) **자동 백업** - 일일 자동 백업 (파일 또는 DB 덤프)
D) **실시간 복제** - 마스터-슬레이브 복제

[Answer]: B

**Reasoning**: 백업 전략은 데이터 손실 방지와 복구 능력에 영향을 줍니다.

---

### Q15: 배포 전략
애플리케이션을 어떻게 배포할까요?

A) **수동 배포** - JAR 파일 직접 실행
B) **스크립트 배포** - Shell 스크립트로 자동화
C) **컨테이너 배포** - Docker 이미지로 배포
D) **CI/CD 파이프라인** - GitHub Actions, Jenkins 등

[Answer]: D

**Reasoning**: 배포 전략은 운영 효율성과 안정성에 영향을 줍니다.

---

## Mandatory NFR Artifacts

### 1. nfr-requirements.md
- [x] 성능 요구사항 (응답 시간, 처리량)
- [x] 확장성 요구사항 (동시 사용자, 데이터 증가)
- [x] 가용성 요구사항 (업타임, 복구 시간)
- [x] 보안 요구사항 (인증, 암호화, 감사)
- [x] 신뢰성 요구사항 (에러 처리, 재시도)
- [x] 유지보수성 요구사항 (로깅, 모니터링)

### 2. tech-stack-decisions.md
- [x] 데이터베이스 선택 및 근거
- [x] 캐싱 전략 및 도구
- [x] 로깅 및 모니터링 도구
- [x] 파일 저장소 선택
- [x] 배포 전략 및 도구
- [x] 보안 설정 및 도구

---

## Next Steps After Plan Approval

1. 사용자가 모든 [Answer]: 태그를 채움
2. AI가 답변을 분석하고 모호한 부분 확인
3. 필요시 추가 질문으로 명확화
4. 사용자가 계획 승인
5. 승인된 계획에 따라 NFR Requirements 아티팩트 생성 시작

---

**참고**: 이 계획은 사용자의 답변에 따라 조정될 수 있습니다. 모든 질문에 답변해주시면 최적의 NFR Requirements를 생성할 수 있습니다.

