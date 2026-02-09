# Frontend Code Summary - Unit 1: Shared Foundation

## Overview

Unit 1 Frontend 코드 생성 완료. React + Vite 기반 프론트엔드 애플리케이션.

---

## Generated Files

### Configuration & Setup
- `frontend/package.json` - 프로젝트 의존성 및 스크립트
- `frontend/vite.config.js` - Vite 빌드 설정
- `frontend/tailwind.config.js` - Tailwind CSS 설정
- `frontend/postcss.config.js` - PostCSS 설정
- `frontend/Dockerfile` - Docker 이미지 빌드 설정
- `frontend/.env.example` - 환경 변수 템플릿
- `frontend/index.html` - HTML 엔트리 포인트

### Application Entry
- `frontend/src/main.jsx` - React 애플리케이션 엔트리
- `frontend/src/App.jsx` - 메인 애플리케이션 컴포넌트
- `frontend/src/index.css` - 글로벌 스타일 (Tailwind)

### Common UI Components
- `frontend/src/components/common/Button.jsx` - 재사용 가능한 버튼
- `frontend/src/components/common/Input.jsx` - 재사용 가능한 입력 필드
- `frontend/src/components/common/Loading.jsx` - 로딩 스피너
- `frontend/src/components/common/ErrorMessage.jsx` - 에러 메시지 표시
- `frontend/src/components/common/Modal.jsx` - 모달 다이얼로그
- `frontend/src/components/common/ConfirmDialog.jsx` - 확인 다이얼로그

### Pages
- `frontend/src/pages/LoginPage.jsx` - 로그인 페이지 (Admin/Table)

### Context (State Management)
- `frontend/src/contexts/AuthContext.jsx` - 인증 상태 관리 (React Context API)

### Services (API Client)
- `frontend/src/services/AuthService.js` - 인증 API 호출
- `frontend/src/services/StorageService.js` - LocalStorage/SessionStorage 유틸리티
- `frontend/src/services/ValidationService.js` - 입력 검증 유틸리티

### Utilities
- `frontend/src/utils/axios.js` - Axios HTTP 클라이언트 설정 (인터셉터)

---

## Key Features Implemented

### 1. Authentication
- ✅ Admin 로그인 폼 (username + password)
- ✅ Table 로그인 폼 (table number)
- ✅ JWT 토큰 저장 (LocalStorage)
- ✅ 인증 상태 관리 (AuthContext)
- ✅ 자동 로그아웃 (토큰 만료 시)

### 2. Common UI Components
- ✅ Button - 다양한 variant (primary, secondary, danger)
- ✅ Input - 에러 상태 표시, 라벨 지원
- ✅ Loading - 스피너 애니메이션
- ✅ ErrorMessage - 에러 메시지 표시
- ✅ Modal - 오버레이 모달
- ✅ ConfirmDialog - 확인/취소 다이얼로그

### 3. HTTP Client
- ✅ Axios 인스턴스 설정
- ✅ Request 인터셉터 (JWT 토큰 자동 추가)
- ✅ Response 인터셉터 (에러 처리)
- ✅ 401 에러 시 자동 로그아웃

### 4. State Management
- ✅ React Context API (AuthContext)
- ✅ 로그인/로그아웃 상태 관리
- ✅ 사용자 정보 저장
- ✅ 토큰 자동 복원 (새로고침 시)

### 5. Validation
- ✅ 입력 필드 검증 (required, minLength, maxLength)
- ✅ 이메일 형식 검증
- ✅ 비밀번호 강도 검증
- ✅ 실시간 검증 피드백

### 6. Storage
- ✅ LocalStorage 유틸리티 (JWT 토큰)
- ✅ SessionStorage 유틸리티 (임시 데이터)
- ✅ JSON 직렬화/역직렬화
- ✅ 에러 처리

---

## Technology Stack

- **Language**: JavaScript (ES6+)
- **Framework**: React 18.2+
- **Build Tool**: Vite 5.0+
- **Styling**: Tailwind CSS 3.4+
- **HTTP Client**: Axios 1.6+
- **Routing**: React Router DOM 6.21+
- **State Management**: React Context API

---

## Running the Frontend

### Development Mode
```bash
cd frontend
npm install
npm run dev
```

### Docker Mode
```bash
docker-compose up frontend
```

### Build for Production
```bash
npm run build
npm run preview
```

---

## Environment Variables

Required:
- `VITE_API_BASE_URL` - Backend API URL (기본값: http://localhost:8000)

---

## Component Usage Examples

### Button
```jsx
<Button variant="primary" onClick={handleClick}>
  클릭하세요
</Button>
```

### Input
```jsx
<Input
  label="사용자명"
  value={username}
  onChange={(e) => setUsername(e.target.value)}
  error={errors.username}
/>
```

### Loading
```jsx
{isLoading && <Loading />}
```

### ErrorMessage
```jsx
<ErrorMessage message={error} />
```

### Modal
```jsx
<Modal isOpen={isOpen} onClose={handleClose} title="제목">
  <p>모달 내용</p>
</Modal>
```

### ConfirmDialog
```jsx
<ConfirmDialog
  isOpen={isOpen}
  onClose={handleClose}
  onConfirm={handleConfirm}
  title="확인"
  message="정말 삭제하시겠습니까?"
/>
```

---

## AuthContext Usage

### Provider Setup
```jsx
import { AuthProvider } from './contexts/AuthContext';

<AuthProvider>
  <App />
</AuthProvider>
```

### Using Auth State
```jsx
import { useAuth } from './contexts/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, login, logout } = useAuth();
  
  // ...
}
```

---

## API Service Usage

### AuthService
```jsx
import AuthService from './services/AuthService';

// Admin 로그인
const response = await AuthService.adminLogin(username, password);

// Table 로그인
const response = await AuthService.tableLogin(tableNumber);
```

### StorageService
```jsx
import StorageService from './services/StorageService';

// 저장
StorageService.setItem('key', { data: 'value' });

// 조회
const data = StorageService.getItem('key');

// 삭제
StorageService.removeItem('key');
```

### ValidationService
```jsx
import ValidationService from './services/ValidationService';

// 검증
const errors = ValidationService.validate(formData, {
  username: { required: true, minLength: 3 },
  password: { required: true, minLength: 8 }
});
```

---

## Styling Guidelines

### Tailwind CSS Classes
- Primary Color: `bg-blue-600`, `text-blue-600`
- Secondary Color: `bg-gray-600`, `text-gray-600`
- Danger Color: `bg-red-600`, `text-red-600`
- Spacing: `p-4`, `m-4`, `gap-4`
- Responsive: `sm:`, `md:`, `lg:`, `xl:`

### Custom CSS
- 글로벌 스타일: `frontend/src/index.css`
- Tailwind 커스터마이징: `frontend/tailwind.config.js`

---

## Next Steps (Unit 2 & 3)

Unit 1에서 구현한 기반 위에 다음 기능들이 추가될 예정:
- Unit 2: 고객 주문 도메인 (메뉴 조회, 장바구니, 주문 생성)
- Unit 3: 관리자 운영 도메인 (주문 관리, 테이블 관리, 메뉴 관리)

---

**문서 버전**: 1.0  
**작성일**: 2026-02-09  
**상태**: 완료
