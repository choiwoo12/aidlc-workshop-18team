# NFR Requirements - Unit 2: Customer Order Domain

## Overview

Unit 2 (Customer Order Domain)의 비기능 요구사항(NFR) 정의입니다. Unit 1의 기술 스택을 상속하고 Unit 2 특화 요구사항을 추가합니다.

---

## Inherited from Unit 1

### Base Technology Stack
- Backend Framework: FastAPI
- Database: SQLite (파일 기반)
- ORM: SQLAlchemy 2.0+
- Frontend Framework: React 18.2+
- Build Tool: Vite 5.0+
- Styling: Tailwind CSS 3.4+
- HTTP Client: Axios 1.6+
- State Management: React Context API
- Authentication: JWT (HS256)
- Password Hashing: bcrypt
- Logging: Python 내장 logging (파일 기반)

---

## Unit 2 Specific NFR Requirements

### NFR-U2-001: Real-time Communication (실시간 통신)

**Category**: Performance & Reliability

**Requirement**: SSE를 통한 실시간 주문 상태 업데이트

**Specifications**:
- **Technology**: Server-Sent Events (SSE)
- **Connection Management**: 자동 재연결 (최대 3회)
- **Keep-alive Interval**: 30초
- **Timeout**: 60초
- **Reconnection Strategy**:
  - 1차 재연결: 즉시
  - 2차 재연결: 5초 후
  - 3차 재연결: 10초 후
  - 3회 실패 시: 에러 메시지 표시

**Rationale**:
- SSE는 단방향 통신으로 주문 상태 업데이트에 적합
- 자동 재연결로 사용자 편의성 향상
- 30초 Keep-alive로 연결 유지 및 서버 부하 균형

**Acceptance Criteria**:
- SSE 연결 설정 시간 < 1초
- 주문 상태 변경 이벤트 전송 지연 < 2초
- 연결 끊김 시 자동 재연결 성공률 > 95%

---

### NFR-U2-002: Menu Query Performance (메뉴 조회 성능)

**Category**: Performance

**Requirement**: 메뉴 조회 API 응답 시간 목표

**Specifications**:
- **Response Time Target**: 1초 이내
- **Caching Strategy**: 캐싱 없음 (항상 최신 데이터)
- **Database Query Optimization**:
  - 인덱스 활용 (store_id, is_available)
  - 필요한 컬럼만 조회
- **Filtering**: 판매 가능 메뉴만 반환 (is_available = true)

**Rationale**:
- 메뉴 변경이 즉시 반영되어야 함
- 소규모 매장(10개 테이블 미만)으로 캐싱 불필요
- 1초 응답 시간으로 사용자 경험 보장

**Acceptance Criteria**:
- 메뉴 조회 API 응답 시간 < 1초 (95th percentile)
- 동시 10개 요청 처리 가능

---

### NFR-U2-003: Order Creation Performance (주문 생성 성능)

**Category**: Performance

**Requirement**: 주문 생성 API 응답 시간 목표

**Specifications**:
- **Response Time Target**: 2초 이내
- **Transaction Management**: 단일 트랜잭션으로 Order + OrderItem 생성
- **Validation**: 서버 측 상세 검증 (메뉴 판매 가능, 가격 일치, 옵션 유효성)
- **Concurrent Processing**: 5개 테이블 동시 주문 처리 가능

**Rationale**:
- 2초 응답 시간으로 사용자 대기 시간 최소화
- 서버 측 검증으로 데이터 무결성 보장
- 소규모 매장 요구사항 충족

**Acceptance Criteria**:
- 주문 생성 API 응답 시간 < 2초 (95th percentile)
- 동시 5개 주문 생성 시 응답 시간 < 3초
- 주문 생성 성공률 > 99%

---

### NFR-U2-004: Cart Management (장바구니 관리)

**Category**: Data Management & Performance

**Requirement**: 장바구니 상태 관리 및 영속성

**Specifications**:
- **Storage**: SessionStorage (클라이언트 측)
- **Synchronization**: 동기화 없음 (주문 생성 시에만 서버 전송)
- **Max Items**: 제한 없음
- **Data Structure**:
  ```json
  {
    "cart_items": [
      {
        "cart_item_id": "uuid",
        "menu_id": 1,
        "menu_snapshot": {...},
        "selected_options": [...],
        "quantity": 2,
        "subtotal": 7000
      }
    ],
    "total_amount": 7000
  }
  ```
- **Persistence**: 브라우저 탭 닫기 시 삭제, 새로고침 시 복원

**Rationale**:
- SessionStorage로 단순하고 빠른 구현
- 서버 저장 불필요 (주문 생성 시에만 전송)
- 제한 없음으로 사용자 자유도 보장

**Acceptance Criteria**:
- 장바구니 추가/수정/삭제 응답 시간 < 100ms
- 페이지 새로고침 시 장바구니 복원 성공률 100%
- 장바구니 데이터 크기 < 1MB

---

### NFR-U2-005: Image Handling (이미지 처리)

**Category**: Performance & Storage

**Requirement**: 메뉴 이미지 처리 및 최적화

**Specifications**:
- **Optimization**: 최적화 없음 (원본 이미지 사용)
- **Storage**: 로컬 파일 시스템 (Unit 1 상속)
- **Max File Size**: 5MB (Unit 1 상속)
- **Allowed Formats**: image/* (Unit 1 상속)
- **Delivery**: 직접 파일 서빙

**Rationale**:
- MVP 범위에서 이미지 최적화 불필요
- 소규모 매장으로 이미지 개수 제한적
- 단순한 구현으로 개발 시간 단축

**Acceptance Criteria**:
- 이미지 업로드 시간 < 3초 (5MB 기준)
- 이미지 로딩 시간 < 2초 (3G 네트워크 기준)

---

### NFR-U2-006: Error Logging (에러 로깅)

**Category**: Maintainability & Reliability

**Requirement**: Unit 2 특화 에러 로깅

**Specifications**:
- **Logging Strategy**: 파일 로깅 (Unit 1 상속)
- **Log Location**: `logs/unit2-{date}.log`
- **Log Format**: 
  ```
  [TIMESTAMP] [LEVEL] [MODULE] [MESSAGE]
  ```
- **Log Levels**:
  - ERROR: 주문 생성 실패, SSE 연결 실패
  - WARNING: 재연결 시도, 유효성 검증 실패
  - INFO: 주문 생성 성공, 메뉴 조회
  - DEBUG: 상세 디버그 정보
- **Rotation**: 30일 후 자동 삭제 (Unit 1 상속)

**Rationale**:
- 파일 로깅으로 영구 기록 보장
- 에러 추적 및 디버깅 용이
- Unit 1과 일관된 로깅 전략

**Acceptance Criteria**:
- 모든 에러 로깅 성공률 100%
- 로그 파일 크기 < 100MB/일

---

### NFR-U2-007: Concurrent User Support (동시 사용자 지원)

**Category**: Scalability & Performance

**Requirement**: 동시 주문 처리 능력

**Specifications**:
- **Concurrent Orders**: 5개 테이블 동시 주문 처리
- **SSE Connections**: 10개 동시 연결 지원
- **Database Connections**: 최소 10개, 최대 20개 (Unit 1 상속)
- **Request Queue**: FastAPI 기본 큐 사용

**Rationale**:
- 소규모 매장(10개 테이블 미만) 요구사항 충족
- 5개 동시 주문으로 충분한 여유
- 10개 SSE 연결로 모든 테이블 커버

**Acceptance Criteria**:
- 5개 동시 주문 생성 시 모두 2초 이내 응답
- 10개 SSE 연결 유지 시 서버 CPU 사용률 < 50%
- 동시 요청 처리 실패율 < 1%

---

### NFR-U2-008: Data Validation (데이터 유효성 검증)

**Category**: Security & Data Integrity

**Requirement**: 주문 데이터 유효성 검증

**Specifications**:
- **Client-side Validation**:
  - 장바구니 비어있지 않음
  - 필수 옵션 선택 확인
  - 수량 > 0
- **Server-side Validation**:
  - 메뉴 판매 가능 여부 (is_available = true)
  - 메뉴 가격 일치 확인
  - 옵션 유효성 확인 (존재하는 옵션인지)
  - 총액 계산 일치 확인
- **Validation Timing**: 주문 생성 시

**Rationale**:
- 클라이언트 측 최소 검증으로 빠른 피드백
- 서버 측 상세 검증으로 데이터 무결성 보장
- 이중 검증으로 보안 강화

**Acceptance Criteria**:
- 클라이언트 검증 응답 시간 < 100ms
- 서버 검증 실패 시 명확한 에러 메시지 반환
- 유효하지 않은 주문 생성 차단율 100%

---

### NFR-U2-009: Session Management (세션 관리)

**Category**: Security & User Experience

**Requirement**: 테이블 세션 관리

**Specifications**:
- **Session Storage**: SessionStorage (클라이언트 측)
- **Session Duration**: 16시간 (Unit 1 상속)
- **Session Data**:
  ```json
  {
    "table_id": 1,
    "table_number": "01",
    "session_started_at": "2026-02-09T10:00:00Z",
    "token": "jwt_token"
  }
  ```
- **Session Restoration**: 페이지 새로고침 시 자동 복원
- **Session Termination**: 브라우저 탭 닫기 시 자동 종료

**Rationale**:
- SessionStorage로 탭별 독립적인 세션 관리
- 16시간 유효 기간으로 하루 영업 시간 커버
- 자동 복원으로 사용자 편의성 향상

**Acceptance Criteria**:
- 세션 복원 성공률 100%
- 세션 만료 시 자동 로그아웃
- 세션 데이터 크기 < 10KB

---

### NFR-U2-010: Error Handling (에러 처리)

**Category**: User Experience & Reliability

**Requirement**: 사용자 친화적 에러 처리

**Specifications**:
- **Error Message Strategy**: 기본 메시지만 표시
- **Error Types**:
  - Network Error: "주문 생성에 실패했습니다. 다시 시도해주세요."
  - Server Error: "주문 생성에 실패했습니다. 다시 시도해주세요."
  - Validation Error: "주문 생성에 실패했습니다. 다시 시도해주세요."
- **Error Recovery**:
  - 주문 생성 실패: 장바구니 유지
  - 메뉴 조회 실패: 빈 목록 표시
  - SSE 연결 실패: 자동 재연결 (최대 3회)
- **User Action**: 수동 재시도 가능

**Rationale**:
- 단순한 에러 메시지로 구현 복잡도 감소
- 장바구니 유지로 사용자 데이터 보호
- 자동 재연결로 사용자 편의성 향상

**Acceptance Criteria**:
- 모든 에러에 대해 사용자 친화적 메시지 표시
- 에러 발생 시 장바구니 데이터 유지율 100%
- SSE 자동 재연결 성공률 > 95%

---

## Performance Summary

### Response Time Targets
- 메뉴 조회: < 1초 (95th percentile)
- 주문 생성: < 2초 (95th percentile)
- 장바구니 조작: < 100ms
- SSE 연결 설정: < 1초
- SSE 이벤트 전송: < 2초

### Concurrent Processing
- 동시 주문 생성: 5개 테이블
- 동시 SSE 연결: 10개
- 동시 메뉴 조회: 10개 요청

### Resource Limits
- 장바구니 최대 항목: 제한 없음
- 이미지 최대 크기: 5MB
- 로그 파일 최대 크기: 100MB/일
- 세션 데이터 최대 크기: 10KB

---

## Security Requirements

### Inherited from Unit 1
- JWT 토큰 기반 인증
- bcrypt 비밀번호 해싱
- HTTPS 통신 (프로덕션)

### Unit 2 Specific
- 서버 측 주문 데이터 유효성 검증
- 클라이언트 측 입력 검증
- SessionStorage 데이터 보호 (XSS 방지는 Unit 1에서 처리)

---

## Reliability Requirements

### Availability
- 서비스 가용성: 99% (로컬 개발 환경)
- SSE 연결 안정성: 95% (자동 재연결 포함)

### Data Integrity
- 주문 데이터 무결성: 100%
- 장바구니 데이터 복원: 100%
- 메뉴 정보 스냅샷 정확성: 100%

### Error Recovery
- SSE 자동 재연결: 최대 3회
- 주문 생성 실패 시 장바구니 유지: 100%
- 에러 로깅: 100%

---

## Maintainability Requirements

### Code Quality
- 코드 스타일: Python PEP 8, JavaScript Standard
- 린터: Pylint (Backend), ESLint (Frontend)
- 타입 힌트: Python Type Hints 사용

### Documentation
- API 문서: FastAPI 자동 생성 (Swagger)
- 코드 주석: 복잡한 로직에만 추가
- README: 설치 및 실행 가이드

### Testing
- 단위 테스트: Build & Test 단계에서 작성
- 통합 테스트: Build & Test 단계에서 작성

---

## Usability Requirements

### UI/UX
- 터치 친화적 UI: 최소 버튼 크기 44x44px (Unit 1 상속)
- 시각적 피드백: 로딩, 성공, 에러 상태 표시
- 장바구니 아이콘: 항목 개수 배지 표시

### Accessibility
- 명확한 에러 메시지
- 로딩 상태 표시
- 버튼 레이블 명확성

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 초안
