#-*-coding:utf8 -*-
from ShellCon import sh_control
import unittest

class sh_control_test(unittest.TestCase):
    def test_get_files_cmd(self):
        x = sh_control()
        res = x.get_files_cmd("/home/jenkins/test/process_20161118_111317")
        print res


if __name__=="__main__":
    unittest.main()

