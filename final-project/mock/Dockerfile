FROM python:3.8

COPY mock.py /app/mock.py
WORKDIR /app

RUN python -m pip install flask

EXPOSE 5000
CMD python mock.py