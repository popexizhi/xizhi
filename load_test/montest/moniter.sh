#!/bin/bash

log_back="/data/nocloadtest" #备份log路径
core_path="/home/slim/test/dev_provision/provision_ue_use"
do_path="/home/lijie/test/xizhi/load_test" #运行路径


save_log()
{
    cd ${do_path} && python MoniterStart.py
}


while true
do
    echo "[`date`]**********************************************"
    for pid in $(ps aux|grep "MoniterStart.py" |grep -v grep|awk '{print $2}');do
        echo Stop moniter.sh , killing pid: $pid
        kill -9 $pid
    done
    save_log 
done    
