#!/bin/bash

TKFEEDBACKSMS_FILE="ReportFromOnlineDQM_SMS.txt"
SENDSMS_FILE="sendsms.txt"
SENDHBSMS_FILE="sendheartbeatsms.txt"

SEND_SMS=0

if [ -f $SENDSMS_FILE ]
    then

    while read line;
      do
      SEND_SMS=`echo $line | awk {'print $1'}`
    done < $SENDSMS_FILE
fi

if [ "$SEND_SMS" -eq 1 ]
    then
    SUBJECT="DQM"
    EMAIL="0041754119021@mail2sms.cern.ch"
    EMAILMESSAGE="ReportFromOnlineDQM_SMS.txt"
    /bin/mail -s "$SUBJECT" "$EMAIL" < $EMAILMESSAGE
    EMAIL_TKDOC="0041764875503@mail2sms.cern.ch"
    #/bin/mail -s "$SUBJECT" "$EMAIL_TKDOC" < $EMAILMESSAGE
    EMAIL_ONCALL="0041764872389@mail2sms.cern.ch"
#    /bin/mail -s "$SUBJECT" "$EMAIL_ONCALL" < $EMAILMESSAGE
fi


SEND_HBSMS=0

if [ -f $SENDHBSMS_FILE ]
    then

    while read line;
      do
      SEND_HBSMS=`echo $line | awk {'print $1'}`
    done < $SENDHBSMS_FILE
fi

if [ "$SEND_HBSMS" -eq 1 ]
    then
    SUBJECT="DQM"
    EMAIL="0041754119021@mail2sms.cern.ch"
    EMAILMESSAGE="ReportHeartbeat_SMS.txt"
    /bin/mail -s "$SUBJECT" "$EMAIL" < $EMAILMESSAGE
    EMAIL_TKDOC="0041764875503@mail2sms.cern.ch"
    #/bin/mail -s "$SUBJECT" "$EMAIL_TKDOC" < $EMAILMESSAGE
    EMAIL_ONCALL="0041764872389@mail2sms.cern.ch"
    #/bin/mail -s "$SUBJECT" "$EMAIL_ONCALL" < $EMAILMESSAGE
fi
