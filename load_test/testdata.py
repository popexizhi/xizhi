# -*- coding:utf8 -*-
import mapping #import host_list
import random, datetime, time
from getjpg import dtjpg
import math
import processt
import numpy
from reportwriter import Report
def gettestdata():
    #hostid
    host_list = mapping.host_list#[0:100]
    host_list_len = len(host_list)
    print "hostid len %d" % host_list_len
    #package_name
    package_name = 100
    package_list = []
    for i in xrange(package_name):
        if 2 == i:
            continue
        package_list.append(i+1)

    print "package len %d " % len(package_list)
    log_list = numpy.zeros((host_list_len*(package_name-1) , 4)) 
    base_time = datetime.datetime.now().microsecond 
    use_time_l = []
    rec_list = []
    index = 0
    for hostid in host_list:
        for i in package_list:
            #use time
            use_time = random.randint(1, 1000)
            # receive_time
            #now = datetime.datetime.now()
            #now_mic = now.microsecond
            now_mic = int(round(time.time() * 1000))
            receive_time = now_mic - random.randint(1, 1000) 
            #print "now_mic %s; receive_time %s" % (str(now_mic), str(receive_time))
            assert receive_time > 0
            log_list[index] = [receive_time, use_time, hostid, i]
            rec_list.append(receive_time)
            use_time_l.append(use_time)
            index = index + 1

    loss(log_list, package_name * len(host_list))
    res = statistics_use(use_time_l, 1) #统计分析全部数据
    dl = {"Max":res[0], "Min":res[1] , "num": res[2], "avg": res[3], "stdev": res[4]}
    rh = Report("rh")
    rh.set_summary(dl)
    rh.set_h3_sum("tps", "tps.jpg")
    rh.set_h3_sum("use_time", "use_time_second.jpg")
    #jpg
    p = processt.processt()
    print "start processt.sta_sec "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print log_list.shape
    res = p.sta_sec(log_list)
    print "start processt.TPS "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x_t, y_t = p.TPS(res)
    print x_t
    print y_t
    b = dtjpg()
    print "start jpg :: tps "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    b.get_jpg(x_t, y_t, "tps")

    
    print "start processt.use_time_second "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x_u, y_u = p.use_time_second(res)

    print x_u
    print y_u
    bu = dtjpg()
    print "start jpg :: use_time_second "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bu.get_jpg(x_u, y_u, "use_time_second")
#    jpg_driver = dtjpg()
#    rec_list.sort()
#    jpg_driver.get_jpg(rec_list, use_time_l, filename="testjpg")
#    con_data = ""
    #for i in log_list:
    #    con_data = "%s%s\n" % (con_data, i)
    print "log_list len %d" % len(log_list)
    
    return log_list

def sta_sec(list_data):
    list_data.sort() #要求list_data中以毫秒为存储单位
    old_d = list_data[0]
    s_sta = {}
    for i in list_data[1:]:
        if if_same_sec(i[0], old_d[0]):
            #同一计数单位，存储
            s_sta[old_d[0]/1000].append(i) 

        else:
            #1.记录新的old_d
            old_d = i
            #2.将新值加入到s_stat
            s_sta[old_d[0]/1000] = [i]
    print s_sta
    return s_sta
def if_same_sec(now_s, def_s):
    return def_s/1000 == now_s/1000

def loss(list_data, pre_totle):
    c_num = len(list_data)
    res = pre_totle - c_num
    print "loss num %d" % res
    return res

def statistics_use(list_data, num):
    Max = max(list_data)
    Min = min(list_data)
    num = len(list_data)
    avg = sum(list_data) / num
    tps = num / avg 
    sdsq = sum([(i - avg) ** 2 for i in list_data])
    stdev = (sdsq / (len(list_data) - 1)) ** .5

    print "Max %d Min %d num %d avg %d std %s ; TPS %s " % (Max, Min, num, avg, str(stdev), str(tps))
    return Max, Min, num, avg, str(stdev)


if __name__=="__main__":
    res = gettestdata()
    #f = open("1.log", "w")
    #f.write(res)
    #f.close()
