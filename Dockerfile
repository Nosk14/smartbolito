FROM resin/rpi-raspbian
ENV FLASK_APP /usr/local/smartbolito/app.py
COPY requirements.txt .
RUN apt-get update \
    && apt-get install python3 python3-dev python3-pip gcc g++
RUN pip3 install --upgrade setuptools pip
RUN pip3 install -r requirements.txt
COPY smartbolito /usr/local/smartbolito/
WORKDIR /usr/local/
CMD gunicorn -w 1 -b 0.0.0.0:5000 --log-level DEBUG smartbolito.app:api
