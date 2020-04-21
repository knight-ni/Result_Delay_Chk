import myfunc
import period
import time
import datetime
import sys
import os

if __name__ == '__main__':
    if (len(sys.argv) == 2):
        #dt = datetime.datetime.now().strftime('%Y%m%d')
        filename = sys.argv[1]
        print(filename)
    else:
        print("file name needed")
        os._exit(1)
    #pre = 'VFG.log'
    hostname,filestr = filename.split('/')[-2:]
    matchdt = filestr.split('.')[-2]
    #ext = 'txt'
    #path = '/opt/log/content_pc/cnnjpopbcon002'
    #filename = path + '/' + pre + '.' + dt + '.' + ext
    #print(filename)
    capstr = ['Read stuff','|A']
    #timeArray = [time.strptime(dt + " " + x, "%Y%m%d %H:%M:%S") for x in period.match_list]
    timeArray = [int(time.mktime(time.strptime(matchdt + " " + x, "%Y%m%d %H:%M:%S"))) for x in period.match_list]
    txt = myfunc.tracef(hostname,filename,capstr,timeArray,matchdt)
    print(txt)
