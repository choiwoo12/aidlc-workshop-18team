# Customer Frontend - Security Requirements

## Overview
프론트엔드 보안 요구사항. XSS, CSRF 등 웹 공격으로부터 보호.

---

## XSS (Cross-Site Scripting) 방어

### React의 기본 보호
**요구사항**: React의 자동 이스케이프 활용

**방법**:
- JSX에서 자동으로 HTML 이스케이프
- `dangerouslySetInnerHTML` 사용 금지
- 사용자 입력 데이터 검증

**예시**:
```typescript
// ✅ Safe: React가 자동 이스케이프
<div>{userInput}</div>

// ❌ Dangerous: XSS 취약점
<div dangerouslySetInnerHTML={{ __html: userInput }} />
```

---

### Input Validation
**요구사항**: 모든 사용자 입력 검증

**검증 항목**:
- 수량: 1 ~ 99 범위
- 문자열: 특수문자 제한
- 길이: 최대 길이 제한

**구현**:
```typescript
const validateQuantity = (value: number): boolean => {
  return value >= 1 && value <= 99;
};

const sanitizeInput = (input: string): string => {
  return input.replace(/[<>]/g, '');
};
```

---

## CSRF (Cross-Site Request Forgery) 방어

### SameSite Cookie
**요구사항**: Backend에서 SameSite 쿠키 설정

**Backend 설정** (참고):
```java
cookie.setSameSite("Strict");
```

---

### CORS 정책
**요구사항**: 허용된 Origin만 API 접근

**Backend CORS 설정** (참고):
```java
configuration.setAllowedOrigins(Arrays.asList(
  "http://localhost:5173",
  "https://tableorder.com"
));
```

---

## 데이터 보안

### Sensitive Data
**요구사항**: 민감한 데이터 노출 방지

**보호 대상**:
- 세션 ID (localStorage에 저장하지만 암호화 불필요 - 임시 세션)
- API 응답 데이터 (콘솔 로그 제한)

**방법**:
```typescript
// Production 환경에서 로깅 비활성화
if (import.meta.env.PROD) {
  console.log = () => {};
  console.error = () => {};
}
```

---

### localStorage Security
**요구사항**: localStorage 데이터 보호

**저장 데이터**:
- 장바구니 (민감하지 않음)
- 세션 ID (임시 세션, 만료 시간 있음)

**주의사항**:
- 비밀번호, 토큰 등 저장 금지
- XSS 공격 시 localStorage 접근 가능

---

## API 보안

### HTTPS Only
**요구사항**: Production 환경에서 HTTPS 필수

**설정**:
```typescript
const API_URL = import.meta.env.PROD
  ? 'https://api.tableorder.com'
  : 'http://localhost:8080';
```

---

### API Error Handling
**요구사항**: 에러 메시지에 민감한 정보 노출 금지

**방법**:
```typescript
catch (error) {
  // ❌ Bad: 상세 에러 노출
  toast.error(error.response.data.stackTrace);

  // ✅ Good: 일반적인 메시지
  toast.error('요청 처리 중 오류가 발생했습니다');
}
```

---

### Rate Limiting
**요구사항**: API 호출 빈도 제한 (Backend)

**Frontend 대응**:
- 중복 클릭 방지 (debounce)
- 로딩 상태 표시

```typescript
const handleSubmit = debounce(async () => {
  if (isLoading) return;
  await createOrder(request);
}, 1000);
```

---

## 인증 및 권한

### No Authentication Required
**현재 상태**: Customer Frontend는 인증 불필요

**이유**:
- 세션 ID만으로 주문 관리
- 테이블 단위 격리

**향후 고려사항**:
- QR 코드 기반 테이블 인증
- 세션 만료 시간 설정

---

## 의존성 보안

### Dependency Scanning
**요구사항**: 정기적인 의존성 취약점 검사

**도구**:
- `npm audit`
- Dependabot (GitHub)
- Snyk

**실행**:
```bash
npm audit
npm audit fix
```

---

### Package Updates
**요구사항**: 보안 패치 즉시 적용

**방법**:
- 주요 의존성 버전 고정
- 보안 업데이트 자동 알림
- 정기적인 업데이트 (월 1회)

---

## Content Security Policy (CSP)

### CSP Headers
**요구사항**: CSP 헤더 설정 (Backend 또는 CDN)

**정책**:
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.tableorder.com;
```

---

## 클라이언트 사이드 보안

### Clickjacking 방어
**요구사항**: X-Frame-Options 헤더 (Backend)

**Backend 설정** (참고):
```java
headers.frameOptions(frame -> frame.deny());
```

---

### Subresource Integrity (SRI)
**요구사항**: CDN 리소스에 SRI 적용 (선택)

**예시**:
```html
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-..."
  crossorigin="anonymous"
></script>
```

---

## 보안 테스트

### Security Checklist
- [ ] XSS 취약점 테스트
- [ ] CSRF 토큰 검증
- [ ] API 인증 테스트
- [ ] 의존성 취약점 스캔
- [ ] HTTPS 강제 적용
- [ ] CSP 헤더 검증

---

### Penetration Testing
**시나리오**:
1. XSS 공격 시도 (입력 필드)
2. CSRF 공격 시도 (외부 사이트)
3. API 무단 접근 시도

---

## 보안 모니터링

### Error Tracking
**도구**: Sentry (선택)

**수집 정보**:
- JavaScript 에러
- API 에러
- 네트워크 에러

**주의**: 민감한 정보 필터링

---

### Security Logs
**로깅 항목**:
- API 호출 실패
- 비정상적인 요청 패턴
- SSE 연결 실패

---

## 보안 우선순위

### Critical
1. XSS 방어
2. HTTPS 적용
3. 의존성 취약점 제거

### High
1. CSRF 방어
2. API 에러 처리
3. CSP 헤더 설정

### Medium
1. Rate limiting
2. 보안 모니터링
3. 정기적인 보안 감사

---

## Notes

- React는 기본적으로 XSS 방어 제공
- Customer Frontend는 인증 불필요 (세션 기반)
- HTTPS는 Production 환경 필수
- 정기적인 의존성 업데이트 중요
- Backend 보안 설정과 협력 필요
