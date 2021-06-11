
from flask import Flask,render_template,request,redirect,url_for
from models import logger
logger=logger()
from student import student
from flask import Flask
app=Flask(__name__)

@app.errorhandler(405)
def not_found(e):
  return render_template("405.html",error=e)

@app.errorhandler(404)
def not_found(e):
  return  render_template("404.html",error=e)

@app.errorhandler(500)
def not_found(e):
  return  render_template("500.html",error=e)


app.register_blueprint(student,url_prefix="/student")
@app.route("/")
def info():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)