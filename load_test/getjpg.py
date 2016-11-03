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
        #plt.figure(figsize=((len(x_list)+20)*5, (len(y_list)+2)) )
        plt.figure(figsize=((10,2)), dpi=80, facecolor='w', edgecolor='k') 
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
        ax.set_xticklabels(xlabels, rotation=30) # rotation 为文字倾斜程度
        plt.plot(y_list)
        plt.grid(axis = 'both')
        plt.title(filename)
        plt.grid()
        plt.show()
        #savefig(filename+".jpg")
        savefig(filename+".jpg", dpi=800)
        print "end get_jpg %s" % str(time.time())
    
    def get_long_figure(self, x, y, filename):
        plt.figure(figsize=((10,2)), dpi=80, facecolor='w', edgecolor='k') 
        plt.xticks(x, rotation=30) #设置横坐标标记,(对应的坐标值,对应的坐标标签 )
        # 设置图的底边距
        plt.subplots_adjust(bottom = 0.50)

        plt.grid() #开启网格
        plt.plot(x, y)
        savefig("%s.jpg" % filename, dpi=800)
        print "end get_jpg %s" % str(time.time())
        

if __name__=="__main__":
    b=dtjpg()
    #b.xa()
    #x = [1477969675, 1477969676, 1477969677]
    #y = [18208, 66922, 10]
    x = [1477985187, 1477985188, 1477985189, 1477985190, 1477985191, 1477985192, 1477985193, 1477985194, 1477985195, 1477985196, 1477985197, 1477985198, 1477985199, 1477985200, 1477985201, 1477985202, 1477985203, 1477985204, 1477985205, 1477985206, 1477985207, 1477985208, 1477985209, 1477985210, 1477985211, 1477985212, 1477985213, 1477985214, 1477985215, 1477985216, 1477985217, 1477985218, 1477985219, 1477985220, 1477985221, 1477985222, 1477985223, 1477985224, 1477985225, 1477985226, 1477985227, 1477985228, 1477985229, 1477985230]
    y = [505.37409984626589, 498.97513895238325, 500.75437364420929, 500.5519185059423, 501.70225651279526, 500.23208970033738, 499.75936037019818, 501.83950922401817, 499.89960788614991, 500.80293978934128, 501.13018339034585, 500.69575715926419, 499.95580943052369, 500.24685794920038, 500.68474781231106, 498.72941583843374, 501.24634367355753, 499.90573412576651, 500.5009540444841, 500.97721783282321, 499.32745926200738, 501.49943709809759, 499.00490270380459, 499.92868814989572, 500.63059887092959, 501.34210105005417, 500.28007499268017, 501.41971329044821, 501.78780445314965, 500.32851804208411, 501.11850089512859, 500.96247977775579, 499.59342922616565, 499.81989247311827, 499.75902581295298, 500.82820677264118, 501.10592444946087, 500.09343891402716, 500.54247164356144, 500.15250854593961, 500.33057018708871, 500.07591684847796, 500.28904576410969, 499.06299851291067]
    #y = [500.43167838312831, 502.68845820507454, 425.30000000000001]
    #b.get_jpg(x, y, "x")
    b.get_long_figure(x, y, "a")
