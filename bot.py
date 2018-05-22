#!/usr/bin/env python
import getpass
import math
import os
from sys import argv
from datetime import datetime
import time
from datetime import datetime

import pause
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# prompt for login credentials
if len(argv) >= 4:
    usernameStr = argv[1]
    passwordStr = argv[2]
    semester = argv[3]
else:
    # prompt for username
    usernameStr = input("SIS Username: ")
    # prompt for password using getpass to ensure password security
    passwordStr = getpass.getpass("SIS Password: ")
    # prompt for the semester being registered for to determine the cart link code
    semester = input(
        "Semester (f = fall, s = spring, or paste SIS Mobile Cart Link): ")

# optional - allows for headless browser configuration, theoretically faster script
chrome_options = Options()
# uncomment for headless browser functionality
if len(argv) >= 5:
    if argv[4] == '-h':
        chrome_options.add_argument("--headless")
        print("Running Headless...")

# get current month
month = datetime.now().month

# if it's the day of registration
if datetime.now().time().hour < 7:
    day = datetime.now().day
else:
    try:
        # if it's the day before registration
        day = datetime.now().day + 1
        datetime(datetime.now().year, month, day)
    except ValueError:
        # catch registering before the day of registration on a month rollover - not sure this will ever happen
        month += 1
        day = 1

# base cart link for sis-mobile
cart_link = "https://sismobile.case.edu/app/student/enrollmentcart/cart/CASE1/UGRD/"

# sketchy math to compute cart link code, append to base link
if semester == 'f':
    # sketchy math to isolate the 'acd' from some year abcd
    cart_link += str(math.floor(datetime.now().year / 1000))
    cart_link += str(datetime.now().year -
                     math.floor(datetime.now().year / 1000) * 1000)
    # signifies august as first month of classes
    cart_link += '8'
elif semester == 's':
    # similar sketchy math
    cart_link += str(math.floor(datetime.now().year / 1000))
    cart_link += str(datetime.now().year + 1 -
                     math.floor(datetime.now().year / 1000) * 1000)
    # signifies january as first month of classes
    cart_link += '1'
else:
    # copy the link
    cart_link = semester

# begin two minutes before registration is supposed to open
start_time = datetime(datetime.now().year, month, day, 6, 58)

pause.seconds(.01)
pause.until(start_time)
print("Script will begin at", start_time, "AM")


driver = webdriver.Chrome(chrome_options=chrome_options,
                          executable_path="/usr/local/bin/chromedriver")
driver.get(cart_link)

# wait for the login screen to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'login-btn')))

username = driver.find_element_by_name("username")
username.send_keys(usernameStr)

password = driver.find_element_by_name('password')
password.send_keys(passwordStr)

login = driver.find_element_by_id('login-btn')
login.click()

# wait for cart to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'cart-select-all')))

selectAll = driver.find_element_by_id('cart-select-all')
selectAll.click()

enroll = driver.find_element_by_id('enroll')

# wait until 7:00AM and then click
pause.until(datetime(datetime.now().year, month, day, 7))
enroll.click()
WebDriverWait(driver, 10)

print("Successfully Registered")
