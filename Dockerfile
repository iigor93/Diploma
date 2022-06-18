FROM python:3.8.10

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY todolist todolist

WORKDIR ./todolist
CMD ./manage.py runserver 0.0.0.0:8000 # python3 -m gunicorn -b 0.0.0.0:8000 todolist.wsgi #todolist
