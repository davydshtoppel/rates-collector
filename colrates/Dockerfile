# pull official base image
FROM python

RUN apt-get update && apt-get install postgresql gcc python3-dev musl-dev -y --no-install-recommends

RUN mkdir /opt/colrates
WORKDIR /opt/colrates

ADD src ./
ADD start-server.sh .
ADD requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ecbrates.settings.prod
ENV DATABASE_USER admin
ENV DATABASE_PASSWORD password
ENV DATABASE_HOST localhost
ENV DATABASE_PORT 5432
ENV DATABASE_NAME colrates

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/opt/colrates/start-server.sh"]
