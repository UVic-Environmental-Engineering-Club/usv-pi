FROM python:3.9-alpine

WORKDIR /usr/

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
