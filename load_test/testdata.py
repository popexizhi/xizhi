# -*- coding:utf8 -*-
import mapping #import host_list
import random, datetime
from dtojpg import dtjpg
import math
from processt import *
def gettestdata():
    log_list = []
    #hostid
    print "hostid len %d" % len(mapping.host_list)
    host_list = mapping.host_list[0:100]
    #package_name
    package_name = 100
    package_list = []
    for i in xrange(package_name):
        if 2 == i:
            continue
        package_list.append(i+1)

    print "package len %d" % len(package_list)
    base_time = datetime.datetime.now().microsecond 
    use_time_l = []
    rec_list = []
    for hostid in host_list:
        for i in package_list:
            #use time
            use_time = random.randint(1, 1000)
            # receive_time
            #receive_time = datetime.datetime.now().microsecond - random.randint(1, 1000) 
            receive_time = math.fabs(datetime.datetime.now().microsecond - base_time )
            log_list.append([receive_time, use_time, hostid, i])
            rec_list.append(receive_time)
            use_time_l.append(use_time)

    loss(log_list, package_name * len(host_list))
    statistics_use(use_time_l, 1) #统计分析全部数据
    #jpg
    print "start processt.sta_sec "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    res = processt.sta_sec(log_list)
    print "start processt.TPS "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x_t, y_t = processt.TPS(res)
    print x_t
    print y_t
    b = dtjpg()
    print "start jpg :: tps "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    b.get_jpg(x_t, y_t, "tps")
    
    print "start processt.use_time_second "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    x_u, y_u = processt.use_time_second(res)

    print x_u
    print y_u
    bu = dtjpg()
    print "start jpg :: use_time_second "+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bu.get_jpg(x_u, y_, "use_time_second")
#    jpg_driver = dtjpg()
#    rec_list.sort()
#    jpg_driver.get_jpg(rec_list, use_time_l, filename="testjpg")
#    con_data = ""
    #for i in log_list:
    #    con_data = "%s%s\n" % (con_data, i)
    print "log_list len %d" % len(log_list)
    
    return con_data

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
