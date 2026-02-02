FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY 99-autoreload.sh /docker-entrypoint.d/
RUN chmod +x /docker-entrypoint.d/99-autoreload.sh

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]

