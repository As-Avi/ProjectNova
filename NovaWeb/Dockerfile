# ---------- Stage 1: build dell'app React ----------
FROM node:22-alpine AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund

COPY public ./public
COPY src ./src

# Il browser chiama /api/ sullo stesso host; sarà nginx a inoltrare la richiesta al backend.
# Per puntare direttamente a un altro server: --build-arg SERVER_URL=https://server/api/
ARG SERVER_URL=/api/
RUN node -e "const fs=require('fs');const f='src/config.json';const c=JSON.parse(fs.readFileSync(f,'utf8'));c.SERVER_URL=process.env.SERVER_URL;fs.writeFileSync(f,JSON.stringify(c,null,2))"

RUN npm run build

# ---------- Stage 2: nginx che serve i file statici ----------
FROM nginx:1.27-alpine

# Indirizzo del backend, sostituito nel template all'avvio del container.
ENV BACKEND_URL=http://host.docker.internal:8000/api/

COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
