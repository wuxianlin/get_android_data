#!/bin/bash

free -h
df -h
lscpu

LOCAL_PATH=`pwd`
echo LOCAL_PATH $LOCAL_PATH
echo PATH $PATH

if [ ! -d data ]; then
    mkdir data
fi

IFS_old=$IFS
IFS=$'\n'

for run in `cat config.json | jq -c .[]`; do
    cmd=`echo $run|jq -r .cmd`
    out=`echo $run|jq -r .out`
    echo start run $cmd
    eval $cmd
    if [ $? -ne 0 ]; then
        rm $out
        echo run failed
    else
        mv $out data
        echo run success
    fi
    sleep 5
done

IFS=$IFS_old

