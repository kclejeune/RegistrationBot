# CWRU SIS Registration Bot:

Ever needed a class with one spot left? Get a bot to do it for you (if you have a mac, at least)

## Installation Scripts: You can trust me, I promise

The script will prompt for an admin password once, and then clean itself up at the end. Now skip to the fun stuff.

### Linux:
```bash
sudo apt install curl
curl -s https://raw.githubusercontent.com/kclejeune/RegistrationBot/master/setup.sh?token=ALM4eInbVfPxflCvkGt5zwkoY9eGwHzfks5b-4F7wA%3D%3D | sh
```

### MacOS (currently unsupported):

```bash
curl -s https://raw.githubusercontent.com/kclejeune/RegistrationBot/master/setup.sh?token=ALM4eInbVfPxflCvkGt5zwkoY9eGwHzfks5b-4F7wA%3D%3D | bash
```
## Manual Installation

First, clone the repository.  
```bash
git clone https://github.com/kclejeune/RegistrationBot.git
```
This script requires python 3 and chromedriver. For linux, install them with 
```bash
sudo apt install python3 python3-pip chromium-chromedriver
```

For mac, use homebrew to install these. To check if you have it and install if not, run
```bash
if [ ! -e /usr/local/bin/brew ]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi
```
If it's installed, you'll see something like `/usr/local/bin/brew`
If you don't see this, run the installation script:
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Now we can install chromedriver and python, and install some additional requirements.
```bash
brew cask install chromedriver
brew install python
cd RegistrationBot
pip3 install -r requirements.txt
```
Finally, we need to synchronize with the naval time server to match with SIS servers.  This just updates your timeserver from time.apple.com to tick.usno.navy.mil. It requires sudo to modify /usr/sbin, but it's considered safe.
```bash
sudo /usr/sbin/systemsetup -setnetworktimeserver "tick.usno.navy.mil"
sudo /usr/sbin/systemsetup -setusingnetworktime on
```
That's it for installation.  Phew.

## The Fun Stuff (kind of):

Start the script the night before (or the day of, if you're up past midnight). It'll automatically log you in the next time it's 7:00AM. 

## WARNING: YOU MUST MAKE SURE YOUR COMPUTER WILL NOT SLEEP BEFORE 7:00.  PLUG IT IN AND CHECK THE SETTINGS. 

Fair warning, it is *highly* recommended to use a utility to prevent your computer from sleeping. 
I'd recommend running `brew cask install keepingyouawake`, which will allow you to 'caffeinate' your computer overnight.

To run the script, use:
```bash
python3 ~/RegistrationBot/bot.py
```
Follow the instructions to enter your username, password (type carefully, you can't see the prompt for security reasons), and the semester you're registering for (i.e. registering for fall classes = f)
That's it, good luck!
