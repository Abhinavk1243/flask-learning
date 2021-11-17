import json
import hashlib
import re
import pandas as pd
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session,g
from models import mysl_pool_connection,logger
from werkzeug.utils import secure_filename
from decorators import *
logger=logger()

upload_folder="flask-learning\\files"
allowed_extension = {'png', 'jpg', 'jpeg'}


def get_user(username):
    sql=f"""select user.ID,user.username,user.password,group_concat(roles.name SEPARATOR "," )
            roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
            left join web_data.roles on user_roles.role_id=roles.id  WHERE username = '{username}'  """
    mycursor.execute(sql) 
    account = mycursor.fetchone()
    session['role']=account[3].split(",")
    session['loggedin']=True
    session['user']=username  
    session["sso_id"] = account[0]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension

pool_cnxn=mysl_pool_connection("mysql_web_data")
mycursor=pool_cnxn.cursor()

auth=Blueprint("auth",__name__,template_folder="templates")

@auth.route("/login/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql=f"""select user.ID,user.username,user.password,group_concat(roles.name SEPARATOR "," )
        roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
        left join web_data.roles on user_roles.role_id=roles.id  WHERE username = '{username}' 
        and password =MD5('{password}') """
        mycursor.execute(sql) 
        account = mycursor.fetchone()
        
        if None not in account:
            session['role']=account[3].split(",")
            session['loggedin']=True
            session['user']=username  
            session["sso_id"] = account[0]
            if request.content_type=="application/json":
                return jsonify({"response":"user logged in !"})
            flash("user logged in !")
            return redirect(url_for("student.student_list"))
        else:
            if "user" in session:
                return redirect(url_for('student.student_list'))     
            if request.content_type=="application/json":
                return jsonify({"response":"invalid login credentials !"})
            flash("invalid login credential")
            
            return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))
    
        
@auth.route("/logout/",methods=['GET'])
def logout():
    session.pop('loggedin', None)
    session.pop("user",None)
    # flash("Logged out successfully")
    return redirect(url_for("home"))
    
@auth.route("/signup/",methods=['POST','GET'])
def signup():
    if "user" in session:
        
        user=session["user"]
        get_user(user)
        # admin=get_roles(["Admin"])
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        password=bytes(request.form['password'],'utf-8')
        pass_hash = hashlib.md5()
        pass_hash.update(password)
        password=pass_hash.hexdigest()
        email_id = request.form['email']
        file = request.files['profile_pic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.path.expanduser("~"),upload_folder, filename))
        else:
            msg=f"extensions does not match with {allowed_extension}"
            return render_template('signup.html',msg=msg)  

        filename = secure_filename(file.filename)
        mycursor.execute(f"SELECT username,id FROM web_data.user WHERE username = '{username}'")
        account = mycursor.fetchone()
        mycursor.execute(f"SELECT * FROM web_data.user WHERE email_id= '{email_id}'")
        email_registered = mycursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif email_registered:
            msg = 'Email id already registered !'
        else:
            val=(username,password,email_id)
            mycursor.execute(f'INSERT INTO web_data.user( username, password , email_id) VALUES {val}')
            pool_cnxn.commit()
            mycursor.execute(f"select id from web_data.user where username='{username}' ")
            user_id=mycursor.fetchone()
            val=(filename,upload_folder,user_id[0])
            mycursor.execute(f'insert into web_data.user_profile_pic (file_name,file_location,user_id) VALUES {val}')
            pool_cnxn.commit()
            mycursor.execute(f'insert into web_data.user_roles values ({user_id[0]},2)')
            pool_cnxn.commit()
            msg = 'You have successfully registered !'
            session['user']=username  
            if request.content_type=="application/json":
                df=pd.read_sql(con=pool_cnxn, sql=f"""SELECT user.Id,user.username,user.email_id, group_concat(roles.name 
                SEPARATOR "," )roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
                left join web_data.roles on user_roles.role_id=roles.id where user.username='{username}' """)
                user=df.to_dict(orient="records")
                user_detail=user[0]
                user_detail["file_name"]==filename
                response={"message":"you are successfull registered !","user_detail":user}
                # flash("user successfully registered !")
                return jsonify(response)
            signup = True
            
            sql=f"""select user.ID,user.username,user.password,group_concat(roles.name SEPARATOR "," )
            roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
            left join web_data.roles on user_roles.role_id=roles.id  WHERE username = '{username}' 
            """
            mycursor.execute(sql) 
            account = mycursor.fetchone()
            session['role']=account[3].split(",")
            session['loggedin']=True
            session['user']=username  
            session["sso_id"] = account[0]
            
            return redirect(url_for('student.student_list'))   
        return render_template('signup.html',msg=msg,**locals())
    else:
        return render_template('signup.html',**locals())