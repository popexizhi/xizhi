# -*- coding:utf8 -*-
import numpy

def sta_sec(list_data):
    sort(list_data) #要求list_data中以毫秒为存储单位
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

def sort(list_data):
    #list_data.argsort()
    print "numpy.argsort(list_data, axis=0)"
    x = numpy.argsort(list_data[:,0])
    list_data = list_data[x]
    print x
    print list_data
    print "***********************************"

def test_sta_sec():
    list_data = numpy.zeros((5, 4))
    list_data[0]=[485643, 1, 133852, 635]
    list_data[1]=[475992, 2, 133852, 196]
    list_data[2]=[495140, 3, 133852, 606]
    list_data[3]=[435714, 4, 133852, 385]
    list_data[4]=[455678, 5, 133852, 387]
    print list_data
    sta_sec(list_data)

test_sta_sec()
