FROM python:3.8.5
ENV PYTHONBUFFERED 1
WORKDIR /code
ADD . /code
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system
