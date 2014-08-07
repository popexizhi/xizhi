# -*- coding: utf-8 -*-

# chamberlain : Ϊardino's wifi �ṩ message
# 
import socket
import sys

###############################################
class chamberlain():
	def __init__(self):
		"""init chamberlain's def ip&buf """ 
		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5005
		self.BUFFER_SIZE = 1024
		self.data=""
		self.conST=0 #socket connect state ,1 <estas> ok

	def setnewadd(self,tcp,port):
		"""set other ip """
		self.TCP_IP=tcp
		self.TCP_PORT=port

	def callpower(self,message="open"):
		self.MESSAGE = message
		self._findpower()
		if(1 == self.conST): #if arduino connect is ok
			self._getdata()
			self._closepower()

	def _findpower(self):
		"""tcp link ardino and send message"""
		self.powercall=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#add socket except popexizhi 07/08/14
		try:
			self.powercall.connect((self.TCP_IP,self.TCP_PORT))
			self.powercall.send(self.MESSAGE)
			self.conST=1
		except:
			(ErrorType,ErrorValue,ErrorTB) =sys.exc_info()
			(errno,err_msg)=ErrorValue
			print "*************chamberlain.py*****************"
			print "Connect server failed:%s, errno=%d" % (err_msg,errno)
			print "ErrorValue:%s" % ErrorTB
	
	def _getdata(self):
		"""get ardino data """
		print "chamberlain-----------get ardino data"
		self.data=self.powercall.recv(self.BUFFER_SIZE)
	
	def _closepower(self):
		"""close tcp link """
		print "chamberlain-----------close tcp link"
		self.powercall.close()
		print "ok,close"

	def showpower(self):
		"""return SERVER_ERR is that <la> arduino isn't open  """
		if(1 == self.conST): #if arduino connect is ok
			return self.data
		else:
			return "SERVER_ERR"


#######################################################################
if __name__ == "__main__":
	testchamberlain=chamberlain()
	testchamberlain.callpower("open")
	print testchamberlain.showpower()
