#!/bin/bash
for logf in $(ls |grep txt|awk '{print $1}') ;do
    echo "${logf} ******" 
    sh save_log.sh ${logf} 10 
done
