#!/usr/bin/env python3

from datetime import datetime, timedelta

import typer
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions

from core import Enroller
from enum import Enum

class BrowserType(str, Enum):
    FIREFOX = "firefox"
    CHROME = "chrome"

def main(
    username: str = typer.Option(None, prompt="SIS Username", help="SIS Username"),
    password: str = typer.Option(
        None,
        prompt="SIS Password",
        confirmation_prompt=True,
        hide_input=True,
        help="SIS Password",
    ),
    url: str = typer.Option(
        "https://sisadmin.case.edu/psp/P92SCWR/?cmd=login",
        help="SIS base URL to use",
    ),
    threads: int = typer.Option(1, help="the number of instances to run"),
    browser: BrowserType = typer.Option(BrowserType.FIREFOX, help="the browser instance to run"),
    test: bool = typer.Option(
        False,
        help="whether to run in test mode by attempting to register immediately instead of waiting",
    ),
    headless: bool = typer.Option(
        True, help="whether to run the script without opening a browser GUI"
    ),
    verbose: bool = typer.Option(False, help="whether to log extra output"),
):
    typer.secho(f"Using {threads} thread(s).")
    Browser, Options = (
        (Firefox, FirefoxOptions) if browser == BrowserType.FIREFOX else (Chrome, ChromeOptions)
    )

    # if it's the day of registration
    today = datetime.now()
    enroll_date = datetime(today.year, today.month, today.day, 7)
    if today.hour > 7:
        # registration is tomorrow
        enroll_date += timedelta(days=1)

    # if we're in the fall semester, register for the spring
    term = (
        f"Spring {enroll_date.year + 1}"
        if 8 <= datetime.now().month <= 12
        else f"Fall {enroll_date.year}"
    )

    if test:
        typer.secho("Testing script...")
        # start 3 seconds after the script
        start_time = datetime.now() + timedelta(seconds=3)
        delay = timedelta(minutes=1)
        enroll_date = datetime.now() + delay
    else:
        # begin 15 minutes before registration is supposed to open
        start_time = enroll_date - timedelta(minutes=15)

    # main stuff
    mid_thread = threads // 2
    for i in range(threads):
        # Click times should "surround" 7AM on enrollment day, in intervals of 2ms apart
        offset = timedelta(milliseconds=5 * (i - mid_thread))
        e = Enroller(
            enroll_time=enroll_date + offset,
            start_time=start_time,
            term=term,
            username=username,
            password=password,
            browser=Browser,
            opts=Options,
            headless=headless,
            test=test,
            base_url=url,
            verbose=verbose,
        )
        e.thread.start()


if __name__ == "__main__":
    typer.run(main)
