# Customer Frontend - Deployment Strategy

## Overview
정적 파일 호스팅 기반 배포 전략. CDN을 활용한 글로벌 배포와 CI/CD 자동화.

---

## Deployment Architecture

```
GitHub Repository
    ↓
GitHub Actions (CI/CD)
    ↓
Build (npm run build)
    ↓
Static Files (dist/)
    ↓
S3 / Netlify / Vercel
    ↓
CloudFront / CDN
    ↓
Users
```

---

## Hosting Options

### Option 1: AWS S3 + CloudFront (권장)

#### S3 Bucket Setup
```bash
# Create S3 bucket
aws s3 mb s3://tableorder-customer-frontend

# Enable static website hosting
aws s3 website s3://tableorder-customer-frontend \
  --index-document index.html \
  --error-document index.html
```

#### Bucket Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::tableorder-customer-frontend/*"
    }
  ]
}
```

#### CloudFront Distribution
```yaml
# cloudfront-config.yml
DistributionConfig:
  Origins:
    - DomainName: tableorder-customer-frontend.s3.amazonaws.com
      Id: S3-tableorder-customer-frontend
      S3OriginConfig:
        OriginAccessIdentity: ""
  DefaultCacheBehavior:
    TargetOriginId: S3-tableorder-customer-frontend
    ViewerProtocolPolicy: redirect-to-https
    Compress: true
    CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6 # CachingOptimized
  PriceClass: PriceClass_100
  Enabled: true
```

---

### Option 2: Netlify (간편)

#### netlify.toml
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  NODE_VERSION = "18"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

---

### Option 3: Vercel (간편)

#### vercel.json
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        }
      ]
    }
  ]
}
```

---

## CI/CD Pipeline

### GitHub Actions

#### .github/workflows/deploy.yml
```yaml
name: Deploy Customer Frontend

on:
  push:
    branches:
      - main
    paths:
      - 'frontend/customer/**'
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: frontend/customer/package-lock.json

      - name: Install dependencies
        working-directory: frontend/customer
        run: npm ci

      - name: Type check
        working-directory: frontend/customer
        run: npm run type-check

      - name: Lint
        working-directory: frontend/customer
        run: npm run lint

      - name: Build
        working-directory: frontend/customer
        run: npm run build
        env:
          VITE_API_URL: ${{ secrets.VITE_API_URL }}

      - name: Deploy to S3
        uses: jakejarvis/s3-sync-action@master
        with:
          args: --delete --cache-control max-age=31536000
        env:
          AWS_S3_BUCKET: ${{ secrets.AWS_S3_BUCKET }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: 'ap-northeast-2'
          SOURCE_DIR: 'frontend/customer/dist'

      - name: Invalidate CloudFront
        uses: chetan/invalidate-cloudfront-action@v2
        env:
          DISTRIBUTION: ${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}
          PATHS: '/*'
          AWS_REGION: 'ap-northeast-2'
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

      - name: Notify success
        if: success()
        run: echo "✅ Deployment successful!"

      - name: Notify failure
        if: failure()
        run: echo "❌ Deployment failed!"
```

---

### Preview Deployments

#### .github/workflows/preview.yml
```yaml
name: Preview Deployment

on:
  pull_request:
    paths:
      - 'frontend/customer/**'

jobs:
  preview:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        working-directory: frontend/customer
        run: npm ci

      - name: Build
        working-directory: frontend/customer
        run: npm run build
        env:
          VITE_API_URL: https://api-staging.tableorder.com

      - name: Deploy to Netlify (Preview)
        uses: nwtgck/actions-netlify@v2
        with:
          publish-dir: './frontend/customer/dist'
          production-deploy: false
          github-token: ${{ secrets.GITHUB_TOKEN }}
          deploy-message: "Preview for PR #${{ github.event.number }}"
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

---

## Deployment Scripts

### scripts/deploy.sh
```bash
#!/bin/bash

set -e

echo "🚀 Deploying Customer Frontend..."

# Environment
ENV=${1:-production}

# Load environment variables
if [ "$ENV" = "production" ]; then
  export $(cat .env.production | xargs)
else
  export $(cat .env.development | xargs)
fi

# Build
echo "🏗️  Building..."
npm run build

# Deploy to S3
echo "📦 Uploading to S3..."
aws s3 sync dist/ s3://tableorder-customer-frontend \
  --delete \
  --cache-control "max-age=31536000" \
  --exclude "index.html"

# Upload index.html with no-cache
aws s3 cp dist/index.html s3://tableorder-customer-frontend/index.html \
  --cache-control "no-cache"

# Invalidate CloudFront
echo "🔄 Invalidating CloudFront..."
aws cloudfront create-invalidation \
  --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
  --paths "/*"

echo "✅ Deployment complete!"
echo "🌐 URL: https://customer.tableorder.com"
```

---

## Cache Strategy

### Cache-Control Headers

#### Static Assets (JS, CSS, Images)
```
Cache-Control: public, max-age=31536000, immutable
```

#### index.html
```
Cache-Control: no-cache, no-store, must-revalidate
```

#### API Responses
```
Cache-Control: no-cache
```

---

### CloudFront Cache Behavior

```yaml
CacheBehaviors:
  # Static assets (versioned)
  - PathPattern: "/assets/*"
    CachePolicyId: 658327ea-f89d-4fab-a63d-7e88639e58f6 # CachingOptimized
    Compress: true
    
  # index.html (no cache)
  - PathPattern: "/index.html"
    CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad # CachingDisabled
    Compress: true
```

---

## Environment Management

### Development
```env
VITE_API_URL=http://localhost:8080
```

### Staging
```env
VITE_API_URL=https://api-staging.tableorder.com
```

### Production
```env
VITE_API_URL=https://api.tableorder.com
```

---

## Rollback Strategy

### Version Tagging
```bash
# Tag release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Rollback to previous version
git checkout v0.9.0
npm run build
./scripts/deploy.sh production
```

### S3 Versioning
```bash
# Enable versioning
aws s3api put-bucket-versioning \
  --bucket tableorder-customer-frontend \
  --versioning-configuration Status=Enabled

# List versions
aws s3api list-object-versions \
  --bucket tableorder-customer-frontend

# Restore previous version
aws s3api copy-object \
  --copy-source tableorder-customer-frontend/index.html?versionId=VERSION_ID \
  --bucket tableorder-customer-frontend \
  --key index.html
```

---

## Health Checks

### Deployment Verification
```bash
#!/bin/bash

URL="https://customer.tableorder.com"

# Check HTTP status
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $STATUS -eq 200 ]; then
  echo "✅ Health check passed"
  exit 0
else
  echo "❌ Health check failed: $STATUS"
  exit 1
fi
```

### Smoke Tests
```typescript
// tests/smoke.test.ts
describe('Smoke Tests', () => {
  it('should load homepage', async () => {
    const response = await fetch('https://customer.tableorder.com');
    expect(response.status).toBe(200);
  });

  it('should load main bundle', async () => {
    const response = await fetch('https://customer.tableorder.com/assets/js/main.js');
    expect(response.status).toBe(200);
  });
});
```

---

## Monitoring

### CloudWatch Alarms
```yaml
# cloudwatch-alarms.yml
Alarms:
  - AlarmName: CustomerFrontend-4xxErrors
    MetricName: 4xxErrorRate
    Threshold: 5
    EvaluationPeriods: 2
    
  - AlarmName: CustomerFrontend-5xxErrors
    MetricName: 5xxErrorRate
    Threshold: 1
    EvaluationPeriods: 1
```

### Uptime Monitoring
- Pingdom
- UptimeRobot
- StatusCake

---

## Security Headers

### Recommended Headers
```
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

---

## Deployment Checklist

### Pre-Deployment
- [ ] Code review 완료
- [ ] 테스트 통과
- [ ] Type check 통과
- [ ] Lint 통과
- [ ] Bundle size 확인
- [ ] 환경 변수 설정

### Deployment
- [ ] 빌드 성공
- [ ] S3 업로드 완료
- [ ] CloudFront 무효화
- [ ] Health check 통과

### Post-Deployment
- [ ] Smoke tests 실행
- [ ] 성능 모니터링
- [ ] 에러 모니터링
- [ ] 사용자 피드백 수집

---

## Notes

- 정적 파일 호스팅으로 간단한 배포
- CDN으로 글로벌 성능 향상
- CI/CD로 자동화된 배포
- 버전 관리로 안전한 롤백
- 모니터링으로 안정성 확보
