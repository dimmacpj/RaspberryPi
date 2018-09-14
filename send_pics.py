import smtplib
import datetime
import os, sys
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

emailTextContent = 'Pics of detected motion'
sendAddress = 'pcctsch@gmail.com'
recieveAddress = 'pcctsch@gmail.com'
emailSubject = 'Pics of detected motion!'

emailPart = MIMEMultipart()
emailPart['From'] = sendAddress
emailPart['To'] = recieveAddress
emailPart['Subject'] = emailSubject

emailPart.attach(MIMEText(emailTextContent,'plain','utf-8'))

oldDir = '/home/pi/NetgearNas'
pics = os.listdir(oldDir)
for pic in pics:
	if pic.endswith('.jpg'):
		filename = pic
		attachedPic = open(filename,'rd')
		picPart = MIMEBase('application','octet-stream')
		picPart.set_payload(attachedPic.read())
		encoders.encode_base64(picPart)
		picPart.add_header('Content-Disposition','attachedPic',filename=filename)
		emailPart.attach(picPart)
		attachedPic.close()

emailText = emailPart.as_string()

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(sendAddress,'ctswest.co.nz')

server.sendmail(sendAddress,recieveAddress,emailText)
server.quit()

newDir = '/home/pi/NetgearNas/SavedPics'
for pic in pics:
	if pic.endswith('.jpg'):
		picOldPath = oldDir + '/' + pic
		picNewPath = newDir + '/' + pic
		shutil.move(picOldPath,picNewPath)
