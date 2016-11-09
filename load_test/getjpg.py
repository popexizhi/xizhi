# -*- encoding:utf8 -*-

import matplotlib #, pylab
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import pylab as pl
import numpy as np
from matplotlib.pyplot import plot,savefig  
import matplotlib.pyplot as plt
import re, time
from datetime import datetime, timedelta
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

    def test_straight_line(self, x, y, z, filename="line", y_max=[]):
        plt.figure(figsize=((10,2)), dpi=80, facecolor='w', edgecolor='k') 
        plt.xlabel("Time(s)")
        x_lab=[]
        #只对x轴为时间处理
        if len(x) > 0 and int(x[0]) > 1478147000:
            x_lab = self.get_xlabel(plt, x, dev=20) # dev为间隔设置
            print x_lab
        else:
            x_lab = x
        plt.xticks(x, x_lab, rotation=30) #设置横坐标标记,(对应的坐标值,对应的坐标标签 )
        #y 轴处理
        if len(y_max) > 0:
            self.ylim(plt, y_max)
        # 设置图的底边距
        plt.subplots_adjust(bottom = 0.50)

        plt.grid() #开启网格
        print len(x)
        print len(y)
        plt.plot(x, y, "g",linewidth=2)
        if len(z) == 0:
            pass
        else:
            plt.plot(x, z, "r-",linewidth=2)
         
        savefig("%s.jpg" % filename, dpi=800)
        #assert 1 == 0
        print "end get_jpg %s" % str(time.time())
        return plt    

    def get_xlabel(self, plt, x, dev=60):
        x_lab = []
        index = 0
        print x
        for i in x:
            if int(i) < 1478570000000:
                i = int(i) * 1000 #秒钟的以毫秒处理
            if 0 == int(int(i)/1000)%dev :
                res = str(self.datetime_from_millis(int(i)))
                lab = res.split(" ")[0]
                res = res.split(" ")[1].split("000")[0]
                print "res %s" % str(res)
                plt.xlabel("Time(s) %s" % lab)
            else:
                res = " "
            x_lab.append(res)
            index = index + 1
        
        return x_lab
    
    def ylim(self, plt , y):
        plt.ylim(0, max(y)+2)
    
    def show(self, plt):
        plt.show()

    from datetime import datetime, timedelta 
    def datetime_from_millis(self, millis, epoch=datetime(1970, 1, 1)):
        """Return UTC time that corresponds to milliseconds since Epoch."""
        res =  epoch + timedelta(milliseconds=millis)
        return res


    def get_cook_jpg(self, labes_u, sizes_u, file_p): 
        #调节图形大小，宽，高
        plt.figure(figsize=(6,9))
        #定义饼状图的标签，标签是列表
        #labels = [u'x',u'y',u'z']
        labels = labes_u
        #每个标签占多大，会自动去算百分比
        #sizes = [60,30,10]
        sizes = sizes_u
        colors = ['red','yellowgreen','lightskyblue']
        #将某部分爆炸出来， 使用括号，将第一块分割出来，数值的大小是分割出来的与其他两块的间隙
        explode = (0.05,0,0)
        
        patches,l_text,p_text = plt.pie(sizes,explode=explode,labels=labels,colors=colors,
        labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
        startangle = 90,pctdistance = 0.6)
        
        #labeldistance，文本的位置离远点有多远，1.1指1.1倍半径的位置
        #autopct，圆里面的文本格式，%3.1f%%表示小数有三位，整数有一位的浮点数
        #shadow，饼是否有阴影
        #startangle，起始角度，0，表示从0开始逆时针转，为第一块。一般选择从90度开始比较好看
        #pctdistance，百分比的text离圆心的距离
        #patches, l_texts, p_texts，为了得到饼图的返回值，p_texts饼图内部文本的，l_texts饼图外label的文本
        
        #改变文本的大小
        #方法是把每一个text遍历。调用set_size方法设置它的属性
        for t in l_text:
            t.set_size=(30)
        for t in p_text:
            t.set_size=(20)
        # 设置x，y轴刻度一致，这样饼图才能是圆的
        plt.axis('equal')
        plt.legend()
        plt.show()
        #filename = "test_cook"
        filename = "%s.jpg" % file_p
        savefig(filename, dpi=80)
        return filename

if __name__=="__main__":
    b=dtjpg()
    #b.xa()
    #x = [1477969675, 1477969676, 1477969677]
    #y = [18208, 66922, 10]
    #x = [1477985187, 1477985188, 1477985189, 1477985190, 1477985191, 1477985192, 1477985193, 1477985194, 1477985195, 1477985196, 1477985197, 1477985198, 1477985199, 1477985200, 1477985201, 1477985202, 1477985203, 1477985204, 1477985205, 1477985206, 1477985207, 1477985208, 1477985209, 1477985210, 1477985211, 1477985212, 1477985213, 1477985214, 1477985215, 1477985216, 1477985217, 1477985218, 1477985219, 1477985220, 1477985221, 1477985222, 1477985223, 1477985224, 1477985225, 1477985226, 1477985227, 1477985228, 1477985229, 1477985230]
    x = [1478147515525,1478147515606,1478147516371,1478147516371,1478147516371,1478147516371,1478147516372,1478147516372,1478147516624,1478147517050,1478147517050,1478147517050,1478147517166,1478147517232,1478147517351,1478147517504,1478147521765,1478147521841,1478147521931,1478147522060,1478147522385,1478147604203,1478147604556,1478147604604,1478147604722,1478147604803,1478147604935,1478147605005,1478147605104,1478147605205,1478147605304,1478147605403,1478147605882,1478147606007,1478147606218,1478147606303,1478147606405,1478147606506,1478147610814,1478147610903,1478147611003,1478147611119,1478147611208,1478147515363]
    y = [505.37409984626589, 498.97513895238325, 500.75437364420929, 500.5519185059423, 501.70225651279526, 500.23208970033738, 499.75936037019818, 501.83950922401817, 499.89960788614991, 500.80293978934128, 501.13018339034585, 500.69575715926419, 499.95580943052369, 500.24685794920038, 500.68474781231106, 498.72941583843374, 501.24634367355753, 499.90573412576651, 500.5009540444841, 500.97721783282321, 499.32745926200738, 501.49943709809759, 499.00490270380459, 499.92868814989572, 500.63059887092959, 501.34210105005417, 500.28007499268017, 501.41971329044821, 501.78780445314965, 500.32851804208411, 501.11850089512859, 500.96247977775579, 499.59342922616565, 499.81989247311827, 499.75902581295298, 500.82820677264118, 501.10592444946087, 500.09343891402716, 500.54247164356144, 500.15250854593961, 500.33057018708871, 500.07591684847796, 500.28904576410969, 499.06299851291067]
    #y = [500.43167838312831, 502.68845820507454, 425.30000000000001]
    #b.get_jpg(x, y, "x")
    #b.get_long_figure(x, y, "a")   
    b.test_straight_line(x,y,[],"test/x_")
    x = [0,1,2,3,4,5,6,7,8,9]
    b.test_straight_line(x,[5,0,5,0,50,0,5,0,5,0],[4,1,4,1,4,1,4,1,4,1],"test/tw")
    b.test_straight_line(x,[5,0,5,0,50,0,5,0,5,0],[4,1,4,1,4,1,4,1,4,1],"test/tw", y_max=y)
    #b.get_cook_jpg()
