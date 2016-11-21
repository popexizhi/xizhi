#-*-coding:utf8-*-
import os, datetime, time
import re, sys
from ShellCon import sh_control

class mon_sta():
    def __init__(self):
        self.sh = sh_control()

    def split_log(self, head_tail_log, start_ms, end_ms):
        res = None
        assert head_tail_log[0] <= head_tail_log[1] # head_tail_log 存在问题
        assert start_ms <= end_ms # split point 存在问题

        print "%s: start_ms:%s ;end_ms: %s;" % (str(head_tail_log), str(start_ms), str(end_ms))
        if head_tail_log[1] <= start_ms:
            return 0
        #if (end_ms <= head_tail_log[0]) and (head_tail_log[0]!= head_tail_log[1]): #如果只有一个点请在2中处理
        if ( (end_ms <= head_tail_log[0]) and (head_tail_log[0]!= head_tail_log[1]) )  or (end_ms < head_tail_log[0] and head_tail_log[0]== head_tail_log[1]): #fix对远离点的有一个点请在2中处理
            return 4
        if (start_ms <= head_tail_log[0]) and (head_tail_log[1] <= end_ms):
            return 2
        if head_tail_log[0] < start_ms < head_tail_log[1] <= end_ms :
            return 1
        if start_ms <= head_tail_log[0] < end_ms < head_tail_log[1] :
            return 3
        if head_tail_log[0] < start_ms < end_ms < head_tail_log[1]:
            return 5
        return res
    
    def process_dir(self, dir_p, start_ms, end_ms):
        
        null_ue=[]
        res = self.sh.get_files_cmd(dir_p)
        list_res = {}
        now_date = datetime.datetime.now().strftime("%Y%m%d")
        err_dir = "/data/err_dir/%s_%st%s" % (now_date, str(start_ms), str(end_ms))
        new_dir = "/home/jenkins/test/process_%s_%sto%s" % (now_date, str(start_ms), str(end_ms))
        self.sh._com("mkdir %s" % new_dir)
        self.sh._com("mkdir %s" % err_dir)
        for i in res:
            if "" == i[0]:
                null_ue.append(i[2])
                self.sh._com("mv %s/%s %s" % (dir_p, i[2], new_dir) ) #0 files mv
                continue
            i = [int(i[0]), int(i[1]), i[2]]
            split_num = self.split_log(i, start_ms, end_ms)
            self.log("%s is %s" % (str(split_num), i[2]))
            list_res[i[2]] = split_num
            
            if 0 == split_num:
                self.zero_d(dir_p, i[2],"%s_%s" % (str(start_ms), str(end_ms)), err_dir)     
            if 1 == split_num:
                self.one_d((start_ms, end_ms), "%s/%s" % (new_dir, i[2]), "%s/%s" % (dir_p, i[2]))
                self.zero_d(dir_p, i[2],"%s_%s" % (str(start_ms), str(end_ms)), err_dir)     
            if 2 == split_num:
                self.sh._com("mv %s/%s %s" % (dir_p, i[2], new_dir) )
            if 3 == split_num:
                self.one_d((start_ms, end_ms), "%s/%s" % (new_dir, i[2]), "%s/%s" % (dir_p, i[2]))
            if 4 == split_num:
                pass


        return new_dir, err_dir, list_res
    


    def zero_d(self, dir_p, fp, mess, err_fp):
        #save fp show err_mess
        cmd = "mv %s/%s %s/%s_%s" % (dir_p, fp, err_fp, fp, mess)
        self.sh._com(cmd)
        
    def one_d(self, ranges, n_fp, dir_old):
        self.sh.save_range_log_f(ranges, dir_old ,n_fp)

    def log(self, mes):
        print "[MoniterStart] %s" % mes

if __name__=="__main__":
    dp = sys.argv[1] #文件路径
    print "dp %s" % dp
    long_t = int(sys.argv[3]) * 1000 #单位:s,转换为毫秒
    print "long_t %d" % long_t 
    sta_t = sys.argv[2] #
    print "sta_t %s" % sta_t
    time_l = sta_t.split(",") #开始时间,使用,分割
    print len(time_l)
    time_l = [int(time_l[0]), int(time_l[1]),int(time_l[2]), int(time_l[3]), int(time_l[4]),int(time_l[5]), 0, 0, 0]
    print "time_l %s" % str(time_l)
    date = time.mktime(time_l)
    print date
    #dp = "/home/jenkins/test/process_20161121_072124"
    #dp = "/home/jenkins/test/process_20161121_090514"
    #date = time.mktime([2016,11,21,05,38,00,0,0,0])
    #long_t = 3600 * 1000 * 2
    sta_time = int(date*1000)
    end_time = int(date*1000 + long_t)
    print "dp %s; sta_time :%s; end_time : %s" % (dp, str(sta_time), str(end_time))
    #assert 1 == 0
    x =  mon_sta()
    res_dir, err_p, res = x.process_dir(dp, sta_time, end_time)
    from analysis_data import use_report
    use_report(res_dir)
