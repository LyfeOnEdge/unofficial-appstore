# unofficial-appstore

![Unofficial Appstore](https://i.imgur.com/QrzIkjk.png)


[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]() [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/unofficial-appstore/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/unofficial-appstore.svg)]()

# About
A desktop gui for the Homebrew Appstore written in python.

Uses the switchbru/4TU team's site as a backend for image and package downloads.

One of the main goals of this app is to provide a homebrew management tool that doesn't require the switch to access the internet. Especially useful for people who always keep their switch in airplane mode. 

#### Download:
https://github.com/LyfeOnEdge/unofficial-appstore/releases

#### Working Stuff:
 - Dynamic Search
 - Categories
 - Downloading directly from the switchbru/4tu site
 - Tracking with the appstore
 - Opening project pages
 - Threaded operations mean the app no longer becomes unresponsive with big downloads
 - Self-updater
 - Buttons load dynamically so only what you need to see loads, this reduces startup time to only a few seconds. 

#### Future plans:
 - Add sorting to lists
 - Improve look and feel with google's material design
 - Add "esc" and "backspace" as hotkeys to exit the details window
 - Direct memloader integration (SD only) for installation directly over USB. 
 
***

# How to run:
#### Windows:
- Extract unofficial-appstore.zip
- Install [python](https://www.python.org/downloads/release/python-373/)
    - __Make sure to keep the tcl/tk checkbox ticked if doing a custom installation__
    - You *must* restart your pc after installing python for the first time.
- Open a command prompt, type `pip install Pillow`
    - This installs a required image library [Pillow](https://pypi.org/project/Pillow/2.2.1/)
- __To run the app: double-click start_appstore.bat__

#### Macintosh:
- Extract unofficial-appstore.zip
- Mac users may already have a compatible version of python installed, try double-clicking unofficial-appstore.py
- If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)
- __To run the app: double-click unofficial-appstore.py__

#### Linux:
- Extract unofficial-appstore.zip
- Navigate to the directory in a terminal
- Type `python3 unofficial-appstore.py`
- If you are missing dependencies do the following:
    - sudo apt install python3 python3-pip python3-tk python3-pil python3-pil.imagetk
- If you don't know how to do this you should probably be using Windows ;D
- __To run the app: `python3 unofficial-appstore.py`__

# How to use:
 - Connect your SD card to your computer
 - Start the app
 - Click the "Select SD root" button
 - A file dialog should appear, select the root of your SD card
 - Select an app you'd like to see more about
 - Click install to have the app properly installed on to the SD card
 - When you're done, unmount your SD card, put it in your homebrewed Nintendo Switch, and reboot.

### Troubleshooting:
 - If you are getting errors about tkinter or pillow look above at the setup instructions for your OS
 - Image download errors are to be expected, please do not report them.

#### Known bugs:
##### Linux:
 -  the highlighted text for the selected category is black in the listbox instead of white

***

# Credits:
 - vgmoose, pwscind, and the 4TU team
 - sudotoph, guts for testing

#### Want to contribute? Have ideas? Questions? Great!
You can find me here: 
**[4TU](https://discord.gg/5AnDNr)**


