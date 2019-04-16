#!/usr/bin/env python3
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

today = datetime.now()
# if it's the day of registration\
enroll_date = datetime(today.year, today.month, today.day, 7)
if today.hour > 7:
    # registration is tomorrow
    enroll_date += timedelta(days=1)

# base cart link for sis-mobile
cart_link = "https://sismobile.case.edu/app/student/enrollmentcart/cart/CASE1/UGRD/"

# sketchy math to compute cart link code and append to base link
month = datetime.now().month
# if we're in the fall semester, register for the spring
if month >= 8 and month <= 12:
    # similar sketchy math
    cart_link += str(math.floor(datetime.now().year / 1000))
    cart_link += str(datetime.now().year + 1 - math.floor(datetime.now().year / 1000) * 1000)
    # signifies january as first month of classes
    cart_link += '1'
# otherwise register for the fall - this assumes no summer registration
else:
    # sketchy math to isolate the 'acd' from some year abcd
    cart_link += str(math.floor(datetime.now().year / 1000))
    cart_link += str(datetime.now().year -
                     math.floor(datetime.now().year / 1000) * 1000)
    # signifies august as first month of classes
    cart_link += '8'

if test:
    print("Testing script...")
    # start 5 seconds after the script
    start_time = datetime.now() + timedelta(seconds=5)
else:
    # begin two minutes before registration is supposed to open
    start_time = enroll_date - timedelta(minutes=2)

print("Script will begin at", start_time)
pause.until(start_time)
driver = webdriver.Chrome()
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

# find the necessary buttons
select_all = driver.find_element_by_id('cart-select-all')
select_all.click()
enroll = driver.find_element_by_id('enroll')

# click enroll in 5 seconds from now if testing
if test:
    enroll_date = datetime.now() + timedelta(seconds=5)

# pause until 7AM and click immediately after
print("Enrolling at: ", enroll_date)
pause.until(enroll_date)
enroll.click()

# keep clicking until a minute after in case we miss it
while datetime.now() < enroll_date + timedelta(minutes=1):
    # once the cart page loads again, find the buttons again and click them
    if EC.presence_of_element_located((By.ID, 'cart-select-all')):
        driver.find_element_by_id('cart-select-all').click()
        driver.find_element_by_id('enroll').click()

# if we're still on the cart page, we messed up :(
if EC.presence_of_element_located((By.ID, 'cart-select-all')):
    print("Registration Failed")
else:
    print("Registration Successful")