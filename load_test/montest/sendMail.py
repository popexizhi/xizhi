#!/usr/bin/env python
# -*- coding: utf-8 -*-
#导入smtplib和MIMEText
import smtplib,sys 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_mail(sub, content, build_num="LOAD_TEST_db", send_list="all"):
    mailto_list = []
    #############   
    #要发给谁
    if ( "all" == send_list):
        mailto_list=["lijie@senlime.com"] #"slim_test@126.com",
    else :
        mailto_list.append(send_list)#["lijie@senlime.com"] #"server@senlime.com",
    #####################
    #设置服务器，用户名、口令以及邮箱的后缀
    mail_host="smtp.office365.com"
    mail_user="dev@senlime.com"
    mail_pass="S2m123,./"
    mail_postfix="office365.com"
    mail_port=587
    ######################
    '''''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("aaa@126.com","sub","content")
    '''
    me=mail_user#+"<"+mail_user+"@"+mail_postfix+">"
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #msg = MIMEText(content,_charset='utf8')
    content = content + "\n mail send 位置:/home/slim/test/dev_provision/provision_ue_use/dbback[192.168.1.84]"
    htm = MIMEText(content,_charset='utf-8')
    msg.attach(htm)
    msg['Subject'] = sub 
    msg['From'] = me 
    msg['To'] = ";".join(mailto_list) 
    try: 
        s = smtplib.SMTP(mail_host,port=mail_port,timeout=20) 
        #s.connect(mail_host) 
        #s.set_debuglevel(1)
        s.ehlo()
        s.starttls()
        s.ehlo()
        
        s.login(mail_user,mail_pass) 
        s.sendmail(me, mailto_list, msg.as_string()) 
        s.close() 
        return True
    except Exception, e: 
        print str(e) 
        return  False
if __name__ == '__main__':
    efile = sys.argv[1] #"testsult.txt"
    f = open(efile)
    conx = f.readlines()
    f.close()
    con_mail = ""
    for i in conx:
        con_mail = con_mail +","+str(i) 
    if send_mail("LOADTEST_db&core_test",con_mail, send_list="all"): 
        print '发送成功'
    else: 
        print '发送失败'
