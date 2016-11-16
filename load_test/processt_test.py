#-*-coding:utf8 -*-
from processt import processt
import unittest
class TestProcesst(unittest.TestCase):
    def test_get_diff_time(self):
        x = processt()
        res = x.get_diff_time(diff_file="regulate_time/use.log")
        assert res["42499"]
    def test_get_ueid_for_filename(self):
        x = processt()
        res = x.get_ueid_for_filename("ue.down.hostid.42499.pid.19962.log.txt_4")
        self.assertEqual(res, "42499")
        res = x.get_ueid_for_filename("ue.down.hostid.4.pid.19962.log.txt_4")
        self.assertEqual(res, "4")
    def test_dir2matrix(self):
        x = processt()
        res = x.dir2matrix("/home/jenkins/test/process_20161115_103635")

    def test_minus(self):
        x = processt()
        res = x.minus(1479175362378,1479175362381,-4.36000013351)
        assert res<60000

if __name__ == '__main__':
    unittest.main()

