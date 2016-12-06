#!/bin/bash
ue_log=$1
old_dir=$2
new_dir=$3
echo ${old_dir}/${ue_log}
echo ${new_dir}/${ue_log}
echo "rtt***************************"
cat ${old_dir}/${ue_log}|grep "Tcp Model recv ping now:"|sed 's/^.*ping now://g'|sed 's/,content: Ping packet [0-9][0-9]* ,ue send tm /,/g'>${new_dir}/${ue_log}_rtt
echo "********************************************"
cat ${new_dir}/${ue_log}_rtt
