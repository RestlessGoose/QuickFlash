# QuickFlash
### Python tool to easily utilize flashrom via a graphical interface. 
### Disclaimer: I am not responsible for bricked devices, data loss, dead chips, thermonuclear war, or the current economic crisis caused by you using this piece of software. Please use with caution while keeping in mind that this is *beta stage* software and is not guaranteed to have 100% stability. 
### This tool does not support Windows or Linux yet.

## Screenshot
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/light.png?raw=true">
  <img alt="Screenshots">
</picture>


Officially Tested on:
---------------------
| Device              | Platform              | Status           |
|---------------------|-----------------------|------------------|
| Dell Latitude E6440 | MacOS Ventura 13.4    | Fully functional |
| ASUS P8B75-V PC     | MacOS Monterey 12.6.8 | Fully functional |


Runtime dependencies
---------------------
* `tcl-tk` updated to version 8.6.13_4
    * If you built this app from source then you can use your current `tcl-tk` version

Build dependencies
------------------
* Homebrew (in order to install Python)
* Python
    * PyUSB
    * py2app
    * pyobjc
* flashrom (along with its own dependencies)

Building
--------
1. Download this repo as a Zip and extract it.
2. Right click the highlighted folder -> Services -> New Terminal at Folder
3. If you haven't already, install [Homebrew](https://brew.sh/)
4. Install Python: `brew install python`
5. Install flashrom: `brew install flashrom`
6. Install PyUSB: `pip3 install pyusb`
7. Install pyobjc: `pip3 install pyobjc`
8. Install py2app: `pip3 install py2app`
9. Make build script executable: `chmod +x build.sh`
10. Run the build script: `./build.sh`
11. Go inside the "bin" folder and double-click the dmg to mount it.
12. Drag QuickFlash Beta.app to the Applications folder
13. Right click on empty space on the dmg -> Eject

Usage
-----
1. Plug in CH341A programmer
2. Run QuickFlash
3. Hit "Initialize" and select chip model on the bottom-left corner.
4. Now you can use "Flash", "Read", Erase" and "Verify".
* If you run into issues, try re-plugging in your programmer and hitting Initialize again.
* In order to select a file to flash or verify, go to File -> Open on the menubar.
* After using "Read", in order to properly save the chip contents you have read, go to File -> Save and specify a name and location.

Credits
-------
* [Flashrom](https://www.flashrom.org/Flashrom) for [flashrom](https://github.com/flashrom/flashrom)
* [py2app](https://github.com/ronaldoussoren/py2app)
