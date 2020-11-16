# Registration Bot

Ever needed a class with one spot left? Get a bot to do it for you (if you're using \*NIX, at least)

## Dependencies

Clone the repository and navigate to its directory.

```bash
git clone https://github.com/kclejeune/RegistrationBot.git
cd RegistrationBot
```

This project uses Nix to manage dependencies. You can install it on macOS with

```
sh <(curl -L https://nixos.org/nix/install) --daemon --darwin-use-unencrypted-nix-store-volume
```

or on Linux with

```
sh <(curl -L https://nixos.org/nix/install) --daemon
```

### Manual Install Instructions

You can alternatively install these dependencies to run the project:
- `python3`
- `selenium`
- `chromedriver`
- `geckodriver`

all further instructions will assume that Nix is installed.
## Using the Script

**WARNING: YOU MUST MAKE SURE YOUR COMPUTER WILL NOT SLEEP BEFORE 7:00.  PLUG IT IN AND CHECK THE SETTINGS**

It is *highly* recommended to use a utility to prevent your computer from sleeping.
I'd recommend running something like `brew cask install keepingyouawake` or `sudo apt install caffeine`, which will allow you to 'caffeinate' your computer overnight.

To run the script, navigate to the RegistrationBot directory and run:

```bash
nix-shell --run "python3 bot.py --threads 8"
```

Follow the instructions to enter your username and password (type carefully, you can't see the prompt for security reasons).
That's it, good luck!
