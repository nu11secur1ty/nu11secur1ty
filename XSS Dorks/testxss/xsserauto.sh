#!/usr/bin/bash

echo "Give your host";
read host 
xsser -u $host --auto --reverse-check -s
	exit 0;
