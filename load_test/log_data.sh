#!/bin/bash
ue_log=$1
old_dir=$2
new_dir=$3
echo ${old_dir}/${ue_log}
echo ${new_dir}/${ue_log}
cat ${old_dir}/${ue_log}| grep "PacketHeader"|sed 's/^.*Tcp Model Test recv time: \(\d*\)/\1/g'|sed 's/\([0-9][0-9]*\),content: PacketHeader{"packet_number":"\([0-9][0-9]*\)","time_stamp":"\([0-9][0-9]*\)"}/\1,\3,\2/g'>${new_dir}/${ue_log}
echo "********************************************"
cat ${new_dir}/${ue_log}
