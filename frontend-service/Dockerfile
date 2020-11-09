FROM python:3.7-alpine
#WORKDIR /app
#ENV FLASK_APP=app/__init__.py

WORKDIR /app
ENV FLASK_APP="app:create_app()"
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]