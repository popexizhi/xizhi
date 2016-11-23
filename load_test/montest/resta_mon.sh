
for pid in $(ps aux|grep "moniter.sh\|MoniterStart" |grep -v grep|awk '{print $2}');do
    echo Stop moniter.sh , killing pid: $pid
        kill -9 $pid
done
echo "backup nohup"
tar -cvzf nohup.tar.gz nohup.out  --remove-files 
ps -ef | egrep moniter.sh | egrep -v egrep

sleep 2

echo "start moniter.sh"
nohup ./moniter.sh &
ps -ef | egrep "moniter.sh|MoniterStart" | egrep -v egrep

