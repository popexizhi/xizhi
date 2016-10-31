# -*- coding:utf8 -*-
import numpy
from dtojpg import dtjpg
import collections
class processt():
    def sta_sec(self, list_data):
        list_data = self.sort(list_data) #要求list_data中以毫秒为存储单位
        print list_data
        old_d = list_data[0]
        j = 0
        s_sta = {}
        #2.将新值加入到s_stat
        s_sta[int(old_d[0]/1000)] = []
        s_sta[int(old_d[0]/1000)].append(old_d)

        for i in list_data[1:]:
            print "*" *20
            print i
            j = j + 1
            if self.if_same_sec(i[0], old_d[0]):
                #同一计数单位，存储
                #print "key is %s" % str(int(old_d[0]/1000))
                s_sta[int(old_d[0]/1000)].append(i) 
                
            else:
                #1.记录新的old_d
                old_d = i
                #2.将新值加入到s_stat
                s_sta[int(old_d[0]/1000)] = []
                s_sta[int(old_d[0]/1000)].append(i)
    
        s_sta = collections.OrderedDict(sorted(s_sta.items())) #按key对dist排序
        for key in s_sta:
            print key
            print s_sta[key]
            #print "%s : %s" % (str(key), str(value))
        return s_sta
    
    def if_same_sec(self, now_s, def_s):
        res = ( int(def_s/1000) == int(now_s/1000) )
        return res
    
    def sort(self, list_data):
        x = numpy.argsort(list_data[:,0])#以第一列排序，返回之后的序列
        list_data = list_data[x] #重新调整列表顺序
        return list_data
    
    def TPS(self, s_sta):
        """
        s_sta : {key[second] : array[list] }
        eg:
            475
            [array([  4.75992000e+05,   2.00000000e+00,   1.33852000e+05,   1.96000000e+02])]
    		495
    		[array([  4.95140000e+05,   3.00000000e+00,   1.33852000e+05,   6.06000000e+02])]
    		485
    		[array([  4.85443000e+05,   1.40000000e+01,   1.33852000e+05,   6.37000000e+02]), 
             array([  4.85633000e+05,   1.30000000e+01,   1.33852000e+05,   6.36000000e+02]), 
             array([  4.85643000e+05,   1.00000000e+00,   1.33852000e+05,   6.35000000e+02]), 
             array([  4.85999000e+05,   1.50000000e+01,   1.33852000e+05,	6.38000000e+02])]
    		455
    		[array([  4.55678000e+05,   5.00000000e+00,   1.33852000e+05,	3.87000000e+02])]
        """
        x_res = [] 
        y_res = []
        size = len(s_sta)
        #res = numpy.zeros((size,2))
        #index = 0
        res = []
        #od = collections.OrderedDict(sorted(s_sta.items())) #按key对dist排序
        for sec in s_sta:
            num = len(s_sta[sec])
            print "%s : %d" % (str(sec), num)
            #res.append([sec, num])
            x_res.append(sec)
            y_res.append(num)
        
        return x_res, y_res
    
    def use_time_second(self, s_sta):
        """
        s_sta : {key[second] : array[list] }
        eg:
            475
            [array([  4.75992000e+05,   2.00000000e+00,   1.33852000e+05,   1.96000000e+02])]
    		495
    		[array([  4.95140000e+05,   3.00000000e+00,   1.33852000e+05,   6.06000000e+02])]
    		485
    		[array([  4.85443000e+05,   1.40000000e+01,   1.33852000e+05,   6.37000000e+02]), 
             array([  4.85633000e+05,   1.30000000e+01,   1.33852000e+05,   6.36000000e+02]), 
             array([  4.85643000e+05,   1.00000000e+00,   1.33852000e+05,   6.35000000e+02]), 
             array([  4.85999000e+05,   1.50000000e+01,   1.33852000e+05,	6.38000000e+02])]
    		455
    		[array([  4.55678000e+05,   5.00000000e+00,   1.33852000e+05,	3.87000000e+02])]
        """
        x_res = []
        y_res = []
        for sec in s_sta:
            num = len(s_sta[sec])
            sum_use_time = 0
            for use_time in s_sta[sec]:
                sum_use_time = sum_use_time + use_time[1]
            #sum_use_time = s_sta[sec].sum(argsort)
            arg_use_time  = sum_use_time / num 
            print "%s : %d, %f" % (str(sec), sum_use_time, arg_use_time)
            x_res.append(sec)
            y_res.append(arg_use_time)
    
        return x_res, y_res
    
    def test_sta_sec(self):
        list_data = numpy.zeros((8, 4))
        # recevie_time, use_time, hostid, package_num
        list_data[0]=[485643, 1, 133852, 635]
        list_data[1]=[475992, 2, 133852, 196]
        list_data[2]=[495140, 3, 133852, 606]
        list_data[3]=[435714, 4, 133852, 385]
        list_data[4]=[455678, 5, 133852, 387]
        list_data[5]=[485633, 13, 133852, 636]
        list_data[6]=[485443, 14, 133852, 637]
        list_data[7]=[485999, 15, 133852, 638]
        print list_data
        self.sta_sec(list_data)
    
    def test_TPS(self):
        list_data = numpy.zeros((8, 4))
        list_data[0]=[485643, 1, 133852, 635]
        list_data[1]=[475992, 2, 133852, 196]
        list_data[2]=[495140, 3, 133852, 606]
        list_data[3]=[435714, 4, 133852, 385]
        list_data[4]=[455678, 5, 133852, 387]
        list_data[5]=[485633, 13, 133852, 636]
        list_data[6]=[485443, 14, 133852, 637]
        list_data[7]=[485999, 15, 133852, 638]
        res = self.sta_sec(list_data)
        x, y = self.TPS(res)
        print x
        print y
        b = dtjpg()
        b.get_jpg(x, y, "TPS")
    
    def test_use_time_second(self):
        list_data = numpy.zeros((8, 4))
        list_data[0]=[485643, 1, 133852, 635]
        list_data[1]=[475992, 2, 133852, 196]
        list_data[2]=[495140, 3, 133852, 606]
        list_data[3]=[435714, 4, 133852, 385]
        list_data[4]=[455678, 5, 133852, 387]
        list_data[5]=[485633, 13, 133852, 636]
        list_data[6]=[485443, 14, 133852, 637]
        list_data[7]=[485999, 15, 133852, 638]
        res = self.sta_sec(list_data)
        x, y =  self.use_time_second(res)
        print x
        print y
        b = dtjpg()
        b.get_jpg(x, y, "use_time")
    #test_sta_sec()
    #test_TPS()
    #test_use_time_second()
