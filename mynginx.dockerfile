FROM nginx:latest


COPY ./nginx.conf /etc/nginx/
COPY ./templates/index.html /data/www/
COPY ./templates/css/*.* /data/www/css/
COPY ./templates/img/*.* /data/www/img/
# RUN ls ./templates/css

EXPOSE 3500
EXPOSE 9000
EXPOSE 9080
CMD ["nginx", "-g", "daemon off;"]
