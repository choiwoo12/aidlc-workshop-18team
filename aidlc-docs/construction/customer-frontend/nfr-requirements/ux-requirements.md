# Customer Frontend - UX Requirements

## Overview
사용자 경험 요구사항. 직관적이고 사용하기 쉬운 인터페이스 제공.

---

## 사용성 (Usability)

### 직관적인 네비게이션
**요구사항**: 3번의 클릭 이내에 모든 기능 접근

**구조**:
```
메뉴 조회 (/) → 장바구니 (/cart) → 주문 완료
                ↓
            주문 내역 (/orders)
```

**방법**:
- 하단 네비게이션 바 (항상 표시)
- 명확한 버튼 레이블
- 뒤로가기 버튼

---

### 명확한 피드백
**요구사항**: 모든 사용자 액션에 즉각적인 피드백

**피드백 유형**:
1. **로딩 상태**: 스피너, 스켈레톤 UI
2. **성공**: Toast 메시지 (초록색)
3. **에러**: Toast 메시지 (빨간색)
4. **정보**: Toast 메시지 (파란색)

**예시**:
```typescript
// 장바구니 담기
toast.success('장바구니에 담았습니다');

// 주문 생성
toast.success('주문이 완료되었습니다');

// 에러
toast.error('주문 생성에 실패했습니다');
```

---

### 에러 복구
**요구사항**: 에러 발생 시 복구 방법 제공

**방법**:
- 재시도 버튼
- 이전 페이지로 돌아가기
- 고객 지원 연락처 (선택)

**예시**:
```typescript
<div className="error-state">
  <p>메뉴를 불러오지 못했습니다</p>
  <Button onClick={retry}>다시 시도</Button>
</div>
```

---

## 접근성 (Accessibility)

### WCAG 2.1 AA 준수
**요구사항**: 웹 접근성 표준 준수

**체크리스트**:
- [ ] 키보드 네비게이션 지원
- [ ] 스크린 리더 호환
- [ ] 색상 대비율 4.5:1 이상
- [ ] 대체 텍스트 제공
- [ ] 포커스 표시

---

### Semantic HTML
**요구사항**: 의미 있는 HTML 태그 사용

**예시**:
```html
<nav>하단 네비게이션</nav>
<main>메인 콘텐츠</main>
<button>주문하기</button>
<img alt="김치찌개" />
```

---

### ARIA Labels
**요구사항**: 스크린 리더를 위한 ARIA 레이블

**예시**:
```typescript
<button aria-label="장바구니에 담기">
  <CartIcon />
</button>

<input
  type="number"
  aria-label="수량"
  aria-describedby="quantity-help"
/>
```

---

### Keyboard Navigation
**요구사항**: 키보드만으로 모든 기능 사용 가능

**지원 키**:
- Tab: 다음 요소로 이동
- Shift+Tab: 이전 요소로 이동
- Enter/Space: 버튼 활성화
- Esc: 모달 닫기

---

### Focus Management
**요구사항**: 포커스 상태 명확히 표시

**방법**:
```css
button:focus {
  outline: 2px solid #007bff;
  outline-offset: 2px;
}
```

---

## 반응형 디자인

### Mobile-First
**요구사항**: 모바일 우선 설계

**Breakpoints**:
- Mobile: < 768px (기본)
- Tablet: 768px ~ 1024px
- Desktop: > 1024px

---

### Touch-Friendly
**요구사항**: 터치 친화적 UI

**기준**:
- 버튼 최소 크기: 44x44px
- 터치 영역 간격: 8px 이상
- 스와이프 제스처 지원 (선택)

---

### Responsive Images
**요구사항**: 화면 크기에 맞는 이미지

**방법**:
```html
<img
  src="menu-small.jpg"
  srcset="menu-small.jpg 480w, menu-large.jpg 1024w"
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="메뉴 이미지"
/>
```

---

## 시각 디자인

### 일관된 디자인 시스템
**요구사항**: 통일된 색상, 타이포그래피, 간격

**색상 팔레트**:
- Primary: #007bff (파란색)
- Success: #28a745 (초록색)
- Warning: #ffc107 (주황색)
- Danger: #dc3545 (빨간색)
- Gray: #6c757d

**타이포그래피**:
- 제목: 24px, Bold
- 본문: 16px, Regular
- 캡션: 14px, Regular

**간격**:
- 기본: 16px
- 작음: 8px
- 큼: 24px

---

### 색상 대비
**요구사항**: WCAG AA 기준 (4.5:1)

**검증**:
- 텍스트 vs 배경
- 버튼 vs 배경
- 링크 vs 배경

---

### 아이콘
**요구사항**: 명확하고 일관된 아이콘

**사용**:
- 메뉴: 🍽️
- 장바구니: 🛒
- 주문내역: 📋
- 추가: ➕
- 삭제: ❌

---

## 인터랙션

### 로딩 상태
**요구사항**: 로딩 중 명확한 표시

**방법**:
1. **스피너**: 짧은 로딩 (< 2초)
2. **스켈레톤 UI**: 긴 로딩 (> 2초)
3. **프로그레스 바**: 단계별 진행

---

### 애니메이션
**요구사항**: 부드러운 전환 효과

**사용 사례**:
- 페이지 전환: Fade in/out
- 모달 열기/닫기: Slide up/down
- 버튼 클릭: Scale down

**성능**:
- 60 FPS 유지
- GPU 가속 (transform, opacity)

---

### 제스처
**요구사항**: 모바일 제스처 지원 (선택)

**지원 제스처**:
- 스와이프: 페이지 전환
- 풀 투 리프레시: 새로고침
- 롱 프레스: 상세 정보

---

## 콘텐츠

### 명확한 문구
**요구사항**: 이해하기 쉬운 텍스트

**예시**:
- ✅ "장바구니에 담기"
- ❌ "Add to Cart"
- ✅ "주문하기"
- ❌ "Submit Order"

---

### 에러 메시지
**요구사항**: 구체적이고 해결 방법 제시

**예시**:
- ❌ "오류가 발생했습니다"
- ✅ "네트워크 연결을 확인해주세요"
- ✅ "수량은 1개 이상이어야 합니다"

---

### 빈 상태
**요구사항**: 빈 상태에 대한 안내

**예시**:
```typescript
<div className="empty-state">
  <p>장바구니가 비어있습니다</p>
  <Button onClick={() => navigate('/')}>
    메뉴 보러가기
  </Button>
</div>
```

---

## 성능 인식

### Perceived Performance
**요구사항**: 체감 성능 향상

**방법**:
1. **낙관적 업데이트**: UI 먼저 업데이트
2. **스켈레톤 UI**: 로딩 중 구조 표시
3. **Progressive loading**: 중요한 콘텐츠 먼저

---

### Optimistic UI
**예시**:
```typescript
// 장바구니 담기 - 즉시 UI 업데이트
addItem(menu, quantity);
toast.success('장바구니에 담았습니다');
// API 호출은 백그라운드에서
```

---

## 오프라인 지원

### Offline Detection
**요구사항**: 오프라인 상태 감지 및 안내

**방법**:
```typescript
useEffect(() => {
  const handleOffline = () => {
    toast.warning('인터넷 연결이 끊어졌습니다');
  };
  
  const handleOnline = () => {
    toast.success('인터넷 연결이 복구되었습니다');
  };

  window.addEventListener('offline', handleOffline);
  window.addEventListener('online', handleOnline);

  return () => {
    window.removeEventListener('offline', handleOffline);
    window.removeEventListener('online', handleOnline);
  };
}, []);
```

---

### Offline Fallback
**요구사항**: 오프라인 시 기본 기능 제공

**방법**:
- 장바구니는 localStorage에서 유지
- 주문 생성은 온라인 필요 (안내 메시지)

---

## 다국어 지원 (향후)

### i18n 준비
**요구사항**: 다국어 지원 가능한 구조

**방법**:
- 하드코딩된 텍스트 최소화
- i18n 라이브러리 사용 (react-i18next)

---

## UX 테스트

### Usability Testing
**시나리오**:
1. 메뉴 조회 → 장바구니 담기
2. 장바구니 → 주문 생성
3. 주문 내역 조회

**측정 지표**:
- 작업 완료 시간
- 에러 발생 횟수
- 사용자 만족도

---

### A/B Testing
**테스트 항목**:
- 버튼 색상
- 문구 (CTA)
- 레이아웃

---

## UX 우선순위

### Critical
1. 명확한 피드백
2. 직관적인 네비게이션
3. 에러 복구

### High
1. 접근성 (WCAG AA)
2. 반응형 디자인
3. 로딩 상태 표시

### Medium
1. 애니메이션
2. 오프라인 지원
3. 제스처 지원

---

## Notes

- 사용자 중심 설계
- 모바일 우선 접근
- 접근성은 필수, 선택 아님
- 지속적인 사용자 피드백 수집
- A/B 테스트로 개선
