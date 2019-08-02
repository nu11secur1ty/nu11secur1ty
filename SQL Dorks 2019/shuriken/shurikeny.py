#!/usr/bin/python
# Author nu11secur1ty
import webbrowser
from colorama import Fore, Back, Style

print(Fore.GREEN + 'Pyt here your d0rk')
print(Fore.RED + 'When you finish with the search, close the browser and press Enter in the terminal')
print(Fore.YELLOW + 'If you deside to not using the program press Ctrl+C')
print(Style.RESET_ALL)

dork = input()
url = "https://www.google.com/search?q=" +(str(dork))+"&oq="+(str(dork))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU"
webbrowser.open_new(url)

