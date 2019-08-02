#!/usr/bin/python
# Author nu11secur1ty
# This is only for education and testing for vulnerability of the systems, 
# do not use for malicious purpose!

from colorama import Fore, Back, Style 
try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

# to search 
print(Fore.GREEN + 'Put your d0rk here\n')
print(Style.RESET_ALL)

# Do not make a lot of requests searching! ;)
query = input()
print("\n")

print(Fore.RED + 'Your result\n')
for maaluk in search(query, tld="com", num=10, stop=25, pause=2): 
    print(maaluk)
print(Style.RESET_ALL)
