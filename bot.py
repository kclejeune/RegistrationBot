#!/usr/bin/env python3
import getpass
import math
from datetime import datetime
from datetime import timedelta
from sys import argv

import pause
from selenium import webdriver
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
# cart_link = "https://sisadmin.case.edu/psc/P92SCWR_18/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_MD_SP_FL.GBL?Action=U&MD=Y&GMenu=SSR_STUDENT_FL&GComp=SSR_START_PAGE_FL&GPage=SSR_START_PAGE_FL&scname=CS_SSR_MANAGE_CLASSES_NAV&ICAJAXTrf=true"
cart_link = "https://sisadmin.case.edu/psp/P92SCWR/?cmd=login"

# sketchy math to compute cart link code and append to base link
month = datetime.now().month
# if we're in the fall semester, register for the spring
if 8 <= month <= 12:
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
driver = webdriver.Firefox()
driver.get(cart_link)

# wait for the login screen to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'login')))

# enter username
username = driver.find_element_by_name("userid")
username.send_keys(usernameStr)

# enter password
password = driver.find_element_by_name('pwd')
password.send_keys(passwordStr)

# click login
login = driver.find_element_by_name('Sign in')
login.click()

driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Classes & Enrollment'])[1]/following::div[3]").click()
pause.seconds(5)
driver.find_element_by_link_text("Shopping Cart").click()
pause.seconds(3)
driver.find_element_by_link_text("Spring 2020").click()

# # wait for cart to load
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.ID, "win15divACAD_CAR_TBL_DESCR$1")))
#
# # Select term
# driver.find_element_by_id("win15divACAD_CAR_TBL_DESCR$1").click()

pause.seconds(3)
# Select courses
chkboxes = driver.find_elements_by_class_name("ps-checkbox")
for c in chkboxes:
    c.click()

driver.find_element_by_link_text("Enroll").click()

# click enroll in 5 seconds from now if testing
if test:
    enroll_date = datetime.now() + timedelta(seconds=5)

# pause until 7AM and click immediately after
print("Enrolling at: ", enroll_date)
pause.until(enroll_date)

driver.find_element_by_link_text("Yes").click()

print("uhhhhh i guess im done here")
