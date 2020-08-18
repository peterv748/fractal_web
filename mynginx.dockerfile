FROM nginx

RUN rm /etc/nginx/conf.d/default.conf

COPY ./backend.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]
