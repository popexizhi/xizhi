#!/bin/bash
rtt_source_dir=$1
rtt_def_file=$2
rtt_def_dir=$3
echo "rtt_source_dir ${rtt_source_dir}; rtt_def_file ${rtt_def_file}; rtt_def_dir ${rtt_def_dir}"
#ls -all ${rtt_source_dir}|grep "_rtt$"|awk -v rtt_source_dir="$rtt_source_dir" -v rtt_def_file="$rtt_def_file" -v rtt_def_dir="$rtt_def_dir" '{print $9;system("cat "rtt_source_dir"/"$9">>"rtt_def_dir"/"rtt_def_file"_back")}'
cat ${rtt_source_dir}/* >${rtt_def_dir}/${rtt_def_file}_back
cat ${rtt_def_dir}/${rtt_def_file}_back |sort > ${rtt_def_dir}/${rtt_def_file}
rm ${rtt_def_dir}/${rtt_def_file}_back
