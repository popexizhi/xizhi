# -*- coding:utf8 -*-
import numpy
from dtojpg import dtjpg
import collections
import os, re
import math
from ShellCon import sh_control
class processt():
    def sta_sec(self, list_data):
        list_data = self.sort(list_data) #要求list_data中以毫秒为存储单位
        print list_data
        if len(list_data) == 0:
            return [] 
        old_d = list_data[0]
        j = 0
        s_sta = {}
        #2.将新值加入到s_stat
        s_sta[int(old_d[0]/1000)] = []
        s_sta[int(old_d[0]/1000)].append(old_d)

        for i in list_data[1:]:
            #print "*" *20
            #print i
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
        #for key in s_sta:
        #    print key
        #    print s_sta[key]
            #print "%s : %s" % (str(key), str(value))
        return s_sta
    
    def if_same_sec(self, now_s, def_s):
        res = ( int(def_s/1000) == int(now_s/1000) )
        return res
    
    def sort(self, list_data):
        x = numpy.argsort(list_data[:,0])#以第一列排序，返回之后的序列
        list_data = list_data[x] #重新调整列表顺序
        return list_data
    
    def loss(self, list_data, pre_totle):
        c_num = len(list_data)
        res = pre_totle - c_num
        print "loss num %d" % res
        return res
    
    def statistics_use(self, list_data, index):
        Max = max(list_data[:,index])
        Min = min(list_data[:,index])
        num = list_data.shape[0]
        avg = sum(list_data[:,index]) / num
        tps = num / avg 
        sdsq = sum([(i - avg) ** 2 for i in list_data[:,1]])
        stdev = (sdsq / (len(list_data) - 1)) ** .5
    
        print "Max %s Min %s num %s avg %s std %s ; TPS %s " % (str(Max), str(Min), str(num), str(avg), str(stdev), str(tps))
        return Max, Min, num, avg, str(stdev)
    
    def percentile(self, list_data):
        data_res =  []
        for i in list_data:
            data_res.append(int(i[0]))
        print data_res
        res = sorted(data_res)
        data_res = numpy.array(data_res)
        r1 = numpy.percentile(data_res, 25)
        r2 = numpy.percentile(data_res, 50)
        r3 = numpy.percentile(data_res, 75)
        r4 = numpy.percentile(data_res, 100)
        
        #print numpy.bincount(data_res)
        #print r1, r2 ,r3,r4

        return res
    
    def zero_num(self, list_data, def_num = 0):
        res = {}
        for i in list_data:
            if def_num == i[0] :
                res[i[1]] = i[0]
        return res
    
    def limit(self, list_data, limit_num, limit_end = 0):
        "[limit_end, limit_num) 直接的的res"
        res = {}
        for i in list_data:
            if (i[0] >= limit_end) and (i[0] < limit_num):
                res[i[1]] = i[0]

        return res
    def get_num_list(self, list_data):
        x = sorted(list_data)
        res = {}
        old = x[0][0]
        res[old] = 1
        for i in x[1:]:
            i = i[0]
            if i == old:
                res[old] = res[old] + 1
            else:
                old = i
                res[old] = 1
        print len(res)
        resD = numpy.zeros((len(res), 2))
        index = 0
        for key in res:
            resD[index:,] = [key, res[key]]
            index = index + 1

        return resD
        
    def test_get_num_list(self):
        """
        """
        x = [[2550, 'ue.down.hostid.15419.pid.43844.log.txt_4'], [2418, 'ue.down.hostid.21320.pid.35105.log.txt_4'], [1605, 'ue.down.hostid.24302.pid.118781.log.txt_4'], [1374, 'ue.down.hostid.21272.pid.114338.log.txt_4'], [2567, 'ue.down.hostid.34309.pid.39941.log.txt_4'], [1496, 'ue.down.hostid.15251.pid.41784.log.txt_4'], [508, 'ue.down.hostid.15449.pid.165843.log.txt_4'], [3006, 'ue.down.hostid.30381.pid.130547.log.txt_4'], [1957, 'ue.down.hostid.15326.pid.42800.log.txt_4'], [2514, 'ue.down.hostid.32407.pid.139733.log.txt_4'], [2738, 'ue.down.hostid.3361.pid.135760.log.txt_4'], [2775, 'ue.down.hostid.27270.pid.21273.log.txt_4']]

        print self.get_num_list(x)

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

    def file2matrix(self, filename):
        fr = open(filename)
        arrayOLlines_len = len(fr.readlines())
        if 0 == arrayOLlines_len:
            print "%s is null" % filename
            return -1
        print "arrayOLlines_len %s" % str(arrayOLlines_len)
        returnMat = numpy.zeros((arrayOLlines_len, 4))
        index = 0
        diff_time = 0#92000 # appserver 与ue的server时间差, 单位:毫秒
        fr = open(filename)
        for line in fr.readlines():
            line = line.split("\n")[0]
            listFromline = line.split(",")
            if len(listFromline) < (2-1): # numpy.zeros 初始化时的形状要求，如果小于这个值，说明数据不完整
                continue
            if len(re.findall(u"\D", listFromline[0]))> 0 or len(re.findall(u"\D", listFromline[1]))> 0 : #行数据不完整,忽略此内容
                listFromline[1] = listFromline[1].split(" ")[0] #处理结尾的空格
                if len(re.findall(u"\D", listFromline[0]))> 0 or len(re.findall(u"\D", listFromline[1]))> 0 : #行数据不完整,忽略此内容
                    print "(%s) \\D" % str(listFromline)
                    continue
                else:
                    pass #继续处理
            listFromline_res = [listFromline[0], listFromline[1], 0, 0]
            listFromline_res[1] = int(listFromline_res[0]) - int(listFromline_res[1]) + diff_time #use_time = receive_time - send_time + diff_time
            
            returnMat[index,:] = listFromline_res
            index +=1

        fr.close()
        return returnMat

    def test_file2matrix(self):
        filename = "testdata/6063.log"
        res = self.file2matrix(filename)
        print res[:,0] + res[:,1]
        #print res[:,1]
    
    def dir2matrix(self, dirname, filename="test/test_soure"):
        sh_com = sh_control()
        fl, ll = sh_com.get_dir_files_lines(dirname)
        arrayOLlines_len = sum(ll)
        if 0 == arrayOLlines_len:
            print "%s is null" % dirname
            return -1, -1
        returnMat = numpy.zeros((arrayOLlines_len, 4))
        index = 0
        #get diff_time
        diff_ue_dir = self.get_diff_time(diff_file="regulate_time/use.log")
        er_fd = {}
        f = open(filename,"w")
        for i in fl:
            #get ueid for filename
            ueid = self.get_ueid_for_filename(i)
            #diff_time = float(diff_ue_dir[ueid]) #为diff_data赋值,为空没有处理
            diff_time = float(0.0) #使用机器矫时，不再使用校正文件
            fr = open("%s/%s" % (dirname, i))
            err_line = 0
            max_err = 0
            for line in fr.readlines():
                line = line.split("\n")[0]
                listFromline = line.split(",")
                if -1 == self.check_data(listFromline): # numpy.zeros 数据完整性处理
                    continue
                listFromline_res = [listFromline[0], listFromline[2], listFromline[1], ueid]
                listFromline_res[1] = self.minus(listFromline[0], listFromline[1] , diff_time)
                #print listFromline_res
                f.write("%s\n" % str(listFromline_res))
                if 0<=listFromline_res[1] < 60000 : #如果存在此问题请检查appserver 与ue的主机时间
                    pass
                else:
                    err_line = err_line + 1
                    #er_fd[i] = err_line
                    #listFromline_res[1] = 500 # 使用0.5s作为差错处理结果
                    max_err = max_err if max_err < listFromline_res[1] else listFromline_res[1] # 记录最小差异
                returnMat[index,:] = listFromline_res
                index +=1
            er_fd[ueid] = max_err

            fr.close()
        f.close()
        return returnMat, er_fd
    def check_data(self, list_line):
        res = -1
        if len(list_line) < (4-1): # numpy.zeros 初始化时的形状要求，如果小于这个值，说明数据不完整 
            return res
        for i in list_line:
            if re.findall(u"\c", i):
                return -1

        return 0 #检查通过

    def minus(self, d1, d2, d3):
        if float(d3)>0:
            d3 = 0
        res =  float(d1) - (float(d2) + float(d3)*1000) #d3 单位转换
        return res

    def get_diff_time(self, diff_file):
        res = {}
        f = open(diff_file)
        com = f.readlines()
        f.close()
        for i in com:
            line = i.split("\n")[0].split(",")
            res[line[0]] = line[1]
        return res
    def get_ueid_for_filename(self, filename, reg_str=u"\d\d*"):
        res = None
        res = re.findall(reg_str, filename)[0]
        return res
    def get_files(self, path, format_str="log"):
        """
            return path  file
        """
        res_files = []
        for i in os.listdir(path):
            if re.findall(format_str, i):
               res_files.append("%s/%s" % (str(path), str(i)))
        return res_files    

    def test_get_files(self):
        path = "testdata"
        res_l = self.get_files(path)
        for i in res_l:
            datas = self.file2matrix(i)
            print datas
if __name__=="__main__":
    x = processt()
    #x.test_file2matrix()
    #x.test_get_files()
    x.test_get_num_list()
