FROM python:3.9

WORKDIR /usr/

RUN pip3 install --upgrade pip setuptools
RUN pip3 install pipenv
RUN pipenv run python -m pip install --upgrade pip
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install
