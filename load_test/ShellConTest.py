#-*-coding:utf8 -*-
from ShellCon import sh_control
import unittest

class sh_control_test(unittest.TestCase):
    def test_get_files_cmd(self):
        x = sh_control()
        #res = x.get_files_cmd("/home/jenkins/test/process_20161118_111317")
        res = x.get_files_cmd("test")
        print res
    
    def test_save_range_log_s(self):
        x = sh_control()
        #res = x.save_range_log_s((None,1), "test/ue_save_range.log")
        res = x.save_range_log_f((1479436452521,1479436458874), "test/ue_save_range.log", "test/in")
        res = x.save_range_log_f((1479436352034,1479436755035), "test/ue_save_range.log", "test/all")
        res = x.save_range_log_f((1479436352034,1479436353000), "test/ue_save_range.log", "test/sta_p")
        res = x.save_range_log_f((1479436744000,1479436755035), "test/ue_save_range.log", "test/end_p")

    def test_filter_file_to_new(self):
        x = sh_control()
        x._com("cp testdata/ue.down.hostid.15449.pid.119099.log.txt_4 testdata/1.log")
        x.filter_file_to_new(fp="1.log", old_dir="testdata", new_dir="testdata/filter")

if __name__=="__main__":
    unittest.main()

