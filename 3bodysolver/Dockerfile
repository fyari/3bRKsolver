FROM python:3.7-alpine
COPY . /app
WORKDIR /app

RUN apk add build-base
RUN pip install -r requirements.txt

CMD ["python","3body.py"]
