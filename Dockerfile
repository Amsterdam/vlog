FROM amsterdam/python:3.8.1-buster

WORKDIR /app_install
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
ADD app .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
