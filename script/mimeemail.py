#import os, sys, re, time, commands, glob
import os
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

def send_mail(DQMMon, Text = None, isSMS = False, attachement=None):

	COMMASPACE = ', '


	emailmessage = "Alarm from Online DQM\n Run:   "+ str(DQMMon.runinfo['run']) +"\n LumiSection:  "+str(DQMMon.runinfo['lumi']) +"\n Beam Mode:  "+str(DQMMon.runinfo['beamMode'])+"\n Numer of Dead ROC: "+str(DQMMon.dead_value)+"\n DataPresent: True"

	server = "localhost"
	#me = 'cctrack@mail.cern.ch'
	me = 'gflouris@cern.ch'
    #### List of emails that receive this email
	#topeople = ['threus@cern.ch','cms-tracker-doc@cern.ch','francesco.palmonari@cern.ch','mia.tosi@cern.ch','erik.butz@cern.ch','Christian.Barth@cern.ch']
	
	topeople = ['gflouris@cern.ch']

	if( isSMS ):
		topeople = ['0041764875503@mail2sms.cern.ch', '0041764872389@mail2sms.cern.ch']


	msg = MIMEMultipart()
	msg['From'] = me
	msg['To']   = COMMASPACE.join(topeople)
	msg['Subject'] = 'TKDoc Notification: RUN ' + str(DQMMon.runinfo['run'])	
	
	if(Text!=None):
		msg['Subject'] = "TKDoc Notification - Application stopped."
		emailmessage = Text


	msg.attach( MIMEText(emailmessage) )


	if (attachement != None and isSMS==False):
		part = MIMEBase('application', "octet-stream")
		part.set_payload( open(attachement,"rb").read() )
		Encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachement))
		msg.attach(part)

	smtp = smtplib.SMTP(server)
	smtp.sendmail(me, topeople, msg.as_string())
	smtp.close()

