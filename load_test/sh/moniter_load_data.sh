#!/bin/bash
ng_process="/data/provision_test/log_backup/process"
while true
do
    echo "">nohup.out
    echo "del and backup 1 days load test log"
    for def_p in "/home/jenkins/test" "/data/err_dir" "/home/jenkins/test/rtt_process";do
        echo "def_p = ${def_p}"
        find ${def_p} -mtime +1 -type d |awk '{system("tar -cvf "$1".tar.gz "$1" --remove-files")}'
        sshpass -p 'abc123,./' scp ${def_p}/*.tar.gz slim@192.168.1.216:${ng_process}
        rm ${def_p}/*.tar.gz
        ls -all  ${def_p}
    done
    echo "one stop "
    sleep 21600
done
