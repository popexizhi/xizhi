#!/bin/bash

VALVE_NUM=5000 #max 
CORE_NUM=1 #core num

dev_path="/home/jenkins/test/process" #检查路径
log_path="/home/jenkins/test" #检查路径
log_back="/data/nocloadtest" #备份log路径
core_path="/home/slim/test/dev_provision/provision_ue_use"
do_path="/home/lijie/test/xizhi/load_test" #运行路径
ana_log="/data/load_use/ana.log"


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
    cd ${do_path} && python analysis_data.py $1 
    
}
save_log()
{
    now_d=`date +%Y,%m,%d,%H,%M,%S,`
    time_long="3600"
    echo "save_log ${now_d}"
    chmod 666 ${dev_path}/*    
    cd ${do_path} && python MoniterStart.py ${dev_path} ${now_d} ${time_long}
    dir_p=`cat ${ana_log}`
    echo ${dir_p}
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
