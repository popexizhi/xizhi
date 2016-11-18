#-*-coding:utf8 -*-
from processt import processt
import unittest
class TestProcesst(unittest.TestCase):
    def test_get_diff_time(self):
        x = processt()
        res = x.get_diff_time(diff_file="regulate_time/use.log")
        assert res["42499"]
    def test_get_ueid_for_filename(self):
        x = processt()
        res = x.get_ueid_for_filename("ue.down.hostid.42499.pid.19962.log.txt_4")
        self.assertEqual(res, "42499")
        res = x.get_ueid_for_filename("ue.down.hostid.4.pid.19962.log.txt_4")
        self.assertEqual(res, "4")
    def test_dir2matrix(self):
        x = processt()
        #res,erl = x.dir2matrix("/home/jenkins/test/process_20161116_160840", "regulate_time/test_source")
        res,erl = x.dir2matrix("/home/jenkins/test/process_20161116_141910", "regulate_time/test_source")
        self.save_erl(erl)
        t = min_get_ue()
        print t.get_ue_app()
        ue_err = t.get_ue_min_log()
        t.get_err_app(ue_err)
        #y = min_get_ue()
        #y.get_ue_list(res, x)
    def save_erl(self, erl):
        f = open("processt_test.log","w")
        com = ""
        for i in erl:
            line = "%s,%s" % (i,erl[i])
            com = "%s%s\n" % (str(com),line)
        f.write(com)
        f.close()
    def test_minus(self):
        x = processt()
        res = x.minus(1479175362378,1479175362381,-4.36000013351)
        assert res<60000
    def test_check_data(self):
        x = processt()
        data = '1479348994350,content: PacketHeader{"packet_number":"2210","time_stamp":"1479349003987'
        res = x.check_data(data.split(","))
        self.assertEqual(res, -1)
        
        data = '1479348994350,content'
        res = x.check_data(data.split(","))
        self.assertEqual(res, -1)
        
        data = '1479348994350,2210,1479349003987'
        res = x.check_data(data.split(","))
        self.assertEqual(res, 0)
class min_get_ue():
    def get_ue_app(self, fp = "regulate_time/ue_app.log"):
        f = open(fp)
        com = f.readlines()
        f.close()
        ue_app = {}
        for i in com:
            line = i.split("\n")[0].split(": ['")
            #print line
            key = line[0]
            try:
                value = line[1].split("'")[0]
                ue_app[key] = value
            except IndexError:
                pass
        self.ue_app = ue_app
        self.show_ue_app()
    def show_ue_app(self):
        for key in self.ue_app:
            print "%s,%s" % (key, self.ue_app[key])

    def get_ue_min_log(self, fp = "processt_test.log"):
        f = open(fp)
        res = []
        for i in f.readlines():
            ueid = i.split(",")[0]
            min_err = i.split(",")[1].split("\n")[0]
            res.append([ueid, min_err])
        return res
    def get_ue_list(self, datas, pt):
        pt.statistics_use(datas) 
    
    def get_err_app(self, ue_err):
        assert self.ue_app
        res = []
        for i in ue_err:
            ueid = i[0]
            value = i[1]
            app_key = self.ue_app[ueid]
            res.append([app_key, float(value)])
        print res
        list_res = {}
        old = 0
        for j in res:
            if j[1] < old:
                list_res[j[0]] = j[1] 
                old = j[1]
        print "**********"
        print list_res
        return list_res

if __name__ == '__main__':
    unittest.main()
    t = min_get_ue()
    print t.get_ue_app()
    #ue_err = t.get_ue_min_log("use_time_second_14793466.log")
    ue_err = t.get_ue_min_log("use_time_second_147934467.log")
    t.get_err_app(ue_err)

