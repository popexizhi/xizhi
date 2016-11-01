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
        table {
            margin-left: 10px;
        }
        td {
            text-align: right;
            color: #000000;
            background: #FFFFFF;
            padding-left: 10px;
            padding-right: 10px;
            padding-bottom: 0;
        }
        th {
            text-align: center;
            padding-right: 10px;
            padding-left: 10px;
            color: #000000;
            background: #FFFFFF;
        }
        div.summary {
            padding-left: 20px;
        }
    </style>
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
        self.write_line('<img src="%s"></img>' % jpg_file)

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
        report.set_h3_sum(title_tps+str(i), x)
