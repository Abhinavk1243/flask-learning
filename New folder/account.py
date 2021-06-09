from flask import Blueprint,render_template,redirect,url_for,request
from models import read_configconnection,logger
logger=logger()
acc_bp=Blueprint("acc_bp",__name__)

@acc_bp.route('/')
def index():
    return render_template("view.html")

@acc_bp.route('/registeration')
def registeration():
    return render_template("registeration.html")

@acc_bp.route('/login')
def login():
    return render_template("student_login.html")

