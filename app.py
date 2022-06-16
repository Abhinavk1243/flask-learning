
from flask import Flask,render_template,request,redirect,url_for,session,g
from decorators import *
from models import mysl_pool_connection,logger
logger=logger()
from student import student
from auth import auth
from flask_sqlalchemy import SQLAlchemy
from admin import admin
from flask import Flask
from functools import wraps
app=Flask(__name__)
app.secret_key="Abhinav154543"

pool_cnxn=mysl_pool_connection("mysql_web_data")
mycursor=pool_cnxn.cursor()

@app.errorhandler(405)
def not_found(e):
  return render_template("405.html",error=e)

@app.errorhandler(404)
def not_found(e):
  return  render_template("404.html",error=e)

@app.errorhandler(500)
def not_found(e):
  return  render_template("500.html",error=e)

@app.before_request
def before_user():
      if request.path=="/":
        return None
      if request.path=="/auth/login/":
        return None
      if request.path=="/auth/signup/":
        return None
      if request.path=="/static/custom.css":
        return None
      if request.path=='/static/custom.js':
        return None
      if request.path=='/test/':
            return None
      if "user" not in session:
        msg="please logged in !"
        return render_template('home.html',msg=msg)

@app.route("/")
def home():
    session["platform"]="web"
    if "user" in session and "sso_id" in session:
      user=session["user"]
      sso_id = session["sso_id"]
      admin=get_roles(["Admin"])
    return render_template('home.html',**locals())
  
@app.route("/graphic_designing/" ,methods = ["GET"])
def graphic_design():
  admin=get_roles(["Admin"])
  user=session["user"]
  sso_id = session["sso_id"]
  return render_template("graphic_design.html",**locals())

@app.route("/digital_marketing/" ,methods = ["GET","POST"])
def digital_marketing():
  admin=get_roles(["Admin"])
  user=session["user"]
  sso_id = session["sso_id"]
  return render_template("digital_marketing.html",**locals())

    



app.register_blueprint(auth,url_prefix="/auth")
app.register_blueprint(admin,url_prefix="/admin")
app.register_blueprint(student,url_prefix="/student")

if __name__=="__main__":
    app.run(debug=True)