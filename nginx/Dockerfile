# Stage 1 - build frontend app
FROM node:12 as build-deps

WORKDIR /app/

#COPY frontend/package.json frontend/package-lock.json /app/

COPY frontend /app/
RUN yarn install
COPY .env /app/.env
RUN yarn build

# Stage 2 - nginx & frontend dist
FROM nginx:alpine

COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-deps /app/dist/ /dist/

CMD ["nginx", "-g", "daemon off;"]
