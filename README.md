Auction service for group 6. Each top level directory contains a microservice. See the readme in each service for instructions to run that service

Iteration Three Instructions:

1) Deploy user-service
	- In terminal navigate to user-service directory
	- docker-compose up -d 
	- docker start user-service_web_1 --attach
	- Note the IP address

2) Edit front end
	- in frontend-service/app/user_client, change the "user_service_ip" variable to the value from above. We are working on a better way to handle this

3) Deploy front end
	- In terminal navigate to frontend-service directory
	- docker-compose up -d 
	- docker start frontend-service_web_1 --attach
	- In browser, naviagate to http://127.0.0.1:5080/home

You will see a list of users returned from the user service


For tests, go to a microservice directory, and setup a virutal environment, installing the packages from requirements.txt. Actvate the virtualenv,  export PYTHONPATH="$PYTHONPATH:"your path". And then run the command pytest