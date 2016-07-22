<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1399197727781" ID="ID_723433277" MODIFIED="1399197743734" TEXT="robot framework">
<node CREATED="1399197744875" ID="ID_225576903" MODIFIED="1399197754875" POSITION="right" TEXT="bas">
<node CREATED="1399197834906" ID="ID_1937477496" MODIFIED="1399197835828" TEXT="PyGtalkRobot">
<node CREATED="1399197855406" ID="ID_230322634" MODIFIED="1399197856890" TEXT="class GtalkRobot">
<node CREATED="1399277217453" ID="ID_291484069" MODIFIED="1399277241015" TEXT="[get message use]">
<node CREATED="1399277056828" ID="ID_1781398968" MODIFIED="1399277058234" TEXT="    def controller(self, conn, message):"/>
<node CREATED="1399277059796" ID="ID_1184416869" MODIFIED="1399277189390" TEXT="    def presenceHandler(self, conn, presence):"/>
</node>
<node CREATED="1399277242140" ID="ID_856707911" MODIFIED="1399277249140" TEXT="[send message use]">
<node CREATED="1399277251312" ID="ID_1808278126" MODIFIED="1399277287546" TEXT="self.conn=xmpp.Client(server, debug=self.debug)"/>
</node>
</node>
</node>
<node CREATED="1469175184212" ID="ID_756255647" MODIFIED="1469175184212" TEXT=""/>
</node>
<node CREATED="1399277298406" ID="ID_371826309" MODIFIED="1399277302234" POSITION="right" TEXT="[next]">
<node CREATED="1399277303640" ID="ID_1600643695" LINK="#ID_1781398968" MODIFIED="1399277331343" TEXT="commet"/>
<node CREATED="1405473596890" ID="ID_540239339" MODIFIED="1405473604468" TEXT="[thinking]">
<node CREATED="1405473605375" ID="ID_941272556" MODIFIED="1405473608000" TEXT="add log">
<node CREATED="1405473609125" ID="ID_751657285" MODIFIED="1405473632203" TEXT="&#x4e0d;&#x540c;&#x63a5;&#x6536;&#x65b9;&#x7684;log show &#x901a;&#x8baf;&#x6548;&#x679c;">
<node CREATED="1405473633078" ID="ID_729120166" MODIFIED="1405473646765" TEXT="GtalkRobot"/>
<node CREATED="1405473647031" ID="ID_1455864652" MODIFIED="1405473654453" TEXT="chamberlain"/>
<node CREATED="1405473656515" ID="ID_309552556" MODIFIED="1405473662375" TEXT="ardino"/>
</node>
</node>
<node CREATED="1405473666359" ID="ID_1607529043" MODIFIED="1405473681953" TEXT="git for GW"/>
<node CREATED="1405473691921" ID="ID_980515826" MODIFIED="1405473712765" TEXT="ardino &#x5904;&#x7406; open &#x547d;&#x4ee4;"/>
<node CREATED="1405580867671" ID="ID_1878016393" MODIFIED="1405580872421" TEXT="about xizhi">
<node CREATED="1405580874093" ID="ID_1787453714" MODIFIED="1405580891062" TEXT="list">
<node CREATED="1405580905109" ID="ID_1902764913" MODIFIED="1405580905109" TEXT="1.why is xizhi?"/>
<node CREATED="1405580905109" ID="ID_1660679224" MODIFIED="1405580905109" TEXT="2.&#x6700;&#x7ec8;&#x76ee;&#x6807;"/>
<node CREATED="1405580905109" ID="ID_1380845218" MODIFIED="1405580905109" TEXT="3.&#x5907;&#x6ce8;&#x8fc7;&#x7a0b;&#x4e2d;&#x7684;idea"/>
<node CREATED="1405580905109" ID="ID_120386735" MODIFIED="1405580905109" TEXT="4.[&#x5f53;&#x524d;&#x72b6;&#x6001;]">
<node CREATED="1405580920078" ID="ID_1646783035" MODIFIED="1405580927015" TEXT="robot using">
<node CREATED="1405582687562" ID="ID_1187404711" MODIFIED="1405582716250" TEXT="uml:struct"/>
<node CREATED="1405582716687" ID="ID_1788116956" MODIFIED="1405582719781" TEXT="&#x95ee;&#x9898;">
<node CREATED="1405582720890" FOLDED="true" ID="ID_825423404" MODIFIED="1469175216752" TEXT="arudino ">
<node CREATED="1405582756406" ID="ID_527782420" MODIFIED="1405583309890">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      string &#x5339;&#x914d; &#x4e0d;&#x662f; == &#xff1f;
    </p>
    <p>
      &#x81ea;&#x5df1;&#x5b9a;&#x4e49;&#x5982;&#x4e0b;:
    </p>
    <p>
      String getcon = String(thisChar);
    </p>
    <p>
      if (getcon== "open" ){
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;//open power
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;_Openpower();
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}
    </p>
    <p>
      thisChar&#x8fdc;&#x7a0b;&#x8f93;&#x51fa;&#x4e3a;open&#x540e;&#x5982;&#x4f55;&#x90fd;&#x4e0d;&#x6267;&#x884c;if&#x4e2d;&#x7684;&#x5b9a;&#x4e49;&#x3002;&#x90c1;&#x95f7;&#xff0c;&#x6700;&#x540e;&#x5c06;&#x547d;&#x4ee4;&#x6539;&#x4e3a;&#x5355;&#x5b57;&#x8282;char&#x7684;&#x5339;&#x914d;&#x662f;&#x8f6c;&#x4e3a;int&#x6bd4;&#x8f83;&#x7684;&#xff0c;&#x5982;&#x4e0b;:
    </p>
    <p>
      if(int(thisChar)==int("o") )
    </p>
    <p>
      {
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;//open power
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;_Openpower();
    </p>
    <p>
      &#xa0;&#xa0;&#xa0;&#xa0;&#xa0;&#xa0;}
    </p>
    <p>
      &#x8c03;&#x8bd5;&#x901a;&#x8fc7;&#x4e86;&#xff0c;&#x4f46;&#x8fd9;&#x4e2a;&#x662f;&#x4e2a;&#x95ee;&#x9898;&#xff0c;&#x8981;&#x641e;&#x6e05;&#x695a;&#x4e00;&#x4e0b;
    </p>
  </body>
</html></richcontent>
</node>
<node CREATED="1405582757078" HGAP="28" ID="ID_948029687" MODIFIED="1405582761359" TEXT="" VSHIFT="17"/>
</node>
<node CREATED="1405582749671" ID="ID_1635771265" MODIFIED="1405582749671" TEXT=""/>
<node CREATED="1405582739171" ID="ID_1083856423" MODIFIED="1405582739171" TEXT=""/>
</node>
<node CREATED="1405582816125" ID="ID_1088828338" MODIFIED="1405582823218" TEXT="[note]">
<node CREATED="1405582828234" ID="ID_915262451" MODIFIED="1405583089015">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      SPI&#x4f7f;&#x7528;&#x65f6;&#x4f1a;&#x5360;&#x7528;13&#x53e3;&#xff0c;&#x81ea;&#x5df1;&#x6d4b;&#x8bd5;&#x65f6;&#x5f00;&#x59cb;&#x5b9a;&#x4e49;pin13&#x4e3a;OUTPUT,&#x8c03;&#x8bd5;&#x65f6;led&#x603b;&#x662f;hight&#xff0c;&#x540e;&#x6765;&#x541e;&#x63d0;&#x9192;&#x624d;&#x53d1;&#x73b0;&#x7684;&#xff0c;&#x8981;&#x597d;&#x597d;&#x770b;&#x624b;&#x518c;&#x554a;!
    </p>
    <p>
      add&#xff1a;http://arduino.cc/en/Tutorial/BarometricPressureSensor
    </p>
    <p>
      &#x5360;&#x7528;&#x7684;&#x662f;13&#xff0c;12&#xff0c;11
    </p>
  </body>
</html></richcontent>
</node>
</node>
</node>
</node>
<node CREATED="1405580905109" ID="ID_1298671356" MODIFIED="1469175245600" TEXT="5.next">
<node CREATED="1469175246618" ID="ID_1649476712" MODIFIED="1469175252473" TEXT="22/6/17">
<node CREATED="1469175253658" ID="ID_1980277983" MODIFIED="1469175287667" TEXT="readme &#x7ffb;&#x8bd1;esperanto &#x7248;"/>
<node CREATED="1469175288019" ID="ID_1921549624" MODIFIED="1469175417488" TEXT="add:&#x571f;&#x58e4;&#x6e7f;&#x5ea6;&#x63a2;&#x6d4b;&#x7684;client"/>
<node CREATED="1469175418620" ID="ID_1105597517" MODIFIED="1469175464792" TEXT="add:&#x901a;&#x4fe1;&#x901a;&#x9053;&#x591a;&#x6761;&#xff08;&#x9632;&#x6b62;&#x5f53;&#x524d;gtalk&#x505c;&#x7528;&#x6216;&#x51fa;&#x95ee;&#x9898;&#x540e;&#x7684;&#x95ee;&#x9898;&#xff09;"/>
<node CREATED="1469175467470" ID="ID_1887046063" MODIFIED="1469175692592" TEXT="add:web&#x7aef;&#x548c;&#x624b;&#x673a;&#x7aef;&#x7684;show&#x548c;&#x76d1;&#x63a7;"/>
</node>
</node>
</node>
</node>
</node>
<node CREATED="1406710559718" ID="ID_890354678" MODIFIED="1406710565437" TEXT="[testcase]">
<node CREATED="1400125054127" ID="ID_946641319" LINK="#ID_788780814" MODIFIED="1400125078189" TEXT="add testcase for chamberlain.py">
<node CREATED="1406712901937" ID="ID_1729439724" MODIFIED="1406712907203" TEXT="test">
<node CREATED="1406712907203" ID="ID_204353418" MODIFIED="1406712916531" TEXT="basic send"/>
<node CREATED="1406712916953" ID="ID_1735584122" MODIFIED="1406712927687" TEXT="basic rec"/>
<node CREATED="1406714703046" ID="ID_16516939" MODIFIED="1406714710171" TEXT="setup">
<node CREATED="1406714711421" ID="ID_1535004337" MODIFIED="1406794955609">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      [next]
    </p>
  </body>
</html></richcontent>
<node CREATED="1406710606906" ID="ID_1411146285" MODIFIED="1406710631703" TEXT="&#x542f;&#x52a8; D server">
<node CREATED="1406794962718" ID="ID_1309277847" MODIFIED="1406794996312" TEXT="&#x5199;&#x5165;testcase&#x7ebf;&#x7a0b;&#x4e2d; state and stop"/>
</node>
</node>
<node CREATED="1406794953796" ID="ID_834685365" MODIFIED="1406794953796">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      &#x591a;&#x7ebf;&#x7a0b;&#x542f;&#x52a8;Dome is ok
    </p>
  </body>
</html></richcontent>
<node CREATED="1406715014906" ID="ID_19391512" MODIFIED="1406715016515" TEXT="http://www.cnblogs.com/tqsummer/archive/2011/01/25/1944771.html"/>
</node>
</node>
</node>
</node>
<node CREATED="1406710569343" ID="ID_1311802622" MODIFIED="1406710604500" TEXT="add testcase for sampleRobot.py">
<node CREATED="1406710647593" ID="ID_1135753740" MODIFIED="1406710668609" TEXT="&#x68c0;&#x6d4b;&#x6bcf;&#x6761;&#x547d;&#x4ee4;&#x7684; &#x8fd4;&#x56de;&#x503c;"/>
</node>
</node>
</node>
<node CREATED="1400124813252" ID="ID_148232757" MODIFIED="1400124867970" POSITION="left" TEXT="ardino add">
<node CREATED="1400124824111" ID="ID_788780814" MODIFIED="1400124927627" TEXT="chamberlain.py - tcp &#x8fde;&#x63a5; command_003_openpower"/>
</node>
</node>
</map>
