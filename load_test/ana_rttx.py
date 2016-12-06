# -*- coding:utf8 -*-
import datetime, time
import numpy
from reportwriter import Report
from processt import processt
from getjpg import dtjpg
import random
from ShellCon import sh_control
import sys, copy

DEFLOG = 0

class ana_rtt():
    def __init__(self):
        self.processt = processt()


    def doing(self, fp, sta, end, save_dir=None):
        """ 
        1.open file
        2.处理数据
        3.出x,y数据
        """
        #1
        datas = self.processt.file2matrix(fp)
        #2
        #res = self.processt.statistics_use(datas, 1)
        #dl = {"Max(microsecond)":res[0], "Min(microsecond)":res[1] , "num": res[2], "avg": res[3], "stdev": res[4]}

        #3
        xy_res = self.processt.sta_sec(datas)
        sta_time = self.change_time_to_second(sta)
        end_time = self.change_time_to_second(end)
        xy_res = self.range_time(xy_res, [sta_time, end_time])
        x_u, y_u, max_u, std_u = self.time_statistics_dic_list(xy_res)
        print self.save_csv([self.datetime_from_second(x_u),y_u, max_u, std_u], fp, save_dir)

        #x_u, y_u= self.processt.use_time_second(xy_res)
        #print self.save_csv([self.datetime_from_second(x_u),y_u], fp)

        yl = y_u
        res = self.statistics_list(yl)
        dl = {"Max(microsecond)":res[0], "Min(microsecond)":res[1] , "num": res[2], "avg": res[3], "stdev": res[4]}
        print dl
        return dl
    
    def range_time(self, s_sta, rt):
        sta = rt[0] if None != rt[0] else 0
        end = rt[1] if None != rt[1] else 9999999999999999
        source = copy.deepcopy(s_sta)
        for key in source:
            self.log("[sta: %s, end: %s]key %s" % (str(sta), str(end), str(key)))
            if float(sta) <= float(key) <= float(end):
                pass
            else:
                s_sta.pop(key)
        return s_sta
    
    def change_time_to_second(self, time_s):
        if None == time_s :
            return time_s
        listt = time_s.split(",")
        dt = datetime.datetime(int(listt[0]), int(listt[1]), int(listt[2]), int(listt[3]), int(listt[4]),int(listt[5]))
        return time.mktime(dt.timetuple())


    def time_statistics_dic_list(self, s_sta):
        x_res = []
        avg_res = []
        max_res = []
        std_res = []
        for sec in s_sta:
            res = self.statistics_list(s_sta[sec], key=1)
            self.log("res %s" % str(res))
            x_res.append(sec)
            avg_res.append(res[3])
            max_res.append(res[0])
            std_res.append(res[4])

        return x_res, avg_res, max_res, std_res

    def statistics_list(self, dlist, key=-1):
        if -1 == key :
            pass
        else:
            new_list = []
            for i in dlist:
                new_list.append(i[key])
            dlist = new_list
        self.log(dlist)
        Max = max(dlist)
        Min = min(dlist)
        num = len(dlist)
        avg = sum(dlist) / num
        sdsq = sum([(i - avg) ** 2 for i in dlist])
        stdev = (sdsq / (len(dlist) - 1)) ** .5
        return float(Max), float(Min), num, float(avg), float(stdev)

    def log(self, mes , leve=0):
        if leve >= DEFLOG:
            print "[ana_rttx] %s" % str(mes)

    def datetime_from_second(self, seconds_list):
        res = []
        for i in seconds_list:
            new_t = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(i))
            res.append(new_t)    
        return res 

    def save_csv(self, xy_list, fp, save_dir):
        x = xy_list[0]
        y = xy_list[1]
        z = xy_list[2]
        a = xy_list[3]
        com = "time,rtt_max,rtt_avg_use_time,rtt_std"
        index = 0
        for i in x:
            com = "%s\n%s,%s,%s,%s" % (com, str(i), str(z[index]), str(y[index]), str(a[index]))
            index = index + 1
        if None == save_dir:
            pass
        else:
            fp = fp.split("/")[-1]
            fp = "%s/%s" % (save_dir, str(fp))
        fp_name = "%s.csv" % fp
        f = open("%s.csvx" % fp, "w")
        f.write(com)
        f.close()
        return fp_name
if __name__=="__main__":
    x = ana_rtt()
    #dp="/data/load_use/rtt_use/ping_time_500"
    #dp="/data/load_use/rtt_use/ping_time_1000_nst" #"2016,12,01,20,26,20", "2016,12,01,22,10,00"
    #dp="/data/load_use/rtt_use/ping_time_1500_nst" # "2016,12,02,10,05,00", "2016,12,02,12,00,00"
    #dp="/data/load_use/rtt_use/ping_time_1500" # "2016,12,01,13,00,00", "2016,12,01,15,30,59"
    #dp="/data/load_use/rtt_use/ping_time_2000_nst" # "2016,12,02,12,00,00", "2016,12,02,15,30,59"
    dp="/data/load_use/rtt_use/ping_time_2000" # "2016,12,01,16,00,00", "2016,12,01,18,10,59"
    x.doing(dp, "2016,12,01,16,00,00", "2016,12,01,18,10,59")
