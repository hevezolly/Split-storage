欣严信呐伺屯闻 招劳人荣�
忮瘃�� 1.0
棱蝾�: 澡眍沐眍� 埋邂铍钿 (sevafinogenov@gmail.com)

蜗妊劳扰:
溧眄�� 忮瘃�� 镳桦铈屙�� �怆�弪�� 疱嚯桤圉桢� 疣耧疱溴脲眄钽� 躔囗桦棂�

倚帕温劳冗:
1) Python 忮瘃梃 礤 龛驽 3.6
2) 徼犭桀蝈赅 hashlib

盐岩缆:
觐眈铍�� 忮瘃�� 腩赅朦眍泐 躔囗桦棂�: node.py
觐眈铍�� 忮瘃�� 皴疴屦� 腩赅朦眍泐 箸豚: NodeServer.py
觐眈铍�� 忮瘃�� 铖眍泐 皴疴屦� 疣耧疱溴脲眄钽� 躔囗桦棂�: MainServer.py
觐眈铍�� 忮瘃�� 噤扈龛耱疣蝾疣 皴疴屦�: administrator.py
祛潴腓: info.py, parse.py, singleFileController.py, MainNodeClient.py, storage_controller.py
蝈耱�: Test_test.py

严欣率� 衔 抢嫌咽� 腩赅朦眍泐 躔囗桦棂�:
桉镱朦珙忄龛�: node.py DIRECTORY [OPTIONS]

箸咫 疣耧疱溴脲眄钽� 躔囗桦棂�

镱玷鲨铐睇� 囵泱戾眚�:
  DIRECTORY             矬螯 漕 腩赅朦眍泐 躔囗桦棂�

铒鲨铐嚯 囵泱戾眚�:
  -h, --help            耧疣怅�
  -w KEY VALUE, --write KEY VALUE
                        玎镨覃忄弪 珥圜屙桢 VALUE 镱 觌� KEY
                        � 玎忮瘌噱� 疣犷蝮.
  -W [KEY=VALUE [KEY=VALUE ...]], --write_multiple [KEY=VALUE [KEY=VALUE ...]]
                        玎镨覃忄弪 礤耜铍� 珥圜屙栝 VALUE 镱 觌囔 KEY
                        羼腓 恹玮囗� 徨� 囵泱祉蝾�, 蝾 镳桧屐噱� 觌� � 珥圜屙��
                        耦 耱囗溧痱眍泐 忖钿� stdin
  -r KEY, --read KEY    恹忸滂� 珥圜屙桢 镱 觌� KEY � 玎忮瘌噱� 疣犷蝮.
  -d KEY, --delete KEY  
                        箐嚯�弪 珥圜屙桢 镱 觌� KEY � 玎忮瘌噱� 疣犷蝮.
  -D [KEY [KEY ...]], --delete_multiple [KEY [KEY ...]]
                        箐嚯�弪 眢耜铍� 珥圜屙栝 镱 觌囔 KEY 桤 躔囗桦棂�
                        羼腓 恹玮囗� 徨� 囵泱戾眚钼, 蝾 镳桧桁噱� 觌�
                        耦 耱囗溧痱眍泐 忖钿� stdin
  -e, --empty           镱腠铖螯� 铟棂噱� 躔囗桦棂� � 玎忮瘌噱� 疣犷蝮.
  -c KEY, --contains KEY
                        恹忸滂� YES 羼腓 觌 耦溴疰栩�� � 躔囗桦棂�, 
			NO, 羼腓 邈� 蜞� 礤� � 玎忮瘌噱� 疣犷蝮.
  -l, --list            恹忸滂� 怦� 觌�, 耦溴疰帙桢�� � 躔囗桦棂�.
  -i, -ignore_register  羼腓 铗 綦嚆 镱耱噔脲�, 蝾 桡眍痂痼弪 疱汨耱�
			忖钿桁钽� 觌� (玎 桉觌屙桢� 觐爨礓 -w/--write, -e/--empty,
			-l/--list, -W/--write_multiple).
  -s, --silent_mode     铗觌噱� 恹忸� 镳钽疣祆�

严欣率� 衔 抢嫌咽� 箸豚 皴蜩:

桉镱朦珙忄龛�: NodeServer.py [-h] [--host HOST] DIRECTORY PORT

镱玷鲨铐睇� 囵泱戾眚�:
  DIRECTORY    矬螯 漕 滂疱牝铕梃 箸豚
  PORT         镱痱 皴疴屦�

optional arguments:
  -h, --help   镱赅琨忄弪 耧疣怅�
  --host HOST  镱痱 躅耱�

严欣率� 衔 抢嫌咽� 皴疴屦� 皴蜩:
桉镱朦珙忄龛�: MainServer.py [-h] [--host HOST] [-c] [-n HOST PORT] DIRECTORY PORT

镱玷鲨铐睇� 囵泱戾眚�:
  DIRECTORY             矬螯 漕 滂疱牝铕梃 皴疴屦�
  PORT                  镱痱 耦赍蜞

optional arguments:
  -h, --help            镱赅琨忄弪 耧疣怅�
  --host HOST           躅耱 耦赍蜞
  -c, --create_new	羼腓 桉镱朦珙忄�, 蝾 耦玟噱� 眍忸� 躔囗桦棂�

橡� 耦玟囗梃 眍忸泐 皴疴屦�, � 礤� 礤 狍溴� 桧纛痨圉梃 钺 箸豚�. 
项潢膻麒螯 桴 祛骓� 蝾朦觐 麇疱� 噤扈龛耱疣蝾疣 皴蜩.
体驿� 玎矬耜囔� 皴疴屦 耦躔囗�弪 桧纛痨圉棹 钺 箸豚� � 镳� 镳钼蝾痦 玎矬耜圊
狍溴� 稃蜞螯�� � 龛� 镱潢膻麒螯��.
皴疴屦 祛骓� 钺眢腓螯, 羼腓 桉镱朦珙忄螯 觌 -c

严欣率� 衔 抢嫌咽� 噤扈龛耱疣蝾疣:

桉镱朦珙忄龛�: administrator.py [-w KEY VALUE] [-r KEY] [-e KEY] [-c INDEX]
                        [-n HOST PORT] [-s] [-d INDEX] [-i] [-h]
                        HOST PORT

镱玷鲨铐睇� 囵泱戾眚�:
  HOST                 	躅耱 皴疴屦�
  PORT                  镱痱 皴疴屦�

铒鲨铐嚯 囵泱戾眚�:
  -w KEY VALUE, --write KEY VALUE
                        耦躔囗�弪 珥圜屙桢 VALUE 镱 觌� KEY � 疣耧疱溴脲眄铄 躔囗桦棂�
  -r KEY, --read KEY    聍栩噱� 珥圜屙桢 镱 觌� KEY
  -e KEY, --empty KEY  	箐嚯�弪 珥圜屙桢 镱 觌� KEY
  -c INDEX, --connect INDEX
                        镱潢膻鬣弪�� � 耋耱怏屐� 箸塍 皴蜩 镱 邈� 桧溴犟�
  -n HOST PORT, --connect_new HOST PORT
                        漕徉怆�弪 眍恹� 箸咫 � 皴螯 镱 邈� 躅耱� HOST � 镱痱� PORT
  -s, --shut            铗觌噱� 皴疴屦
  -d INDEX, --disconnect INDEX
                        铗觌噱� 箸咫 皴蜩 镱 邈� 桧溴犟� INDEX 铗 皴疴屦�
  -i, --indexes        	恹忸滂� 耧桉铌 桧溴犟钼 嚓蜩忭 箸腩�
  -h, --help

碾� 疣犷螓 噤扈龛耱疣蝾疣 礤钺躅滂� 玎矬眄 皴疴屦. 橡� 镥疴铎 邈� 玎矬耜�, 
噤扈龛耱疣蝾� 漕腈屙 漕徉忤螯 � 礤泐 箸臌 � 镱祛� 觐爨礓�

administrator.py -n HOST PORT 镳� 铎 皴疴屦 镱稃蜞弪�� 镱潢膻麒螯�� � 箸塍 镱
溧眄 躅耱� � 镱痱� � 镳桉忸弪 屐� 桧溴犟. 腕戾疣鲨� 桧溴犟钼 磬麒磬弪�� � 0

� 箧� 耋耱怏屐� 箸塍 祛骓� 镱潢膻麒螯�� 镱 邈� 桧溴犟� � 镱祛� 觐爨礓�

administrator.py -c INDEX

� 铗觌栩� 邈� - � 镱祛� 觐爨礓� 

administrator.py -d INDEX

箸磬螯 桧溴犟� 镱潢膻麇眄 箸腩� 祛骓� � 镱祛� 觐爨礓�

administrator.py -i 

觌 -s 镱腠铖螯� 铗觌噱� 皴疴屦 忪羼蝈 耦 怦屐� 镱潢膻麇眄� � 礤祗 箸豚扈

闲忍判 妊衔塑俏吕腿� 欣严信呐伺屯蚊� 招劳人荣�:

1) 潆� 磬鬣豚 礤钺躅滂祛 镳铊龛鲨桊钼囹� 箸臌 腩赅朦眍泐 躔囗桦棂�

潆� 桧桷栲鲨� 箸豚 磬漕 耦玟囹� 矬耱簋 滂疱牝铕棹, � 溧眄铎 镳桁屦� .\foo1

� 恹镱腠栩� 觐爨礓�:

NodeSetvet.py .\foo1 1111

沅� 1111 - � 镱痱 耦赍蜞, 觐蝾瘥� 狍溴� 桉镱朦珙忄螯�� 箸腩�

� 镱祛� 觌� --host 祛骓� 箨噻囹� 躅耱 箸豚. 镱 箪铍鬣龛� 桉镱朦珞弪�� localhost

蜞觇� 驽 钺疣珙� 祛骓� 耦玟囹� 礤钽疣龛麇眍� 觐腓麇耱忸 箸腩�.

2) 溧脲� 礤钺躅滂祛 玎矬耱栩� 皴疴屦 疣耧疱溴脲眄钽� 躔囗桦棂�

潆� 钽� 磬漕 耦玟囹� 妁� 钿眢 滂疱牝铕棹, � 溧眄铎 镳桁屦� .\bar � 恹镱腠栩� 觐爨礓�

MainServer.py .\bar 2222 -c

沅� 2222 - � 镱痱 皴疴屦�, 镱 觐蝾痤祗 狍潴� 镱潢膻鬣螯�� 镱朦珙忄蝈腓.

镳� 桉镱朦珙忄龛� 觌� --host 祛骓� 箨噻囹� 躅耱 皴疴屦�. 项 箪铍鬣龛� 桉镱朦珞弪�� localhost

觌 -c 铗忮鬣弪 玎 耦玟囗桢 眍忸泐 皴疴屦�. 橡� 镱怛铕眍� 玎矬耜� 桉镱朦珙忄龛� 觌� -c 镳桠邃弪
� 铟桉蜿� 躔囗桦棂�.

玎戾鬣龛�: � 皴疴屦� 镱赅 礤 镱潢膻麇� 龛 钿桧 箸咫. 项潢膻麒螯 箸臌 耢铈弪 噤扈龛耱疣蝾�

3) 羼腓 皴疴屦 猁� 玎矬� 镥疴 疣�, 蝾 � 礤祗 礤钺躅滂祛 镱潢膻麒螯 箸臌.

� 溴豚弪�� � 镱祛� 觐爨礓� 噤扈龛耱疣蝾疣:

administrator.py localhost 2222 -n localhost 1111

溧眄�� 觐爨礓� 镱潢膻鬣弪 � 皴疴屦� � 躅耱铎 localhost � 镱痱铎 2222
箸咫 � 躅耱铎 localhost � 镱痱铎 1111. 彦疴屦 玎镱祉栩 铗 箸咫 镱� 桧溴犟铎 0.
橡� 镱怛铕眍� 玎矬耜� 皴疴屦�, 铐 镱稃蜞弪�� 噔蝾爨蜩麇耜� 镱潢膻麒螯�� � 铎� 箸塍.

铋 驽 觐爨礓铋 祛骓� 镱潢膻麒螯 � 皴疴屦� 漯筱桢 箸臌. 铐� 狍潴� 耦躔囗屙� 镱�
桧溴犟囔� 1, 2 � �.�. 

耧桉铌 桧溴犟钼 箸腩�, 镱潢膻麇眄 � 皴疴屦� 祛骓� 筲桎弪�, 桉镱朦珙忄� 觐爨礓�

administrator.py localhost 2222 -i

� 耠篦噱, 羼腓 耦邃桧屙桢 � 箸腩� (矬耱�, 潆� 镳桁屦�, 邈� 桧溴犟 - 0) 镱蝈��眍, 祛骓�
玎眍忸 镱潢膻麒螯�� � 箸塍 � 镱祛� 觐爨礓�

administrator.py localhost 2222 -c 0

牮铎� 钽�, 祛骓� 怵篦眢� 铗觌栩� 箸咫 铗 皴疴屦� � 镱祛� 觐爨礓�

administrator.py localhost 2222 -d 0

沅� 忪羼蝾 0 祛驽� 猁螯 桧溴犟 膻犷泐 漯筱钽� 镱潢膻麇眄钽� 箸豚.
镳� 铎 铗觌屙睇� 箸咫 狍溴� 恹觌屙.

牮铎� 钽� 祛骓� 铗觌栩� 忮顸 皴疴屦. � 溴豚弪�� � 镱祛� 觐爨礓�

administrator.py localhost 2222 -s

镳� 铎 狍溴� 恹觌屦� 皴疴屦, � 蜞赕� 怦� 镱潢膻麇眄 � 礤祗 箸臌.

潆� 忡噼祛溴轳蜮�� � 躔囗桦棂屐 祛骓� 桉镱朦珙忄螯 觐爨礓�:

administrator.py localhost 2222 -w KEY VALUE,
administrator.py localhost 2222 -r KEY,
administrator.py localhost 2222 -e KET.

� 觐爨礓� 溴轳蜮篁 囗嚯钽梓眍 耦铗忮蝰蜮簋� 觐爨礓囔 腩赅朦眍泐 躔囗桦棂�,
� 祛泱� 猁螯 恹玮囗� 赅� 桤 administrator.py, 蜞� � 桤 client.py
 