FROM node:16.20 as build

ARG listen_domain
ARG version

COPY . /.
RUN npm install
RUN echo "VITE_APP_BACKEND=${listen_domain}" > .env && echo "VITE_APP_VERSION=${version}" >> .env
RUN npm run build

FROM nginx:stable

ARG listen_domain

RUN rm /etc/nginx/conf.d/default.conf && mkdir /www
COPY --from=build dist/ /www
COPY --from=build nginx.conf /etc/nginx/nginx.conf
RUN sed -i "s/<site>/${listen_domain}/g" /etc/nginx/nginx.conf
