# -*- coding:utf8 -*-
import numpy

def sta_sec(list_data):
    list_data = sort(list_data) #要求list_data中以毫秒为存储单位
    print list_data
    old_d = list_data[0]
    s_sta = {}
    for i in list_data[1:]:
        print "*" *20
        print i
        if if_same_sec(i[0], old_d[0]):
            #同一计数单位，存储
            s_sta[int(old_d[0]/1000)].append(i) 
            
        else:
            #1.记录新的old_d
            old_d = i
            #2.将新值加入到s_stat
            s_sta[int(old_d[0]/1000)] = []
            s_sta[int(old_d[0]/1000)].append(i)
    for key in s_sta:
        print key
        print s_sta[key]
        #print "%s : %s" % (str(key), str(value))
    return s_sta

def if_same_sec(now_s, def_s):
    res = ( int(def_s/1000) == int(now_s/1000) )
    #print "def_s/1000 == now_s/1000 %s" % str(res)
    #print "def_s %d == now_s %d" % (int(now_s/1000), int(def_s/1000))
    return res

def sort(list_data):
    x = numpy.argsort(list_data[:,0])#以第一列排序，返回之后的序列
    list_data = list_data[x] #重新调整列表顺序
    return list_data

def TPS(s_sta):
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
        print "%s : %d" % (str(sec), num)
        x_res.append(sec)
        y_res.append(num)

    return x_res, y_res

def use_time_second(s_sta):
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

def test_sta_sec():
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
    sta_sec(list_data)

def test_TPS():
    list_data = numpy.zeros((8, 4))
    list_data[0]=[485643, 1, 133852, 635]
    list_data[1]=[475992, 2, 133852, 196]
    list_data[2]=[495140, 3, 133852, 606]
    list_data[3]=[435714, 4, 133852, 385]
    list_data[4]=[455678, 5, 133852, 387]
    list_data[5]=[485633, 13, 133852, 636]
    list_data[6]=[485443, 14, 133852, 637]
    list_data[7]=[485999, 15, 133852, 638]
    res = sta_sec(list_data)
    print TPS(res)

def test_use_time_second():
    list_data = numpy.zeros((8, 4))
    list_data[0]=[485643, 1, 133852, 635]
    list_data[1]=[475992, 2, 133852, 196]
    list_data[2]=[495140, 3, 133852, 606]
    list_data[3]=[435714, 4, 133852, 385]
    list_data[4]=[455678, 5, 133852, 387]
    list_data[5]=[485633, 13, 133852, 636]
    list_data[6]=[485443, 14, 133852, 637]
    list_data[7]=[485999, 15, 133852, 638]
    res = sta_sec(list_data)
    print use_time_second(res)

#test_sta_sec()
#test_TPS()
test_use_time_second()
