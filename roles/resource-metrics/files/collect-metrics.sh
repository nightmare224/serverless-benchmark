#!/bin/bash
APPNAME=$1
OUTFILE=$2
rm -f ${APPNAME}
# while true; do docker stats --format 'table |{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}' --no-stream | ts '%Y/%m/%d %H:%M:%S' | grep k8s_${APPNAME} >> ${OUTFILE}; done &
docker stats --format 'table |{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}|{{.BlockIO}}' | ts | awk -v appname=${APPNAME} '/1/ && match($4, ".k8s_"appname".*")'