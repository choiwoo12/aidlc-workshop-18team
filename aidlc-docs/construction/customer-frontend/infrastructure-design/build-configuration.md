# Customer Frontend - Build Configuration

## Overview
Vite 기반 빌드 설정. 최적화된 프로덕션 빌드와 효율적인 개발 환경 구성.

---

## Vite Configuration

### vite.config.ts
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      },
    },
  },

  build: {
    target: 'es2015',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false, // Production에서 source map 제거
    minify: 'terser',
    
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
        pure_funcs: ['console.log', 'console.info'],
      },
    },

    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor 분리
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'zustand-vendor': ['zustand'],
          'axios-vendor': ['axios'],
        },
        
        // 파일명 패턴
        chunkFileNames: 'assets/js/[name]-[hash].js',
        entryFileNames: 'assets/js/[name]-[hash].js',
        assetFileNames: 'assets/[ext]/[name]-[hash].[ext]',
      },
    },

    chunkSizeWarningLimit: 500, // 500KB
  },

  optimizeDeps: {
    include: ['react', 'react-dom', 'zustand', 'axios'],
  },
});
```

---

## TypeScript Configuration

### tsconfig.json
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,

    /* Path mapping */
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### tsconfig.node.json
```json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
```

---

## Package Configuration

### package.json
```json
{
  "name": "customer-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "react-toastify": "^9.1.3"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "prettier": "^3.1.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "vitest": "^1.0.4"
  }
}
```

---

## ESLint Configuration

### .eslintrc.cjs
```javascript
module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh'],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    '@typescript-eslint/no-explicit-any': 'warn',
  },
};
```

---

## Prettier Configuration

### .prettierrc
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

### .prettierignore
```
dist
node_modules
*.md
```

---

## Environment Variables

### .env.development
```env
VITE_API_URL=http://localhost:8080
VITE_APP_NAME=TableOrder Customer
VITE_APP_VERSION=1.0.0
```

### .env.production
```env
VITE_API_URL=https://api.tableorder.com
VITE_APP_NAME=TableOrder Customer
VITE_APP_VERSION=1.0.0
```

### .env.example
```env
VITE_API_URL=http://localhost:8080
VITE_APP_NAME=TableOrder Customer
VITE_APP_VERSION=1.0.0
```

---

## Git Configuration

### .gitignore
```
# Dependencies
node_modules

# Build output
dist
dist-ssr
*.local

# Environment variables
.env.local
.env.production.local

# Editor
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

# Testing
coverage
.nyc_output

# Misc
.cache
```

---

## VS Code Configuration

### .vscode/settings.json
```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true
}
```

### .vscode/extensions.json
```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss"
  ]
}
```

---

## Build Scripts

### scripts/build.sh
```bash
#!/bin/bash

echo "🔨 Building Customer Frontend..."

# Type check
echo "📝 Type checking..."
npm run type-check

# Lint
echo "🔍 Linting..."
npm run lint

# Build
echo "🏗️  Building..."
npm run build

# Check bundle size
echo "📦 Bundle size:"
du -sh dist

echo "✅ Build complete!"
```

### scripts/analyze.sh
```bash
#!/bin/bash

echo "📊 Analyzing bundle..."

# Install analyzer
npm install -D rollup-plugin-visualizer

# Build with analyzer
vite build --mode production

echo "✅ Analysis complete! Check stats.html"
```

---

## Build Optimization

### Code Splitting Strategy
```typescript
// Lazy load pages
const MenuPage = lazy(() => import('@/pages/MenuPage'));
const CartPage = lazy(() => import('@/pages/CartPage'));
const OrderHistoryPage = lazy(() => import('@/pages/OrderHistoryPage'));

// Lazy load heavy components
const OrderDetailModal = lazy(() => import('@/organisms/OrderDetail'));
```

### Tree Shaking
```typescript
// ✅ Good: Named imports
import { useState, useEffect } from 'react';

// ❌ Bad: Default import
import React from 'react';
```

### Dynamic Imports
```typescript
// Load library only when needed
const loadToast = async () => {
  const { toast } = await import('react-toastify');
  return toast;
};
```

---

## Build Performance

### Cache Configuration
```typescript
// vite.config.ts
export default defineConfig({
  cacheDir: 'node_modules/.vite',
  
  build: {
    // Enable build cache
    cache: true,
  },
});
```

### Parallel Processing
```json
// package.json
{
  "scripts": {
    "build:parallel": "npm-run-all --parallel type-check lint build"
  }
}
```

---

## Build Verification

### Size Limits
```json
// package.json
{
  "scripts": {
    "size-limit": "size-limit"
  },
  "size-limit": [
    {
      "path": "dist/assets/js/*.js",
      "limit": "200 KB"
    }
  ]
}
```

### Lighthouse CI
```yaml
# lighthouserc.js
module.exports = {
  ci: {
    collect: {
      staticDistDir: './dist',
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
      },
    },
  },
};
```

---

## Build Output

### Expected Structure
```
dist/
├── index.html
├── assets/
│   ├── js/
│   │   ├── main-[hash].js
│   │   ├── react-vendor-[hash].js
│   │   ├── zustand-vendor-[hash].js
│   │   └── axios-vendor-[hash].js
│   ├── css/
│   │   └── main-[hash].css
│   └── images/
│       └── placeholder-[hash].png
└── favicon.ico
```

### Size Targets
- main.js: < 100KB (gzipped)
- react-vendor.js: < 50KB (gzipped)
- zustand-vendor.js: < 10KB (gzipped)
- axios-vendor.js: < 20KB (gzipped)
- Total: < 200KB (gzipped)

---

## Notes

- Vite는 빠른 HMR과 최적화된 빌드 제공
- TypeScript로 타입 안정성 확보
- ESLint + Prettier로 코드 품질 유지
- 환경 변수로 설정 관리
- Bundle size 모니터링 필수
