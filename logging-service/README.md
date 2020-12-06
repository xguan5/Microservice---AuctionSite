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

# Logging Service
docker run  -v ~/development/mpcs51205-group6/logging-service/app:/service/app \
    -di -P --hostname logging --name logging -p 6010:5000 \
    --network auction-network \
    ubuntu:14.04 /bin/bash 

docker exec -it logging /bin/bash
cd /service/app
sudo apt-get update

# Start Mongo
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 0C49F3730359A14518585931BC711F9BA15703C6
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | tee /etc/apt/sources.list.d/mongodb.list
apt-get install mongodb
sudo apt-get install mongodb-org
sudo service mongodb start

# Start Flask
apt-get install python3-pip
pip3 install -r requirements.txt
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP="app.py"

python3 -m flask run --host="0.0.0.0"