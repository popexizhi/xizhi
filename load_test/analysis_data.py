# -*- coding:utf8 -*-
import datetime, time
import numpy
from reportwriter import Report
from processt import processt
from getjpg import dtjpg
import random
from ShellCon import sh_control
import sys

PRE_PACK=10 #单ue预定义的发包量
UE_NUM = 3000 #ue数量
class analy_d():
    def __init__(self):
        self.processt = processt()
        self.jpg = dtjpg()
        self.sh = sh_control()
        self.now_lab = str(int(time.time()))
        self.rh = Report("test/test_%s" % str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")))
    
    def get_z(self, path):
        """从ue.down.hostid.10279.pid.169185.log.txt_4 中获得log.txt_后的数字 """
        res = float(path.split("log.txt_")[-1])
        return res
    def test_get_z(self):
        file_p = "ue.down.hostid.10279.pid.169185.log.txt_4"
        assert 4.0 == self.get_z(file_p)


    def one_ue(self, path, jpg_path="test/one_ue"):
        pre_pack = self.get_z(path)
        datas = self.processt.file2matrix(path)
        if type(-1) == type(datas):
            return -1 #文件为空
        res = self.processt.sta_sec(datas)      
        x_t, y_t = self.processt.TPS(res)
        z_t = []
        for i in x_t:
            #z_t.append(PRE_PACK)
            z_t.append(pre_pack)
        print "start get jpg %s" % str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))
        res = self.diff_jpg(x_t, y_t, z_t, jpg_path, diff_min=1) 
        print "end get jpg %s" % str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))

        return res
    
    def static_ue_list(self, path):
        res = self.sh.get_files_wc(path)
        #res = self.processt.percentile(res)
        # zero ue个数统计
        res_z = self.processt.zero_num(res) 
        print "zero_ue %d" % len(res_z)
        
        #30 s 以下传输数据ue统计
        pack_s_num = self.get_z(res[0][1]) #当前固定使用第一个文件的后缀作为标准获取内容
        res_limit = self.processt.limit(res, limit_num=pack_s_num*30, limit_end = 1)
        print "res_limit_len %d " % len(res_limit)
        #print "res_limit %s " % res_limit

        #jpg
        f_p = "test/cookue%s" % str(self.now_lab)
        labes_u = [u'0 package', u'>30s', u'others']
        other = len(res) - len(res_z) - len(res_limit)
        sizes_u = [len(res_z), len(res_limit), other]
        cook_jpg = self.jpg.get_cook_jpg(labes_u, sizes_u, f_p)
        res_list = {}
        res_list[labes_u[0]] = res_z 
        res_list[labes_u[1]] = res_limit 
        self.rh.set_cooke_list(res_list, cook_jpg)
        return res_z, res_limit, cook_jpg 

    def random_ue_list(self, ue_list_dir, num=10):
        """
        1.随机筛选
        2.生成图表，保存报告
        """
        #1.
        ue_list_p = self.sh.get_ue_log(ue_list_dir) 
        ue_list =[]
        f = open(ue_list_p)
        ue_list = f.readlines()
        f.close()
        rand_ue_dir = self.get_rand(ue_list, num)
        print "********************:%d" % len(rand_ue_dir)
        print rand_ue_dir

        #2.
        res_dir ={}
        for key in rand_ue_dir:
            path_ue = "%s/%s" % (str(ue_list_dir), str(rand_ue_dir[key]))
            print "path_ue: %s" % path_ue
            res = self.one_ue(path_ue, "test/one%s_%s" % (str(self.now_lab), str(rand_ue_dir[key]))) #_%s_" % str(self.now_lab)
            res_dir[str(rand_ue_dir[key])] = res

        print "all " * 20
        print res_dir
        for key in res_dir:
            self.rh.set_h3_sum_list("%s" % str(key), res_dir[key])


    def get_rand(self, ue_list , num):
        res = {}
        while len(res) < num :
            x = random.randint(0, len(ue_list)-1)
            print x
            print ue_list[x]
            res[x] = ue_list[x].split("\n")[0]
        return res

    def diff_jpg(self, x_t, y_t, z_t, path, diff_min = 10):   
        #diff_min = 10 #分割图使用时间 默认为10min
        diff_min = 60 * diff_min #
        print len(x_t)
        #assert len(x_t) > diff_min
        print len(y_t)
        #assert len(y_t) > diff_min
        #assert len(z_t) > diff_min
        t = int(len(x_t)/diff_min) + 1 
        res_l = []
        for z in xrange(t):
            save_path = "%s_%s" % (str(path),str(z))
            print "start %s.jpg" % save_path
            sta_point = z * diff_min
            end_point = (z+1) * diff_min if (z+1)*diff_min<len(x_t) else len(x_t)
            print "sta : %s; end: %s" % (str(sta_point), str(end_point))
            self.jpg.test_straight_line(x_t[sta_point:end_point], y_t[sta_point:end_point], z_t[sta_point:end_point], save_path, y_max=y_t)
            res_l.append(save_path)

        return res_l

    def get_report(self, path):
        #get datas
        pre_data = 100
        loss = 0
        uedir, uelog = self.sh.save_ue_log(path)
        for i in self.processt.get_files(uedir):
            datas = self.processt.file2matrix(i)
            if type(-1) == type(datas):
                return -1 #无数据处理
            loss = loss + self.processt.loss(datas, pre_data)
            res = self.processt.statistics_use(datas, 1)
            dl = {"Max(microsecond)":res[0], "Min(microsecond)":res[1] , "num": res[2], "avg": res[3], "stdev": res[4]}
            #assert 1 == 0                
            res = self.processt.sta_sec(datas)

            x_t, y_t = self.processt.TPS(res)
            z_t = []
            
            for u in x_t:
                z_t.append(PRE_PACK*UE_NUM)    
            tps_jpg_name = "test/tps_%s_" % str(self.now_lab)
            #self.jpg.get_jpg(x_t, y_t, tps_jpg_name)
            tps_jpg_list = self.diff_jpg(x_t, y_t, z_t, tps_jpg_name)
            
            x_u, y_u = self.processt.use_time_second(res)
            use_time_jpg_name = "test/use_time_second_%s_" % str(self.now_lab)
            #self.jpg.get_jpg(x_u, y_u, use_time_jpg_name)
            use_time_list = self.diff_jpg(x_u, y_u, [],use_time_jpg_name)
            
            #save html
            self.rh.set_summary(dl)
            self.rh.set_h3_sum_list("tps", tps_jpg_list)
            self.rh.set_h3_sum_list("use_time_second", use_time_list)
           

    def save_report(self):
        self.sh.back_test()


def use_report(dir_ue_log="/home/jenkins/test/process"):
    x = analy_d()
    #dir_ue_log="/home/jenkins/test/old/old"
    if (-1 == x.get_report(dir_ue_log)):
        print "no data"
    else:    
        #x.one_ue("one_ue.log")
        x.static_ue_list(dir_ue_log)
        x.random_ue_list(dir_ue_log)
        
        #x.static_ue_list(dir_ue_log)
        x.save_report()
        
def test():
    x = analy_d()
    #x.test_get_z()
    x.static_ue_list("/home/jenkins/test/process_20161109_123112")

if __name__=="__main__":
    try:
        dir_ue_log = sys.argv[1]
    except IndexError:
        dir_ue_log = None
    
    if None != dir_ue_log:
        print "use path %s" % dir_ue_log
        use_report(dir_ue_log)
    if "test" == dir_ue_log:
        test()
    else:
        #test()
        #assert 1 == 0
        use_report()
