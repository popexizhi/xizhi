# -*- coding:utf8 -*-
from datetime import datetime
from copy import deepcopy
import re, time, os
from dtojpg import dtjpg #绘图使用(matplotlib)
from host_scapy import process_cap 
from reportwriter import Report #html 
LOCAL_MAC = '"e4:1f:13:6d:c2:d0"' #本机mac
def process_data():
    f=open("c.cap.log")
    con = f.readlines()
    f.close()
    use_data = ""
    old_data = new_data = ""
    t = 0
    for i in con:
        old_data = new_data
        new_data = i.split(",")[0]
        if (new_data == old_data):
            t = t + 1
            if t < 2:
                use_data = use_data + i
            else:
                pass
        else:
            use_data =  use_data + i
            t = 0
    
    f=open("get.log", "w")
    f.writelines(use_data)
    f.close()
class pd():
    def __init__(self, f="get.log", file_path = ""):
        self.file_path = file_path
        f=open(f)
        self.con = f.readlines()
        f.close()
        self.data_list = []
        self.arat_list = []#记录每秒钟的完成详细内容
        self.jpgd = dtjpg() #jpg 

    def get_start_end_time(self):
        st_data = en_data = [""]
        self.con.sort()
        self.in_packet_num = self.out_packet_num = self.total_packet_num = 0
        for i in self.con:
            st_data = en_data
            en_data = i.split(",")
            #平均时长
            if (st_data[0] == en_data[0]):
                #print st_data
                #print st_data[0]
                #print en_data[0]
                #print "id:%s ; st: %s, en: %s" % (st_data[0],st_data[1], en_data[1])
                if (2 == len(st_data[1].split("."))):
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
                pass
            #丢包率计算
            if (LOCAL_MAC == en_data[2]):
                #src 为 本机 ，定义为: 发送报文
                self.out_packet_num = self.out_packet_num + 1
            else:
                self.in_packet_num = self.in_packet_num + 1

            self.total_packet_num = self.total_packet_num + 1
        #self.show_data_list()i
    def show_data_list(self):
        for i in self.data_list:
            print [j for j in i]
    
    def src_data_(self, sort_by="get_time"):
        """sort by sort_by ::处理原始数据"""
        
        if ("get_time" == sort_by):
            lab_num =3
        if ("send_time" == sort_by):
            lab_num =2
        #按指定时间截排序
        _atrt_list = self.data_list_sort_by_(lab_num)
        
        #以秒钟为单位统计响应结果
        arat_list = []#每秒钟的原始数据列表
        a_now = datetime.strptime("1900-01-01 00:00:00", "%Y-%m-%d %H:%M:%S") #datetime(1900,1,1)
        a_now_list = []
        #print "** " * 20
        for i in _atrt_list:
            #同n秒钟计入相同的统计范围
            res = (a_now.year != i[0].year) or (a_now.month != i[0].month) or (a_now.day != i[0].day) or\
                            (a_now.hour != i[0].hour) or (a_now.minute != i[0].minute) or (a_now.second != i[0].second) 
            if res:
                t = deepcopy(a_now_list)                    
                arat_list.append([a_now, t])
                a_now = i[0]
                a_now_list = []
                a_now_list.append(i[1].total_seconds())
            else:
                a_now_list.append(i[1].total_seconds())
            
        #print "\t\t len is %d" % len(arat_list)
        #print arat_list
        self.arat_list = deepcopy(arat_list)
        return self.arat_list

    def ATRT(self, sort_by="get_time"):
        """sort by sort_by ::平均每秒钟的响应时间 """
        arat_list = self.src_data_(sort_by)
        data_list = []
        for i in arat_list:
            if (i[0] == datetime(1900,1,1) ):
                pass
            else:
                #print "** " * 5
                data_list.append(str(i[0]) + ";" + str(sum(i[1])/len(i[1])))
                #print str(i[0]) + "\t" + str(sum(i[1])/len(i[1]))
                #print sum(i[1])/len(i[1])        
        res = self.ana_data_summary(self.data_list, num = 1, unit_s = 1)#分析平均使用时间
        self.save_jpg(data_list, "Atrt_")
        return res

    def TPS(self, sort_by="get_time"):
        """sort by sort_by ::平均每秒钟完成事务数 """
        print "start TPS " + str(sort_by)
        arat_list = self.src_data_(sort_by)
        time_data_list = [] #jpg use
        ana_data_list = []
        for i in arat_list:
            if (i[0] == datetime(1900,1,1) ):
                pass
            else:
                #print "** " * 5
                time_data_list.append(str(i[0])+ ";" + str(len(i[1])))
                #print str(i[0]) + "\t" + str(len(i[1]))
                ana_data_list.append([i[0], len(i[1])])
        self.save_jpg(time_data_list, "TPS_avg_"+sort_by)
        #print "data_list is %s" % ana_data_list
        res = self.ana_data_summary(ana_data_list, num = 1)#分析平均每秒完成事务数
        return res

    def save_jpg(self, data_list, filename):
        #self.jpgd = dtjpg()
        self.jpgd.xa(data_list, self.file_path+"//"+filename)
        #self.jpgd.sub_plot(data_list, filename)
    def data_list_sort_by_(self, lab_num): 
        time_list = []
        for i in self.data_list:
            time_list.append([i[lab_num], i[1] , i])
        time_list.sort()
        #for i in time_list:
        #    print str(i[0]) +"\t"+str(i[1])
        return time_list

    def ana_data_summary(self, data_list, num = 1, unit_s = 0):
        """对data_list[num]列表做数据概述，提供 
        [self.avg_len长度个数, self.avg_max最大值, self.avg_min最小值, self.avg均值, self.median中位数, self.avg_stdev标准方差,self.TPS ]
        unit_s = 1为使用指定num的seconds格式，否则直接使用num本身定义
        """
        avg_list = []
        for i in data_list:
            x = float(i[num]) if unit_s == 0 else i[num].total_seconds()
            avg_list.append(x)
        self.avg_len = len(avg_list)
        self.avg_max = max(avg_list)
        self.avg_min =min(avg_list)
        #print avg_list
        self.avg = sum(avg_list)/len(avg_list)
        avg_list.sort()
        self.median = (avg_list[self.avg_len//2]) #中位数
        print "len is %d" % self.avg_len
        print "max time is %f" % self.avg_max
        print "min time is %f" % self.avg_min
        print "avg is %f" % self.avg
        print "median is %f" % self.median 

        self.avg_sdsq = sum([(i - self.avg) ** 2 for i in avg_list])
        #print "**" * 20
        #print avg_list
        #for i in avg_list:
            #print i
            #print (i - avg) ** 2
        #print "**" * 20
        self.avg_stdev = (self.avg_sdsq/(len(avg_list) - 1)) ** .5
        print "stdev is %f" % self.avg_stdev #标准方差

        arat_list = self.src_data_("send_time")
        start_time = arat_list[1]
        #print "start_time is %s" % str(start_time[0])
        arat_list = self.src_data_()
        end_time = arat_list[-1]
        #print "end_time is %s" % str(end_time[0])
        test_time_list = [start_time[0], end_time[0], (end_time[0] - start_time[0]).total_seconds()]
        print "start_time is %s; end_time is %s; use time is %f" % (str(start_time[0]), str(end_time[0]), (end_time[0] - start_time[0]).total_seconds())
        self.TPS = (self.avg_len/(end_time[0] - start_time[0]).total_seconds())
        print "TPS is %f" % self.TPS

        return [self.avg_len, self.avg_max, self.avg_min, self.avg, self.median, self.avg_stdev, self.TPS, test_time_list]

if __name__=="__main__":
    file_path = str(time.time())
    os.system("mkdir "+ file_path)
    file_cap = "d.cap"
    print (time.strftime("%T:%M:%S"))
    x = process_cap(file_cap)
    x.save_file()
    #x.save_db()
    print (time.strftime("%T:%M:%S"))


    #process_data()
    t = pd(file_cap +".log", file_path)
    t.get_start_end_time()
    TPS_res = t.TPS()
    print "* " * 50
    #print TPS_res
    #t.ana_data_summary(t.data_list, num = 1, unit_s = 1)#分析平均使用时间
    ATRT = t.ATRT()
    print ATRT
    #send_time
    st = pd(file_cap +".log", file_path)
    st.get_start_end_time()
    st.TPS("send_time")
    
    print "* " * 50
    #备份cap 文件
    os.system("cp "+ file_cap+" "+file_path )
    os.system("cp "+ file_cap+".log"+" "+file_path )
    
    report = Report(file_path +"//test")
    report.write_line('<h1>Performance Results Report</h1>')

    report.write_line('<h2>Summary</h2>')
    report.write_line('<div class="summary">')
    report.write_line('<b>transactions:</b> %d<br />' %ATRT[0] )
    report.write_line('<b>Average Transaction Response Time:</b> %f<br />' %ATRT[3] )
    report.write_line('<b>TPS:</b> %f<br />' % ATRT[6])
    report.write_line('<b>run time:</b> %f secs<br />' % ATRT[7][2])
    report.write_line('<b>test start:</b> %s<br />' % str(ATRT[7][0]) )
    report.write_line('<b>test finish:</b> %s<br /><br />' % str(ATRT[7][1]) )
    #self.in_packet_num = self.out_packet_num
    report.write_line('<h3>Loss Num</h3>')
    report.write_line('<b>in_packet_num:</b> %d<br /><br />' % st.in_packet_num )
    report.write_line('<b>out_packet_num:</b> %d<br /><br />' % st.out_packet_num )
    report.write_line('<b>total packet num:</b> %d<br /><br />' % st.total_packet_num )
    report.write_line('<b>loss num(in_packet_num-transactions):</b> %d<br /><br />' % (st.in_packet_num-ATRT[0]) )
    report.write_line('<b>输入包中非本次测试输入包个数(out_packet_num-transactions):</b> %d<br /><br />' % (st.out_packet_num-ATRT[0]) )
            
            
    
    report.write_line('</div>')
    
    report.write_line('<h3>Average Transaction Response Time</h3>')
    report.write_line('<b>max time is </b> %f secs<br />' % ATRT[1])
    report.write_line('<b>min time is </b> %f secs<br />' % ATRT[2])
    report.write_line('<b>median time is </b> %f secs<br />' % ATRT[4])
    report.write_line('<b>stdev is </b> %f secs<br />' % ATRT[5])
    
    x_avar = 'Atrt_.jpg'
    report.write_line('<img src="'+x_avar+'" width="80%" height="80%"></img>')


    report.write_line('<h3>Transactions per Second</h3>')
    report.write_line('<b>max time is </b> %f <br />' % TPS_res[1])
    report.write_line('<b>min time is </b> %f <br />' % TPS_res[2])
    report.write_line('<b>median time is </b> %f <br />' % TPS_res[4])
    report.write_line('<b>stdev is </b> %f <br />' % TPS_res[5])

    x_tps = 'TPS_avg_get_time.jpg'
    x_tps_send_time = 'TPS_avg_send_time.jpg' 
    report.write_line('<img src="'+x_tps +'" width="80%" height="80%"></img><br />')
    report.write_line('<img src="'+ x_tps_send_time +'" width="80%" height="80%"></img>')

