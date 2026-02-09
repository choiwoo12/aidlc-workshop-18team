# Customer Frontend

테이블오더 서비스 고객용 프론트엔드

## 🚀 Quick Start

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 빌드
npm run build

# 테스트
npm test
```

## 📁 프로젝트 구조

```
src/
├── atoms/              # 기본 컴포넌트 (구현 필요)
├── molecules/          # 조합 컴포넌트 (구현 필요)
├── organisms/          # 복합 컴포넌트 (구현 필요)
├── pages/              # 페이지 컴포넌트 (구현 필요)
├── stores/             # Zustand 스토어
│   └── useCartStore.ts ✅
├── services/           # API 서비스
│   └── apiClient.ts    ✅
├── utils/              # 유틸리티
│   └── storage.ts      ✅
├── types/              # TypeScript 타입
│   └── index.ts        ✅
├── test/               # 테스트 설정
│   └── setup.ts        ✅
├── App.tsx             ✅
├── main.tsx            ✅
└── index.css           ✅
```

## ✅ 구현 완료

- ✅ 프로젝트 설정 (Vite, TypeScript, Vitest)
- ✅ 타입 정의
- ✅ Storage 유틸리티 (TDD)
- ✅ Cart Store (TDD)
- ✅ API Client
- ✅ 기본 App 구조

## 📝 구현 필요

나머지 컴포넌트와 페이지는 `aidlc-docs/construction/customer-frontend/code/` 디렉토리의 구현 가이드를 참고하여 구현하세요.

### 우선순위

1. **High**: MenuPage, CartPage (핵심 플로우)
2. **Medium**: OrderHistoryPage, API 서비스
3. **Low**: 애니메이션, 최적화

## 🧪 테스트

```bash
# 모든 테스트 실행
npm test

# Watch 모드
npm test -- --watch

# Coverage
npm test -- --coverage
```

## 🔧 환경 변수

`.env.development` 파일에서 설정:

```env
VITE_API_URL=http://localhost:8080
```

## 📚 참고 문서

- 설계 문서: `aidlc-docs/construction/customer-frontend/`
- 구현 가이드: `aidlc-docs/construction/customer-frontend/code/`
