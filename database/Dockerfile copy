FROM postgres

RUN mkdir sql

COPY . sql/

WORKDIR sql/

RUN psql --host localhost --port 5432 --user Postgres -c "CREATE DATABASE threebody OWNER 'Postgres';"

EXPOSE 5432

