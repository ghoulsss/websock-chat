# Stage 1: Development
FROM node:22-alpine AS development

WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./
COPY yarn.lock* ./
COPY pnpm-lock.yaml* ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код
COPY . .

# Открываем порты
EXPOSE 5173 4173

# Команда для разработки
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 2: Production build
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Stage 3: Production
FROM nginx:alpine AS production

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]