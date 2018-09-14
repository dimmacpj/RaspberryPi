import os, sys
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#define a function to get the new file name
def getFileName():
	return datetime.datetime.now().strftime('%Y%m%d%H%M%S.jpg')

#set the email address of sender, receiver and the content of subject
#set the value of email content(body)
email_send = 'pcctsch@gmail.com'
#email_send = 'dimmacpj3@sina.com'
email_receive = 'pcctsch@gmail.com'
subjects = 'Motion Detected!'
body = 'Motion deteced!!!'


#create a multipart instance, it represents the email itself
#and set the values of From, To and subject
msg = MIMEMultipart()
msg['From'] = email_send
msg['To'] = email_receive
msg['Subject'] = subjects


#create an instance of MIMEText, it represents the content of the email
#and attach the MIMEText to msg(multipart instantce)
msg.attach(MIMEText(body,'plain','utf-8'))

pics = os.listdir('/home/pi/NetgearNas')
for pic in pics:
	if pic.endswith('.avi'):
		filename = pic
		attachment = open(filename,'rb')
		part = MIMEBase('application','octet-stream')
		part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition','attachment',filename=filename)
		msg.attach(part)
'''
#add a filename which is the name of the file in the directory
filename = getFileName()
#filename = '20180909113101.jpg'
#then open the file and read it, and treat it as the attachment of the email
attachment = open(filename,'rb')
#create an MIMEBase instance, it represents the attachment
part = MIMEBase('application','octet-stream')
#payload is part of the part(MIMEBase), set the attachment to payload
part.set_payload(attachment.read())
#the use base64 to encode the part
encoders.encode_base64(part)
#add header for the MIMEBase instance, a header is what we're actually sending
part.add_header('Content-Disposition','attachment',filename=filename) 
#attach the part(MIMEBase) to the overall msg
msg.attach(part)
'''

#convert the MIMEText of th msg into a plain text string
text = msg.as_string()


#create an smtp instance for an smtp connection, 
#and then start the connection in TLS mode,
#log in on an smtp server with email address and password
server = smtplib.SMTP('smtp.gmail.com',587)
#server = smtplib.SMTP('smtp-mail.outlook.com',587)
server.starttls()
#server = smtplib.SMTP_SSL('smtp.sina.com')
server.login(email_send,'ctswest.co.nz')


#send email
#terminate smtp connection after send the email
server.sendmail(email_send,email_receive,text)
server.quit()
