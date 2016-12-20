#!/bin/bash
rtt_source_dir=$1
rtt_backup_file=$2
echo "rtt_source_dir ${rtt_source_dir}; rtt_backup_file ${rtt_backup_file};"
mkdir ${rtt_backup_file}
#ls -all ${rtt_source_dir}|grep "_rtt$"|awk -v rtt_source_dir="${rtt_source_dir}" -v rtt_backup_file="${rtt_backup_file}" '{print $9;system("mv "rtt_source_dir/$9" "rtt_backup_file)}'
ls -all ${rtt_source_dir}|grep "_rtt$"|awk -v rtt_source_dir="${rtt_source_dir}" -v rtt_backup_file="${rtt_backup_file}" '{print $9;system("mv "rtt_source_dir"/"$9" "rtt_backup_file)}'
ls -all ${rtt_source_dir}|grep "_rtt$"
