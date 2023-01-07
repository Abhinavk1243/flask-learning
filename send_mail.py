import smtplib
import pandas as pd
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from models import getconfig
from jinja2 import Environment, FileSystemLoader


def send_mail(receivers_email,mail_content,subject=None,files_name=None,data=None,html_template=None,image=None):
    """Method for sending emails to multiple email addrss ,with multiple attachments and html template

    Args:
        receivers_email (list): list of receivers email id
        mail_content (string ): content for mail
        subject (string, optional): subject for email . Defaults to None.
        files_name (list, optional): list of attachments file(pdf ,docx ,png  files etc). Defaults to None.
        data (dictonary, optional): dictonary in the form of json dict for render data in html table. Defaults to None.
        html_template (file, optional): file name of html template want ot send without .html extension  . Defaults to None.
    """
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.starttls()
    message = MIMEMultipart('mixed')
    message['From'] = getconfig("email","sender")
    message['To'] = ",".join([str(i) for i in receivers_email])
    message['Subject'] = subject
    message.attach(MIMEText(mail_content, 'plain'))
    if image is not None:
        img_file_path=os.path.expanduser("~")+f"\\flask-learning\\files\\{image}"
        img = open(img_file_path, 'rb')
        msgImage = MIMEImage(img.read())
        img.close()
        msgImage.add_header('Content-ID', f'<{image}>')
        msgText = MIMEText(f"<br><img src='{img_file_path}'><br>", 'html')
        message.attach(msgText)
        message.attach(msgImage)
    
    if files_name is not None:
        
        for files in files_name:
            attach_file_name = os.path.expanduser("~")+f"\\flask-learning\\files\\{files}"
            attach_file = open(attach_file_name, 'rb')
            payload = MIMEBase('application', "octet-stream")
            payload.set_payload((attach_file).read())
            encoders.encode_base64(payload) 

            payload.add_header(
                "Content-Disposition",
                f"attachment; filename= {files}",
            )
            message.attach(payload)

    if html_template is not None:
        enviornment_var = Environment(loader=FileSystemLoader('templates/'))
        content_data={}
        df=pd.DataFrame.from_dict(data["student"])
        content_data["student_data"]=df.to_dict("records")
        content_data["columns"]=list(df.columns)
        mail_template = enviornment_var.get_template(f"{html_template}.html")
        html = mail_template.render(content_data=content_data)
        message.attach(MIMEText(html, 'html'))

    body = message.as_string()
    mail.login(getconfig("email","sender"),getconfig("email","password"))
    mail.sendmail(getconfig("email","sender"), receivers_email,body)
    mail.quit()

def main():
    mail_content='''Hello, This a sample email send by Abhinav from python using
                    email.mime and smtp with multiple attachent  '''
    subject='Sample mail from python'
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
    html_template="mail"
    # files_name=["log_file.log"]
    receivers_email=["abhinavkumar1243@gmail.com"]
    # image="sharecare.png"
    send_mail(receivers_email,mail_content,subject=subject,html_template=html_template,data=data)
if __name__=="__main__":
    main()