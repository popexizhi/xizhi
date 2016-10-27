# -*- coding:utf8 -*-
from datetime import datetime
from copy import deepcopy
import re, time, os
LOCAL_MAC = '"00:0c:29:10:a6:8d"'

class loss_data_ana():
    def __init__(self, f="d.cap.log"):
        self.file_path = f
        f=open(f)
        self.con = f.readlines()
        f.close()
        self.data_list = []
        self.loss_list = {}

    def get_start_end_time(self):
        st_data = en_data = [""]
        self.con.sort()
        self.in_packet_num = self.out_packet_num = self.total_packet_num = 0
        for i in self.con:
            st_data = en_data
            en_data = i.split(",")
            #平均时长
            if (st_data[0] == en_data[0]):
                #self.loss_list[st_data[0]] = self.loss_list[st_data[0]] + 1
                if (2 == len(st_data[1].split("."))):
                    self.loss_list[en_data[0]] = self.loss_list[en_data[0]] + 1
                    time_format = '"%Y-%m-%d %H:%M:%S.%f"'
                else:
                    time_format = '"%Y-%m-%d %H:%M:%S"'
                send_time = datetime.strptime(st_data[1], time_format)

                if (2 == len(en_data[1].split("."))):
                    time_format = '"%Y-%m-%d %H:%M:%S.%f"'
                else:
                    time_format = '"%Y-%m-%d %H:%M:%S"'
                get_time = datetime.strptime(en_data[1], time_format)

                self.data_list.append([st_data[0],get_time - send_time, send_time, get_time])
                #print "id:%s ; use:%s" % (st_data[0],str(get_time - send_time))
            else:
                #print "i is "+ str(i)
                #print en_data[0]
                if "" == i:
                    pass
                else:
                    self.loss_list[en_data[0]] = 0
            #丢包率计算
            if (LOCAL_MAC == en_data[2]):
                #src 为 本机 ，定义为: 发送报文
                self.out_packet_num = self.out_packet_num + 1
            else:
                self.in_packet_num = self.in_packet_num + 1
    def get_loss_data(self):
        for i in self.loss_list:
            if 0 == self.loss_list[i]:
                print i

if __name__ == "__main__":
    t = loss_data_ana()
    t.get_start_end_time()
    t.get_loss_data()
