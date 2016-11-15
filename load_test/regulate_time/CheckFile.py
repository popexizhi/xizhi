#-*-coding:utf8-*-
import os,re
class CheckFile():
    def __init__(self, path):
        self.path = path

    def get_file_r(self, reg_str=u"\d\d*(?=.db)", reg_f_str="\d\d*(?=/)"):
        rootdir = self.path
        list_dirs = os.walk(rootdir)
        res_dir = {}
        for root, dirs, files in list_dirs:
            #for d in dirs: 
            #    dir_p = os.path.join(root, d)     
            #    print "dir_p %s" % dir_p
            dir_p = root
            for f in files:
                print "\tf %s" % f
                reg_res = re.findall(reg_str, f)
                if len(reg_res) > 0:
                    print reg_res
                    reg_str_key = reg_res[0]
                    dir_p_value = re.findall(reg_f_str, dir_p)
                    res_dir[reg_str_key] = dir_p_value
        self.show_res_dir(res_dir)
        return res_dir

    def show_res_dir(self, res_dir, fname="ue_time.log"):
        res = ""
        for key in res_dir:
            res=res + "%s: %s\n" % (str(key), str(res_dir[key]))
        f = open(fname,"w")
        f.write(res)
        f.close()
        return res


    def test_walk(self, path):
        index = 0
        for root, dirs, files in os.walk(path):
            print "root %s" % str(root)
            print "dirs %s" % str(dirs)
            print "files %s" % str(files)
            print "～" *5 +str(len(files))

    def get_app_update(self, fp="list_app_update.log"):
        res = {}
        f = open(fp)
        com = f.readlines()
        f.close()
        
        for i in com:
            key = i.split(",")[0]
            value = i.split(",")[1].split("\n")[0]
            res[key] = value
        return res

    def get_ue_update(self, ue_fp):
        ue_app_dir = self.get_file_r(u"\d\d*(?=.db)", reg_f_str="\d\d*(?=/)")
        app_update_dir = self.get_app_update()
        res = {}
        for key in ue_app_dir:
            if len(ue_app_dir[key])>0:
                res[key] = app_update_dir[ue_app_dir[key][0]]
        self.show_res_dir(res, ue_fp)
if __name__=="__main__":
    #a = CheckFile("/home/slim/test/integration_test/test_frame_demo/agent/provision_code/dbback")
    a = CheckFile(".")
    #a.get_file_r(u"\d\d*(?=.db)", reg_f_str="\d\d*(?=/)") #查询db名称中的数字, reg_f_str为appserver的host_id
    #a.test_walk(".")
    a.get_ue_update("use.log")
