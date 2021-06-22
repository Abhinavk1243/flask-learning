import json
import hashlib
import re
import pandas as pd
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session,g
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
        sql=f"select user.username,user.password,roles.name from web_data.user cross join web_data.user_roles\
            on user.id=user_roles.user_id cross join web_data.roles on user_roles.role_id =roles.id \
            WHERE username = '{username}'  and password =MD5('{password}') "
        mycursor.execute(sql) 
        account = mycursor.fetchall()
        
        if account:
            role_list=[]
            if len(account)>1:
                for i in account:
                    role_list.append(i[-1])
                    session['role']=role_list
            else:
                session['role']=[account[0][-1]]
            session['loggedin']=True
            session['user']=username  
            
            return redirect(url_for("student.student_list"))
        else:
            if "user" in session:
                return redirect(url_for('student.student_list'))     
            msg="invalid login credential"
            return render_template('home.html',msg=msg)
    else:
        return redirect(url_for("home"))
    
        
@auth.route("/logout/",methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop("user",None)
    flash("Logged out success fully")
    return redirect(url_for("home"))
    
@auth.route("/signup/",methods=['POST','GET'])
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        re_pass=request.form["re-password"]
        email_id = request.form['email']
        mycursor.execute(f"SELECT * FROM web_data.user WHERE username = '{username}'")
        account = mycursor.fetchone()
        mycursor.execute(f"SELECT * FROM web_data.user WHERE email_id= '{email_id}'")
        email_registered = mycursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif email_registered:
            msg = 'Email id already registered !'
        else:
            """val=(username,password,email_id)
            print(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mycursor.execute(f'INSERT INTO web_data.user( username, user_psw, email_id) VALUES {val}')
            mydb.commit()"""
            msg = 'You have successfully registered !'
        return render_template('signup.html',msg=msg)   
    else:
        return render_template('signup.html',msg=msg)


"""m = hashlib.md5()
m.update(b"abhi12")
print (m.hexdigest())"""