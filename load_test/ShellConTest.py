#-*-coding:utf8 -*-
from ShellCon import sh_control
import unittest, time

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

    def test_get_dir_files(self):
        x = sh_control()
        print x._com("ls -all /home/jenkins/test2|wc -l")
        print time.time()
        x.get_dir_files("/home/jenkins/test2","testdata/filter")
        print time.time()
        print x._com("ls -all testdata/filter|wc -l")

    def test_com(self):
        x = sh_control()
        print x._com("sh log_data.sh ue.down.hostid.32245.pid.184468.log.txt_4 testdata test")

    def test_zero_file_process(self):
        x = sh_control()
        print x.zero_file_process(backup_dir="/data/load_use/process", new_dir="/data/load_use/backup")

    def test_is_new_file(self):
        x = sh_control()
        fp = "testdata/x"
        x._com("echo 'test'>%s" % fp)
        self.assertEqual(x.is_new_file(fp), False)
        x._com("echo 'test'>%s" % fp)
        time.sleep(1)
        self.assertEqual(x.is_new_file(fp, 1), True)
if __name__=="__main__":
    unittest.main()

