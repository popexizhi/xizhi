#-*-coding:utf8-*-
import os, datetime, time
import re, sys
from ShellCon import sh_control
from Map import load_test_cfg


class mon_sta():
    def __init__(self):
        self.sh = sh_control()

    def split_log(self, head_tail_log, start_ms, end_ms):
        res = None
        print "*"*50
        print "split log in err_log or process...."
        print "%s: start_ms:%s ;end_ms: %s;" % (str(head_tail_log), str(start_ms), str(end_ms))
        #assert head_tail_log[0] <= head_tail_log[1] # head_tail_log 存在问题
        if head_tail_log[0] <= head_tail_log[1]: # head_tail_log 存在问题
            assert start_ms <= end_ms # split point 存在问题
        else:
            return res

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
    
    def process_dir_for_ana(self, dir_p, start_ms, end_ms):
        
        null_ue=[]
        res = self.sh.get_files_cmd(dir_p)
        list_res = {}
        now_date = datetime.datetime.now().strftime("%Y%m%d")
        err_dir = "/data/err_dir/%s_%st%s" % (now_date, str(start_ms), str(end_ms))
        new_dir = "/home/jenkins/test/process_%s_%sto%s" % (now_date, str(start_ms), str(end_ms))
        self.sh._com("mkdir %s" % new_dir)
        self.sh._com("mv %s/*  %s" % (dir_p, new_dir) )
#        for i in res:
#            if "" == i[0] or len(str(i[0]))>16:
#                null_ue.append(i[2])
#                self.sh._com("mv %s/%s %s" % (dir_p, i[2], new_dir) ) #0 files mv
#                continue
#            #print str(i)
#            #print dir_p
#            i = [int(i[0]), int(i[1]), i[2]]
#            split_num = self.split_log(i, start_ms, end_ms)
#            self.log("%s is %s" % (str(split_num), i[2]))
#            list_res[i[2]] = split_num
#            
#            if 0 == split_num:
#                self.zero_d(dir_p, i[2],"%s_%s" % (str(start_ms), str(end_ms)), err_dir)     
#            if 1 == split_num:
#                self.one_d((start_ms, end_ms), "%s/%s" % (new_dir, i[2]), "%s/%s" % (dir_p, i[2]))
#                self.zero_d(dir_p, i[2],"%s_%s" % (str(start_ms), str(end_ms)), err_dir)     
#            if 2 == split_num:
#                self.sh._com("mv %s/%s %s" % (dir_p, i[2], new_dir) )
#            if 3 == split_num:
#                self.one_d((start_ms, end_ms), "%s/%s" % (new_dir, i[2]), "%s/%s" % (dir_p, i[2]))
#            if 4 == split_num:
#                pass


        return new_dir, err_dir, list_res
    


    def zero_d(self, dir_p, fp, mess, err_fp):
        #save fp show err_mess
        cmd = "mv %s/%s %s/%s_%s" % (dir_p, fp, err_fp, fp, mess)
        self.sh._com(cmd)
        
    def one_d(self, ranges, n_fp, dir_old):
        self.sh.save_range_log_f(ranges, dir_old ,n_fp)

    def log(self, mes):
        print "[MoniterStart] %s" % mes

    def ana_use_dir(self, mes, filep):
        print "*" * 30
        str_ = 'echo "%s">>%s' % (str(mes), str(filep))
        self.sh._com(str_)
        print str_

    def save_rtt_data(self, rtt_process, res_dir, sta_time, end_time):
        self.sh.rtt_save_time_only(rtt_process, res_dir, sta_time, end_time)

    def filter_files(self, source_dir=load_test_cfg["source_dir"], process_dir=load_test_cfg["process_dir"], backup_dir=load_test_cfg["backup_dir"]):
        self.sh.get_dir_files(source_dir, process_dir, backup_dir)

    def tar_save_log(self, dir_process, dir_tar, format_file="log.txt"):
        #str_ = "mv %s/*%s* %s" % (dir_process, format_file, dir_tar)
        str_ = "rm -rf %s&&mkdir %s&&chmod 777 %s" % (dir_process,  dir_process, dir_process) #fix:不再保持直接删除,17-03-17
        self.sh._com(str_)

    def start_doing(self, start_time, long_time=load_test_cfg["long_time"], log_save_time=load_test_cfg["log_save_time"], is_wait = 1):
        self.log("start_time: %s" % str(start_time))
        
        diff_time = 0
        load_test_cfg["source_dir"] = "/home/lijie/load_use/"
        self.filter_files(load_test_cfg["source_dir"], load_test_cfg["process_dir"], load_test_cfg["backup_dir"])
        now_time = int(time.time())
        self.log("start process_dir_for_ana")

        self.tar_save_log(load_test_cfg["backup_dir"], load_test_cfg["tar_backup_dir"])
        sta_time = int(start_time*1000 - log_save_time*3600*1000) 
        end_time = int(start_time*1000) #单位毫秒
        res_dir, err_p, res = self.process_dir_for_ana(load_test_cfg["process_dir"], sta_time, end_time)
        print res_dir
        #assert 1 == 0 
        self.save_rtt_data(load_test_cfg["processRtt_dir"], res_dir, sta_time, end_time)
        #self.ana_use_dir(res_dir, load_test_cfg["ana_log"])
        print "python analysis_data_Ue.py %s" % res_dir
        

if __name__=="__main__":
    x =  mon_sta()
    x.start_doing(time.time())
