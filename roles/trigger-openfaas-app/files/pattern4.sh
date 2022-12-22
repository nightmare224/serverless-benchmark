#!bin/bash

# twenty_per_three
APPNAME=$1
REQUEST_CONCURRENT=$2
hey -t 0 -n ${REQUEST_CONCURRENT} -c ${REQUEST_CONCURRENT} http://127.0.0.1:8080/function/${APPNAME} > /tmp/out
