#ls -1 testdata| xargs -i sed -i "s/$/ {}/g" testdata/{}
echo "start grep "
#cat uelog/*|grep "PacketHeader"> now.log
cat old/*|grep "PacketHeader"|sed 's/^.*Tcp Model Test recv time: \(\d*\)/\1/g'|sed 's/\(\d*\),content: Packeeader{"packet_number":"\(\d*\)/\1,\2/g'|sed 's/","time_stamp":"/,/g'|sed 's/"}//g'>now.log

echo "start vi "
#vim -S ue.vim now.log
