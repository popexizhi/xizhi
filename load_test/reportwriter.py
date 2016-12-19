#-*-coding:utf8-*-
#!/usr/bin/env python
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


class Report(object):
    def __init__(self, results_dir):
        self.results_dir = results_dir
        self.fn = results_dir + 'results.html'
        self.write_head_html()


    def write_line(self, line):
        with open(self.fn, 'a') as f:
            f.write('%s\n' % line)


    def write_head_html(self):
        with open(self.fn, 'w') as f:
            f.write("""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <meta charset="utf-8" />
    <title>Multi-Mechanize - Results</title>
    <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
    <meta http-equiv="Content-Language" content="en" />
    <style type="text/css">
        body {
            background-color: #FFFFFF;
            color: #000000;
            font-family: Verdana, sans-serif;
            font-size: 11px;
            padding: 5px;
        }
        h1 {
            font-size: 16px;
            background: #FF9933;
            margin-bottom: 0;
            padding-left: 5px;
            padding-top: 2px;
        }
        h2 {
            font-size: 13px;
            background: #C0C0C0;
            padding-left: 5px;
            margin-top: 2em;
            margin-bottom: .75em;
        }
        h3 {
            font-size: 12px;
            background: #EEEEEE;
            padding-left: 5px;
            margin-bottom: 0.5em;
        }
        h4 {
            font-size: 11px;
            padding-left: 20px;
            margin-bottom: 0;
        }
        p {
            margin: 0;
            padding: 0;
        }
        td, th {
            border: 1px solid #dddddd;
            padding: 8px;
        }
        tr:nth-child(even) {
            background-color: #dddddd;
        }
        div.summary {
            padding-left: 20px;
        }
    </style>
    <script type="text/javascript"
       src="rtt/dygraph-combined-dev.js"></script>

</head>
<body>
<h1>Performance Results Report</h1>
""")

    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write("""\
</body>
</html>
""")
    def set_summary(self, dist_list):
        self.write_line('<h2>Summary</h2>')
        self.write_line('<div class="summary">')
        for i in dist_list:
            con = "<b>%s: %s</b><br />\n" % (str(i), str(dist_list[i])) 
            self.write_line(con)
        self.write_line("</div>")
    
    def set_h3_sum(self, title_h3, jpg_file):
        self.write_line('<h3>%s</h3>' % str(title_h3))
        self.write_line('<img src="%s" width="50%%" height="100%%"></img>' % jpg_file)

    def set_h3_sum_list(self, title_h3, jpg_file_list):
        self.write_line('<h3>%s</h3>' % str(title_h3))
        str_j = ""
        print jpg_file_list
        if type(-1) == type(jpg_file_list) :
            str_j = "null"
        else:
            for jpg in jpg_file_list:
                str_j = str_j + '<img src="%s.jpg" width="100%%" height="100%%"></img>\n' % str(jpg)

        print str_j
        self.write_line(str_j)
    def set_dygraph_h3(self, title_h3, dl, dy_name, dy_csv, dy_dir):
        html_str ="""\
<h3>%s</h3>
<p>%s</p>
<div id="%s"style="width:1500px;height:300px;"></div>
<script type="text/javascript">
    g4 = new Dygraph(
    document.getElementById("%s"),
        "%s/%s",//pathtoCSVfile
        {
            rollPeriod:1,
            showRoller:true,
            avoidMinZero:true,//y轴的最小值不为0，相当于y=0那条线上升了
            title:"%s",
            titleHeight:50,//标题高度
            axisLabelWidth:100,//XY轴的标题的宽度
            maxNumberWidth:9,//整数位数超过这个值就转为科学计数法显示1e6
        }//options
    );
</script> """ % (title_h3, str(dl), dy_name, dy_name, dy_dir, dy_csv, dy_name)
        print html_str
        self.write_line(html_str)
    
    def rtt_set(self, rtt_dl, rtt_name, rtt_csv, rtt_dir):
        res = rtt_dl
        print str(res)
        if 0 == len(res):
            res = [0,0,0,0,0]
        dl = {"Max(microsecond)":res[0], "Min(microsecond)":res[1], "avg": res[3], "stdev": res[4]} 
        self.set_dygraph_h3("rtt", dl, rtt_name, rtt_csv, rtt_dir)


    def set_cooke_list(self, list_cook_file, jpg_file, title_name = ""):
        size =  len(list_cook_file)
        # jpg
        cook_jpg = """
               <h3>ue log statistics %s</h3>
                <td>
                <img src="%s" width="100%%" height="100%%"></img>
                    </td>
        """ % (str(title_name), str(jpg_file))
        use_str = ""
        data_file = self.save_files(list_cook_file, jpg_file)
        for i in list_cook_file:
            list_cook_head_ = "<h4>%s</h4>" % str(i) #i : 0 package
            cook_list = ""
            index = 0
            for j in list_cook_file[i]:
                cook_list = cook_list + "\n%s<br>" % str(j) 
                index = index + 1
                if index > 10 : #
                    cook_list = cook_list + '<a href="%s" title="">file_list..</a>' % data_file
                    break
            use_str = use_str + "<td>\n\t%s\n\t%s\n</td>" % (str(list_cook_head_), str(cook_list))
        str_j = "<table>\n%s\n%s </table>" % (cook_jpg, use_str)
        
        print str_j
        self.write_line(str_j)
    def save_files(self, list_cook_file, jpg_file):
        res = "%s_.txt" % jpg_file
        com = ""
        for i in list_cook_file:
            com = com + "%s :\n" % str(i)
            for j in list_cook_file[i]:
                com =  com + "\t\t%s\n" % str(j)
        f = open(res, "w")
        f.write(com)
        f.close()
        return res



if __name__ =="__main__":
    report = Report("all")
    i = 100
    dist_list = {}
    dist_list["transactions "]= i 
    dist_list["errors "]= i 
    dist_list["run time "]= i 
    dist_list["rampup "]= i 
    dist_list["test start "]=  i 
    dist_list["test finish "]=  i 
    dist_list["time-series interval "]=  i
    print dist_list
    report.set_summary(dist_list)
#    if user_group_configs=:
#        report.write_line('<b>workload configuration:</b><br /><br />')
#        report.write_line('<table>')
#        report.write_line('<tr><th>group name</th><th>threads</th><th>script name</th></tr>')
#        for user_group_config in user_group_configs:
#            report.write_line('<tr><td>%s</td><td>%d</td><td>%s</td></tr>' %
#            (user_group_config.name, user_group_config.num_threads, user_group_config.script_file))
#        report.write_line('</table>')
    x = 'TPS.jpg'
    title_tps = "Throughput: 5 sec time-series"
    for i in xrange(3):
        self.set_h3_sum(title_tps+str(i), x)
