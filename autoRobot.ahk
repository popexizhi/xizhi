

run,python sampleRobot.py, , ,NewPID
;<unu>run的第二个参数为python sampleRobot.py 为以python运行这个脚本；但如果为python,sampleRobot.py,这个文件则是The working directory for the launched item了
;<du>run的last参数是OutputVarPID这样可以很好的监控进程运行环境了

while True
{
	process,Exist,%NewPID%
	;MsgBox The PID is,%NewPID%
	;MsgBox %ErrorLevel%
	if ErrorLevel>0
		robot_num=1
	else
		run,python sampleRobot.py, , ,NewPID	
}
;:) ok了,是while的多语句要使用{},好吧自己的尝试问题:)
