#!/usr/bin/env python
from DQMInterface import *
from mimeemail import *
import sqlite3
import datetime
import time

conn = sqlite3.connect('alarms_log.db')
dbcursor = conn.cursor()
try:
    dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE id=1 )')
except sqlite3.Error as exerror:
    if(exerror):
        dbcursor.execute('''CREATE TABLE alarms(id integer PRIMARY KEY,date, run int, lumi int, dead_value int, DataPresent)''')

serverurl = 'https://cmsweb.cern.ch/dqm/online'


def PrintAlarm(DQMMon):

        print("=========================================")
        print(DQMMon.runinfo['run'])
        print(DQMMon.runinfo['lumi'])
        print(DQMMon.runinfo['beamMode'])
        print(DQMMon.runinfo['run_type'])
        print(DQMMon.dead_value)
        print("isDataPresent "+str(DQMMon.isDataPresent))
        print("=========================================")


run_proc = 0

while True:

    DQMMon = DQMInterface(serverurl, 0) #Run=0 it takes the latest run
    if(DQMMon.onlinePublishing):
        DQMMon.refresh()
        DQMMon.getRunInfo()
        DQMMon.getdeadRocTrendLayer_1()
        DQMMon.getIsDataPresent()
      
        if(DQMMon.runinfo['lumi'] < 4 ):
            continue

        if(DQMMon.runinfo['run']!=run_proc):
               print("Proceesing run: "+str(DQMMon.runinfo['run']))
        run_proc = DQMMon.runinfo['run']


        if(DQMMon.runinfo['beamMode']=='stable' and DQMMon.runinfo['run_type']=='pp_run' and (DQMMon.dead_value>70 or DQMMon.isDataPresent==False)):
            #Run is written in db only if the sms/email has been sent
            dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE run="%s" )' % DQMMon.runinfo['run'])
            alarm_handled, = dbcursor.fetchone()

            if(alarm_handled!=1):
                PrintAlarm(DQMMon)

                dbcursor.execute("INSERT INTO alarms(date, run, lumi, dead_value, DataPresent) VALUES (?, ? , ? , ?, 1);",(datetime.datetime.now(), DQMMon.runinfo['run'], DQMMon.runinfo['lumi'], DQMMon.dead_value))
                conn.commit()
                send_mail(DQMMon)
                send_mail(DQMMon, isSMS=True) #sendsms

                ###Checks to avoid spam
                now = datetime.datetime.now()
                onehour = datetime.timedelta(hours=1)
                onehour_ago = now - onehour

                dbcursor.execute("SELECT COUNT(*) FROM alarms WHERE date BETWEEN ? AND ? ", (onehour_ago, now))
                alarms_in_hour, = dbcursor.fetchone()
                print("Alarms "+str(alarms_in_hour))
                if(alarms_in_hour>3):
                    send_mail(DQMMon, Text="Application stopped. Number of alarms in an hour exceeded the limit. \nCheck manually.")
                    quit()
    time.sleep(50)
