#-*-coding:utf8 -*-
from MoniterStart import mon_sta
import unittest

class mon_sta_test(unittest.TestCase):
    def test_split_log(self):
        x = mon_sta()
        sta_ms = 2
        end_ms = 5
        self.assertEqual(0, x.split_log([1,2,"0_1_2"], sta_ms, end_ms))
        self.assertEqual(0, x.split_log([0,1,"0_0_1"], sta_ms, end_ms))
        self.assertEqual(0, x.split_log([1,2,"0_2_2"], sta_ms, end_ms))
        self.assertEqual(4, x.split_log([6,8,"4_6_8"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([2,5,"2_2_5"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([3,4,"2_3_4"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([2,3,"2_2_3"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([4,5,"2_4_5"], sta_ms, end_ms))
        self.assertEqual(2, x.split_log([5,5,"2_5_5"], sta_ms, end_ms))
        self.assertEqual(1, x.split_log([1,2,"1_1_2"], sta_ms, end_ms))
        self.assertEqual(1, x.split_log([1,3,"1_1_3"], sta_ms, end_ms))
        self.assertEqual(3, x.split_log([5,6,"3_5_6"], sta_ms, end_ms))
        self.assertEqual(3, x.split_log([4,6,"3_4_6"], sta_ms, end_ms))
        self.assertEqual(5, x.split_log([0,6,"5_0_6"], sta_ms, end_ms))


if __name__=="__main__":
    unittest.main()

