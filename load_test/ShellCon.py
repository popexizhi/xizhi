#-*- coding:utf8 -*-
import subprocess
import re, time, sys
import thread
class sh_control():
    def __init__(self):
        pass
    
    def log(self, message):
        print "*" * 20
        print message
    
    def _com(self, cmd):
        getchar = "a"
        self.log(cmd)
        self.app_log_b = subprocess.Popen([cmd], shell=True,  stdout = subprocess.PIPE, stdin = subprocess.PIPE)
        # Send the data and get the output
        stdout, stderr = self.app_log_b.communicate(getchar)
    def _list_com(self, com_list):
         for i in com_list:
              self._com(i)

    def get_ue_log(self, path):
        res_log = "ue_log.log"
        com_list = ["ls -all %s|grep 'log.txt_'|awk '{print $9}'>%s" % (path, res_log)] 
        self._list_com(com_list)
        return res_log

    def save_ue_log(self, path):
        ue_log = "ue_log.log"
        ue_dir = "uelog_d"
        com_list = ["cat %s/*.log.txt*>%s" % (str(path), str(ue_log)), "mv %s %s/" % (str(ue_log), str(ue_dir))]
        self._list_com(com_list)
        return ue_dir, ue_log

if __name__=="__main__":
    x = sh_control()
    x.get_ue_log("/home/jenkins/test")
