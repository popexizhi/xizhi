#!/bin/bash
ue_log=$1
echo ${ue_log}
cat ${ue_log}|grep "PacketHeader"|sed 's/^.*Tcp Model Test recv time: \(\d*\)/\1/g'|sed 's/\(\d*\),content: Packeeader{"packet_number":"\(\d*\)/\1,\2/g'|sed 's/","time_stamp":"/,/g'|sed 's/"}//g'>${ue_log}
echo "********************************************"
cat ${ue_log}
