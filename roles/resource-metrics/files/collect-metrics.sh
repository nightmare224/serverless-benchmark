#!/bin/bash
APPNAME=$1
OUTFILE=$2
rm -f ${OUTFILE}-${USER}
# while true; do docker stats --format 'table |{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}' --no-stream | ts '%Y/%m/%d %H:%M:%S' | grep k8s_${APPNAME} >> ${OUTFILE}; done &
docker stats --format 'table |{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}|{{.BlockIO}}' | ts '%Y/%m/%d %H:%M:%S' | awk -v appname=${APPNAME} '/1/ && match($3, ".k8s_"appname".*")' >> ${OUTFILE}-${USER} &