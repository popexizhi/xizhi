#-*-coding:utf8 -*-
from processt import processt
import unittest
class TestProcesst(unittest.TestCase):
    def test_get_diff_time(self):
        x = processt()
        res = x.get_diff_time(diff_file="regulate_time/list_app_update.log")
        print res
        print res["9113"]
    def test_get_ueid_for_filename(self):
        x = processt()
        res = x.get_ueid_for_filename("ue.down.hostid.42499.pid.19962.log.txt_4")
        self.assertEqual(res, "42499")
        res = x.get_ueid_for_filename("ue.down.hostid.4.pid.19962.log.txt_4")
        self.assertEqual(res, "4")
if __name__ == '__main__':
    unittest.main()

