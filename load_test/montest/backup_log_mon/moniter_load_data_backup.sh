#!/bin/bash

#备份原始log文件为tar.gz，移动到nginx服务器存储
backlog_dir="/data/load_use/tar_backup/backup" #原始ue log存储的位置
ng_backup_uelog_dir="/data/provision_test/log_backup/nocloadtest" #ng ue log备份目录
while true
do
    echo "[`date`]**********************************************"
    now=`date '+%Y-%m-%d_%H-%M-%S'`
    now_data="uelog.${now}"
    echo "">nohup.out
    echo "mv load test log to ng server"
    tar -cvzf ${backlog_dir}/${now_data}.tar.gz ${backlog_dir}/*.log.txt* --remove-files
    echo "stop ${now_data}"

    #ssh to ng
    scp ${backlog_dir}/*.tar.gz slim@192.168.1.216:${ng_backup_uelog_dir}
    rm ${backlog_dir}/*.tar.gz
    sleep 3600
done
