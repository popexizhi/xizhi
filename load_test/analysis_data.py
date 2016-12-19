# -*- coding:utf8 -*-
import datetime, time
import numpy
from reportwriter import Report
from processt import processt
from getjpg import dtjpg
import random
from ShellCon import sh_control
import sys
from ana_rttx import ana_rtt 


PRE_PACK=10 #单ue预定义的发包量
UE_NUM = 3000 #ue数量
class analy_d():
    def __init__(self):
        self.processt = processt()
        self.jpg = dtjpg()
        self.sh = sh_control()
        self.now_lab = str(int(time.time()))
        self.ana_rtt = ana_rtt()
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
        
        dis = {"one_ue": [x_t, y_t]}
        f_ue = self.save_txt(dis, str(jpg_path))
        
        res = self.diff_jpg(x_t, y_t, z_t, jpg_path, diff_min=1) 
        print "end get jpg %s" % str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S"))

        return res
   
    def ues_packages_line(self, res_list):
        #ue packages line
        resD = self.processt.get_num_list(res_list)
        f_p = "test/ues_package_line_%s" % str(self.now_lab)
            
        resD_jpg_p = self.jpg.test_straight_line_u(resD[:,0], resD[:,1],[],filename = f_p, dev=500)
        print resD_jpg_p

    def static_ue_list(self, path):
        res = self.sh.get_files_wc(path)
        dis = {"static_ue_package": [res]}
        f_ue = self.save_txt(dis, "test/static_ue_list%s" % str(self.now_lab))
        
        self.ues_packages_line(res) 


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
        labes_u = [u'0 package', u'<30s', u'others']
        other = len(res) - len(res_z) - len(res_limit)
        sizes_u = [len(res_z), len(res_limit), other]
        cook_jpg = self.jpg.get_cook_jpg(labes_u, sizes_u, f_p)
        res_list = {}
        res_list[labes_u[0]] = res_z 
        res_list[labes_u[1]] = res_limit
        title_name = "totle_ue_num :%d, 0 packages:%d, <30s packages:%d" % (len(res), len(res_z), len(res_limit))
        self.rh.set_cooke_list(res_list, cook_jpg, title_name)
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
        if num >= len(ue_list): #如果被抽取样本不足num无法抽取
            num = len(ue_list) -2 
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
    
    def get_ana_rtt(self, path, data_dir):
        sta = path.split("_")[-1].split("to")[-2]
        end = path.split("_")[-1].split("to")[-1]
        rtt_d = "%s/%sto%s.rttd" % (path, sta, end.split("/")[0])
        res_d = self.ana_rtt.doing(rtt_d, None, None, data_dir)
        if -1 == res_d[0]:
            return -1
        cvs_f = res_d[0].split("/")[-1]
        dl = res_d[1]
        res_rtt = {"dl":dl, "name": "rtt", "csv": cvs_f, "dir":data_dir}
        return res_rtt
        

    def get_report(self, path):
        #get datas
        pre_data = 100
        loss = 0
        #uedir, uelog = self.sh.save_ue_log(path)
        #for i in self.processt.get_files(uedir):  #使用文件加载
            #datas = self.processt.file2matrix(i)
        for i in [1]:
            datas, er_fd = self.processt.dir2matrix(path, "test/test/soure_%s" % self.now_lab) #加载文件夹中全部log的数据
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
            dis = {"tps": [x_t, y_t, z_t]}
            f_ue = self.save_txt(dis, str(tps_jpg_name))
            tps_jpg_list = self.diff_jpg(x_t, y_t, z_t, tps_jpg_name)

            #rtt 
            res_rtt = self.get_ana_rtt(path, "test/rtt_data")
            if type(-1) != type(res_rtt):
                rtt_dl = res_rtt["dl"]
                rtt_name = res_rtt["name"]
                rtt_csv = res_rtt["csv"]
                rtt_dir = res_rtt["dir"]
            else:
                rtt_dl = {}
                rtt_name = "null"
                rtt_csv = ""
                rtt_dir = ""
            #use_time
            x_u, y_u = self.processt.use_time_second(res)
            use_time_jpg_name = "test/use_time_second_%s_" % str(self.now_lab)
            #self.jpg.get_jpg(x_u, y_u, use_time_jpg_name)
            dis = {"use_time": [x_u, y_u], "err_use_time_file": [er_fd]}
            f_ue = self.save_txt(dis, str(use_time_jpg_name))
            use_time_list = self.diff_jpg(x_u, y_u, [],use_time_jpg_name)
            
            #save html
            self.rh.set_summary(dl)
            self.rh.set_h3_sum_list("tps", tps_jpg_list)
            self.rh.rtt_set(rtt_dl, rtt_name, rtt_csv, rtt_dir)
            self.rh.set_h3_sum_list("use_time_second", use_time_list)
           

    def save_report(self):
        self.sh.back_test()

    def save_process_data(self, dir_ue_log):
        self.sh.tar_save(dir_ue_log)

    def save_txt(self, data_l, file_name):
        file_p = "%s.txt" % str(file_name)
        com = "t1,t2,t3"
        for key in data_l:
            com = com + "%s:\n" % str(key)
            for value in data_l[key]:
                com = com + "%s," % str(value)

        f = open(file_p, "w")
        f.write(com)
        f.close()

        return file_p

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
    #dir_p = "/home/jenkins/test/process_20161110_135236/"
    dir_p = "/home/jenkins/test/process_20161116_160840/"
    x.get_report(dir_p)
    #x.static_ue_list(dir_p)
    #x.random_ue_list(dir_p)

if __name__=="__main__":
    try:
        dir_ue_log = sys.argv[1]
    except IndexError:
        dir_ue_log = None
    print "dir_ue_log "+str(dir_ue_log) 
    if "test" == dir_ue_log:
        test()
    if None != dir_ue_log:
        print "use path %s" % dir_ue_log
        use_report(dir_ue_log)
    else:
        #test()
        #assert 1 == 0
        use_report()
