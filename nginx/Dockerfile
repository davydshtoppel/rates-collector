FROM nginx

COPY default.conf.template /etc/nginx/templates/
COPY static /usr/share/nginx/html/static
COPY media /usr/share/nginx/html/media

ENV RATES_HOST 127.0.0.1
ENV RATES_PORT 8000