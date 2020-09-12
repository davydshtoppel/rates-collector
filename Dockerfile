# pull official base image
FROM python

RUN apt-get update && apt-get install postgresql gcc python3-dev musl-dev -y --no-install-recommends

RUN mkdir /opt/rates-collector
WORKDIR /opt/rates-collector

ADD ecbrates/src/ ./
ADD ecbrates/start-server.sh .
ADD requirements.txt .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE ecbrates.settings.prod

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2

EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/opt/rates-collector/start-server.sh"]
