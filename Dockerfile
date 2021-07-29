FROM python:3.8.5
ENV PYTHONBUFFERED 1
WORKDIR /code
ADD . /code
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system
