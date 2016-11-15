#-*-coding:utf8 -*-
from processt import processt
import unittest
class TestProcesst(unittest.TestCase):
    def test_get_diff_time(self):
        x = processt()
        res = x.get_diff_time(diff_file="regulate_time/list_app_update.log")
        print res

if __name__ == '__main__':
    unittest.main()

