# check if homebrew is installed and install if not
if [ ! -e /usr/local/bin/brew ]; then
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

# clone the repository
git clone https://github.com/kclejeune/RegistrationBot.git

# install necessary dependencies
brew cask install chromedriver
brew install python

# navigate to the directory and install requirements
cd RegistrationBot
pip3 install -r requirements.txt
clear
echo "Installation complete. Refer to README.md for running instructions."