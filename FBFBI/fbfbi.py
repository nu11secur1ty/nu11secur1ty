#!/usr/bin/python3
# Authors: @nu11secur1ty
# FBFBI

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from modules import ping 
	
#enter the link to the website you want to automate login.
website_link="https://lookup-id.com/"

#enter your login username
v = input("Please give the URL of the facebook account_name\nFor example: https://www.facebook.com/userblabla\n")
# the victim (https://www.facebook.com/someuser)
account=v

#enter the element for username input field
element_for_account="fburl"

#enter the element for submit button
element_for_submit="check"


#browser = webdriver.Safari()	#for macOS users[for others use chrome vis chromedriver]
# Linux
browser = webdriver.Chrome('chromedriver')	#uncomment this line,for chrome users
# Windows
browser = webdriver.Chrome()	#uncomment this line,for chrome users
#browser = webdriver.Firefox()	#uncomment this line,for chrome users

browser.get((website_link))	

try:
	account_element = browser.find_element_by_name(element_for_account)
	account_element.send_keys(account)		
	
	signInButton = browser.find_element_by_name(element_for_submit)
	signInButton.click()
	
	print("payload is deployed...\n")
	
except Exception:
	#### This exception occurs if the element are not found in the webpage.
	print("Some error occured :(")
