FROM python:3.8-slim

LABEL org.opencontainers.image.source https://github.com/timrcase/cryptoprices-operator

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY cryptoprices-operator.py .
CMD [ "kopf", "run", "/app/cryptoprices-operator.py" ]
