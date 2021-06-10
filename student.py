import json
import os
from datetime import datetime
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash
from models import read_configconnection,logger
from werkzeug.utils import secure_filename
logger=logger()
upload_folder='D:\\ashu\\GitHub\\files'
allowed_extension = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv','docx'}

student=Blueprint("student",__name__,template_folder="templates")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension

@student.route("/submit_form/")
def submit_form():
    return render_template("student_create.html")

@student.route("/",methods=['GET'])
def student_list():
    
    if request.args:
        mydb=read_configconnection()
        mycursor=mydb.cursor()
        dict_1=request.args.to_dict()
        sql="select * from  web_data.student " 
        no_of_cond=0
        for i in list(dict_1.keys()):
            if no_of_cond==0:
                sql=sql+f"  where {i}={dict_1[i]}"
                no_of_cond=1
            else:
                sql=sql+f" and {i}={dict_1[i]}"
                
        print(sql)
        try:
            mycursor.execute(sql)
            record=mycursor.fetchall()
        except Exception as error:
            return render_template("404.html",error=error)
        if record==[]:
            message=f"error :'data at {dict_1} not found '"
            return render_template("404.html",error=message)
        else:
            return render_template("student.html",record=record)
        
    else:
        mydb=read_configconnection()
        mycursor=mydb.cursor()
        sql="select * from  web_data.student "
        mycursor.execute(sql)
        record=mycursor.fetchall()
        return render_template("student.html",record=record)

@student.route("/",methods=["POST"])
def create_student():
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    if request.method=='POST':

        name=request.form["name"]
        
        if (request.form["age"]).isdigit:
            age=int(request.form["age"])

        else:
            return render_template("404.html",error="Feild age should  be a digit or numeric value not  alpa value")
        
        file=request.files['file']
        
        print(file.filename)
    
        if file and allowed_file(file.filename):
            file_name=secure_filename(file.filename)
            file.save(os.path.join(upload_folder, file_name))
        else:
            return render_template("404.html",error=f"only .txt, .pdf, .png, .jpg, .jpeg,\
                 .gif,.csv,.docx ")
        val_1=(file_name,upload_folder)
        try:
            sql_1=f"insert into web_data.files (file_name, file_location) values {val_1} "
            mycursor.execute(sql_1)
            mydb.commit()
        except Exception as error:
            logger.error(f"exception arise : {error}")
            print(f"Exception arise : {error}")     

        val=(name,age)
    
    try:
        sql=f"insert into web_data.student(student_name, student_age) values {val}"
        mycursor.execute(sql)
        mydb.commit()
        logger.debug(f"data {val} successfully inserted")
        print("data inserted")

    except Exception as error:
        logger.error(f"exception arise : {error}")
        print(f"Exception arise : {error}")
        return render_template("404.html",error=error)

    finally:
        mydb.close()
    
    return redirect(url_for("student.student_list"))


@student.route("/<int:id>",methods=['DELETE'])
def remove_student(id):
    if request.method=='DELETE':
        mydb=read_configconnection()
        mycursor=mydb.cursor()


        try:
            sql=f"delete from  web_data.student where student_id={id} "
            mycursor.execute(sql)
            mydb.commit()
            
            logger.debug(f"record of id = {id} is deleted from the database")

        except Exception as error:
            logger.error(f"exception arise : {error}")
            print(f"Exception arise : {error}")
            return render_template("404.html",error=error)

        finally:
            mydb.close()
        
    return "OK"

@student.route("/update_form/<data>")
def update_form(data):
    print("----------------------------")
    print("----------------------------")
    data=json.loads(data)
    name=data['name']
    age=data['age']
    id=data['id']
    
    return render_template("/update_form.html/",name=name,id=id,age=age)


@student.route("/<data>",methods=["PUT"])
def student_update(data):
    mydb=read_configconnection()
    mycursor=mydb.cursor()
    data=json.loads(data)
    s_name=data["s_name"]
    age=data['age']
    student_id=data['id']

    
    
    try:
        sql=f"update web_data.student set student_name='{s_name}',\
        student_age={age} where student_id={student_id}"
        mycursor.execute(sql)
        mydb.commit()
        print(f"Data updatated successfully")
    except Exception as error:
        print(f"error arise : {error}")
        return render_template("404.html",error=error)
    finally:
        mydb.close()
    
    
    return 'updated'
    




