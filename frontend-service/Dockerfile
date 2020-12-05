FROM python:3.7-alpine

WORKDIR /app
COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev postgresql-contrib postgresql
RUN pip install -r requirements.txt

ENV FLASK_APP="app:create_app()"

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .

CMD ["flask", "run"]
