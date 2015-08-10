#!/bin/sh
PID=`ps -x | grep -v grep | grep pubron.py | awk '{print $1}'`
kill -9 ${PID}
