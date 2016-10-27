# -*- encoding:utf8 -*-
from datetime import datetime
from scapy.all import *
import struct
import re
from cap_sqlit import savesqlit
import time
SRSPORT="12200"
class process_cap():
    def __init__(self, f = "a.cap"):
        self.pack = rdpcap(f)
        self.log_file = f + ".log"
        self.data_list = []
        
        self.err = 0
        #self.get_data_()
        self.ana_gdata_()

        self.get_data_(self.in_data_fgw)
        #self.get_data_(self.in_data_bgw)
        print "in_data*** " * 50
        print len(self.data_list)
        #self.get_data_(self.ou_data_fgw)
        self.get_data_(self.ou_data_bgw)
        print "all_data*** " * 50
        print len(self.data_list)
    
    def ana_gdata_(self):
        print "start ana_gdata_"+str(time.strftime("%T:%M:%S"))
        self.in_data_bgw = []
        self.in_data_fgw = []
        in_data_bgw = []
        in_data_fgw = []
        self.ou_data_bgw = []
        self.ou_data_fgw = []
        ou_data_bgw = []
        ou_data_fgw = []
        other_port = ""
        for i in self.pack:
            if "" == other_port:
                print "" == other_port
                other_port = str(i[TCP].sport)
                print i[TCP].sport
            try:
                #print i[TCP]
                if (str(i[TCP].sport)==SRSPORT ):
                    if str(i[TCP].dport) == other_port:
                        ou_data_bgw.append(i)
                    else:
                        ou_data_fgw.append(i)
                else:
                    if str(i[TCP].sport) == other_port:
                        in_data_bgw.append(i)
                    else:
                        in_data_fgw.append(i)
            except :
                print "ERR " * 50
                print i.command()
        #sort_list
        print "num_in_fgw.data is in " + str(len(in_data_fgw))
        print "num_in_bgw.data is in " + str(len(in_data_bgw))
        self.in_data_bgw = self.cap_list_sort(in_data_bgw)
        self.in_data_fgw = self.cap_list_sort(in_data_fgw)
        print "num_in_data_fgw is in " + str(len(self.in_data_fgw))
        print "num_in_data_bgw is in " + str(len(self.in_data_bgw))
        self.ou_data_fgw = self.cap_list_sort(ou_data_fgw) #[popexizhi]
        self.ou_data_bgw = self.cap_list_sort(ou_data_bgw) #[popexizhi]
        print "num out_data_fgw " + str(len(self.ou_data_fgw))
        print "num out_data_bgw " + str(len(self.ou_data_bgw))
        print "end ana_gdata_"+str(time.strftime("%H:%M:%S"))
    
    def cap_list_sort(self, list_):
        sort_list = []
        sort_list_ = []
        res_list = []
        seq_ack_syn = 0 #初始化ack_syn值
        j = 0
        for i in list_:
            if (18 == i[TCP].flags):
                seq_ack_syn = i[TCP].seq
            if (24 == i[TCP].flags):
                seq = i[TCP].seq - seq_ack_syn
                if seq < 0 :
                    seq_ack_syn = i[TCP].seq
                    sort_list_ = copy.deepcopy(sort_list)
                    sort_list = []
                    sort_list.append([i[TCP].seq-seq_ack_syn, j])
                else:
                    sort_list.append([seq , j])
            if (16 == i[TCP].flags):
                try:
                    #print "i[TCP].flags ==16L "* 5
                    #print i[Raw] #通过检测Raw是否存在判断TCP数据
                    t = i[Raw].load #通过检测Raw是否存在判断TCP数据
                    seq = i[TCP].seq - seq_ack_syn
                    if seq < 0 :
                        seq_ack_syn = i[TCP].seq
                        sort_list_ = copy.deepcopy(sort_list)
                        sort_list = []
                        sort_list.append([i[TCP].seq-seq_ack_syn, j])
                    else:
                        sort_list.append([seq , j])
                except : #IndexError:#忽略处理ack 的len = 0
                    #print i[Padding]
                    #print "IndexError"
                    pass
            j = j + 1
        sort_list.sort()
        if len(sort_list_)>0:
            sort_list_.sort()
            sort_list = sort_list_ + sort_list
        old_seq = ""
        for i in sort_list:
            if (i[0] == old_seq):#seq去重
                continue
            else:
                old_seq = i[0]
                old_seq_num = i[1]
            #print "i.seq is "+ str(i[0])
            res_list.append(copy.deepcopy(list_[i[1]]))
            #print i[0]
        return res_list

    def get_data_(self, pack_list):
        self.half_pack = ""
        print "start get_data_"+str(time.strftime("%T:%M:%S"))
        for i in pack_list:
            #判断包体是否包含load
            res = len(re.split(r"load=", i.command())) < 2 #使用load切割来判断是否存在此标志
            if res :
                continue
            load_data = i.load
            #是否连包,半包判断packet_splitx
            #print "i.command()"+"$$ " * 20
            #print datetime.fromtimestamp(i.time) 
            #print i.command()
            noc_packet_list = self.packet_splitx(load_data) 
            for res in noc_packet_list:
                message_type = res[1] 
                res = res[3] 
                #对L2数据处理
                if ( 6 == message_type):
                    #print repr(message_type)
                    #print repr(res)
                    packet_log_time = datetime.fromtimestamp(i.time)
                    packet_id = self.packet_send_(res)
                    #print "log tim is %s, packet_id is %s" % (str(packet_log_time), str(packet_id))
                    #print "** " * 20
                    #print "src: %s; des: %s" % (str(i.src), str(i.dst))
                    insert_data = '"'+str(packet_id)+'","'+str(packet_log_time)+'","'+str(i.src)+'","'+str(i.dst)+'"'
                    self.data_list.append(insert_data)
                #print len(load_data)
    def check_ping_(self, noc_packet_len):
        """ping pong包丢弃 """
        if (0 == noc_packet_len):
            if(len(self.half_pack) > 4 ):
                format_use = "!4s%ds" % (len(self.half_pack) - 4)
                header, other = struct.unpack(format_use, self.half_pack)
                self.half_pack = copy.deepcopy(other)
            if(4 == len(self.half_pack)):
                self.half_pack = ""
            else:
                print "ping pong err len(self.half_pack)"
                
            return 0
        return 1
                

    def packet_splitx(self, load_data):
        """粘包，半包处理 """
        noc_packet_list = []
        #加入load_data到self.half_pack
        #print "half_pack load_data" + "^^ " * 50
        #print repr(self.half_pack)
        if len(self.half_pack) >0:
            print "ERR" * 30
            self.err = self.err + 1
        if 10 == self.err :
            print "first is \x00 " * 50
            print load_data[xxx]
        if len(self.half_pack) == 0:
            self.err = 0
        
        self.half_pack = self.half_pack + copy.deepcopy(load_data)
        #print repr(load_data)
        #处理self.half_pack
        tcp_load_len = len(self.half_pack)
        #print "Itcp_load_len is %d" % tcp_load_len
        if (tcp_load_len < 4) :
            pass #包长不够缓存，等待完整包处理
        else:       
            if (4==tcp_load_len):
                format_use = "!cbH"
                version, message_type, noc_packet_len = struct.unpack(format_use, self.half_pack)
            else:
                format_use = "!cbH%ds" % (tcp_load_len - 4)
                version, message_type, noc_packet_len, o_res = struct.unpack(format_use, self.half_pack)
            #对包头的检查,未完成
            self.check_header_(version)
            #ping pong处理
            self.check_ping_(noc_packet_len)
            tcp_packet_len = len(self.half_pack)

            while (tcp_packet_len >= 4):
            #对包头的检查,未完成
                self.check_header_(version)
                if (0 == self.check_ping_(noc_packet_len)):
                    tcp_packet_len = len(self.half_pack)
                    if (tcp_packet_len >=4):
                        version, message_type, noc_packet_len = struct.unpack("!cbH", self.half_pack[0:4])
                        
                    continue
                else:
                    if((tcp_packet_len - 4) > noc_packet_len):
                        #包体 处理
                        format_use = "!4s%ds%ds" % (noc_packet_len, len(self.half_pack)-noc_packet_len-4)
                        #print "II" + str(format_use)
                        header, noc_packet, other = struct.unpack(format_use, self.half_pack)    
                        noc_packet_list.append([version, message_type, noc_packet_len, noc_packet])
                        self.half_pack = copy.deepcopy(other)#重置缓存
                        tcp_packet_len = len(self.half_pack)
                        #print "IItcp_load_len is %d" % tcp_packet_len
                        if (tcp_packet_len >= 4):
                            format_use = "!cbH"
                            version, message_type, noc_packet_len = struct.unpack(format_use, self.half_pack[0:4])
                            
                    if ((tcp_packet_len - 4) == noc_packet_len):
                        #包体处理，封装返回值
                        noc_packet  = copy.deepcopy(self.half_pack[4:-1])
                        noc_packet_list.append([version, message_type, noc_packet_len, noc_packet])
                        self.half_pack = "" #清空缓存
                        tcp_packet_len = 0
                    if ((tcp_packet_len - 4) < noc_packet_len):
                        #等待重新加载
                        break
        

        return noc_packet_list

    def check_header_(self, res):
        """检查包头 """
        #format_use = "!c%ds" % (len(res)-1)
        #version, other = struct.unpack(format_use, res)
        assert res == '\x00' #如果存在半包一定是从版本号开始的

    def packet_split(self, load_data):
        """粘包处理 """
        noc_packet_list = []
        #noc_packet = []
        format_use = "!cbH%ds" % (len(load_data) - 4)
        version, message_type, noc_packet_len, res =  struct.unpack(format_use, load_data)
        tcp_load_len  = len(res)
        
        while ((tcp_load_len > 4) and (tcp_load_len > noc_packet_len)): 
            format_use = "!%ds%ds" % (noc_packet_len, tcp_load_len-noc_packet_len)
            noc_packet, other_res = struct.unpack(format_use, res)
            noc_packet_list.append([version, message_type, noc_packet_len, noc_packet])
                
            format_use = "!cbH%ds" % (len(other_res) - 4)
            version, message_type, noc_packet_len, res =  struct.unpack(format_use, other_res)
            tcp_load_len  = len(res)

        if ((tcp_load_len > 4) and (tcp_load_len == noc_packet_len)):
            noc_packet_list.append([version, message_type, noc_packet_len, res])
        if (tcp_load_len < noc_packet_len): #这个应该是有半包吧？当前没有处理
            print "&& " * 50
            print "tcp_load_len is %d, noc_packet_len is %d, len(res) is %d" % (tcp_load_len, noc_packet_len, len(res))
            print repr(res)
        if (tcp_load_len <= 4):
            print "&& " * 100
            print repr(res)

        return noc_packet_list

    def packet_send_(self, packet_res):
        """packet_res 中发送内容 """
        #print "start packet_send_"+ str(time.strftime("%T:%M:%S"))
        len_packet_res = 4 #new id int #23 #包体中标识字符长度
        format_use = "!2ii%ds" % int(len(packet_res)-len_packet_res-8)
        #print "::\t\t" + format_use
        #print packet_res
        target_host_id , host_id, packet_send, other_res = struct.unpack(format_use, packet_res)
        #res = datetime.strptime(str(packet_send), '%Y-%m-%d %H:%M:%S.%f')
        #print res
        res = str(target_host_id)+"_"+str(host_id)+"_"+ str(packet_send)
        return res
    
    def save_file(self):
        print "start save_file"+ str(time.strftime("%T:%M:%S"))
        f = open(self.log_file, "w")
        for i in self.data_list:
            f.write(i+"\n")
        f.close()

    def save_db(self):
        s_db = savesqlit(dbname=self.log_file+".db")
        s_db.create_datas()
        for i in self.data_list:
            s_db.add_totle(i)
if __name__=="__main__":
    print (time.strftime("%T:%M:%S"))
    x = process_cap("d.cap")
    x.save_file()
    #x.save_db()
    print (time.strftime("%T:%M:%S"))
