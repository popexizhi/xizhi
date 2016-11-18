#-*-coding:utf8-*-
import os
import re
from ShellCon import sh_control

class mon_sta():
    def __init__(self):
        self.sh = sh_control()

    def get_file_last_time(self, fp):
        pass
    
    def get_dir_last(self, dir_p):
        print self.sh.get_ue_log(dir_p)

if __name__=="__main__":
    x =  mon_sta()
    dp = "/home/jenkins/test/process_20161118_111317/"
    x.get_dir_last(dp)
