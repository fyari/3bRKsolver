FROM python:2

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/master/src

COPY requirements.txt /opt/services/master/src
COPY . /opt/services/master/src

WORKDIR /opt/services/master/src

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "/opt/services/master/src/app.py" ]
