FROM python:3.8

COPY . /app
WORKDIR /app

RUN python -m pip install -r requirements.txt

ENTRYPOINT pytest -s -v --alluredir=/tmp/allure