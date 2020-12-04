#

#WORKDIR /frontend-service/app
#ENV FLASK_APP="app:create_app()"

#ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN apk update
#RUN apk add postgresql-dev gcc python3-dev musl-dev
#COPY requirements.txt requirements.txt
#RUN pip install -r requirements.txt
#EXPOSE 5000

#COPY . .
# CMD ["flask", "run", "--host", "0.0.0.0"]
#CMD ["flask", "run"]


#FROM ubuntu:14.04

#FROM python:3.7-alpine

#WORKDIR /authentication-service/app
#COPY requirements.txt requirements.txt

#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN apk update
#RUN apk add postgresql-dev gcc python3-dev musl-dev
#RUN pip install -r requirements.txt

#RUN apk add postgresql
#RUN (addgroup -S postgres && adduser -S postgres -G postgres || true)
#RUN mkdir -p /var/lib/postgresql/data
#RUN mkdir -p /run/postgresql/
#RUN chown -R postgres:postgres /run/postgresql/
#RUN chmod -R 777 /var/lib/postgresql/data
#RUN chown -R postgres:postgres /var/lib/postgresql/data
#RUN su - postgres -c "initdb /var/lib/postgresql/data"
#RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf
#RUN su - postgres -c "pg_ctl start  -D /var/lib/postgresql/data -o \"-p 5433\""
#RUN su - postgres -c "pg_ctl start -D /var/lib/postgresql/data -l /var/lib/postgresql/log.log && psql --command \"ALTER USER postgres WITH ENCRYPTED PASSWORD 'postgres';\" && psql --command \"CREATE DATABASE authentication_db;\""

#ENV FLASK_APP="app:create_app()"

#ENV FLASK_RUN_HOST=0.0.0.0

#EXPOSE 5000

#COPY . .

#CMD ["flask", "run"]
