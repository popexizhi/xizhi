import sqlite3
import re

class savesqlit():
	def __init__(self,dbname='cap_test.db',testid="1"):
		self.db=dbname
		self.testid=testid

	def create_datas(self,sql="CREATE TABLE load_cap (id text, packet_time text, src text, dst text )"):
		#create
		
		try:
			self.conn=sqlite3.connect(self.db)
			self.conn.execute(sql)
			self.conn.close()
		except:
			print "create table err"
			pass

	def add_datas(self,datas,dbname='load_cap', dbcol='id, packet_time, src, dst'):
		#insert {}
		#Opened database
		self.conn=sqlite3.connect(self.db)
		#create table

		#save dates
		try:
			for key in datas:
				usetime_errmassage=re.sub("\t","','",datas[key]) # #sub usetime and errmassage 
				print usetime_errmassage
				
				sql="insert into "+dbname+"("+dbcol+")"+" VALUES ( '"+key+"','"+usetime_errmassage+"','"+self.testid+"')"
				print sql
				self.conn.execute(sql)
				self.conn.commit()
		except BaseException,e:
			
			print "except %s" % e
		finally:
			self.conn.close()


	def inster_data(self,data, dbname='sencond_url_usetime', dbcol='url, usetime,errmassage,ID'):
		#insert 
		#Opened database
		self.conn=sqlite3.connect(self.db)
		#create table

		#save dates
		try:
			#print re.sub("\'","",data)
			sql="insert into "+dbname+"("+dbcol+")"+" VALUES ( "+re.sub("\'","",data)+")"
			print sql
			self.conn.execute(sql)
			self.conn.commit()

		except BaseException,e:
			
			print "except %s" % e
		finally:
			self.conn.close()


	
	def add_totle(self,datas):
		#create table
		create_sql='''CREATE TABLE load_cap (id text, packet_time text, src text, dst text)'''
		self.create_datas(create_sql)

		#save sql
		insert_datas=datas
		table_name="load_cap"
		table_col="id, packet_time, src, dst"
		self.inster_data(insert_datas, table_name, table_col)


if __name__=="__main__":
	a=savesqlit()
	a.create_datas()
	totle_data='"16777226_97_2016-03-11 17:33:19.499","2016-03-11 17:31:50.471245","6c:0b:84:41:a1:d2","e4:1f:13:6d:c2:d0"'
	a.add_totle(totle_data)		
