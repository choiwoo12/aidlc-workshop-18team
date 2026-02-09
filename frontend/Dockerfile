# Stage 1: Base
FROM node:18-alpine as base

WORKDIR /app

# Stage 2: Dependencies
FROM base as dependencies

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci || npm install

# Stage 3: Development
FROM dependencies as development

# Copy application code
COPY . .

# Expose port
EXPOSE 5173

# Run development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
