#-*- coding:utf8 -*-
import subprocess
import re, time, sys
import thread, os
class sh_control():
    def __init__(self):
        pass
    
    def log(self, message):
        #print "*" * 20
        #print message
        pass
    
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
        com_list = ["mkdir %s/test" % spath, "mv %s/*.jpg %s/test" % (spath, spath), "mv %s/*.txt %s/test" % (spath, spath),"scp -r %s slim@192.168.32.167:%s" % (spath, dpath), "rm -rf %s/*" % spath]
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

    def get_files_cmd(self, path, file_format="log.txt", cmd_s=["tail -n 1 %s/%s", "head -n 1 %s/%s"]):
        res = []
        tail_cmd = cmd_s[0]
        head_cmd = cmd_s[1]
        for i in os.listdir(path):
            if re.findall(file_format, i):
                line_res = []
                head_out,res_err = self._com(head_cmd % (str(path), str(i)))
                assert None == res_err # res_err wc -l 出现问题请手动检查
                tail_out,res_err = self._com(tail_cmd % (str(path), str(i)))
                assert None == res_err # res_err wc -l 出现问题请手动检查
                #print "res_out %s; res_err %s" % (str(res_out), str(res_err))
                head_out = head_out.split(",")[0]
                tail_out = tail_out.split(",")[0]
                
                res.append([head_out, tail_out, str(i)])
        return res

    def get_dir_files_lines(self, path, file_format="log.txt"):
        res = self.get_files_wc(path, file_format)
        file_list = []
        line_list = []
        for i in res:
            file_list.append(i[1])
            line_list.append(int(i[0]))
            
        return file_list, line_list
    
    def save_range_log_s(self, ranges, fp):
        print "ranges %s; fp %s" % (str(ranges), fp)

    def save_range_log_f(self, ranges, fp, new_fp):
        print "open f ranges %s; fp %s" % (str(ranges), fp)
        sta_ms = ranges[0] if None != ranges[0] else 0
        end_ms = ranges[1] if None != ranges[1] else 2479000000000

        f = open(fp)
        com = f.readlines()
        f.close()
        new_com = []
        for i in com:
            point = i.split(",")[0]
            if int(sta_ms) <= int(point) <= int(end_ms):
                new_com.append(i)
            if int(end_ms) < int(point):
                break
        for j in new_com:
            com.remove(j)

        self.save_file("%s_bk" % fp, com)
        self.save_file(new_fp, new_com)
        return new_fp

    def save_file(self, fp, com):
        f = open(fp, "w")
        for i in com:
            f.write(i)
        f.close()

if __name__=="__main__":
    x = sh_control()
    #x.get_ue_log("/home/jenkins/test")
    #print x.get_files_wc("/home/jenkins/test")
    fl, ll = x.get_dir_files_lines("/home/jenkins/test/process_20161115_103635")
    print len(fl)
    print sum(ll)
