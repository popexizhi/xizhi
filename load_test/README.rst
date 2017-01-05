load_test
=====
启动脚本位置及功能
-------
当前用户权限:
[备份 tar_backup]
./montest/backup_log_mon/moniter_load_data_backup.sh
[计算处理结果，出测试报告]
./montest/ana/ana_moniter.sh

sudo :
[处理原始log]
./montest/moniter.sh
[备份全部结果log]
./sh/moniter_load_data.sh


负载测试工具

依赖安装
--------
windows 依赖安装

 .(64 ) \\\\192.168.1.15\ftproot\incoming\lijie\use-tool-scapy

 .(32 ) https://github.com/Kondziowy/scapy_win64/tree/master/win32

安装成功后测试
::
    $ >>> from scapy.all import *

运行方法
---------
1.cap包要求为指定relay的使用端口如下:

tcpdump -x -i eth0 tcp port 13200 -w dx.cap

当前只支持处理一个relay端口监控的数据报文

2.将运行结果的cap包放到当前目录下直接python process_data.py
运行完成后目录下新生成一个文件夹，直接打开文件夹中的testresults.html 及为测试结果

3.L2流量结果图

3.1 在打开的cap文件的wireshark安装目录中添加wireskark\noc.lua文件

3.2 使用wrieshark打开cap文件，选择statistics -> IO Graph 

filter中添加两条如下,生成图像即要求内容:

NOC.MsgType == 6 and tcp.srcport ==13200

NOC.MsgType == 6 and tcp.dstport ==13200
