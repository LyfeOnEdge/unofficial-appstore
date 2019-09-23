# unofficial-appstore

![Unofficial Appstore](https://i.imgur.com/bN2NItf.png)


[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)]() [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/unofficial-appstore/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/unofficial-appstore.svg)]()

# About
A desktop gui for the Homebrew Appstore written in python.

Uses the switchbru/4TU team's site as a backend for image and package downloads.

One of the main goals of this app is to provide a homebrew management tool that doesn't require the switch to access the internet.

##### Working Stuff:
 - Dynamic Search
 - Categories
 - Downloading directly from the switchbru/4tu site
 - Tracking with the appstore
 - Opening project pages
 - Threaded operations mean the app no longer becomes unresponsive with big downloads
 - Self-updater

##### Future plans:
 - Direct memloader integration (SD only) for installation directly over usb 

# How to run:
##### Windows:
- Extract unofficial-appstore.zip
- Install [python](https://www.python.org/downloads/release/python-373/)
- Double-click start_appstore.bat

##### Macintosh:
- Extract unofficial-appstore.zip
- Mac users may already have a compatible version of python installed, try double-clicking unofficial-appstore.py
--If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)

##### Linux:
- Extract unofficial-appstore.zip
- Navigate to the directory in a terminal
- Type "python unofficial-appstore.py"
  - If you are missing dependencies do the following:
  - sudo apt-get install python3 python3-pip python3-tk
- If you don't know how to do this you should probably be using Windows ;D

# How to use:
 - Connect your SD card to your computer
 - Start the app
 - Click the "Select SD root" button
 - A file dialog should appear, select the root of your SD card
 - Select an app you'd like to see more about
 - Click install to have the app properly installed on to the SD card
 - When you're done, unmount your SD card, put it in your SD card, and reboot.

##### Want to contribute? Have ideas? Questions? Great!
You can find me here: 
**[4TU](https://discord.gg/5AnDNr)**
