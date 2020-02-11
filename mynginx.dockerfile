FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY conf.d/*.conf /etc/nginx

COPY conf.d/*.html /usr/share/nginx/html