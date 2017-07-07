from DQMInterface import *
from mimeemail import *
import sqlite3
import datetime


conn = sqlite3.connect('alarms_log.db')
dbcursor = conn.cursor()
try:
    dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE id=1 )')
except sqlite3.Error as exerror:
    if(exerror):
        dbcursor.execute('''CREATE TABLE alarms(id integer PRIMARY KEY,date, run int, lumi int, dead_value int, DataPresent)''')

serverurl = 'https://cmsweb.cern.ch/dqm/online'

DQMMon = DQMInterface(serverurl, 297702)



if(DQMMon.onlinePublishing):

    DQMMon.getRunInfo()
    DQMMon.getdeadRocTrendLayer_1()
    DQMMon.refresh()

    #print(DQMMon.runinfo['run'])
    # print(DQMMon.runinfo['lumi'])
    # print(DQMMon.runinfo['beamMode'])
    # print(DQMMon.runinfo['run_type'])
    # print(DQMMon.dead_value)

    if(DQMMon.runinfo['beamMode']=='stable' and DQMMon.runinfo['run_type']=='pp_run' and (DQMMon.dead_value>70)):
    #Run is written in db only if the sms/email has been sent
        dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE run="%s" )' % DQMMon.runinfo['run'])
        alarm_handled, = dbcursor.fetchone()
        
        if(alarm_handled!=1):  
            #print("alarm_not_handled")
            dbcursor.execute("INSERT INTO alarms(date, run, lumi, dead_value, DataPresent) VALUES (?, ? , ? , ?, 1);",(datetime.datetime.now(), DQMMon.runinfo['run'], DQMMon.runinfo['lumi'], DQMMon.dead_value))
            conn.commit()
            send_mail(DQMMon)
            #send_mail(DQMMon, isSMS=True) #sendsms

            ###Checks to avoid spam
            now = datetime.datetime.now()
            onehour = datetime.timedelta(hours=1)
            onehour_ago = now - onehour

            dbcursor.execute("SELECT COUNT(*) FROM alarms WHERE date BETWEEN ? AND ? ", (onehour_ago, now))
            alarms_in_hour, = dbcursor.fetchone()
            if(alarms_in_hour>2):
                send_mail(DQMMon, Text="Application stopped. Number of alarms in an hour exceeded the limit. \nCheck manually.")
                exit()
        




