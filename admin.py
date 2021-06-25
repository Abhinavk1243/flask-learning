from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session
import json
import pandas as pd
from models import mysl_pool_connection,logger
from werkzeug.utils import secure_filename
from decorators import required_roles

pool_cnxn=mysl_pool_connection()
mycursor=pool_cnxn.cursor()
admin=Blueprint("admin",__name__,template_folder="templates")

@admin.route("/",methods=["GET"])
@required_roles(["Admin"])
def admin_panel():   
    sql="""SELECT user.Id,user.username,user.email_id, group_concat(roles.name SEPARATOR "," )
    roles FROM web_data.user cross join web_data.user_roles  ON user.id = user_roles.user_id 
    cross join web_data.roles on user_roles.role_id=roles.id GROUP BY user_roles.user_id """
    mycursor.execute(sql)
    record=mycursor.fetchall()
    return render_template("admin.html",record=record,user=session["user"])

@admin.route("/user_role_form/",methods=["GET"])
@required_roles(["Admin"])
def user_role_form():
    sql="select roles.name from web_data.roles"
    mycursor.execute(sql)
    roles=mycursor.fetchall()
    if request.args:
        user_id=request.args['user_id']
        return render_template("create_user_role.html",create=False,edit=True,roles=roles)
    return render_template("create_user_role.html",create=True,edit=False,roles=roles)
    
@admin.route("/create_role/",methods=["POST"])
@required_roles(["Admin"])
def create_role():
    user_new_roles=request.get_json(force=True)
    username=user_new_roles["username"]
    mycursor.execute(f"select id from web_data.user where username='{username}' ")
    user_id=mycursor.fetchone() 

    # check user exist or not
    if user_id==None:
        message=f"user : {username} does not exist "
        return json.dumps({'error': True,'message':message})
    roles=user_new_roles["role"]
    
    user_new_roles=user_new_roles["role"].split(",")
     
    # fetch role_id of user input role name
    role_id=[]
    sql=f"select id from web_data.roles where name='{user_new_roles[0]}' "
    mycursor.execute(sql)
    role_id.append(mycursor.fetchone()[0])
    if len(user_new_roles)>1:
        for i in range(1,len(user_new_roles)):
            sql=f"select id from web_data.roles where name='{user_new_roles[i]}' "
            mycursor.execute(sql)
            role_id.append(mycursor.fetchone()[0])
    
    # role_id which is not assigned to the user from user input roles
    valid_role_id=[]
    for i in role_id:
        sql=f"select user_id from web_data.user_roles where user_id={user_id[0]} and role_id ={i}  "
        mycursor.execute(sql)
        isuser_have_role=mycursor.fetchone()
        if isuser_have_role==None:
            valid_role_id.append(i) 
    if len(valid_role_id)==0:
        message=f"user {username} already assigned by {roles} roles "
        return json.dumps({'error': True,'message':message})
    
    # value for insert many in user_role table
    values=[]
    for new_role_id in valid_role_id:
        values.append((user_id[0],new_role_id))
    
    try:
        sql=f"INSERT INTO web_data.user_roles  VALUES (%s,%s) "           
        mycursor.executemany(sql,values)
        pool_cnxn.commit()   
    except Exception as error:
        return json.dumps({'error': True,'message':error})
    df=pd.read_sql(con=pool_cnxn, sql=f"""SELECT user.Id,user.username,user.email_id, group_concat(roles.name 
    SEPARATOR "," )roles FROM web_data.user cross join web_data.user_roles  ON user.id = user_roles.user_id 
    cross join web_data.roles on user_roles.role_id=roles.id where user.id={user_id[0]}""")
    user=df.to_dict('r')
    return json.dumps({'error': False ,"user":user})
    
@admin.route("/",methods=["PUT"])
@required_roles(["Admin"])
def edit_user_role():
    return "pass"



