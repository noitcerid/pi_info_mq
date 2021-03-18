FROM python:3.8

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY config.py .
COPY server.py .

CMD [ "python", "./server.py" ]