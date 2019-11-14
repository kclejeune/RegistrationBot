#!/usr/bin/env python3
import getpass
from datetime import datetime, timedelta
from sys import argv
from threading import Thread

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
num_threads = 1

if "-n" in argv:
    num_threads_i = argv.index("-n") + 1
    num_threads = int(argv[num_threads_i])
elif "--num-threads" in argv:
    num_threads_i = argv.index("--num-threads") + 1
    num_threads = int(argv[num_threads_i])

print("Using {} thread(s).".format(num_threads))
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
    # begin 15 minutes before registration is supposed to open
    start_time = enroll_date - timedelta(minutes=15)


def browser_init(
    Browser=Chrome, Options=ChromeOptions, headless=False, size=(1920, 1080)
):
    options = Options()
    options.headless = headless
    driver = Browser(options=options)
    if headless:
        driver.set_window_size(size[0], size[1])
    return driver


class Enroller:
    thread = None
    driver = None
    enroll_time = None

    def __init__(
        self,
        enroll_time=enroll_date,
        browser=Chrome,
        opts=ChromeOptions,
        headless=False,
        size=(1920, 1080),
        test=False,
    ):
        self.driver = browser_init(
            Browser=browser, Options=opts, headless=headless, size=size
        )
        self.enroll_time = enroll_time
        self.thread = Thread(target=self.enroll)
        self.headless = headless
        self.verbose = verbose
        self.test = test

    def log(self, msg, debug=True):
        if self.headless or self.verbose or not debug:
            print("{}: {}".format(self.thread.name, msg))

    def enroll(self):
        self.log("Starting browser at {}".format(start_time), debug=False)
        pause.until(start_time)

        # setup the web self.driver
        self.driver.get(base_url)
        # wait for the login screen to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))
        )

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

        self.driver.save_screenshot("preenroll_{}.png".format(self.enroll_time))

        self.log("Clicking enroll.")
        self.driver.find_element_by_link_text("Enroll").click()

        # pause until 7AM and click immediately after
        self.log("Waiting to enroll until {}".format(self.enroll_time), debug=False)
        pause.until(self.enroll_time)
        self.driver.find_element_by_link_text("Yes").click()
        self.log("Enroll request sent.", debug=False)
        pause.seconds(10)
        self.driver.save_screenshot("confirm_page_{}.png".format(self.enroll_time))

# click enroll in 5 seconds from now if testing
if test:
    enroll_date = datetime.now() + timedelta(seconds=45)

# main stuff
mid_thread = int(num_threads / 2)
for i in range(num_threads):
    # Click times should "surround" 7AM on enrollment day, in intervals of 2ms apart
    offset = timedelta(milliseconds=2 * (i - mid_thread))
    e = Enroller(
        enroll_date + offset,
        browser=Firefox,
        opts=FirefoxOptions,
        headless=headless,
        test=test,
    )
    e.thread.start()
