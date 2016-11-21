#-*-coding:utf8-*-
import os, time
import re
from ShellCon import sh_control

class mon_sta():
    def __init__(self):
        self.sh = sh_control()

    def get_file_last_time(self, fp):
        pass
    
    def get_dir_first_last(self, dir_p):
        
        null_ue=[]
        res = self.sh.
        for i in res:
            if "" == i[0]:
                null_ue.append(i[1])
                continue
            if start_ms < int(i[0]) <= end_ms:
                print "%s is %d< %s <=%d" % (i[1], start_ms, i[0], end_ms)
            else:
                #print "err %d< %s <=%d" % (int(start_ms - long_ms), i[0], start_ms)
                pass
    

if __name__=="__main__":
    x =  mon_sta()
    dp = "/home/jenkins/test/process_20161118_111317/"
    wait_time = 30*60*1000 
    #end_time = int(time.time()*1000) - wait_time
    end_time = 1479432160000
    res = x.get_dir_last(dp, end_time, wait_time)
