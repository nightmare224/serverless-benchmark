APPNAME=$1
OUTFILE=$2
rm -f ${APPNAME}
# docker stats --format 'table \t{{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}' --no-stream | ts '%Y/%m/%d %H:%M:%S'
while true; do docker stats --format 'table |{{.Name}}|{{.CPUPerc}}|{{.MemPerc}}|{{.NetIO}}|{{.BlockIO}}' --no-stream | ts '%Y/%m/%d %H:%M:%S' | grep k8s_${APPNAME} >> ${OUTFILE}; done &