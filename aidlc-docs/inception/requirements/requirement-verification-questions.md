# Requirements Verification Questions

요구사항을 명확히 하기 위해 다음 질문에 답변해주세요. 각 질문의 [Answer]: 태그 뒤에 선택한 옵션의 문자를 입력해주세요.

---

## Question 1
테이블오더 서비스의 배포 환경은 어떻게 되나요?

A) 클라우드 환경 (AWS, Azure, GCP 등)
B) 온프레미스 서버
C) 하이브리드 (클라우드 + 온프레미스)
D) 로컬 개발 환경만 (배포 계획 없음)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Question 2
백엔드 API 서버의 기술 스택 선호도가 있나요?

A) Node.js (Express, NestJS 등)
B) Python (FastAPI, Django, Flask 등)
C) Java (Spring Boot 등)
D) Go
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 3
프론트엔드 프레임워크 선호도가 있나요?

A) React
B) Vue.js
C) Angular
D) Vanilla JavaScript (프레임워크 없음)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 4
데이터베이스 기술 선호도가 있나요?

A) 관계형 데이터베이스 (PostgreSQL, MySQL 등)
B) NoSQL 문서 데이터베이스 (MongoDB, DynamoDB 등)
C) NoSQL 키-값 데이터베이스 (Redis 등)
D) 인메모리 데이터베이스 (개발용)
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Question 5
실시간 주문 모니터링을 위한 Server-Sent Events (SSE) 구현 시, 대체 기술 고려가 필요한가요?

A) SSE만 사용 (요구사항대로)
B) WebSocket도 고려
C) 폴링(Polling) 방식도 고려
D) 실시간 업데이트 불필요 (수동 새로고침)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 6
테이블 태블릿의 자동 로그인 정보 저장 방식은?

A) LocalStorage
B) SessionStorage
C) Cookie
D) IndexedDB
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 7
관리자 인증의 JWT 토큰 저장 방식은?

A) LocalStorage
B) SessionStorage
C) HttpOnly Cookie
D) Memory only (새로고침 시 재로그인)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 8
메뉴 이미지는 어떻게 관리하나요?

A) 외부 URL만 저장 (이미지는 외부 호스팅)
B) 서버에 업로드 및 저장
C) 클라우드 스토리지 (S3, Cloud Storage 등)
D) 이미지 기능 제외
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 9
비밀번호 해싱 알고리즘 선호도가 있나요?

A) bcrypt (요구사항에 명시됨)
B) Argon2
C) PBKDF2
D) 간단한 해싱 (개발용)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
매장 식별자(Store ID)의 형식은?

A) 숫자 ID (1, 2, 3...)
B) UUID
C) 사람이 읽을 수 있는 코드 (store-001, cafe-gangnam 등)
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 11
테이블 번호의 형식은?

A) 숫자만 (1, 2, 3...)
B) 문자 포함 가능 (A1, B2, VIP-1 등)
C) 아직 결정 안 됨
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 12
주문 상태 변경 권한은?

A) 관리자만 변경 가능
B) 고객도 일부 변경 가능 (예: 취소)
C) 자동으로만 변경 (시간 기반)
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 13
과거 주문 내역의 보관 기간은?

A) 영구 보관
B) 일정 기간 후 삭제 (예: 1년)
C) 아직 결정 안 됨
D) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 14
동시 접속 예상 규모는? (매장당)

A) 소규모 (10개 테이블 미만)
B) 중규모 (10-50개 테이블)
C) 대규모 (50개 테이블 이상)
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 15
API 문서화 도구 선호도가 있나요?

A) Swagger/OpenAPI
B) Postman Collection
C) 수동 문서 (Markdown)
D) 문서화 불필요
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 16
에러 처리 및 로깅 수준은?

A) 기본 콘솔 로그만
B) 파일 기반 로깅
C) 중앙 집중식 로깅 시스템 (ELK, CloudWatch 등)
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 17
개발 환경 설정 방식은?

A) Docker Compose
B) 로컬 설치 (각자 설치)
C) 클라우드 개발 환경
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 18
테스트 커버리지 목표는?

A) 단위 테스트만 (핵심 로직)
B) 단위 + 통합 테스트
C) 단위 + 통합 + E2E 테스트
D) 테스트 작성 안 함
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 19
코드 스타일 및 린팅 도구 사용 여부는?

A) ESLint/Prettier (JavaScript/TypeScript)
B) 언어별 표준 린터 사용
C) 린팅 도구 사용 안 함
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 20
버전 관리 브랜치 전략은?

A) Git Flow
B) GitHub Flow (main + feature branches)
C) Trunk-based development
D) 아직 결정 안 됨
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

**답변 완료 후 "완료했습니다" 또는 "done"이라고 알려주세요.**
