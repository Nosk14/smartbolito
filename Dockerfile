FROM python:3.7.1-alpine3.8
ENV FLASK_APP /usr/local/smartbolito/app.py
COPY requirements.txt .
RUN apk add --update --no-cache --virtual build-dependencies \
    g++ gcc libxslt-dev python3-dev \
    && pip3 install -r requirements.txt \
    && apk del build-dependencies
COPY smartbolito /usr/local/smartbolito/
WORKDIR /usr/local/
CMD gunicorn -w 1 -b 0.0.0.0:5000 --log-level DEBUG smartbolito.app:api
