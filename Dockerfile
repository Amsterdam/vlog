FROM amsterdam/python:3.8-buster as app

WORKDIR /app_install
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD deploy /deploy

WORKDIR /src
ADD src .

ARG DATABASE_ENABLED=false 
ARG SECRET_KEY=collectstatic 
RUN python manage.py collectstatic --no-input

USER datapunt

CMD ["/deploy/docker-run.sh"]

# devserver
FROM app as dev

USER root

RUN apt-get update \
 && apt-get install -y \
    libgv-python \
    graphviz \
    graphviz-dev

WORKDIR /app_install
ADD requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt
RUN chmod -R a+r /app_install

USER datapunt
WORKDIR /src

# Any process that requires to write in the home dir
# we write to /tmp since we have no home dir
ENV HOME /tmp

CMD ["python manage.py runserver 0.0.0.0"]

# tests
FROM dev as tests

USER datapunt
WORKDIR /tests
ADD tests .

ENV COVERAGE_FILE=/tmp/.coverage
ENV PYTHONPATH=/src

CMD ["pytest"]
