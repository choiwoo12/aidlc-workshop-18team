# Stage 1: Base
FROM node:18-alpine AS base

WORKDIR /app

# Stage 2: Dependencies
FROM base AS dependencies

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci || npm install

# Stage 3: Development
FROM dependencies AS development

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Run development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
