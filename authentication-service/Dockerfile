#FROM python:3.7-alpine

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

FROM python:3.7-alpine

WORKDIR /authentication-service/app
COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

ENV FLASK_APP="app:create_app()"

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .

CMD ["flask", "run"]
