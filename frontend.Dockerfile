# STAGE 1: Build the React Application
FROM node:20-slim AS build

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY ./frontend/package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY ./frontend/ .

# Direct build bypassing package.json scripts
RUN npx vite build

# STAGE 2: Serve the assets using Nginx
FROM nginx:alpine

# Copy the built assets from Stage 1 to Nginx's html folder
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 (standard for HTTP)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
