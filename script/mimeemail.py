#!/usr/bin/env python -u

import os, sys, re, time, commands, glob
from optparse import OptionParser, OptionGroup
from threading import Thread
import random
import smtplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email import Encoders

def send_mail(attachement):

	emailmessage = open("ReportFromOnlineDQM.txt","r").read()
	runnumber = open("reference.txt","r").readline()
	COMMASPACE = ', '

	server = "localhost"
	#        me = 'cctrack@mail.cern.ch'
	#        me = 'threus@cern.ch'
	me = 'gflouris@cern.ch'
#### 2012 operation
#	topeople = ['threus@cern.ch','cms-tracker-doc@cern.ch','francesco.palmonari@cern.ch','borrell@mail.cern.ch','lino.demaria@cern.ch','mia.tosi@cern.ch','erik.butz@cern.ch']
#### 2013 commissioning
#	topeople = ['threus@cern.ch','cms-tracker-doc@cern.ch','francesco.palmonari@cern.ch','mia.tosi@cern.ch','erik.butz@cern.ch','Christian.Barth@cern.ch']
#### 201 AGR
#	topeople = ['threus@cern.ch','cms-tracker-doc@cern.ch','francesco.palmonari@cern.ch','erik.butz@cern.ch','Christian.Barth@cern.ch']
### TESTING
	#topeople = ['threus@cern.ch']
	topeople = ['gflouris@cern.ch']
	msg = MIMEMultipart()
	msg['From'] = me
	msg['To']   = COMMASPACE.join(topeople)
	#	msg['To']   = me
	msg['Subject'] = 'TKDoc Notification: RUN ' + str(runnumber)

	msg.attach( MIMEText(emailmessage) )

	isnewbadmodule = os.path.getsize('tkmap_bm_input.txt')

	if int(isnewbadmodule) > 0:
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(attachement,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachement))
		msg.attach(part)

#        fp = open(attachement, 'rb')
#	img = MIMEImage(fp.read())
#	fp.close()
#	msg.attach(img)


	smtp = smtplib.SMTP(server)
	#        smtp.sendmail(me, [me], msg.as_string())
	smtp.sendmail(me, topeople, msg.as_string())
	smtp.close()


ifile_checkemail = open("sendemail.txt","r")
emailtosend = ifile_checkemail.readline()
print(emailtosend)
if int(emailtosend) == 1:
	send_mail('newbadmodules_tkmap.png')
