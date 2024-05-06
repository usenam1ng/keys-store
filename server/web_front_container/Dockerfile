FROM nginx

COPY index.html /usr/share/nginx/html
COPY styles.css /usr/share/nginx/html

COPY src /usr/share/nginx/html/src

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]