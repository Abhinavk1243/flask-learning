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
pool_cnxn=mysl_pool_connection("mysql_web_data")
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
    user=session["user"]
    admin=get_roles(["Admin"])
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
            student=mycursor.fetchall()
        except Exception as error:
            return jsonify({"error":error})
        if student==[]:
            message=f"error :'data at {query_params_dict} not found '"
            return jsonify({"error":message})
        else:
            if request.content_type=="application/json":
                df=pd.read_sql(con=pool_cnxn, sql=sql)
                student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
                return jsonify(student)   
            return render_template("student.html",**locals())         
    else:
        sql="select * from  web_data.student "
        if request.content_type=="application/json":
            df=pd.read_sql(con=pool_cnxn, sql=sql)
            student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
            return jsonify(student)   
        mycursor=pool_cnxn.cursor()
        mycursor.execute(sql)
        student=mycursor.fetchall()
        return render_template("student.html",**locals())
            
@student.route("/",methods=["POST"])
@required_roles(["Admin"])
def create_student():  
    student_data=request.get_json(force=True)
    mycursor=pool_cnxn.cursor()    
    try:
        student_name=student_data['student_name']
        student_age=student_data['student_age']
    except Exception as error:
        return jsonify({"error":error})

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
        return jsonify({"error":error})
    df=pd.read_sql(con=pool_cnxn, sql='SELECT * FROM web_data.student ORDER BY student_id DESC LIMIT 1')
    student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
    return jsonify(student[0])
   
@student.route("/",methods=['DELETE'])
@required_roles(["Admin"])
def remove_student():
    if request.method=='DELETE':        
        mycursor=pool_cnxn.cursor()
        student_data=request.get_json(force=True)
        student_id=student_data["student_id"]
        sql=f"""select student_id,student_name,student_age from web_data.student where student_id={student_id}"""
        df=pd.read_sql(con=pool_cnxn, sql=sql)
        student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
        if student==[]:
            error=f"student with id {student_id} not exist"
            return jsonify({"error":error})
        try:
            sql=f"delete from  web_data.student where student_id={student_id} "
            mycursor.execute(sql)
            pool_cnxn.commit()            
            logger.debug(f"record of id = {id} is deleted from the database")
        except Exception as error:
            logger.error(f"exception arise : {error}")
            print(f"Exception arise : {error}")
            return jsonify({"error":error})             
    return jsonify(student)
    
@student.route("/studentForm/",methods=["GET"])
@required_roles(["Admin"])
def studentForm():
    user=session["user"]
    admin=get_roles(["Admin"])
    if request.args:
        student_id=request.args.get('id') 
        print(student_id)       
        df=pd.read_sql(con=pool_cnxn, sql=f"select * from  web_data.student where student_id={student_id}")
        record=df.to_dict('list')
        student_id=record['student_id'][0]
        update=True
        return render_template("/studentForm.html/",**locals())
    else:
        update=False
        record={'student_name':"",'student_age':0,"student_id":0}
        return render_template("/studentForm.html/",**locals())

@student.route("/",methods=["PUT"])
@required_roles(["Admin"])
def student_update(): 
    mycursor=pool_cnxn.cursor()
    student_data=request.get_json(force=True)
    try:
        student_name=student_data["student_name"]
        student_age=student_data['student_age']
        student_id=student_data['student_id']
    except Exception as error:
        return jsonify({"error":error})
    mycursor.execute(f"select student_id from web_data.student where student_id={student_id}")
    if mycursor.fetchone()==None:
        error=f"student with id {student_id} not exist"
        return jsonify({"error":error})
    try:
        sql=f"""update web_data.student set student_name='{student_name}',
        student_age={student_age} where student_id={student_id}"""
        mycursor.execute(sql)
        pool_cnxn.commit()
        print(f"Data updatated successfully")
    except Exception as error:
        print(f"error arise : {error}")
        return jsonify({"error":error})
    df=pd.read_sql(con=pool_cnxn, sql=f'SELECT * FROM web_data.student where student_id={student_id}')
    student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
    return jsonify(student[0])