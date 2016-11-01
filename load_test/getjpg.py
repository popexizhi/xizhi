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

    def get_jpg(self, x_list, y_list, filename):
        print "start get_jpg %s; x len %d; y len %d" % (str(time.time()), len(x_list), len(y_list))
        fig,ax = plt.subplots() #图像显示的行列数和第几个图像
        #plt.plot(x_list, y_list)
        #plt.xticks(x_list, x_list) #设置横坐标标记,(对应的坐标值,对应的坐标标签 )
        xticks = range(0, len(x_list)) 
        #xlabels = [x_list[index] for index in xticks]
        xlabels = x_list
        xticks.append(len(x_list))
        #xlabels.append(x_list)
        ax.set_xticks(xticks)
        print xticks
        print xlabels
        ax.set_xticklabels(xlabels, rotation=20) # rotation 为文字倾斜程度
        plt.plot(y_list)
        plt.grid(axis = 'both')
        plt.title(filename)
        plt.grid()
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
