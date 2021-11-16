FROM python:3.8-alpine

LABEL org.opencontainers.image.source https://github.com/timrcase/cryptoprices-operator

RUN apk --update add gcc build-base
RUN pip install --no-cache-dir kopf requests
ADD cryptoprices-operator.py /
CMD kopf run /cryptoprices-operator.py