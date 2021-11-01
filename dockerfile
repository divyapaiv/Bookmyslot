FROM ubuntu 

RUN apt-get update
RUN apt-get install python3 -y curl  
RUN apt-get install python-dev
RUN apt-get install python3-pip -y curl 
RUN apt-get install mysql-server -y curl  
RUN apt-get install libmysqlclient-dev -y curl  
RUN apt-get install nano
RUN pip install Flask 
RUN pip install requests 
RUN pip install mysqlclient
RUN pip install mysql-connector-python-rf
RUN pip3 install mysql-connector-python
RUN pip3 install flask-session

RUN pip3 install passlib
ADD app.py /
ADD sql.txt /
WORKDIR /

EXPOSE 5001
