#!/bin/bash
dir_p="backup_log"
save_p="~/test"
log_f=$1
packet_number_per_second=$2
echo "save log:${log_f} packet_number_per_second: ${packet_number_per_second}"
mkdir ${dir_p}
mv ${log_f} ${dir_p}/${log_f}_${packet_number_per_second}
scp ${dir_p}/${log_f}_${packet_number_per_second} jenkins@192.168.1.99:${save_p}
ssh jenkins@192.168.1.99 "cd ${save_p};sh log_data.sh ${log_f}_${packet_number_per_second}"
