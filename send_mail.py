import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from models import getconfig

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
message = MIMEMultipart()
message['From'] = getconfig("email","sender")
message['To'] = "abhinavkumar1243@gmail.com"
message['Subject'] = 'A test mail sent by Python. It has an attachment.'
mail_content = '''Hello, This is a test mail. In this mail we are sending some attachments.The mail 
is sent using Python SMTP library.Thank You'''

message.attach(MIMEText(mail_content, 'plain'))
attach_file_name = os.path.expanduser("~")+"\\flask-learning\\files\\Navigator.pdf"
attach_file = open(attach_file_name, 'rb') 
payload = MIMEBase('application', "octet-stream")
payload.set_payload((attach_file).read())
encoders.encode_base64(payload) 

payload.add_header(
    "Content-Disposition",
    "attachment; filename= nav.pdf",
)

message.attach(payload)
text = message.as_string()
mail.login(getconfig("email","sender"),getconfig("email","password"))
mail.sendmail(getconfig("email","sender"), "abhinavkumar1243@gmail.com", text)
mail.quit()


