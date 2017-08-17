#!/usr/bin/env python
import datetime
import time
import os
import sys
#import checkOnlineDQM_Run2
import sqlite3
from mimeemail import *
from utils import WriteOut

conn = sqlite3.connect('logbook.db')
dbcursor = conn.cursor()


itr = 0
run_proc = 0

WriteOut("Monitoring service")
while True:



	os.system("python checkOnlineDQM_Run2.py")

	dbcursor.execute("SELECT * FROM processed_runs ORDER BY id DESC LIMIT 1")
	result = dbcursor.fetchone()

	if(result!=None):
		if(run_proc!=result[2]):
			run_proc = result[2]
			WriteOut("Proceesing run: "+str(result[2]))


	###Checks to avoid spam
	now = datetime.datetime.now()
	onehour = datetime.timedelta(hours=1)
	onehour_ago = now - onehour

	dbcursor.execute("SELECT COUNT(*) FROM alarms WHERE date BETWEEN ? AND ? ", (onehour_ago, now))
	alarms_in_hour, = dbcursor.fetchone()
	#print("Alarms "+str(alarms_in_hour))
	if(alarms_in_hour>3):
	    send_mail(None, Text="Application stopped. Number of alarms in an hour exceeded the limit. \nCheck manually.")
	    quit()

	#itr = itr +1
	#if(itr==20):
	#	exit()
	time.sleep(30)
