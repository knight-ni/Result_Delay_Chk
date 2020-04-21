#!/bin/sh
ps -ef|grep "python3.7 /home/nibo/scripts/content_check/main.py"|grep -vE "grep|$dt"|awk '{print "kill -9 "$2}'|sh
ps -ef|grep "/home/nibo/scripts/content_check/start.sh"|grep -v grep|awk '{if($2!="'"${pid}"'" && $2!="'"${ppid}"'") print "kill -9 "$2}'|sh
