#!/bin/bash

# one_sec_one_fun
APPNAME=$1
for i in {0..60}; do
    curl -m 600 http://127.0.0.1:8080/function/${APPNAME} > /dev/null &
	sleep 1
done