import json
import pandas as pd
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session
from models import mysl_pool_connection,logger
#from df_sql import csv_to_table,create_table,checkTableExists
from werkzeug.utils import secure_filename
from functools import wraps
from decorators import required_roles,get_roles

#looger
logger=logger()

#pool connection
pool_cnxn=mysl_pool_connection()
mycursor=pool_cnxn.cursor()

#file uplaoder
upload_folder="flask-learning\\files"
allowed_extension = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv','docx'}

#make student blueprint
student=Blueprint("student",__name__,template_folder="templates")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension


@student.route("/",methods=['GET'])
@required_roles(["Admin","teacher","user"])
def student_list():    
    if request.args:            
        mycursor=pool_cnxn.cursor()
        query_params_dict=request.args.to_dict()
        sql="select * from  web_data.student " 
        no_of_cond=0
        print(query_params_dict)
        for i in list(query_params_dict.keys()):
            if no_of_cond==0:
                if (query_params_dict[i]).isalpha:
                    sql=sql+f"  where {i}='{query_params_dict[i]}' "
                else:
                    sql=sql+f" and {i}=int({query_params_dict[i]})"

                no_of_cond=1
            else:
                if (query_params_dict[i]).isalpha:
                    sql=sql+f" and {i}='{query_params_dict[i]}' "
                else:
                    sql=sql+f" and {i}=int({query_params_dict[i]})"
        try:
            mycursor.execute(sql)
            record=mycursor.fetchall()
        except Exception as error:
            return render_template("404.html",error=error)
        if record==[]:
            message=f"error :'data at {query_params_dict} not found '"
            return render_template("404.html",error=message)
        else:
            return render_template("student.html",record=record,user=session["user"],admin=get_roles(["Admin"]))         
    else:            
        mycursor=pool_cnxn.cursor()
        sql="select * from  web_data.student "
        mycursor.execute(sql)
        record=mycursor.fetchall()
        return render_template("student.html",record=record,user=session["user"],admin=get_roles(["Admin"]))
    

@student.route("/<data>",methods=["POST"])
@required_roles(["Admin"])
def create_student(data):   
    
    mycursor=pool_cnxn.cursor()    
    student_data=json.loads(data)
    student_name=student_data['student_name']
    student_age=student_data['student_age']
    val=(student_name,student_age)
        
    try:
        sql=f"insert into web_data.student(student_name, student_age) values {val}"
        mycursor.execute(sql)
        pool_cnxn.commit()
        logger.debug(f"data {val} successfully inserted")
        print("data inserted")
    except Exception as error:
        logger.error(f"exception arise : {error}")
        print(f"Exception arise : {error}")
        return render_template("404.html",error=error)
    return redirect(url_for("student.student_list"))
    

@student.route("/<int:student_id>",methods=['DELETE'])
@required_roles(["Admin"])
def remove_student(student_id):
    
    if request.method=='DELETE':        
        mycursor=pool_cnxn.cursor()
        try:
            sql=f"delete from  web_data.student where student_id={student_id} "
            mycursor.execute(sql)
            pool_cnxn.commit()            
            logger.debug(f"record of id = {id} is deleted from the database")
        except Exception as error:
            logger.error(f"exception arise : {error}")
            print(f"Exception arise : {error}")
            return render_template("404.html",error=error)                 
    return "DELETED"
    
@student.route("/studentForm/",methods=["GET"])
@required_roles(["Admin"])
def studentForm():
    if request.args:
        student_id=request.args.get('id')        
        df=pd.read_sql(con=pool_cnxn, sql=f"select * from  web_data.student where student_id={student_id}")
        record=df.to_dict('list')
        
        
        return render_template("/studentForm.html/",record=record,update=True,post=False,user=session["user"],admin=get_roles(["Admin"]))
    else:
        record={'student_name':"",'student_age':0,"student_id":0}
        return render_template("/studentForm.html/",record=record,update=True,post=False,user=session["user"],admin=get_roles(["Admin"]))

@student.route("/<data>",methods=["PUT"])
@required_roles(["Admin"])
def student_update(data): 
      
    mycursor=pool_cnxn.cursor()
    student_data=json.loads(data)
    student_name=student_data["student_name"]
    student_age=student_data['student_age']
    student_id=student_data['student_id']
    try:
        sql=f"update web_data.student set student_name='{student_name}',\
        student_age={student_age} where student_id={student_id}"
        mycursor.execute(sql)
        pool_cnxn.commit()
        print(f"Data updatated successfully")
    except Exception as error:
        print(f"error arise : {error}")
        return render_template("404.html",error=error)
    return 'updated'
    





