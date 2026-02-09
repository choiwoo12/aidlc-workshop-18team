# 요구사항 검증 질문

요구사항 문서를 검토한 결과, 몇 가지 기술적 세부사항과 구현 방향에 대한 명확화가 필요합니다. 각 질문에 대해 [Answer]: 태그 뒤에 선택한 옵션의 문자(A, B, C 등)를 입력해주세요.

---

## Question 1
**백엔드 기술 스택**: 어떤 백엔드 프레임워크/언어를 사용하시겠습니까?

A) Node.js (Express/NestJS)
B) Python (Django/FastAPI/Flask)
C) Java (Spring Boot)
D) Go
E) Other (please describe after [Answer]: tag below)

[Answer]: C

---

## Question 2
**프론트엔드 기술 스택**: 고객용 및 관리자용 웹 인터페이스에 어떤 프레임워크를 사용하시겠습니까?

A) React
B) Vue.js
C) Angular
D) Vanilla JavaScript (프레임워크 없음)
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 3
**데이터베이스 선택**: 어떤 데이터베이스를 사용하시겠습니까?

A) PostgreSQL
B) MySQL
C) SQLite
D) MongoDB
E) Other (please describe after [Answer]: tag below)

[Answer]: in-memory DB

---

## Question 4
**배포 환경**: 애플리케이션을 어디에 배포하실 계획입니까?

A) AWS (EC2, RDS, S3 등)
B) 로컬 서버 (On-premises)
C) Docker 컨테이너
D) 클라우드 플랫폼 (Heroku, Vercel, Netlify 등)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 5
**메뉴 이미지 저장**: 메뉴 이미지를 어떻게 관리하시겠습니까?

A) 외부 URL 링크만 저장 (이미지는 외부 호스팅)
B) 서버에 파일 업로드 및 저장
C) 클라우드 스토리지 (S3, Cloud Storage 등)
D) 이미지 기능 제외 (텍스트만)
E) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Question 6
**테이블 수**: 매장당 예상되는 테이블 수는 얼마입니까?

A) 10개 이하
B) 11-30개
C) 31-50개
D) 51개 이상
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 7
**다중 매장 지원**: 초기 버전에서 여러 매장을 지원해야 합니까?

A) 단일 매장만 지원 (매장 ID는 하드코딩 또는 설정 파일)
B) 다중 매장 지원 (각 매장이 독립적으로 운영)
C) 다중 매장 지원 (중앙 관리 시스템)
D) Other (please describe after [Answer]: tag below)

[Answer]: C ]

---

## Question 8
**주문 상태 업데이트**: 고객 화면에서 주문 상태를 실시간으로 업데이트해야 합니까?

A) 필수 기능 (SSE 또는 WebSocket 사용)
B) 선택 기능 (나중에 추가 가능)
C) 불필요 (고객은 주문 후 상태 확인 안 함)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 9
**메뉴 관리 우선순위**: 메뉴 관리 기능(등록/수정/삭제)의 우선순위는?

A) MVP 필수 기능 (초기 버전에 포함)
B) MVP 이후 추가 (초기에는 데이터베이스 직접 입력)
C) 관리자 UI 대신 API만 제공
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 10
**인증 보안 수준**: 테이블 태블릿 인증의 보안 수준은?

A) 간단한 비밀번호 (4자리 PIN)
B) 복잡한 비밀번호 (영문+숫자+특수문자)
C) 비밀번호 없음 (테이블 번호만)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 11
**주문 삭제 권한**: 관리자가 주문을 삭제할 수 있는 조건은?

A) 모든 주문 삭제 가능 (제한 없음) 
B) 대기중 상태의 주문만 삭제 가능
C) 완료되지 않은 주문만 삭제 가능 (대기중/준비중)
D) Other (please describe after [Answer]: tag below)

[Answer]: A, 상태변경에 취소도 추가 됐으면 함

---

## Question 12
**과거 주문 내역 보관 기간**: 과거 주문 내역을 얼마나 보관하시겠습니까?

A) 영구 보관
B) 30일
C) 90일
D) 1년
E) Other (please describe after [Answer]: tag below)

[Answer]: D

---

## Question 13
**에러 로깅**: 시스템 에러 및 로그를 어떻게 관리하시겠습니까?

A) 콘솔 로그만 (개발 환경)
B) 파일 로그 (서버에 저장)
C) 외부 로깅 서비스 (CloudWatch, Sentry 등)
D) 로깅 불필요
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 14
**API 문서화**: API 문서를 자동 생성하시겠습니까?

A) Swagger/OpenAPI 사용
B) 수동 문서 작성 (Markdown)
C) 문서 불필요 (코드 주석만)
D) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Question 15
**테스트 코드**: 테스트 코드 작성 범위는?

A) Unit 테스트 + Integration 테스트
B) Unit 테스트만
C) Integration 테스트만
D) 테스트 코드 불필요
E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

**작성 완료 후 "완료" 또는 "done"이라고 알려주세요.**
