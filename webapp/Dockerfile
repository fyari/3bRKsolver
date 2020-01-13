FROM python:3


ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/webapp/src

#VOLUME ["/opt/services/webapp/src"]

COPY requirements.txt /opt/services/webapp/src
COPY . /opt/services/webapp/src

WORKDIR /opt/services/webapp/src

RUN pip install -r requirements.txt



EXPOSE 5090
CMD ["python", "app.py"]
