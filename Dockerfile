FROM python:3.8.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY todolist todolist

CMD todolist/manage.py runserver 0.0.0.0:8000
