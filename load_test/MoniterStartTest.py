#-*-coding:utf8 -*-
from MoniterStart import mon_sta
import unittest, re

class mon_sta_test(unittest.TestCase):
    def test_split_log(self):
        x = mon_sta()
        sta_ms = 2
        end_ms = 5
        self.assertEqual(0, x.split_log([1,2,"0_1_2"], sta_ms, end_ms))
        self.assertEqual(0, x.split_log([0,1,"0_0_1"], sta_ms, end_ms))
        self.assertEqual(0, x.split_log([1,2,"0_2_2"], sta_ms, end_ms))
        self.assertEqual(4, x.split_log([6,8,"4_6_8"], sta_ms, end_ms))
        self.assertEqual(4, x.split_log([5,6,"4_5_6"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([2,5,"2_2_5"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([3,4,"2_3_4"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([2,3,"2_2_3"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([4,5,"2_4_5"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([5,5,"2_5_5"], sta_ms, end_ms))
        self.assertEqual(1, x.split_log([1,3,"1_1_3"], sta_ms, end_ms))
        self.assertEqual(1, x.split_log([1,5,"1_1_5"], sta_ms, end_ms))
        self.assertEqual(3, x.split_log([4,6,"3_4_6"], sta_ms, end_ms))
        self.assertEqual(3, x.split_log([2,6,"3_2_6"], sta_ms, end_ms))
        self.assertEqual(5, x.split_log([0,6,"5_0_6"], sta_ms, end_ms))
    def test_process_dir(self):
        
        x =  mon_sta()
        dp = "test"
        sta_time = 1479436452044
        end_time = 1479436745045
        print "*****************"
        self.assertEqual(2, x.split_log([sta_time, end_time, "log_%d_%d" % (sta_time, end_time)], sta_time, end_time))
        res = x.process_dir(dp, sta_time, end_time)
        for key in res:
            pre_res = int(re.findall("\d$", key)[0])
            print pre_res
            self.assertEqual(res[key], pre_res)
        print "*****************"

if __name__=="__main__":
    unittest.main()

