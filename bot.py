#!/usr/bin/env python3
import getpass
from datetime import datetime
from datetime import timedelta
from sys import argv

import pause
from selenium.webdriver import Firefox, Chrome, FirefoxOptions, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# sketchy argparse
if "-h" in argv or "--help" in argv:
    print("Commands: ")
    print("\t --ignore or -i: Skip duplicate password request because you are lazy")
    print(
        "\t --firefox or -f: Use Firefox instead of default chrome for the more astute among us"
    )
    print(
        "\t --headless or -h: Runs the bot headlessly because why should you have a head"
    )
    print("\t --verbose or -v: Prints out a bunch of shit")
    print("\t --creds or -c: For the very lazy")
    print()
    exit()


test = "-t" in argv or "--test" in argv
ignore_password_validation = "--ignore-password" in argv or "-i" in argv
use_firefox = "--firefox" in argv or "-f" in argv
headless = "--headless" in argv or "-h" in argv
verbose = "--verbose" in argv or "-v" in argv
use_cred_file = "--cred" in argv or "-c" in argv


if use_firefox:
    Browser = Firefox
    Options = FirefoxOptions
else:
    Browser = Chrome
    Options = ChromeOptions

if use_cred_file:
    with open("creds.txt", "r") as f:
        usernameStr = f.readline()[:-1]
        passwordStr = f.readline()
else:
    # prompt for username
    usernameStr = input("SIS Username: ")
    # prompt for password using getpass to ensure password security
    passwordStr = getpass.getpass("SIS Password: ")
    if not ignore_password_validation:
        passConfirm = getpass.getpass("Confirm Password: ")
        if passwordStr != passConfirm:
            print("Passwords do not match.")
            exit(0)

# if it's the day of registration
today = datetime.now()
enroll_date = datetime(today.year, today.month, today.day, 7)
if today.hour > 7:
    # registration is tomorrow
    enroll_date += timedelta(days=1)

base_url = "https://sisadmin.case.edu/psp/P92SCWR/?cmd=login"

# if we're in the fall semester, register for the spring
term = "{} {}".format(
    "Spring" if 8 <= datetime.now().month <= 12 else "Fall", enroll_date.year
)

if test:
    print("Testing script...")
    # start 3 seconds after the script
    start_time = datetime.now() + timedelta(seconds=3)
else:
    # begin two minutes before registration is supposed to open
    start_time = enroll_date - timedelta(minutes=2)

if headless or verbose:
    print("Running in headless mode")

print("Script will begin at", start_time)
pause.until(start_time)

# setup the web driver
options = Options()
options.headless = headless
driver = Browser(options=options)
if headless:
    driver.set_window_size(1920, 1080)
driver.get(base_url)
# wait for the login screen to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login")))

if headless or verbose:
    print("Logging into SIS")
# enter username
username = driver.find_element_by_name("userid")
username.send_keys(usernameStr)

# enter password
password = driver.find_element_by_name("pwd")
password.send_keys(passwordStr)

# click login
login = driver.find_element_by_name("Sign in")
login.click()
pause.seconds(3)
driver.find_element_by_xpath(
    "//img[@alt='a calendar with magnifying glass icon']"
).click()
pause.seconds(3)

if headless or verbose:
    print("Opening Shopping Cart")
driver.find_element_by_link_text("Shopping Cart").click()
pause.seconds(3)
try:
    driver.find_element_by_link_text(term).click()
    pause.seconds(3)
except BaseException:
    pass

if headless or verbose:
    print("Selecting courses")
# Select all courses in shopping cart
chkboxes = driver.find_elements_by_class_name("ps-checkbox")
for c in chkboxes:
    c.click()
if headless or verbose:
    print("Selected {} courses".format(len(chkboxes)))

if headless or verbose:
    print("Clicking Enroll")
driver.find_element_by_link_text("Enroll").click()

# click enroll in 5 seconds from now if testing
if test:
    enroll_date = datetime.now() + timedelta(seconds=3)

# pause until 7AM and click immediately after
print("Waiting to enroll until: {}".format(enroll_date))
pause.until(enroll_date)
driver.find_element_by_link_text("Yes").click()
pause.seconds(10)
driver.save_screenshot("confirm_page_{}.png".format(today))
