FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
COPY package-lock.json .

RUN npm install

COPY src/ src/
COPY public/ public/
COPY index.html .
COPY vite.config.ts .
COPY tsconfig.json .
COPY tsconfig.app.json .
COPY tsconfig.node.json .
COPY eslint.config.ts .

RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

# El comando por defecto de Nginx ya inicia el servidor
CMD ["nginx", "-g", "daemon off;"]