from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from models import mysl_pool_connection,logger
import pandas as pd
import json

pool_cnxn=mysl_pool_connection("mysql_web_data")
mycursor=pool_cnxn.cursor()
logger=logger()

app = Flask(__name__)
api = Api(app)
  
class student(Resource):

    def get(self):
        sql="select * from  web_data.student "
        df=pd.read_sql(con=pool_cnxn, sql=sql)
        student = df.to_dict('records')
        response={"method":"GET","data":student,"support": {"url": "http://127.0.0.1:5000/",
                                             "text": "To return student"}}
        return jsonify(response)
  
    # Corresponds to POST request
    def post(self):
          
        try:
            # data =request.get_data()

            # print(data)
           
            # student_data= data.decode()
            student_data =request.get_json()
            mycursor=pool_cnxn.cursor()  
            student_name=student_data['student_name']
            student_age=student_data['student_age']
       

            val=(student_name,student_age)
       
            sql=f"insert into web_data.student(student_name, student_age) values {val}"
            mycursor.execute(sql)
            pool_cnxn.commit()
            logger.debug(f"data {val} successfully inserted")
       
            df=pd.read_sql(con=pool_cnxn, sql='SELECT * FROM web_data.student ORDER BY student_id DESC LIMIT 1')
            student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
            response={"method":"POST","data":student[0],"support": {"url": "http://127.0.0.1:5000/",
                                                "text": "New record created"}}
            return jsonify(response)
        except Exception as error:
            print("========================================================")
            print(error)
            logger.error(f"exception arise : {error}")
            return jsonify({"error":error}), 500
  
    def delete(self):
        mycursor=pool_cnxn.cursor()
        student_data=request.get_json(force=True)
        student_id=student_data["student_id"]
        sql=f"""select student_id,student_name,student_age from web_data.student where student_id={student_id}"""
        df=pd.read_sql(con=pool_cnxn, sql=sql)
        student = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
        if student==[]:
            error=f"student with id {student_id} not exist"
            return jsonify({"error":error}),400
        try:
            sql=f"delete from  web_data.student where student_id={student_id} "
            mycursor.execute(sql)
            pool_cnxn.commit()            
            logger.debug(f"record of id = {id} is deleted from the database")
        except Exception as error:
            logger.error(f"exception arise : {error}")
            print(f"Exception arise : {error}")
            return jsonify({"error":error}),500  
        response={"method":"DELETE","data":student[0],"support": {"url": "http://127.0.0.1:5000/",
                                             "text": "Record deleted successfully"}}           
        return jsonify(response)
    
    def put(self):
        mycursor=pool_cnxn.cursor()
        student_data=request.get_json(force=True)
        try:
            student_name=student_data["student_name"]
            student_age=student_data['student_age']
            student_id=student_data['student_id']
            logger.debug(student_id)
        except Exception as error:
            logger.error(error)
            return jsonify({"error":error})
        mycursor.execute(f"select student_id from web_data.student where student_id={student_id}")
        if mycursor.fetchone()==None:
            error=f"student with id {student_id} not exist"
            return jsonify({"error":error}),400
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
        response={"method":"PUT","data":student[0],"support": {"url": "http://127.0.0.1:5000/",
                                             "text": "Update record"}}
        return jsonify(response)
  
  
# adding the defined resources along with their corresponding urls
api.add_resource(student, '/student/')

# @app.route("/student/",methods=['GET'])
# def get_student():
#     return jsonify({"name":"abhinav"})
  
  
# driver function
if __name__ == '__main__':
  
    app.run(debug = True)