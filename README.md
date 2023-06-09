# QuickFlash
### Python tool to easily utilize flashrom via a graphical interface. 
### Disclaimer: I am not responsible for bricked devices, data loss, dead chips, thermonuclear war, or the current economic crisis caused by you using this piece of software. Please use with caution while keeping in mind that this is *beta stage* software and is not guaranteed to have 100% stability. 
### This tool does not support Windows or Linux yet.
### Standalone version needs to be tested further. Use with caution.

## Screenshot
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/light.png?raw=true">
  <img alt="Read & Save option">
</picture>


Officially Tested on:
---------------------
| Device              | Platform           | Status           |
|---------------------|--------------------|------------------|
| Dell Latitude E6440 | MacOS Ventura 13.4 | Fully functional |


Prerequisites
-------------
- Mac or hackintosh
- CH341A programmer
- Python 3
    - Pillow
    - PyQt5
    - pyusb
- flashrom

Preparation
-----------
1. Open terminal and paste in `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`, to install [Homebrew](https://brew.sh/). Skip this step if you already have it.
2. Install flashrom: enter `brew install flashrom` into terminal after Homebrew is installed.
4. Install Python: enter `brew install python` into terminal after flashrom is installed.
5. If you want to use the Standalone version, stop at this step and head straight to Usage. If not, continue on step 6.
6. Install Pillow: enter `pip3 install Pillow` into terminal after Python is installed.
7. Install PyQt5: enter `pip3 install PyQt5` into terminal after Pillow is installed.
8. Install pyusb: enter `pip3 install pyusb` into terminal after PyQt5 is installed.

Building
--------
1. Download this repo as a Zip and extract it.
2. Right click the highlighted folder -> Services -> New Terminal at Folder
3. Make build script executable: `chmod +x build`
4. Run the build script: `./build`
5. Go inside the "App" or "App_Standalone" folder and double-click the dmg to mount it.
6. Drag QuickFlash.app to the Applications folder
7. Right click on empty space on the dmg -> Eject

Usage
-----
1. Plug in CH341A programmer
2. Run QuickFlash
3. Hit "Initialize" and select chip model on the bottom-left corner.
4. Now you can use "Flash", "Read", Erase" and "Verify".
5. If you run into issues, try re-plugging in your programmer. If nothing works, go to Tools -> Install Driver on the menubar and follow the instructions for installing CH341A drivers on your Mac.
6. In order to select a file to flash or verify, go to File -> Open on the menubar.
7. After using "Read", in order to properly save the chip contents you have read, go to File -> Save and specify a name and location.

Credits
-------
[WCHSoftGroup](https://github.com/WCHSoftGroup) for [ch34xser_macos](https://github.com/WCHSoftGroup/ch34xser_macos)

[Flashrom](https://www.flashrom.org/Flashrom) for [flashrom](https://github.com/flashrom/flashrom)
