# -*- encoding:utf8 -*-

import matplotlib #, pylab
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import pylab as pl
import numpy as np
from matplotlib.pyplot import plot,savefig  
import matplotlib.pyplot as plt
import re, time
class dtjpg():
    def __init__(self):
        self.size = 0

    def xa(self, data_list, filename):
        time_list = []
        a_list = []
        for i in data_list:
            time, a = i.split(";")
            time = re.split(r"[. ]",time)[1]
            time_list.append(time)
            a_list.append(a)
        
        #import pylab as pl
        date = pl.datestr2num( time_list )
        #value = a_list.astype(np.float)
        #print date
        print "&& "* 20
        print "x :len(data_list) is "+ str(len(data_list))
        print a_list
        print "Y :max(a_list)+1 is " + str(( float(max(a_list))+1)//1)
        #print "figsize : %f " % (len(data_list)*(max(a_list)+1))
        jpg_length = len(time_list)+1
        if (jpg_length > 100): 
            jpg_length = 100
        pl.figure(figsize=(jpg_length, 10), dpi=16)
        pl.xticks(date,time_list)
        pl.plot(date, a_list)
        pl.grid(axis='both')#显示辅助线
        pl.title(filename)
        savefig(filename+".jpg")
    
    def sub_plot(self, data_list, filename):
        time_list = []
        a_list = []
        self.size = self.size + 1
        for i in data_list:
            time, a = i.split(";")
            time_list.append(time)
            a_list.append(a)

        plt.subplot(2, 1, self.size)
        date = pl.datestr2num( time_list)
        plt.figure(figsize=(len(time_list)+1, float(max(a_list))+1), dpi=8)
        plt.xticks(date, time_list)
        plt.plot(date, a_list)
        plt.grid(axis = 'both')
        plt.title(filename)
        
        if( 2 == self.size ):
            savefig(filename+".jpg")

    def get_jpg(self, x_list, y_list, filename):
        print "start get_jpg %s; x len %d; y len %d" % (str(time.time()), len(x_list), len(y_list))
        plt.subplot(1, 1, 1) #图像显示的行列数和第几个图像
        #plt.figure(figsize =(len(x_list)+1, float(max(y_list))+1), dpi = 8)
        #plt.xticks(x_list, y_list) #设置横坐标标记
        #plt.yticks(y_list)
        #print "x_list %s" % str(x_list)
        #print "y_list %s" % str(y_list)
        plt.plot(x_list, y_list)
        plt.xticks(x_list, x_list) #设置横坐标标记,(对应的坐标值,对应的坐标标签 )
        plt.grid(axis = 'both')
        plt.title(filename)
        plt.show()
        savefig(filename+".jpg")
        print "end get_jpg %s" % str(time.time())


if __name__=="__main__":
    b=dtjpg()
    #b.xa()
    x = [1477969675, 1477969676, 1477969677]
    y = [18208, 66922, 10]
    #y = [500.43167838312831, 502.68845820507454, 425.30000000000001]
    b.get_jpg(x, y, "x")
