# -*- coding: utf-8 -*-

# chamberlain : Ϊardino's wifi �ṩ message
# 
import socket

###############################################
class chamberlain():
	def __init__(self):
		"""init chamberlain's def ip&buf """ 
		self.TCP_IP = '127.0.0.1'
		self.TCP_PORT = 5005
		self.BUFFER_SIZE = 1024
		self.data=""

	def setnewadd(self,tcp,port):
		"""set other ip """
		self.TCP_IP=tcp
		self.TCP_PORT=port

	def callpower(self,message="open"):
		self.MESSAGE = message
		self._findpower()
		self._getdata()
		self._closepower()

	def _findpower(self):
		"""tcp link ardino and send message"""
		self.powercall=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.powercall.connect((self.TCP_IP,self.TCP_PORT))
		self.powercall.send(self.MESSAGE)
	
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
		return self.data


#######################################################################
if __name__ == "__main__":
	testchamberlain=chamberlain()
	testchamberlain.callpower("open")
	print testchamberlain.showpower()
