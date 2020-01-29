FROM amsterdam/python:3.8-buster as app

WORKDIR /app_install
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD deploy /deploy

WORKDIR /app
ADD app .

RUN SECRET_KEY=collectstatic python manage.py collectstatic --no-input

USER datapunt

CMD ["/deploy/docker-run.sh"]

# stage 2, tests
FROM app as tests

USER root
WORKDIR /app_install
ADD requirements_dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt

WORKDIR /app
USER datapunt

ENV COVERAGE_FILE=/tmp/.coverage

CMD ["pytest"]
