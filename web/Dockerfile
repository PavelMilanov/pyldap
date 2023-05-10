FROM node:16.20 as build

COPY . /.
RUN npm install
RUN echo "VITE_APP_BACKEND=backend:8000" > .env
RUN npm run build


FROM nginx:stable
ARG listen_ip

RUN rm /etc/nginx/conf.d/default.conf && mkdir /www
COPY --from=build dist/ /www
COPY --from=build nginx.conf /etc/nginx/nginx.conf
RUN sed -i "s/server_name x.x.x.x;/server_name ${listen_ip};/" /etc/nginx/nginx.conf
