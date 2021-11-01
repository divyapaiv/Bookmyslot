from flask import Flask, request, url_for, session
import mysql.connector
from mysql.connector import (connection)
import re
import requests
from flask_session import Session
from passlib.hash import sha256_crypt
app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'your secret key'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@dmin@123'
app.config['MYSQL_DB'] = 'bookmyslot'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
mysql = connection.MySQLConnection(user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'],
                              host=app.config['MYSQL_HOST'],
                              database=app.config['MYSQL_DB'])

@app.route('/moviesbycity', methods=['GET','POST'])
def moviesbycity():
    if  "cityname" in request.form :
       cursor = mysql.cursor()
       cursor.execute('SELECT * FROM MovieSchedules ms,Theatres th,Location l,SHOWTIME sh,Movies m \
            WHERE ms.Movies_ID=m.Movies_ID \
            AND ms.Theatres_ID=th.Theatres_ID \
            AND ms.SHOWTIME_ID=sh.SHOWTIME_ID\
            AND th.Location_ID=l.Location_ID\
            AND l.LocationName = "'+(cityname)+'"')
       movies = cursor.fetchall()
       print(movies)
    return(movies)

@app.route('/checkmoviesshowtime', methods=['GET','POST'])
def checkmoviesshowtime():
    if  "moviename" in request.form :
       moviename = request.form['moviename']
       cursor = mysql.cursor()
       cursor.execute('SELECT * FROM MovieSchedules ms,Theatres th,Location l,SHOWTIME sh,Movies m \
            WHERE ms.Movies_ID=m.Movies_ID \
            AND ms.Theatres_ID=th.Theatres_ID \
            AND ms.SHOWTIME_ID=sh.SHOWTIME_ID\
            AND th.Location_ID=l.Location_ID\
            AND m.Movies_Name= "'+(moviename)+'"')
       movies = cursor.fetchall()
       print(movies)
    return(movies)


@app.route('/checkavailableseats', methods=['GET','POST'])
def checkavailableseats():
    if  "schedule_id" in request.form :
       schedule_id = request.form['schedule_id']
       cursor = mysql.cursor()
       cursor.execute('SELECT ms.seats FROM MovieSchedules ms,Theatres th,Location l,SHOWTIME sh,Movies m \
            WHERE ms.Movies_ID=m.Movies_ID \
            AND ms.Theatres_ID=th.Theatres_ID \
            AND ms.SHOWTIME_ID=sh.SHOWTIME_ID\
            AND th.Location_ID=l.Location_ID\
            AND m.Schedule_id= "'+(schedule_id)+'"')
       seats = cursor.fetchall()[0]
       print(seats)
    return(seats)

@app.route('/signup', methods =['POST'])
def signup():
  msg = ''
  print(request.form.to_dict())
  print(request.method)
  print("username" in request.form.to_dict())
  print("password" in request.form.to_dict())
  if request.method == 'POST' and "username" in request.form and "password" in request.form:
    username = request.form['username']
    password = sha256_crypt.encrypt( request.form['password'])
    cursor = mysql.cursor()
    cursor.execute('SELECT * FROM Users WHERE UserName = "'+(username)+'"')
    account = cursor.fetchone()
    if account:
      msg = 'Account already exists !'
       # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
      #     msg = 'Invalid email address !'
    elif not re.match(r'[A-Za-z0-9]+', username):
      msg = 'Username must contain only characters and numbers !'
    elif not username: #or not password or not email:
      msg = 'Please fill out the form !'
    else:
      cursor.execute('INSERT INTO Users(Username,Password) VALUES (%s, %s)', (username, password))
      mysql.commit()
      msg = 'You have successfully registered !'
  elif request.method == 'POST':
    msg = 'Please fill out the form !'
    #return render_template('register.html', msg = msg)
  print(msg)
  return "<h1>"+msg+"</h1>"


@app.route('/login', methods=['GET','POST'])
def login():
  msg = ''
  print(request.form['username'])
  print(request.form['password'])
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    username = request.form['username']
    password = request.form['password']
    cursor = mysql.cursor()
    cursor.execute('SELECT * FROM Users WHERE UserName = %s', (username,))
    Users = cursor.fetchone()
    encrypted_password = Users[2]
    if Users and sha256_crypt.verify(password, encrypted_password):
      session["loggedin"] = True
      session["id"] = Users[0]
      session["username"] = Users[1]
      msg = 'Logged in successfully !'
    else:
      msg = 'Incorrect username or password !'
  print(msg)
  return "<h1>"+msg+"</h1>"

@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    msg = 'Logged out successfully !'
    print(msg)
    return "<h1>"+msg+"</h1>"
@app.route('/bookticket', methods=['GET'])
def bookticket():
    if  "schedule_id" in request.form and "count" in request.form and "username" in request.form
    and session["id"]!=null:
       schedule_id = request.form['schedule_id']
       count = int(request.form['count'])
       cursor = mysql.cursor()
       cursor.execute('SELECT ms.seats FROM MovieSchedules ms,Theatres th,Location l,SHOWTIME sh,Movies m \
            WHERE ms.Movies_ID=m.Movies_ID \
            AND ms.Theatres_ID=th.Theatres_ID \
            AND ms.SHOWTIME_ID=sh.SHOWTIME_ID\
            AND th.Location_ID=l.Location_ID\
            AND ms.Schedule_id= "'+(schedule_id)+'"')
       seats = cursor.fetchall()[0]
       if(seats>count):
            msg="<h1> The number of seats available are less than the count provided</h1>"
       elif(count<=0) :
            msg="<h1>Enter a valid number of seats</h1>"
       else 
       try:
        cursor.execute('Update INTO BookTicket(Users_ID,Schedule_id,count) VALUES (%s, %s, %d)', (session["id"],schedule_id,count))
        cursor.execute('Update INTO MovieSchedules ms set ms.seats=ms.seats-'+count+' where ms.Schedule_id='schedule_id)
        mysql.commit()
        msg="<h1>Booking is successfull</h1>"
       except:        
        mysql.rollback()
        msg=" <h1>Error occured rollbacking</h1>"
    
    elif (session["id"]==null):
         msg=" <h1>Please login to continue!</h1>"
    return(msg)

app.run()


