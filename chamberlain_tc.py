#
"""
test for chamberlain.py
"""
import os
import subprocess
from chamberlain import chamberlain
import unittest
import threading
class Dserver(threading.Thread):
	def __init__(self,num,path):
		threading.Thread.__init__(self)
		self.thread_cont=num
		self.path=path

	def run(self): 
		#Overwrite run() method
		print "********************Demo server"
		os.system("pwd")
		os.system("python "+self.path)
		self.thread_cont=self.thread_cont-1
	 
	def stop(self):
		print "********************over Dserver"
		



class test_chamberlain(unittest.TestCase):


	
	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def testcallpower(self):
		"""test message to sever """
		print "testcallpower"
		_testopen=chamberlain()
		_testopen.callpower('o')
		res=_testopen.showpower()
		print res
		

	def testshowpower(self):
		"test server recve message"
		print "testshowpower"
		#_testopen=chamberlain()
		#_testopen.callpower('c')
		#print _testopen.showpower()


if __name__=="__main__":
	"""start Demo Server """
	thread = Dserver(1,"testD\\Servertcp.py")
	thread.start()
	
	unittest.main()
