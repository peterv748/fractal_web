FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY conf.d/defalt.conf /etc/nginx/nginx.conf
