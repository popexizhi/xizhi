#-*- coding:utf8 -*-
import subprocess
import re, time, sys
import thread, os
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
        return stdout, stderr
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

    def back_test(self, spath="test", dpath="/data/provision_test/load_test"):
        com_list = ["mkdir %s/test" % spath, "mv %s/*.jpg %s/test" % (spath, spath),"scp -r %s slim@192.168.1.25:%s" % (spath, dpath), "rm -rf %s/*" % spath]
        self._list_com(com_list)

    def get_files_wc(self, path, file_format="log.txt"):
        res = []
        cmd_str = "cat %s/%s|wc -l"
        for i in os.listdir(path):
            if re.findall(file_format, i):
                res_out,res_err = self._com(cmd_str % (str(path), str(i)))
                #print "res_out %s; res_err %s" % (str(res_out), str(res_err))
                assert None == res_err # res_err wc -l 出现问题请手动检查
                
                res.append([int(res_out.split("\n")[0]), str(i)])
        return res
if __name__=="__main__":
    x = sh_control()
    #x.get_ue_log("/home/jenkins/test")
    print x.get_files_wc("/home/jenkins/test")
