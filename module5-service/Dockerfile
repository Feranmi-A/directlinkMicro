# Module5 Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN echo "Skipping build; using placeholder Express server"

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/src ./src
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "src/app.js"]
