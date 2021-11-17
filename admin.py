from configparser import MAX_INTERPOLATION_DEPTH
from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session
import smtplib
import json
import pandas as pd
from models import mysl_pool_connection,logger
from werkzeug.utils import secure_filename
from decorators import required_roles,get_roles
logger=logger()
pool_cnxn=mysl_pool_connection("mysql_web_data")
mycursor=pool_cnxn.cursor()
admin=Blueprint("admin",__name__,template_folder="templates")

@admin.route("/",methods=["GET"])
@required_roles(["Admin"])
def admin_panel():   
    admin=get_roles(["Admin"])
    sql="""SELECT user.Id,user.username,user.email_id, group_concat(roles.name SEPARATOR "," )
    roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
    left join web_data.roles on user_roles.role_id=roles.id GROUP BY  user.username"""
    if request.content_type=="application/json":
        df=pd.read_sql(con=pool_cnxn, sql=sql)
        user_roles = [{col:getattr(row, col) for col in df} for row in df.itertuples()]
        return json.dumps(user_roles)
    else:
        user=session["user"]
        mycursor.execute(sql)
        sso_id = session["sso_id"]
        record=mycursor.fetchall()
        return render_template("admin.html",**locals())

@admin.route("/user_role_form/",methods=["GET"])
@required_roles(["Admin"])
def user_role_form():
    admin=get_roles(["Admin"])
    user=session["user"]
    sso_id = session["sso_id"]
    sql="select roles.name from web_data.roles"
    mycursor.execute(sql)
    roles=mycursor.fetchall()
    sql="""SELECT user.Id,user.username,user.email_id, group_concat(roles.name SEPARATOR "," )
        roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
        left join web_data.roles on user_roles.role_id=roles.id GROUP BY  user.username"""
    mycursor.execute(sql)
    users=mycursor.fetchall()
    
    if request.args:
        
        user_id=request.args['user_id']
        create=False
        user_role=users[3]
        username=users[1]
        return render_template("create_user_role.html",**locals())
    create=True
    return render_template("create_user_role.html",**locals())
    
@admin.route("/create_role/",methods=["POST"])
@required_roles(["Admin"])
def create_role():
    
    user_new_roles=request.get_json(force=True)
    username=user_new_roles["username"]
    print(username)
    mycursor.execute(f"select id from web_data.user where username='{username}' ")
    user_id=mycursor.fetchone() 
    roles=user_new_roles["roles"]
    user_new_roles=user_new_roles["roles"].split(",")
     
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
        message=f'user {username} already assigned by {roles} roles'
        return json.dumps({'error':True,'message':message})
    
    # value for insert many in user_role table
    values=[]
    for new_role_id in valid_role_id:
        values.append((user_id[0],new_role_id))
    
    try:
        sql=f"INSERT INTO web_data.user_roles  VALUES (%s,%s) "           
        mycursor.executemany(sql,values)
        pool_cnxn.commit()   
        logger.debug(f"{values} is inserted in user_roles table")
    except Exception as error:
        logger.error(f"error arise : {error}")
        return json.dumps({'error': True,'message':error})
    df=pd.read_sql(con=pool_cnxn, sql=f"""SELECT user.Id,user.username,user.email_id, group_concat(roles.name 
    SEPARATOR "," )roles FROM web_data.user left join web_data.user_roles  ON user.id = user_roles.user_id 
    left join web_data.roles on user_roles.role_id=roles.id where user.id={user_id[0]}""")
    user=[{col:getattr(row, col) for col in df} for row in df.itertuples()]
    
    return json.dumps({'error':False ,"user":user[0]})
    
# @admin.route("/sendmail/",methods=["GET"])
# def send_mail():
#     mail = smtplib.SMTP('smtp.gmail.com', 587)
#     mail.starttls()
#     mail.login("abhinavflasklearning@gmail.com", "abhinav@12")
#     message = "testing message , this ,message is sent by using python"
#     mail.sendmail("abhinavflasklearning@gmail.com", "abhinavkumar1243@gmail.com", message)
#     mail.quit()
#     return jsonify({"sender":"abhinavflasklearning","receiver":"abhinavkumar1243"})



