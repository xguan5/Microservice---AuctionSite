# Auction Site user-service

To Deploy: 

Run the following replacing the source volume with your directory:
docker run  -v ~/development/mpcs51205-group6/user-service-kenny/app:/service/app \
    -di -P --hostname user --name user -p 5004:5000 \
    --network auction-network \
    ubuntu:14.04 /bin/bash 

docker exec -it user /bin/bash
cd /service/app

apt-get update
apt-get install python3-pip
apt-get install postgresql
apt-get install libpq-dev

pip3 install -r requirements.txt

sudo service postgresql start
sudo -u postgres psql
In postgres:
= create database user_db;
= alter user postgres WITH password 'postgres'; 
= \q

export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP="app.py"
python3 -m flask run --host="0.0.0.0"


