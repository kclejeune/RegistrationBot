#!/bin/bash

# check if homebrew is installed and install if not
if [[ ! command -v brew > /dev/null ]]; then
    echo "Installing Homebrew"
    # run the installer from https://brew.sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # handle the m1 case
    if [[ -d /opt/homebrew ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
fi

if [[ ! command -v nix > /dev/null ]]; then
    echo "Installing Nix"
    # run the nix installer from https://nixos.org
    sh <(curl -L https://nixos.org/nix/install) --daemon --darwin-use-unencrypted-nix-store-volume
fi

# install browsers
brew install firefox

# change time server to match SIS
sudo /usr/sbin/systemsetup -setnetworktimeserver "tick.usno.navy.mil"
sudo /usr/sbin/systemsetup -setusingnetworktime on

echo "Installation complete. Refer to README.md for running instructions."
