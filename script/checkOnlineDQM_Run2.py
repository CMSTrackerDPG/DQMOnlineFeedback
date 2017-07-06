from DQMInterface import *
import sqlite3
import datetime

conn = sqlite3.connect('alarms_log.db')
dbcursor = conn.cursor()
try:
    dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE id=0 )')
except sqlite3.Error as exerror:
    if(exerror):
        dbcursor.execute('''CREATE TABLE alarms(id integer PRIMARY KEY,date, run int, lumi int, dead_value int, DataPresent)''')

serverurl = 'https://cmsweb.cern.ch/dqm/online'

DQMMon = DQMInterface(serverurl, 297726)

if(DQMMon.onlinePublishing):

    DQMMon.getRunInfo()
    DQMMon.getdeadRocTrendLayer_1()
    DQMMon.refresh()

    print(DQMMon.runinfo['run'])
    print(DQMMon.runinfo['lumi'])
    print(DQMMon.runinfo['beamMode'])
    print(DQMMon.runinfo['run_type'])
    print(DQMMon.dead_value)

    if(DQMMon.runinfo['beamMode']=='stable' and DQMMon.runinfo['run_type']=='pp_run' and (DQMMon.dead_value>70)):
        #Run is written in db only if the sms/email has been sent
        dbcursor.execute('SELECT EXISTS(SELECT 1 FROM alarms WHERE run="%s" )' % DQMMon.runinfo['run'])
        alarm_handled, = c.fetchone()
        print(alarm_handled)
        if(alarm_handled!=1):
            dbcursor.execute("INSERT INTO alarms(date, run, lumi, dead_value, DataPresent) VALUES (?, ? , ? , ?, 1);",(datetime.datetime.now(), DQMMon.runinfo['run'], DQMMon.runinfo['lumi'], DQMMon.dead_value))
            conn.commit()
            #Write the message in txt file(and db?)
            #Do something to send sms and email
            #DQMMon.refresh()
