FROM python:alpine

RUN mkdir /opt/colrates-feeder
WORKDIR /opt/colrates-feeder

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD src ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RATES_URL http://localhost:8000

CMD ["python",  "/opt/colrates-feeder/poller.py"]
