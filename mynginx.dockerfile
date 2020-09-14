FROM nginx:latest


COPY ./nginx.conf /etc/nginx/
COPY ./templates/index.html /data/www/
COPY ./static/styles/css/*.* /data/www/static/styles/css/
COPY ./static/img/*.* /data/www/static/img/
# RUN ls ./templates/css

EXPOSE 3500
EXPOSE 9000
EXPOSE 9080
CMD ["nginx", "-g", "daemon off;"]
