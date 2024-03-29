import time
from datetime import datetime
from threading import Thread

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def pause(until: datetime):
    """block until a specified datetime

    Args:
        until (datetime): the time at which to resume program execution
    """
    while True:
        diff = until - datetime.now()
        if diff.total_seconds() > 0:
            time.sleep(diff.total_seconds() / 2)
        else:
            break


class Enroller:
    def __init__(
        self,
        enroll_time,
        start_time,
        term,
        username: str,
        password: str,
        base_url: str,
        browser,
        opts,
        headless=False,
        size=(1920, 1080),
        verbose=False,
        test=False,
    ):
        self.driver = self._browser_init(
            Browser=browser, Options=opts, headless=headless, size=size
        )
        self.start_time = start_time
        self.enroll_time = enroll_time
        self.term = term
        self.thread = Thread(target=self.register)
        self.headless = headless
        self.verbose = verbose
        self.test = test
        self.base_url = base_url
        self.username = username
        self.password = password

    def _browser_init(self, Browser, Options, headless=False, size=(1920, 1080)):
        options = Options()
        options.headless = headless
        driver = Browser(options=options)
        if headless:
            driver.set_window_size(size[0], size[1])
        return driver

    def log(self, msg, debug=True):
        if self.headless or self.verbose or not debug:
            print(f"{self.thread.name}: {msg}")

    def register(self):
        # wait until 15 minutes before registration to start the browser
        self.log(f"Waiting to begin until {self.start_time}")
        pause(self.start_time)

        # log in once we hit the start time and navigate to the shopping cart
        self.authenticate()
        self.open_cart()

        # pause until 7AM and click immediately after
        self.log(f"Waiting to enroll until {self.enroll_time}", debug=False)
        pause(self.enroll_time)
        self.enroll()

        # clean up stray processes
        if self.headless:
            self.cleanup()

    def authenticate(self):
        # setup the web self.driver
        self.log("Loading SIS")
        self.driver.get(self.base_url)
        # wait for the login screen to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))
        )

        self.log("Logging in")
        # enter username & password
        self.driver.find_element_by_name("userid").send_keys(self.username)
        self.driver.find_element_by_name("pwd").send_keys(self.password)

        # click login
        self.driver.find_element_by_name("Sign in").click()
        time.sleep(5)
        self.driver.find_element_by_xpath(
            "//img[@alt='a calendar with magnifying glass icon']"
        ).click()
        time.sleep(5)

    def open_cart(self):
        self.log("Opening shopping cart.")
        self.driver.find_element_by_link_text("Shopping Cart").click()
        time.sleep(5)
        try:
            self.driver.find_element_by_link_text(self.term).click()
            time.sleep(5)
        except BaseException:
            pass

        try:
            self.log("Selecting courses...")
            # Select all courses in shopping cart
            chkboxes = self.driver.find_elements_by_class_name("ps-checkbox")
            for c in chkboxes:
                c.click()
            self.log("Selected {} courses".format(len(chkboxes)))

            # self.driver.save_screenshot("preenroll_{}.png".format(self.enroll_time))

            self.log("Clicking enroll.")
            self.driver.find_element_by_link_text("Enroll").click()
        except BaseException:
            print("No courses in shopping cart. Terminating script.")
            exit(0)

    def enroll(self):
        self.driver.find_element_by_link_text("Yes").click()
        self.log(f"Enroll request sent at {datetime.now()}", debug=False)
        time.sleep(10)
        if self.headless:
            self.driver.save_screenshot(f"confirm_page_{self.enroll_time}.png")

    def cleanup(self):
        if self.headless:
            self.driver.quit()
        exit(0)
