#!/bin/bash

ABSPATH=`readlink -f $0`
DIRPATH=`dirname $ABSPATH`
cd ${DIRPATH}

taglist=`sed -n 's/\[v\] *//pg' deploy/ansible/taglist | tr '\n' ',' | sed 's/,$//'`
if [ -z "$taglist" ]; then
	log "INFO" -e 'No task to do.\nPlease select the task you want to do in "deploy/ansible/taglist" file.'
else
    count=$(sed -n 's/\[x\] *//pg' deploy/ansible/taglist | wc -l)
    if [ ${count} -eq 0 ]; then
       ansible-playbook playbook.yml -i inventory
    else
        ansible-playbook playbook.yml -i inventory --skip-tags always --tags $taglist
    fi
fi
