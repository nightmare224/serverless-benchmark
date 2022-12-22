#!bin/bash

# twenty_per_three
APPNAME=$1
hey -t 0 -n 2 -c 2 http://127.0.0.1:8080/function/${APPNAME} > /tmp/out
