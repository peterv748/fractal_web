FROM nginx

# RUN rm /etc/nginx/conf.d/default.conf

COPY conf.d/default.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]
