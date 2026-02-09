# Customer Frontend - Infrastructure Design Summary

## Overview
Customer Frontend의 Infrastructure Design 완료. 빌드, 배포, 모니터링 인프라 설계.

---

## 문서 목록

1. **build-configuration.md** - Vite, TypeScript, ESLint, Prettier 설정
2. **deployment-strategy.md** - S3/CloudFront, Netlify, Vercel 배포 전략
3. **monitoring-and-observability.md** - 성능, 에러, 사용자 분석

---

## 핵심 인프라

### 빌드 도구
- **Vite**: 빠른 HMR, 최적화된 빌드
- **TypeScript**: 타입 안정성
- **ESLint**: 코드 품질
- **Prettier**: 코드 포맷팅

### 배포 플랫폼
- **AWS S3 + CloudFront** (권장): 확장성, 성능
- **Netlify**: 간편한 배포
- **Vercel**: 자동 최적화

### CI/CD
- **GitHub Actions**: 자동화된 빌드 및 배포
- **Preview Deployments**: PR별 미리보기

### 모니터링
- **Web Vitals**: 성능 지표
- **Error Tracking**: 에러 추적
- **Analytics**: 사용자 분석

---

## 빌드 설정

### Vite Configuration
```typescript
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') },
  },
  build: {
    target: 'es2015',
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'zustand-vendor': ['zustand'],
          'axios-vendor': ['axios'],
        },
      },
    },
  },
});
```

### Bundle Size Targets
- main.js: < 100KB (gzipped)
- react-vendor.js: < 50KB (gzipped)
- Total: < 200KB (gzipped)

---

## 배포 전략

### AWS S3 + CloudFront
```bash
# Build
npm run build

# Deploy to S3
aws s3 sync dist/ s3://tableorder-customer-frontend --delete

# Invalidate CloudFront
aws cloudfront create-invalidation --distribution-id XXX --paths "/*"
```

### Cache Strategy
- Static assets: `max-age=31536000, immutable`
- index.html: `no-cache, no-store, must-revalidate`

### CI/CD Pipeline
```yaml
on:
  push:
    branches: [main]

jobs:
  deploy:
    - Checkout
    - Install dependencies
    - Type check
    - Lint
    - Build
    - Deploy to S3
    - Invalidate CloudFront
```

---

## 모니터링

### Performance Metrics
- **LCP**: < 2.5초
- **FID**: < 100ms
- **CLS**: < 0.1
- **API Response**: < 1초

### Error Tracking
- JavaScript errors
- API errors
- Network errors
- Error rate < 1%

### User Analytics
- Page views
- User journeys
- Conversion rate
- Cart abandonment

---

## 환경 관리

### Development
```env
VITE_API_URL=http://localhost:8080
```

### Production
```env
VITE_API_URL=https://api.tableorder.com
```

---

## 디렉토리 구조

```
frontend/customer/
├── public/
├── src/
│   ├── atoms/
│   ├── molecules/
│   ├── organisms/
│   ├── templates/
│   ├── pages/
│   ├── stores/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   ├── components/
│   ├── App.tsx
│   └── main.tsx
├── dist/                    # Build output
├── node_modules/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .eslintrc.cjs
├── .prettierrc
├── .env.development
├── .env.production
└── .gitignore
```

---

## 다음 단계: Code Generation

Customer Frontend의 모든 설계가 완료되었습니다. 이제 **Code Generation** 단계로 진행합니다.

### Code Generation 방식 선택

**A) TDD 방식 (Test-Driven Development)**
- 시간/토큰: 1.5~2배 소요
- 품질: 높음 (기능 누락 방지, 테스트 우선 설계)
- 권장: 복잡한 비즈니스 로직, 장기 유지보수 프로젝트

**B) 일반 방식 (Standard)**
- 시간/토큰: 기준
- 품질: 표준
- 권장: 간단한 프로토타입, 빠른 구현

---

## 검증 체크리스트

- [x] 빌드 설정 완료
- [x] 배포 전략 수립 완료
- [x] 모니터링 계획 수립 완료
- [x] 환경 변수 관리 완료
- [x] CI/CD 파이프라인 정의 완료
- [x] 디렉토리 구조 정의 완료

---

## Notes

- Vite로 빠른 개발 및 최적화된 빌드
- S3 + CloudFront로 글로벌 배포
- GitHub Actions로 자동화된 CI/CD
- Web Vitals로 성능 모니터링
- 환경별 설정 분리
