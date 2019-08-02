# encoding: utf-8
try:
    from dorkdef import *
except ImportError:
    print("[¡] Error importing DorkDef module")
    exit()
    
try:
    import argparse
except ImportError:
    print("Error importing argparse")

#---------------------------ARGPARSER---------------------------
parser = argparse.ArgumentParser()

parser.add_argument('--url', '-u', action='store', dest='URL',
help='URL to scan')

parser.add_argument('--dorks', '-d', action='append', dest='dorks',
default=[],
help='Dorks to scan (all, login, vulns, info, deprecated), to select more than 1 type use multiple --dork, example: --dork deprecated --dork info.')


parser.add_argument('--verbose', '-v', action='store_true', default=False,
dest='verbose',
help='Verbose')

parser.add_argument('-ban', '-b', action='store_false', default=True,
dest='ban',
help='This command sleep 50 second between each google request (Recommended [still beta¡¡])')

results = parser.parse_args()


#---------------------------CLASS DORKS---------------------------

dorkme = dork(results.URL, results.dorks, results.verbose, results.ban)   # POO

dorkme.searchs()
