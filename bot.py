#!/usr/bin/env python
import getpass
import math
import os
from sys import argv
import time
from datetime import datetime
from datetime import timedelta
import pause
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

test = len(argv) >= 2 and (argv[1] == '-t' or argv[1] == '--test')

# prompt for username
usernameStr = input("SIS Username: ")
# prompt for password using getpass to ensure password security
passwordStr = getpass.getpass("SIS Password: ")
passConfirm = getpass.getpass("Confirm Password: ")
if passwordStr != passConfirm:
    print("Passwords do not match.")
    exit(0)
    
# prompt for the semester being registered for to determine the cart link code
semester = input(
    "Semester (f = fall, s = spring, or paste SIS Mobile Cart Link): ")

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
    cart_link += str(datetime.now().year + 1 - math.floor(datetime.now().year / 1000) * 1000)
    # signifies january as first month of classes
    cart_link += '1'
else:
    # copy the link
    cart_link = semester

if test:
    print("Testing script...")
    start_time = datetime.now()
else:
    # begin two minutes before registration is supposed to open
    start_time = datetime(datetime.now().year, month, day, 6, 58)

print("Script will begin at", start_time)
pause.until(start_time)
driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get(cart_link)

# wait for the login screen to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login-btn')))

# enter username
username = driver.find_element_by_name("username")
username.send_keys(usernameStr)

# enter password
password = driver.find_element_by_name('password')
password.send_keys(passwordStr)

# click login
login = driver.find_element_by_id('login-btn')
login.click()

# wait for cart to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 'cart-select-all')))

select_all = driver.find_element_by_id('cart-select-all')
select_all.click()
enroll = driver.find_element_by_id('enroll')

# wait until 7:00AM and then click enroll
if not test:
    pause.until(datetime(datetime.now().year, month, day, 7))
else:
    pause.until(datetime(datetime.now().year, datetime.now().month, datetime.now().day, 14, 56))

enroll.click()
WebDriverWait(driver, 10)

if EC.presence_of_element_located((By.ID, 'cart-select-all')):
    print("Registration Failed")
else:
    print("Successfully Registered")
