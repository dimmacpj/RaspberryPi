import smtplib
import datetime
import os, sys
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

emailTextContent = 'Frontyard of detected motion'
sendAddress = 'pcctsch@gmail.com'
recieveAddress = 'pcctsch@gmail.com'
emailSubject = 'Frontyard detected motion!'

emailPart = MIMEMultipart()
emailPart['From'] = sendAddress
emailPart['To'] = recieveAddress
emailPart['Subject'] = emailSubject

emailPart.attach(MIMEText(emailTextContent,'plain','utf-8'))

oldDir = '/home/pi/Pictures'
pics = os.listdir(oldDir)
for pic in pics:
	if pic.endswith('.jpg') or pic.endswith('.avi'):
		filename = pic
		os.chdir('/home/pi/Pictures')
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

'''newDir = '/home/pi/NetgearNas/SavedPics'
for pic in pics:
	if pic.endswith('.jpg'):
		picOldPath = oldDir + '/' + pic
		picNewPath = newDir + '/' + pic
		filePic = open(pic,'rd')
		filePic.close()
		shutil.copy(picOldPath,picNewPath)
'''
os.system('sudo cp *.jpg /home/pi/NetgearNas')
os.system('sudo cp *.avi /home/pi/NetgearNas')
os.system('sudo rm *.avi')
os.system('sudo rm *.jpg')
