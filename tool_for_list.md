# Introduction #
Iloj -- pope的开箱即用工具 记录

# 内容 #
这里是一个记录位置，会包含如下:

1.项目位置 

2.使用场景/范围 

3.下一步计划 

[唯一的目标: 好用，做自己的轮子] 

# 目录 #

## 基础统计工具
    
    https://github.com/popexizhi/moniter_log.git 

    branch: base_statistics
    static.py   
    四分位: x.quartiles
    标准统计结果: x.statistics_list 
    指定百分比的排序值: x.percentage_avg 

## nginx log 分析工具
    
    https://github.com/popexizhi/moniter_log.git 

    branch: nginx_monitor 

    process_log $1  # 过滤原始log,生成只包含$request_time $upstream_response_time 的log  
    python process_log.py $1_tmp  #对此log 统计处理,并产生ld类似的报告,这里的图形展示依赖dygraph的相关js
## dygraph use list
