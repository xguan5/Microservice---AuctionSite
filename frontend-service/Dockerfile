FROM python:3.7-alpine



WORKDIR /frontend-service/app
COPY requirements.txt requirements.txt

RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

ENV FLASK_APP="app:create_app()"

ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000
COPY . .

#CMD ["python", "app.py"]

# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["flask", "run"]
