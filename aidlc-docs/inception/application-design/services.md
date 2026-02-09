# Services - 테이블오더 서비스

## Overview
서비스 계층의 정의와 오케스트레이션 패턴을 설명합니다. 서비스는 비즈니스 로직을 캡슐화하고 컴포넌트 간 조정을 담당합니다.

---

## 1. Backend Services (Spring Boot)

### 1.1 OrderService

#### 책임
- 주문 생성 및 관리
- 주문 상태 변경
- 주문 검증 및 비즈니스 규칙 적용
- 주문 이력 관리

#### 주요 기능
1. **주문 생성 오케스트레이션**
   - 주문 검증 (메뉴 존재, 테이블 세션 유효성)
   - 주문 항목 생성
   - 총 금액 계산
   - 주문 저장
   - SSE 이벤트 발송 (관리자에게 신규 주문 알림)

2. **주문 상태 변경 오케스트레이션**
   - 상태 변경 검증
   - 상태 업데이트
   - SSE 이벤트 발송 (고객에게 상태 변경 알림)

3. **주문 삭제 오케스트레이션**
   - 주문 존재 확인
   - 주문 항목 삭제
   - 주문 삭제
   - 테이블 총 주문액 재계산

#### 의존성
- `OrderMapper`: 데이터 액세스
- `MenuService`: 메뉴 정보 조회
- `TableService`: 테이블 및 세션 검증
- `SSEService`: 실시간 이벤트 전송

#### 트랜잭션 경계
- `createOrder`: 주문 생성 전체 과정
- `updateOrderStatus`: 상태 변경
- `deleteOrder`: 주문 삭제

---

### 1.2 MenuService

#### 책임
- 메뉴 CRUD 관리
- 메뉴 검증
- 이미지 업로드 조정
- 메뉴 순서 관리

#### 주요 기능
1. **메뉴 등록 오케스트레이션**
   - 메뉴 정보 검증 (필수 필드, 가격 범위)
   - 이미지 업로드 (FileService 호출)
   - 메뉴 저장
   - 캐시 무효화 (필요시)

2. **메뉴 수정 오케스트레이션**
   - 메뉴 존재 확인
   - 메뉴 정보 검증
   - 이미지 업로드 (변경 시)
   - 기존 이미지 삭제 (변경 시)
   - 메뉴 업데이트

3. **메뉴 삭제 오케스트레이션**
   - 메뉴 존재 확인
   - 활성 주문에 사용 중인지 확인
   - 이미지 파일 삭제
   - 메뉴 삭제

#### 의존성
- `MenuMapper`: 데이터 액세스
- `FileService`: 파일 업로드/삭제
- `OrderService`: 메뉴 사용 여부 확인

#### 트랜잭션 경계
- `createMenu`: 메뉴 등록 전체 과정
- `updateMenu`: 메뉴 수정 전체 과정
- `deleteMenu`: 메뉴 삭제 전체 과정

---

### 1.3 TableService

#### 책임
- 테이블 관리
- 세션 라이프사이클 관리
- 테이블 초기 설정
- 세션 검증

#### 주요 기능
1. **테이블 초기 설정 오케스트레이션**
   - 테이블 정보 검증
   - PIN 생성 및 해싱
   - 세션 ID 생성
   - 테이블 저장

2. **세션 시작 오케스트레이션**
   - 새로운 세션 ID 생성
   - 테이블 세션 상태 업데이트
   - 세션 시작 시각 기록

3. **세션 종료 오케스트레이션**
   - 현재 주문 내역 조회
   - 주문 이력으로 이동 (OrderHistoryMapper)
   - 테이블 초기화 (주문 목록, 총 주문액 0)
   - 세션 상태 업데이트

#### 의존성
- `TableMapper`: 데이터 액세스
- `OrderMapper`: 주문 조회
- `OrderHistoryMapper`: 주문 이력 저장

#### 트랜잭션 경계
- `setupTable`: 테이블 초기 설정
- `startSession`: 세션 시작
- `endSession`: 세션 종료 전체 과정

---

### 1.4 AuthService

#### 책임
- 사용자 인증
- JWT 토큰 관리
- 비밀번호 해싱 및 검증
- 로그인 시도 제한

#### 주요 기능
1. **로그인 오케스트레이션**
   - 사용자 조회
   - 비밀번호 검증
   - 로그인 시도 횟수 확인
   - JWT 토큰 생성
   - 로그인 성공 기록

2. **토큰 검증 오케스트레이션**
   - 토큰 파싱
   - 토큰 만료 확인
   - 사용자 정보 추출

3. **비밀번호 관리**
   - bcrypt 해싱
   - 비밀번호 검증

#### 의존성
- `UserMapper`: 사용자 데이터 액세스
- `JwtTokenProvider`: JWT 토큰 생성/검증

#### 트랜잭션 경계
- `authenticate`: 로그인 전체 과정

---

### 1.5 SSEService

#### 책임
- SSE 연결 관리
- 실시간 이벤트 전송
- 클라이언트 연결 상태 관리
- 타임아웃 및 재연결 처리

#### 주요 기능
1. **연결 관리**
   - 클라이언트 연결 등록 (clientId → SseEmitter 매핑)
   - 연결 해제 처리
   - 타임아웃 처리
   - 연결 상태 모니터링

2. **이벤트 전송 오케스트레이션**
   - 특정 클라이언트에게 이벤트 전송
   - 매장별 브로드캐스트
   - 전체 브로드캐스트
   - 이벤트 직렬화

3. **에러 처리**
   - 전송 실패 시 재시도
   - 연결 끊김 감지
   - 자동 재연결 지원

#### 의존성
- 없음 (독립적인 서비스)

#### 이벤트 타입
- `NEW_ORDER`: 신규 주문 생성
- `ORDER_STATUS_CHANGED`: 주문 상태 변경
- `ORDER_DELETED`: 주문 삭제
- `SESSION_ENDED`: 세션 종료

---

### 1.6 FileService

#### 책임
- 파일 업로드 처리
- 파일 저장 및 삭제
- 파일 검증
- 파일 경로 관리

#### 주요 기능
1. **파일 업로드 오케스트레이션**
   - 파일 검증 (형식: JPG/PNG, 크기: 최대 5MB)
   - 파일명 생성 (UUID + 확장자)
   - 파일 저장 (로컬 디렉토리)
   - 파일 경로 반환

2. **파일 삭제 오케스트레이션**
   - 파일 존재 확인
   - 파일 삭제
   - 에러 처리

3. **파일 검증**
   - MIME 타입 확인
   - 파일 크기 확인
   - 파일 확장자 확인

#### 의존성
- `FileStorageConfig`: 파일 저장 경로 설정

#### 설정
- 업로드 디렉토리: `uploads/menus/`
- 최대 파일 크기: 5MB
- 허용 형식: JPG, PNG

---

## 2. Frontend Services (React)

### 2.1 ApiClient Service

#### 책임
- HTTP 요청 처리
- 요청/응답 인터셉터
- 에러 처리
- 토큰 관리

#### 주요 기능
1. **요청 인터셉터**
   - Authorization 헤더 추가 (JWT 토큰)
   - Content-Type 설정
   - 요청 로깅 (개발 환경)

2. **응답 인터셉터**
   - 응답 데이터 추출
   - 에러 응답 처리
   - 토큰 만료 시 자동 갱신

3. **에러 처리**
   - 네트워크 에러
   - 서버 에러 (5xx)
   - 클라이언트 에러 (4xx)
   - 타임아웃

#### 설정
- Base URL: `/api`
- Timeout: 10초
- Retry: 3회 (네트워크 에러 시)

---

### 2.2 SSEClient Service

#### 책임
- SSE 연결 관리
- 이벤트 리스너 등록
- 재연결 로직
- 연결 상태 관리

#### 주요 기능
1. **연결 관리**
   - EventSource 생성
   - 연결 상태 모니터링
   - 자동 재연결 (3회 시도)
   - 연결 해제

2. **이벤트 처리**
   - 이벤트 리스너 등록/제거
   - 이벤트 파싱
   - 이벤트 핸들러 호출

3. **에러 처리**
   - 연결 실패 처리
   - 재연결 로직
   - 타임아웃 처리

#### 설정
- 재연결 간격: 3초
- 최대 재연결 시도: 3회
- 타임아웃: 30초

---

## 3. Service Orchestration Patterns

### 3.1 주문 생성 플로우

```
Customer → OrderService.createOrder()
  ├─> MenuService.getMenuById() (메뉴 검증)
  ├─> TableService.validateSession() (세션 검증)
  ├─> OrderMapper.insertOrder() (주문 저장)
  ├─> OrderMapper.insertOrderItems() (주문 항목 저장)
  └─> SSEService.broadcastEventToStore() (신규 주문 알림)
```

### 3.2 주문 상태 변경 플로우

```
Admin → OrderService.updateOrderStatus()
  ├─> OrderMapper.selectOrderById() (주문 조회)
  ├─> OrderMapper.updateOrderStatus() (상태 업데이트)
  └─> SSEService.sendEvent() (고객에게 상태 변경 알림)
```

### 3.3 메뉴 등록 플로우

```
Admin → MenuService.createMenu()
  ├─> FileService.saveFile() (이미지 업로드)
  ├─> MenuMapper.insertMenu() (메뉴 저장)
  └─> SSEService.broadcastEventToStore() (메뉴 변경 알림, 선택적)
```

### 3.4 세션 종료 플로우

```
Admin → TableService.endSession()
  ├─> OrderMapper.selectOrdersByTableAndSession() (현재 주문 조회)
  ├─> OrderHistoryMapper.insertOrderHistory() (이력 저장)
  ├─> TableMapper.updateSessionStatus() (세션 상태 업데이트)
  └─> SSEService.sendEvent() (세션 종료 알림, 선택적)
```

---

## 4. Service Communication Patterns

### 4.1 동기 통신
- **REST API**: Controller ↔ Service ↔ Repository
- **직접 호출**: Service ↔ Service (같은 트랜잭션 내)

### 4.2 비동기 통신
- **SSE**: Backend → Frontend (실시간 이벤트)
- **이벤트 기반**: Service → SSEService (이벤트 발행)

### 4.3 데이터 흐름
```
Frontend (React)
  ↓ HTTP Request (Axios)
Backend Controller
  ↓ Method Call
Backend Service
  ↓ Method Call
Backend Repository (MyBatis)
  ↓ SQL Query
Database (H2)
  ↑ Result Set
Backend Repository
  ↑ Domain Object
Backend Service
  ↑ DTO
Backend Controller
  ↑ HTTP Response (JSON)
Frontend (React)
```

---

## 5. Service Layer Best Practices

### 5.1 트랜잭션 관리
- Service 레이어에서 `@Transactional` 사용
- 읽기 전용 트랜잭션: `@Transactional(readOnly = true)`
- 트랜잭션 경계는 비즈니스 로직 단위

### 5.2 에러 처리
- Service에서 비즈니스 예외 발생
- Controller에서 HTTP 상태 코드 매핑
- GlobalExceptionHandler에서 일관된 에러 응답

### 5.3 검증
- Service 레이어에서 비즈니스 규칙 검증
- Controller에서 입력 데이터 검증 (`@Valid`)
- 검증 실패 시 명확한 예외 메시지

### 5.4 로깅
- Service 메서드 시작/종료 로깅
- 에러 발생 시 상세 로깅
- 성능 모니터링 (실행 시간)

---

## 6. Service Dependencies Summary

### OrderService
- **의존**: MenuService, TableService, SSEService, OrderMapper
- **의존됨**: CustomerController, AdminController

### MenuService
- **의존**: FileService, MenuMapper
- **의존됨**: CustomerController, AdminController, OrderService

### TableService
- **의존**: OrderMapper, OrderHistoryMapper, TableMapper
- **의존됨**: AdminController, OrderService

### AuthService
- **의존**: UserMapper, JwtTokenProvider
- **의존됨**: AuthController, JwtAuthenticationFilter

### SSEService
- **의존**: 없음
- **의존됨**: OrderService, MenuService, TableService

### FileService
- **의존**: FileStorageConfig
- **의존됨**: MenuService

---

## Notes

- 서비스 레이어는 비즈니스 로직의 중심
- 트랜잭션 경계는 서비스 메서드 단위
- 서비스 간 의존성은 최소화
- 순환 의존성 방지
- 상세한 비즈니스 규칙은 Functional Design에서 정의
