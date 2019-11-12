#!/usr/bin/env python3
import getpass
from datetime import datetime
from datetime import timedelta
from sys import argv
from threading import Thread

import pause
from selenium.webdriver import Firefox, Chrome, FirefoxOptions, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# sketchy argparse
test = "-t" in argv or "--test" in argv
ignore_password_validation = "--ignore-password" in argv or "-i" in argv
use_firefox = "--firefox" in argv or "-f" in argv
headless = "--headless" in argv or "-h" in argv
verbose = "--verbose" in argv or "-v" in argv
num_threads = 1

if "-n" in argv:
    num_threads_i = argv.index("-n") + 1
    num_threads = int(argv[num_threads_i])
elif "--num-threads" in argv:
    num_threads_i = argv.index("--num-threads") + 1
    num_threads = int(argv[num_threads_i])

print("Using {} thread(s).".format(num_threads))

if use_firefox:
    Browser = Firefox
    Options = FirefoxOptions
else:
    Browser = Chrome
    Options = ChromeOptions

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


def browser_init(Browser=Chrome, Options=ChromeOptions, headless=False, size=(1920, 1080)):
    options = Options()
    options.headless = True
    driver = Browser(options=Options)
    if headless:
        driver.set_window_size(size[0], size[1])
    return driver


class Enroller:
    thread = None
    driver = None
    enroll_time = None

    def __init__(self, enroll_time=enroll_date, browser=Chrome, opts=ChromeOptions, headless=False,
                 size=(1920, 1080)):
        self.driver = browser_init(Browser=browser, Options=opts, headless=headless, size=size)
        self.enroll_time = enroll_time
        self.thread = Thread(target=self.enroll)

    def log(self, msg):
        if headless or verbose:
            print("{}: {}".format(self.thread.ident, msg))

    def enroll(self):
        print("Starting browser at", start_time)
        pause.until(start_time)

        # setup the web self.driver
        self.driver.get(base_url)
        # wait for the login screen to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login")))

        self.log("Logging into SIS")
        # enter username & password
        self.driver.find_element_by_name("userid").send_keys(usernameStr)
        self.driver.find_element_by_name("pwd").send_keys(passwordStr)

        # click login
        self.driver.find_element_by_name("Sign in").click()
        pause.seconds(3)
        self.driver.find_element_by_xpath(
            "//img[@alt='a calendar with magnifying glass icon']"
        ).click()
        pause.seconds(3)

        self.log("Opening shopping cart.")
        self.driver.find_element_by_link_text("Shopping Cart").click()
        pause.seconds(3)
        try:
            self.driver.find_element_by_link_text(term).click()
            pause.seconds(3)
        except BaseException:
            pass

        self.log("Selecting courses...")
        # Select all courses in shopping cart
        chkboxes = self.driver.find_elements_by_class_name("ps-checkbox")
        for c in chkboxes:
            c.click()
        self.log("Selected {} courses".format(len(chkboxes)))

        self.driver.save_screenshot("preenroll_{}.png".format(today))

        self.log("Clicking enroll.")
        self.driver.find_element_by_link_text("Enroll").click()

        # click enroll in 5 seconds from now if testing
        if test:
            self.enroll_time = datetime.now() + timedelta(seconds=3)

        # pause until 7AM and click immediately after
        print("Waiting to enroll until {}".format(self.enroll_time))
        pause.until(self.enroll_time)
        self.driver.find_element_by_link_text("Yes").click()
        pause.seconds(10)
        self.driver.save_screenshot("confirm_page_{}.png".format(today))


# main stuff

