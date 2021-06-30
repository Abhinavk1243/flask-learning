from datetime import date
import smtplib
import pandas as pd
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from models import getconfig
from jinja2 import Environment, FileSystemLoader
enviornment_var = Environment(loader=FileSystemLoader('D:\\ashu\\GitHub\\flask-learning\\templates\\'))

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
message = MIMEMultipart('mixed')
message['From'] = getconfig("email","sender")
message['To'] = "abhinavkumar1243@gmail.com"
message['Subject'] = 'Sample mail from python'
mail_content = '''Hello, This a sample email send by Abhinav
from python using email.mime and smtp  with attachent  fot html template and plane text'''

message.attach(MIMEText(mail_content, 'plain'))
#attach_file_name = os.path.expanduser("~")+"\\flask-learning\\files\\Navigator.pdf"
#attach_file = open(attach_file_name, 'rb') 
#payload = MIMEBase('application', "octet-stream")
#payload.set_payload((attach_file).read())
#encoders.encode_base64(payload) 

#payload.add_header(
    #"Content-Disposition",
    #"attachment; filename= nav.pdf",
#)

content_data={}
data={"student":[
        {         
            "name": 'abhinav',
            "id":2,
            "age":22
        },
        {  
            "name": 'abhishek',
            "id":3,
            "age":23
        },
        {  
            "name": 'aakash',
            "id":4,
            "age":22
        }
        ],
        
}

df=pd.DataFrame.from_dict(data["student"])
content_data["student_data"]=df.to_dict("records")
content_data["columns"]=list(df.columns)
mail_template = enviornment_var.get_template('mail.html')
html = mail_template.render(content_data=content_data)

message.attach(MIMEText(html, 'html'))

#message.attach(payload)
body = message.as_string()
mail.login(getconfig("email","sender"),getconfig("email","password"))
mail.sendmail(getconfig("email","sender"), "abhinavk1236@gmail.com",body)
mail.quit()


