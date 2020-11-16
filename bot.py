#!/usr/bin/env python3
from core import Enroller
import getpass
from datetime import datetime, timedelta
import argparse
from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions


def main(args):
    print(f"Using {args.threads} thread(s).")
    Browser, Options = (
        (Firefox, FirefoxOptions)
        if args.browser == "firefox"
        else (Chrome, ChromeOptions)
    )

    if args.credentials:
        with open(args.credentials, "r") as f:
            usernameStr = f.readline().strip()
            passwordStr = f.readline().strip()
    else:
        # prompt for username
        usernameStr = input("SIS Username: ")
        # prompt for password using getpass to ensure password security
        passwordStr = getpass.getpass("SIS Password: ")
        if not args.ignore:
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

    # if we're in the fall semester, register for the spring
    term = (
        f"Spring {enroll_date.year + 1}"
        if 8 <= datetime.now().month <= 12
        else f"Fall {enroll_date.year}"
    )

    if args.test:
        print("Testing script...")
        # start 3 seconds after the script
        start_time = datetime.now() + timedelta(seconds=3)
        delay = timedelta(minutes=1)
        enroll_date = datetime.now() + delay
    else:
        # begin 15 minutes before registration is supposed to open
        start_time = enroll_date - timedelta(minutes=15)

    # main stuff
    mid_thread = args.threads // 2
    for i in range(args.threads):
        # Click times should "surround" 7AM on enrollment day, in intervals of 2ms apart
        offset = timedelta(milliseconds=5 * (i - mid_thread))
        e = Enroller(
            enroll_time=enroll_date + offset,
            start_time=start_time,
            term=term,
            username=usernameStr,
            password=passwordStr,
            browser=Browser,
            opts=Options,
            headless=args.headless,
            test=args.test,
            base_url=args.url,
            verbose=args.verbose,
        )
        e.thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Parse and print the results

    parser.add_argument(
        "--browser",
        "-b",
        type=str,
        choices=["chrome", "firefox"],
        default="chrome",
        help="Specify the browser to use (default chrome)",
    )
    parser.add_argument(
        "--threads",
        "-n",
        type=int,
        default=1,
        help="Number of thread instances to spawn (default 1)",
    )
    parser.add_argument(
        "--credentials",
        "-c",
        type=str,
        help="load user credentials from this file with username on first line, password on second line",
    )
    parser.add_argument(
        "--url",
        "-u",
        type=str,
        default="https://sisadmin.case.edu/psp/P92SCWR/?cmd=login",
        help="specify a different SIS base URL (defaults to the login page)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run as a headless (non-visible) browser",
    )
    parser.add_argument(
        "--ignore",
        "-i",
        action="store_true",
        help="Skip the duplicate password prompt",
    )
    parser.add_argument(
        "--test", "-t", action="store_true", help="run a test to verify functionality",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="print out more status stuff",
    )

    args = parser.parse_args()
    main(args)
