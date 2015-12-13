import webiopi
import subprocess
import RPi.GPIO as GPIO_PY
import os
import glob
import time
import sys
import smtplib
GPIO = webiopi.GPIO

PIR = 17 # GPIO pin using BCM numbering
from email.mime.text import MIMEText 

motion = False
# setup function is automatically called at WebIOPi startup
def setup():
    # set the GPIO used by the light to output
    GPIO.setFunction(PIR, GPIO.IN)

# loop function is repeatedly called by WebIOPi 
def loop():
    # retrieve current datetime
	global motion
	if GPIO.digitalRead(PIR):
		if motion == False:
			print("Motion Detected")
			SendEmail("Motion Detected!")
			motion = True
	else:
		motion = False
	webiopi.sleep(1)

# destroy function is called at WebIOPi shutdown
def destroy():
    GPIO.digitalWrite(PIR, GPIO.LOW)

def SendEmail(MessageText): 
	#enter the e-mail account username between the quotes 
	smtp_user = "raspi.arduino.bbb"
	#enter the e-mail account password between the quotes
	smtp_pass = "raspberryarduino" 
	#sys.argv[1] is the 1st parameter that is passed to #this program and it contains the text for the body #of the e-mail 
	msg = MIMEText(MessageText) 
	#enter the target e-mail address between the quotes 
	msg['To'] = "captanwaar@gmail.com" #enter the e-mail account username between the quotes 
	msg['From'] = "raspi.arduino.bbb" #enter the message subject between the quotes 
	msg['Subject'] = "Motion Detection Alert" #enter the SMTP server URL or IP Address between the quotes 
	s = smtplib.SMTP_SSL("smtp.gmail.com", 465)
	s.login(smtp_user,smtp_pass)
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()
	
@webiopi.macro
def shutDown():
	subprocess.call(["sudo","shutdown","-h","now"])	