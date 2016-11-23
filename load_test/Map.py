#-*-coding:utf8-*-
load_test_cfg = {
    "source_dir": "/home/jenkins/test2", #原始log位置
    "process_dir" : "/data/load_use/process", #tcp发包过滤后存储位置
    "backup_dir": "/data/load_use/backup", #原始log 备份位置


    "long_time" :1, #process data处理的持续时间, 单位:h
    "log_save_time" : 1, #log_save data处理时间, 单位:h
    "ana_log" : "/data/load_use/ana.log" ,#可以处理的analysis_data dir file
    "end" : 0 
}
