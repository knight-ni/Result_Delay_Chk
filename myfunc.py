import time
import os
import datetime
import bisect
import re
import MailSender
import requests
#import prettytable

dtstr="%Y-%m-%d %H:%M:%S"
restr=r"(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}).*Read stuff=(\d{8})|.*"
send="172.30.5.14"
receiv=["log@jsvfprelog001.nanjing.china.local"]
author="Knight.Ni"

def ts2dt(ts):
    tmp=time.localtime(ts)
    dt=time.strftime("%Y-%m-%d %H:%M:%S", tmp)
    return dt

def get_log_info(s):
    dt=re.search(restr,s)
    return [dt.group(1),dt.group(2)]

def get_match_info(timeArray,dt): 
    tm = datetime.datetime.now().strftime("%H:%M:%S")
    dtstr = dt + " " + tm
    now = time.mktime(time.strptime(dtstr, '%Y%m%d %H:%M:%S'))
    pos = bisect.bisect(timeArray, now) 
    match_time = ts2dt(timeArray[pos]) 
    match_num = pos + 1
    return [match_time,match_num]

def sendmail(hostname,txt):
    send_from = 'content_check---devenvironment_linux'
    my_mail_send = MailSender.MailSender(send,send_from)
    subject = 'time gap checking for ' + hostname
    content_string = txt
    receivers = receiv
    try:
        my_mail_send.send(subject, content_string, receivers)
        my_mail_send.close()
    except BaseException:
        print("Error When Sending Mail")

def toAlertManager(url, alertname, instance, service, severity, gaps, author):
    alerts1 = '''[
      {
        "labels": {
           "alertname": "%s",
           "instance": "%s",
           "service": "%s",
           "severity": "%s"
         },
         "annotations": {
            "summary": "%s spend %s seconds on getting result.",
            "author": "%s"
          }
      }
    ]''' % (alertname, instance, service, severity, instance, gaps, author)

    data = alerts1
    response = requests.post(url, data=data)
    return response.text


def tracef(hostname,filename,capstr,timeArray,matchdt):
    url = 'http://10.41.15.16:9093/api/v1/alerts'
    with open(filename) as f:
        f.seek(0,2)
        while True:
            msg = []
            last_pos = f.tell() 
            line = f.readline().strip()
            chk = all([word in line for word in capstr])
            if chk:
                try:
                    loginfo = get_log_info(line)
                    matchinfo = get_match_info(timeArray,matchdt)
                    realtime = ts2dt(time.time())
                    matchtime,matchnum = matchinfo
                    logtime,lognum = loginfo
                    logtm = int(time.mktime(datetime.datetime.strptime(logtime,dtstr).timetuple()))
                    matchtm = int(time.mktime(datetime.datetime.strptime(matchtime,dtstr).timetuple()))
                    gaps = 16 - (matchtm - logtm)
                    if gaps > 3:
                        alertname = 'result delay alert'
                        instance = hostname
                        service = 'result'
                        severity = 'dying'
                        toAlertManager(url, alertname, instance, service, severity, gaps, author)
                except Exception as e:
                    print(e)
                    #pass
    return gaps

def mktable(data):
    pt= prettytable.PrettyTable(["Name",  "Data"],border=True, header=True, padding_width=3,align="c")
    #pt.set_style(MSWORD_FRIENDLY)
    pt.hrules = prettytable.ALL
    pt.vrules = prettytable.ALL
    pt.align["Name"] = "c"
    pt.valign["Name"] = "m"
    pt.align["Data"] = "c"
    pt.valign["Data"] = "m"
    for k,v in data.items():
       pt.add_row([k,v]) 
    text = pt.get_html_string(format=True)
    oldhead = '<table frame="box" rules="all">'
    newhead = '<table frame="box" rules="all" align="center" border="1" cellpadding="0" cellspacing="0" style="width: 70%;margin-left:auto;margin-right:auto;">'
    text = text.replace(oldhead,newhead)
    return text

if __name__ == '__main__':
    url = 'http://10.41.15.16:9093/api/v1/alerts'
    alertname = 'result delay alert'
    instance = 'cnnjpopbcon002'
    service = 'result'
    severity = 'dying'
    author = 'Knight.Ni'
    gaps = 50
    res=toAlertManager(url, alertname, instance, service, severity, gaps, author)
    print(res)
