# def add(num1,num2):
#     return num1+num2

from models import mysl_pool_connection
import pandas as pd
import json
import requests

conn=mysl_pool_connection("mysql_web_data")

def get_user():
    res=requests.get("https://reqres.in/api/users")
    return res.json



def get_user_data():
    sql="""select * from web_data.student"""
    user_df=pd.read_sql(sql=sql,con=conn)
    user_df["date_created"]= pd.to_datetime(user_df["date_created"]) 
    user_df["date_created"]=user_df["date_created"].dt.strftime('%Y-%m-%d')
    user_json=user_df.to_dict("records")
    # return user_json
    
    return json.dumps(user_json)
    
    
    
# print(get_user_data())