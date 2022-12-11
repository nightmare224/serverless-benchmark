#!bin/bash

# twenty_per_three
APPNAME=$1
hey -t 0 -z 1m -c 20 -q 5 http://127.0.0.1:8080/function/${APPNAME} > /tmp/out