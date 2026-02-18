# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /frontend

# Copy package.json & package-lock.json first for caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the frontend files
COPY . .

# Build the React app (Vite)
RUN npm run build

# Stage 2: Serve static files
FROM node:20-alpine AS serve

WORKDIR /frontend

# Install serve globally
RUN npm install -g serve

# Copy built files from the build stage
COPY --from=build /frontend/dist ./dist

# Expose port
EXPOSE 3000

# Serve built static files
CMD ["serve", "-s", "dist", "-l", "3000"]
