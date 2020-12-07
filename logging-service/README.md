# Auction Site logging-service

To Deploy: 

# RabbitMQ
docker run -d --hostname messaging --network auction-network --name messaging -p 15672:15672 -p 5672:5672 rabbitmq:3-management 
docker exec -it messaging /bin/bash
apt-get update
apt-get install -y procps
apt-get install -y vim
apt-get install -y net-tools
apt-get install -y openssh-client

# Mongo DB
Run the following replacing the source volume with your directory:
docker run  -v ~/development/mpcs51205-group6/logging-service/db:/service/db \
    -di -P --hostname mongo_db --name mongo_db -p 27017:27017 \
    --network auction-network \
    mongo

docker exec -it mongo_db mongo
use logging_db

# Logging Service
Run the following replacing the source volume with your directory:
docker run  -v ~/development/mpcs51205-group6/logging-service/app:/service/app \
    -di -P --hostname logging --name logging -p 6010:5000 \
    --network auction-network \
    python:3 /bin/bash 

docker exec -it logging /bin/bash
cd /service/app
apt-get update

# Start Flask
pip install -r requirements.txt
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP="app.py"

python -m flask run --host="0.0.0.0"




