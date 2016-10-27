sudo kill -9 `ps aux|grep "port $1" -w |awk  '{print $2}'`
