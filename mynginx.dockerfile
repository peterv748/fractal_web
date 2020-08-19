FROM nginx:latest

# RUN rm /etc/nginx/conf.d/default.conf
# VOLUME /var/log/nginx/error_log.log/
# VOLUME /var/log/nginx
COPY ./nginx.conf /etc/nginx/
# COPY ./nginx.conf /etc/conf.d/default.conf
COPY ./templates/index.html /data/www/
RUN ls /data/www/

CMD ["nginx", "-g", "daemon off;"]
