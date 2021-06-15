import json
import re
import pandas as pd
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash
from models import read_configconnection,logger
from df_sql import csv_to_table,create_table,checkTableExists
from werkzeug.utils import secure_filename
logger=logger()
auth=Blueprint("auth",__name__,template_folder="templates")
@auth.route("/")
def home():
    return render_template('home.html')

@auth.route("/login/",methods=['POST'])
def login():
    
    if request.method=='POST':
        username=request.form['uname']
        password=request.form['psw']
        mydb=read_configconnection()
        mycursor=mydb.cursor()
        print(f"SELECT * FROM web_data.user WHERE username = '{username}' ")
        mycursor.execute(f"SELECT * FROM web_data.user WHERE username = '{username}'  AND user_psw='{password}' ")
        account = mycursor.fetchone()
        if account:
            msg='account logged in'
            return render_template('home.html',msg=msg)
        else:
            msg = 'Incorrect username / password !'
            return render_template('home.html',msg=msg)
        

    

@auth.route("/register/",methods=['POST'])
def regiteration():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and "psw-repeat" in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        re_pass=request.form['psw-repeat']
        email = request.form['email']
        mydb=read_configconnection()
        mycursor=mydb.cursor()
        print(f"SELECT * FROM web_data.user WHERE username = '{username}' ")
        mycursor.execute(f"SELECT * FROM web_data.user WHERE username = '{username}'")
        account = mycursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'

        elif password!=re_pass:
            msg="password does not match with above"
        else:
            val=(username,password,email)
            print(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mycursor.execute(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mydb.commit()
            msg = 'You have successfully registered !'


    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        
    return render_template('register.html',msg=msg)
