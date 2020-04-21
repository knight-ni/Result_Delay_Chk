#!/bin/sh
host=cnnjpopbcon002
pid=$$
ppid=`ps -p $pid -o ppid=|sed -e 's/ //g'`
dt=`date +'%Y%m%d'`
file='/opt/log/content_pc/'${host}'/VFG.log.'${dt}'.txt'
ps -ef|grep "python3.7 /home/nibo/scripts/content_check/main.py"|grep -vE "grep|$dt"|awk '{print "kill -9 "$2}'|sh
ps -ef|grep "/home/nibo/scripts/content_check/start.sh"|grep -v grep|awk '{if($2!="'"${pid}"'" && $2!="'"${ppid}"'") print "kill -9 "$2}'|sh

step=1
for (( i = 0; i < 60; i=(i+step) )); do
    if [ -f $file ];then
        ps -ef|grep -v grep|grep -q "python3.7 /home/nibo/scripts/content_check/main.py $file"
        if [ $? -ne 0 ];then
            /root/python37/bin/python3.7 /home/nibo/scripts/content_check/main.py ${file} 
        fi
    fi
    sleep $step
done
exit 0
