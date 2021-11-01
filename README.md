# Bookmyslot
Bookmyslot provides list of api's needed to perform actions inorder to book a ticket for a movie. 
Inorder to execute this project Install below libraries.
Ubuntu 16.04 : 
apt-get install python3 -y curl  
apt-get install python-dev
apt-get install python3-pip -y curl 
apt-get install mysql-server -y curl  
apt-get install libmysqlclient-dev -y curl
apt-get install curl

To install libraries required for the project use  
pip3 install Flask --no-cache-dir
pip3 install requests  --no-cache-dir
pip3 install mysqlclient --no-cache-dir
pip3 install mysql-connector-python-rf --no-cache-dir
pip3 install mysql-connector-python3 --no-cache-dir
pip3 install flask-session --no-cache-dir

To start mysql server run below command 
service mysql start &
To load the database with test data use below command by replacing file name with sql.txt
mysql -u [username] -p [database_name] < [filename].sql

To run the api script use 
python movies.apy

To test the project run below curl commands 
Find shows by city. 

curl -X POST -d "cityname=Bangalore" "http://127.0.0.1:5000/moviesbycity"

Login 


curl -X POST -d "username=<username>&password=<password>" "http://127.0.0.1:5000/login"
  
Signup 
  
  
curl -X POST -d "username=<username>&password=<password>" "http://127.0.0.1:5000/signup"
  
bookticket 
  
curl -X POST -d "schedule_id=<schedule_id>&count=<count>" "http://127.0.0.1:5000/bookticket"
  
checkavailableseats 
  
curl -X POST -d "moviesname=<moviesname>" "http://127.0.0.1:5000/checkavailableseats"
  


