FROM python:3.7-alpine
#WORKDIR /app
#ENV FLASK_APP=app/__init__.py

WORKDIR /app
ENV FLASK_APP="app:create_app()"
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000

ENV POSTGRES_DB authentication
COPY database_schema.sql /docker-entrypoint-initdb.d/

COPY . .
CMD ["flask", "run"]