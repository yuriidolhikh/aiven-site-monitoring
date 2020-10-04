FROM python:latest

RUN pip install requests kafka-python psycopg2-binary

VOLUME ["/code"]

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code"