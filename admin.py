from flask import Blueprint,render_template,redirect,url_for,request,jsonify,flash,session
from models import mysl_pool_connection,logger
from werkzeug.utils import secure_filename
from decorators import required_roles

pool_cnxn=mysl_pool_connection()
mycursor=pool_cnxn.cursor()

admin=Blueprint("admin",__name__,template_folder="templates")

@admin.route("/",methods=["GET"])
@required_roles(["Admin"])
def admin_panel():   
    sql="select user.id,user.username,user.email_id,roles.name from web_data.user left join\
        web_data.user_roles on user.id=user_roles.user_id left join web_data.roles on user_roles.role_id =roles.id;"
    mycursor.execute(sql)
    record=mycursor.fetchall()
    return render_template("admin.html",record=record,user=session["user"])
    
@admin.route("/create_role/",methods=["POST"])
@required_roles(["Admin"])
def create_role():
    if request.method=="POST":
        username=request.form["username"]
        role_name=request.form["role"]
        
        mycursor.execute(f"select id from web_data.user where username='{username}' ")
        user_id=mycursor.fetchone() 
        if user_id==None:
            flash(f"error :'user : {username} does not exist '")
            return redirect(url_for("admin.admin_panel"))

        
        mycursor.execute(f"select id from web_data.roles where name='{role_name}' ")
        role_id=mycursor.fetchone()
        if role_id==None:
            flash(f"error 'role : {role_name} does not exist' ")
            return redirect(url_for("admin.admin_panel"))
        
        value=(user_id[0],role_id[0])
        
        mycursor.execute(f"select * from web_data.user_roles where user_id={user_id[0]} and role_id={role_id[0]}")
        if mycursor.fetchone()!=None:
            flash(f" error : 'User : {username} is already allowed this role : {role_name}'")
            return redirect(url_for("admin.admin_panel"))

        """try:
            mycursor.execute(f"insert into web_data.user_roles values {value} ")
            pool_cnxn.commit()     
        
        except Exception as error:
            flash(error)
            return redirect(url_for("admin_panel"))"""
        return redirect(url_for("admin.admin_panel"))


    return redirect(url_for("admin.admin_panel"))
    



