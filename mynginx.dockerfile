FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY conf.d/*.conf /etc/nginx/conf.d

COPY conf.d/*.html /usr/share/nginx/html