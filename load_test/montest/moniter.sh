#!/bin/bash

VALVE_NUM=3000 #max 
CORE_NUM=1 #core num

dev_path="/home/jenkins/test/process" #检查路径
log_path="/home/jenkins/test" #检查路径
log_back="/data/nocloadtest" #备份log路径
core_path="/home/slim/test/dev_provision/provision_ue_use"
do_path="/home/lijie/test/xizhi/load_test" #运行路径



send_mail()
{
        echo "send mail "
        cat $1
        python sendMail.py $1
}
backup_log()
{
    tar -cvzf ${log_back}/$1_log.tar.gz ${log_path}/*log.txt* --remove-files 
}
do_ana()
{   
    now_d=`date +%Y%m%d_%H%M%S`
    echo "sta ana ${now_d}"
    mv ${dev_path} ${dev_path}_${now_d}
    mkdir ${dev_path}
    chmod 777 ${dev_path}
    backup_log ${now_d}
    echo "">nohup.out
    cd ${do_path} && python analysis_data.py ${dev_path}_${now_d} 
    
}


diff_num()
{
    echo "NOW $1, MAX $2"
    if (( $2 > $1 ))
    then
        echo "res is pass"
        return 0
    else
        echo "(def is $2) > (now is $1) res is ">>mail_err
        do_ana 
        return -1
    fi
}
while true
do
    echo "[`date`]**********************************************"
    dev_log_num=`ls -all ${dev_path}|grep "log.txt"|wc -l`
    echo "dev db_num ${dev_log_num}"
    echo "************************************************"
    echo "log个数检查"
    echo "[load test log 准备pass]个数检查 is pass" >mail_err
    diff_num ${dev_log_num} ${VALVE_NUM}
    sleep 300
done    
