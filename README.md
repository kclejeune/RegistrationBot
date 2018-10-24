# CWRU SIS Registration Bot:

Ever needed a class with one spot left? Get a bot to do it for you (if you have a mac, at least)

## The Boring Stuff:

If you're smart, you'll take my word for it that this works. Run this and your life will be magical.

```bash
curl -s https://raw.githubusercontent.com/kclejeune/RegistrationBot/master/setup.sh?token=ALM4eBzhoydr7WglKdEZVdufTLT7Iiyiks5bDfUIwA%3D%3D | sh
```
The script will prompt for an admin password once, and then clean itself up at the end. Now skip to the fun stuff.

### Manual Install (the really boring stuff):

First, clone the repository.  
```bash
git clone https://github.com/kclejeune/RegistrationBot.git
```
This script requires python 3 and chromedriver. For linux, look at the dependencies; you can figure out the rest with sudo apt. For mac, use homebrew to install these. 
To determine whether homebrew is installed, run:
```bash
which brew
```
If it's installed, you'll see something like `/usr/local/bin/brew.`
If you're on a mac and it isn't installed, do so using the following script:
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
Finally, we need to synchronize with the naval time server to match with SIS servers.  This just updates your timeserver from time.apple.com to tick.usno.navy.mil. It requires sudo to modify /usr/sbin, but it's completely safe.
```bash
sudo /usr/sbin/systemsetup -setnetworktimeserver "tick.usno.navy.mil"
sudo /usr/sbin/systemsetup -setusingnetworktime on
```
That's it for installation.  Phew.
## The Fun Stuff (kind of):
Start the script the night before (or the day of, if you're up past midnight). It'll automatically log you in the next time it's 7:00AM. 
## WARNING: YOU MUST MAKE SURE YOUR COMPUTER WILL NOT SLEEP BEFORE 7:00.  PLUG IT IN AND CHECK THE SETTINGS.
To run, use:
```bash
python3 ~/RegistrationBot/bot.py
```
DO NOT CLOSE THE TERMINAL WINDOW. Follow the instructions to enter your username, password (type carefully, you can't see the prompt for security reasons), and the semester you're registering for (i.e. registering for fall classes = f)
That's it, good luck!
