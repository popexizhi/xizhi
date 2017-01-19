#-*- coding:utf8 -*-
import subprocess
import re, time, sys
import thread, os
from Map import load_test_cfg
class sh_control():
    def __init__(self):
        pass
    
    def log(self, message):
        #print "*" * 20
        print "[ShellCon] %s" % str(message)
        pass
    
    def _com(self, cmd):
        #getchar = "a"
        getchar = ""
        #self.log(cmd)
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

    def tar_save(self, dir_ue_log, ng_dir=load_test_cfg["ng_process_tar"]):
        dir_ue_log = re.sub(u"/$","", dir_ue_log)
        self.log(dir_ue_log)
        com_list = ["tar -cvzf %s.tar.gz %s --remove-files" % (dir_ue_log, dir_ue_log), "scp %s.tar.gz slim@192.168.1.216:%s" % (dir_ue_log, ng_dir), "rm -rf %s.tar.gz" % dir_ue_log ]
        return self._list_com(com_list)


    def back_test(self, spath="test", dpath="/data/provision_test/load_test"):
        com_list = ["mkdir %s/test" % spath, "mv %s/*.jpg %s/test" % (spath, spath), "mv %s/*.txt %s/test" % (spath, spath),"scp -r %s slim@192.168.1.216:%s" % (spath, dpath), "rm -rf %s/*" % spath, "mkdir %s/test" % spath, "mkdir %s/test/rtt_data" % spath, "mkdir %s/test/test" % spath]
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

        self.save_file(new_fp, new_com)
        self.save_file("%s_bk" % fp, com)
        self._com("mv %s_bk %s" % (fp, fp))
        #self.save_file("%s" % fp, com)
        return new_fp

    def save_file(self, fp, com):
        try:
            f = open(fp, "w")
        except:
            str_ = "chmod 666 %s" % fp
            self._com(str_)
            f = open(fp, "w")
        for i in com:
            f.write(i)
        f.close()

    def filter_file_to_new(self, fp, old_dir, new_dir, backup_dir, is_zero_process=1):
        if False == self.is_new_file("%s/%s" % (old_dir, fp)):
            return None 
        if None == backup_dir or 0 == is_zero_process:
            pass
        else:
            self._com("mv %s/%s %s" % (old_dir, fp, backup_dir))
        #time.sleep(1)    
        str_com = """sh log_data.sh %s %s %s""" % (fp, backup_dir, new_dir)
        self.log("str_com (%s)" % str(str_com))
        res = self._com(str_com)
        return res
    
    def is_new_file(self, fp, wait_time=30):
        res = False
        if wait_time <= int(time.time() - os.stat(fp).st_mtime) :
            return True
        return res
    
    def filter_file_for_rtt(self, fp, backup_dir, new_dir):
        str_com = """sh rtt_data.sh %s %s %s""" % (fp, backup_dir, new_dir)
        self.log("str_com (%s)" % str(str_com))
        res = self._com(str_com)
        return res

    def rtt_save_time(self, rtt_dir, rtt_process, statime, endtime):
        #rtt_save.sh
        rf = "%sto%s.rttd" % (str(statime), str(endtime))
        str_com = """sh rtt_save.sh %s %s %s""" % (rtt_dir , rf , rtt_process)
        self.log("str_com (%s)" % str(str_com))
        res = self._com(str_com)
        #process data range [statime, endtime]
        self.split_range_file("%s/%s" % (rtt_process, rf), statime, endtime, rtt_dir)
        
        new_dir_rtt = "%s/%s_%s" % (rtt_dir, str(statime), str(endtime))
        new_dir = """mkdir %s""" % new_dir_rtt
        mv_file = """mv %s/*_rtt %s""" % (rtt_dir, new_dir_rtt)
        backup_rtt_file = "sh rtt_backup.sh %s %s" % (rtt_dir, new_dir_rtt)
        self._list_com([backup_rtt_file])

        return res
    def split_range_file(self, rtt_dir, sta, end, old_dir):
        """ save [sta, end] in rtt_dir; other in old_dir"""
        print "start:split_range_file"
        f = open(rtt_dir)
        com = f.readlines()
        f.close()
        other=""
        range_in = ""
        for line in com:
            if 2 == len(line.split(",")): #数据结构验证
                i = line.split(",")[0]
            else:
                continue
            if int(sta)<= int(i) <= int(end):
                range_in = "%s%s" % (str(range_in), str(line))
            else:
                other = "%s%s" % (str(other), str(line))
        self.save_file(rtt_dir, range_in)
        self.save_file("%s/other_rtt" % old_dir, other)


    def zero_file_process(self, backup_dir, new_dir):
        #get zero line file
        res = self.get_dir_files_lines(backup_dir,"log.txt")        
        #second process files
        line_list = res[1]
        file_list = res[0]
        index = 0
        res_zero_file = []
        for i in line_list:
            self.log("index is %s" % str(index))
            fp = str(file_list[index])
            if 0 == int(i) and re.findall("log.txt",fp):
               res_zero_file.append(fp)
               #old_dir, new_dir, backup_dir
               str_com = """sh log_data.sh %s %s %s""" % (fp, new_dir, backup_dir)
               self.log(fp)
               self.log(str_com)
               res = self._com(str_com)
            index = index + 1
        return res_zero_file

    def get_dir_files(self, old_dir, new_dir, backup_dir, file_format=".log.txt"):
        
        for i in os.listdir(old_dir):
            if re.findall(file_format, i):
                line_res = []
                res = self.filter_file_to_new(i, old_dir, new_dir, backup_dir)
                if None != res:
                    rtt_res = self.filter_file_for_rtt(i, backup_dir, load_test_cfg["processRtt_dir"])
                    #self.log("file: %s;\n res: %s" % (i,str(rtt_res)))
        #self.zero_file_process(backup_dir, new_dir)
if __name__=="__main__":
    x = sh_control()
    #x.get_ue_log("/home/jenkins/test")
    #print x.get_files_wc("/home/jenkins/test")
    #fl, ll = x.get_dir_files_lines("/home/jenkins/test/process_20161115_103635")
    #print len(fl)
    #print sum(ll)
    while 1:
        print x._com("sh test_lo.sh")
        time.sleep(10)
