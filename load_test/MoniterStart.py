#-*-coding:utf8-*-
import os, time
import re
from ShellCon import sh_control

class mon_sta():
    def __init__(self):
        self.sh = sh_control()

    def split_log(self, head_tail_log, start_ms, end_ms):
        res = None
        assert head_tail_log[0] <= head_tail_log[1] # head_tail_log 存在问题
        assert start_ms <= end_ms # split point 存在问题

        print "%s: start_ms:%s ;end_ms: %s;" % (str(head_tail_log[2]), str(start_ms), str(end_ms))
        if head_tail_log[1] <= start_ms:
            return 0
        if (end_ms <= head_tail_log[0]) and (head_tail_log[0]!= head_tail_log[1]): #如果只有一个点请在2中处理
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
        for i in res:
            if "" == i[0]:
                null_ue.append(i[1])
                continue
            split_num = self.split_log(i)
            print "%s is %s" % (str(split_num), i[2])

if __name__=="__main__":
    x =  mon_sta()
    dp = "/home/jenkins/test/process_20161118_111317/"
    wait_time = 30*60*1000 
    #end_time = int(time.time()*1000) - wait_time
    end_time = 1479432160000
    res = x.get_dir_last(dp, end_time, wait_time)
