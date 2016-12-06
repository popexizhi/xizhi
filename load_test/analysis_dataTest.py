#-*- coding:utf8 -*-
from analysis_data import analy_d 
import unittest
class analysis_data_test(unittest.TestCase):
    def test_get_ana_rtt(self):
        x = analy_d()
        x.get_ana_rtt("/home/jenkins/test/process_20161206_1481008855893to1481012455893/", "testdata")


if __name__=="__main__":
    unittest.main()
