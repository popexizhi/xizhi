#-*-coding:utf8-*-
import os, datetime
import re
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


        return list_res
    


    def zero_d(self, dir_p, fp, mess, err_fp):
        #save fp show err_mess
        cmd = "mv %s/%s %s/%s_%s" % (dir_p, fp, err_fp, fp, mess)
        self.sh._com(cmd)
        
    def one_d(self, ranges, n_fp, dir_old):
        self.sh.save_range_log_f(ranges, dir_old ,n_fp)

    def log(self, mes):
        print "[MoniterStart] %s" % mes

if __name__=="__main__":
    x =  mon_sta()
    #dp = "/home/jenkins/test/process_20161118_111317/test"
    dp = "test"
    sta_time = 1479436452044
    end_time = 1479436745045
    res = x.process_dir(dp, sta_time, end_time)
