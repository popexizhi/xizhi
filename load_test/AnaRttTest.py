#-*-coding:utf8-*-
from ana_rttx import ana_rtt
import unittest

class ana_rttTest(unittest.TestCase):
    def test_range_time(self):
        x = ana_rtt()
        tk = {1:"", 2:"", 3:"", 4:"", 5:""}
        self.assertEqual(x.range_time(tk, [1,None]),tk)
        self.assertEqual(x.range_time(tk, [None,5]),tk)
        self.assertEqual(x.range_time(tk, [2,4]),{2:"",3:"",4:""})



if __name__=="__main__":
    unittest.main()
