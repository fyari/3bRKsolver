FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /opt/services/3bodysolver
RUN mkdir -p /opt/services/3bodysolver/src

COPY requirements.txt /opt/services/3bodysolver/src
COPY 3body.py /opt/services/3bodysolver/src

WORKDIR /opt/services/3bodysolver/src

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
#RUN pip install numpy scipy Psycopg2 sqlalchemy

#EXPOSE 5000

CMD [ "python", "/opt/services/3bodysolver/src/3body.py" ]

#3body.py  calculate the result and write it in database table RESULT