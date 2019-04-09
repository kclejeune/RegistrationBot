#!/bin/bash

# clone the repository
git clone https://github.com/kclejeune/RegistrationBot.git

# install necessary dependencies
sudo apt install chromium-chromedriver python3 python3-pip
clear

# navigate to the directory and install requirements
cd ~/RegistrationBot
chmod +x bot.py
pip3 install -r requirements.txt
clear

echo "Installation complete. Refer to README.md for running instructions."
