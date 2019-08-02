# DorkMe
<a href="https://asciinema.org/a/XT6U3c9XqwSNN4vTetxssc0e9" target="_blank"><img src="https://asciinema.org/a/XT6U3c9XqwSNN4vTetxssc0e9.png" /></a>

# Dependencies
     pip install -r requirements.txt
It is highly recommended to add more dorks for an effective search, keep reading to see how


# Usage

python DorkMe.py --help

Examples:

python DorkMe.py --url target.com --dorks vulns -v (recommended for test)

python DorkMe.py --url target.com --dorks Deprecated,Info -v (multiple dorks)

python DorkMe.py --url target.com --dorks all -v (test all)


# About
DorkMe is a tool designed with the purpose of making easier the searching of vulnerabilities with Google Dorks, such as SQL Injection vulnerabilities.

Any idea, failure etc please report to telegram: blueudp

dork folder contains -> dorks to search, result folder contains -> results of DorkMe execution

Tested in ParrotOS and Kali Linux 2.0
# Beta Version
Remember DorkMe is beta, to avoid bans DorkMe wait about 1 minute on each request and 3 minutes every 100 requests

# Add Dorks 

If you want to add new dorks put it in one of the files in the dorks folder (preferable in its category), if it is not, you can add it to mydorks.txt.
    to add it: in the first line add the dork, in the second the severity: high , medium or low, and finally its description, look at the other files to do it correctly
Dork List:
    
    http://www.conzu.de/en/google-dork-liste-2018-conzu/
    https://www.exploit-db.com/google-hacking-database/
    Find admin Panels: https://starhackx.blogspot.com/2014/02/list-of-dorks-to-find-admin-panels_23.html#.W27U5uFKjV0
    

EXAMPLE:

    inurl:php?id= [enter]
    
    high [enter]
    
    SQLi [enter]
    
    (space)
    
    another dork
    

# Termux
To install on termux run pip2 and python2 instead of pip and python

# Well... WTF is dorking?
   Google hacking, also named Google dorking, is a computer hacking technique that uses Google Search and other Google applications to find security holes in the configuration and computer code that websites use.
   
For example, SQL injection usually has this structure in the url "file.php? Id = [vuln]", to look for pages vulnerable to SQLi we can use the operator "inurl:", which only shows results with X string in the url , we can also use the "filetype: [extension]" operator to search for sensitive files, a hyphen in front of a word so that the word does not appear in the search, quote a phrase or word to ALWAYS appear in the search results, etc. 

List of special operators: https://ahrefs.com/blog/google-advanced-search-operators/

# Contact Me
Name: Eduardo Pérez-Malumbres

Telegram: @blueudp

Twitter: https://twitter.com/blueudp
