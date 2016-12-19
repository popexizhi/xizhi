#-*-coding:utf8-*-
load_test_cfg = {
    "source_dir": "/home/jenkins/test2", #原始log位置
    "process_dir" : "/data/load_use/process", #tcp发包过滤后存储位置
    "processRtt_dir" : "/home/jenkins/test/rtt_process", #rtt过滤后存储位置
    "backup_dir": "/data/load_use/backup", #原始log 备份位置
    #test use
    #"process_dir" : "/data/load_use/process_test", #tcp发包过滤后存储位置
    #"source_dir": "/home/jenkins/test2/data/load_use/tar_backup", #原始log位置
    #"backup_dir": "/data/load_use/backup_test", #原始log 备份位置
    "tar_backup_dir" : "/data/load_use/tar_backup", #tar 文件生成的dir

    "long_time" :1, #process data处理的持续时间, 单位:h
    "log_save_time" : 1, #log_save data处理时间, 单位:h
    "ana_log" : "/data/load_use/ana.log" ,#可以处理的analysis_data dir file

    #nginx 
    "ng_process_tar": "/data/provision_test/log_backup/process", #nginx process backup
    "end" : 0 
}
