FROM python:alpine

RUN mkdir /opt/ecb
WORKDIR /opt/ecb

ADD requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD ecb-poller/src ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RATES_URL http://localhost:8000

CMD ["python",  "/opt/ecb/poller.py"]
