#!/bin/bash
ue_log=$1
echo ${ue_log}
cat ${ue_log}| grep "PacketHeader"|sed 's/^.*Tcp Model Test recv time: \(\d*\)/\1/g'|sed 's/\([0-9][0-9]*\),content: PacketHeader{"packet_number":"\([0-9][0-9]*\)","time_stamp":"\([0-9][0-9]*\)"}/\1,\3,\2/g'>process/${ue_log}
echo "********************************************"
cat process/${ue_log}
