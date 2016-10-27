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
""")


    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write("""\
</body>
</html>
""")


if __name__ =="__main__":
    report = Report("x")
    i = 100
    report.write_line('<h1>Performance Results Report</h1>')

    report.write_line('<h2>Summary</h2>')

    report.write_line('<div class="summary">')
    report.write_line('<b>transactions:</b> %d<br />' % i)#results.total_transactions)
    report.write_line('<b>errors:</b> %d<br />' % i)#results.total_errors)
    report.write_line('<b>run time:</b> %d secs<br />' % i)#run_time)
    report.write_line('<b>rampup:</b> %d secs<br /><br />' % i)#rampup)
    report.write_line('<b>test start:</b> %s<br />' % str(i))#results.start_datetime)
    report.write_line('<b>test finish:</b> %s<br /><br />' % str(i))#results.finish_datetime)
    report.write_line('<b>time-series interval:</b> %s secs<br /><br /><br />' % str(i))#ts_interval)
#    if user_group_configs=:
#        report.write_line('<b>workload configuration:</b><br /><br />')
#        report.write_line('<table>')
#        report.write_line('<tr><th>group name</th><th>threads</th><th>script name</th></tr>')
#        for user_group_config in user_group_configs:
#            report.write_line('<tr><td>%s</td><td>%d</td><td>%s</td></tr>' %
#            (user_group_config.name, user_group_config.num_threads, user_group_config.script_file))
#        report.write_line('</table>')
    report.write_line('</div>')
    report.write_line('<h3>Throughput: 5 sec time-series</h3>')
    x = 'TPS.jpg'
    report.write_line('<img src="%s"></img>' % x)

