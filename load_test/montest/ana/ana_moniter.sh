#!/bin/bash

VALVE_NUM=5000 #max 
CORE_NUM=1 #core num

dev_path="/home/jenkins/test/process" #检查路径
log_path="/home/jenkins/test" #检查路径
log_back="/data/nocloadtest" #备份log路径
core_path="/home/slim/test/dev_provision/provision_ue_use"
do_path="/home/lijie/test/xizhi/load_test" #运行路径
ana_log="/data/load_use/ana.log"

backup_log()
{
    tar -cvzf ${log_back}/$1_log.tar.gz ${log_path}/*log.txt* --remove-files 
}
do_ana()
{   
    cd ${do_path} && python analysis_data.py $1 
    
}


old_dir=""
while true
do
    echo "[`date`]**********************************************"
    dir_new=`tail -n 1 ${ana_log}`
    echo "dir_new is ${dir_new}"
    if [ "${dir_new}"x == "${old_dir}"x ]
    then
        echo "old_dir is now"
        sleep 600
    else
        do_ana ${dir_new} 
        old_dir=${dir_new}
    fi
done    
