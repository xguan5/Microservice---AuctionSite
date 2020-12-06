# Auction Site payment-service

To Deploy: 

Run the following replacing the source volume with your directory:
docker run  -v ~/development/mpcs51205-group6/payment-service/app:/service/app \
    -di -P --hostname payment --name payment -p 5011:5000 \
    --network auction-network \
    ubuntu:14.04 /bin/bash 

docker exec -it payment /bin/bash
cd /service/app

apt-get update
apt-get install python3-pip
apt-get install postgresql
apt-get install libpq-dev

pip3 install -r requirements.txt

sudo service postgresql start
sudo -u postgres psql
In postgres:
= create database payment_db;
= alter user postgres WITH password 'postgres'; 
= \q

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP="app.py"
python3 -m flask run --host="0.0.0.0"


