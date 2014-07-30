#
"""
test for chamberlain.py
"""
import os
import subprocess
from chamberlain import chamberlain
import unittest
import thread
class test_chamberlain(unittest.TestCase):
	
	def setUp(self):
		"""start Demo Server """
		dserver="testD\\Servertcp.py"
		os.system("pwd")
		arg="python "+dserver
		thread.start_new_thread(subprocess.call,arg)
		#os.system("python "+dserver)
	
	def testcallpower(self):
		"""test message to sever """
		print "testcallpower"
		pass

	def testshowpower(self):
		"test server recve message"
		print "testshowpower"
		pass


if __name__=="__main__":
	unittest.main()
