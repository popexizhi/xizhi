

run,python sampleRobot.py, , ,NewPID
;<unu>run�ĵڶ�������Ϊpython sampleRobot.py Ϊ��python��������ű��������Ϊpython,sampleRobot.py,����ļ�����The working directory for the launched item��
;<du>run��last������OutputVarPID�������Ժܺõļ�ؽ������л�����

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
;:) ok��,��while�Ķ����Ҫʹ��{},�ð��Լ��ĳ�������:)
