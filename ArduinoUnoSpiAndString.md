# Introduction #
Arduino uno 

&lt;de&gt;

 继电器部分test

# Details #

robot using

uml:总体结构图：

昨天调试的是图中green部分，ardunio上的code
问题
arudino
string 匹配 不是 == ？
自己定义如下:
String getcon = String(thisChar);
if (getcon== "open" ){
> //open power
> _Openpower();
> }
thisChar远程输出为open后如何都不执行if中的定义。郁闷，最后将命令改为单字节char的匹配是转为int比较的，如下:
if(int(thisChar)==int("o") )
{
> //open power
>_Openpower();
> }
调试通过了，但这个是个问题，要搞清楚一下



[note](note.md) 
SPI使用时会占用13口，自己测试时开始定义pin13为OUTPUT,调试时led总是hight，后来吞提醒才发现的，要好好看手册啊! 
add：http://arduino.cc/en/Tutorial/BarometricPressureSensor 
占用的是13，12，11 
