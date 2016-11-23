
for pid in $(ps aux|grep "moniter.sh\|ana_moniter.sh" |grep -v grep|awk '{print $2}');do
    echo Stop moniter.sh , killing pid: $pid
        kill -9 $pid
done
echo "backup nohup"
tar -cvzf nohup.tar.gz nohup.out  --remove-files 
ps -ef | egrep moniter.sh | egrep -v egrep

sleep 2

echo "start moniter.sh"
nohup ./moniter.sh &
nohup ./ana_moniter.sh &
ps -ef | egrep "moniter.sh|ana_moniter.sh" | egrep -v egrep

