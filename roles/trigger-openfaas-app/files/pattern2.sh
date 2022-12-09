#!bin/bash

# twenty_per_three
APPNAME=$1
for i in {1..20}; do
	temp+=" http://127.0.0.1:8080/function/${APPNAME}"
done
for i in {0..20}; do
	curl -Z $temp > /dev/null
    sleep 3
done