import json
import re
import pandas as pd
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session
from models import mysl_pool_connection,logger
from werkzeug.utils import secure_filename
logger=logger()

mydb=mysl_pool_connection()
mycursor=mydb.cursor()

auth=Blueprint("auth",__name__,template_folder="templates")


@auth.route("/login/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['psw']
        mycursor.execute(f"select * from web_data.user WHERE username = '{username}'  and password ='{password}' ")
        account = mycursor.fetchone()
        if account:
            session['loggedin']=True
            session['user']=username            
            return redirect(url_for("student.student_list"))
        else:
            if "user" in session:
                return redirect(url_for('student.student_list'))

            msg = 'Incorrect username / password !'
            return render_template('home.html',msg=msg)
    else:
        return redirect(url_for("home"))
        
@auth.route("/logout/",methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop("user",None)
    return redirect(url_for("home"))
    
@auth.route("/signup/",methods=['POST'])
def regiteration():
    msg_reg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        re_pass=request.form['psw_repeat']
        email_id = request.form['email']
        mycursor.execute(f"SELECT * FROM web_data.user WHERE username = '{username}'")
        account = mycursor.fetchone()
        mycursor.execute(f"SELECT * FROM web_data.user WHERE email_id= '{email_id}'")
        email_registered = mycursor.fetchone()
        if account:
            msg_reg = 'Account already exists !'
        elif email_registered:
            msg_reg = 'Email id already registered !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            msg_reg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg_reg= 'Username must contain only characters and numbers !'
        elif not username or not password or not email_id:
            msg_reg = 'Please fill out the form !'

        elif password!=re_pass:
            msg_reg="password does not match with above"
        else:
            """val=(username,password,email_id)
            print(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mycursor.execute(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mydb.commit()"""
            msg_reg = 'You have successfully registered !'
        
    return render_template('home.html',msg_reg=msg_reg)
