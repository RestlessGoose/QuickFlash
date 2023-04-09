# QuickFlash
### Simple Python tool to easily utilize flashrom via a graphical interface. 

### Only tested under MacOS!

## Screenshot
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/light.png?raw=true">
  <img alt="Read & Save option">
</picture>


Prerequisites
-------------
- CH341A programmer
- CH34xVCPDriver
- flashrom
- Python 3

Preparation
-----------
- Download and install [CH34xVCPDriver](https://github.com/WCHSoftGroup/ch34xser_macos)
- Open terminal and paste in `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`, to install [Homebrew](https://brew.sh/)
- Install flashrom: enter `brew install flashrom` into terminal after homebrew is installed.

Usage
-----
- Plug in CH341A programmer
- Run QuickFlash
- Hit "Initialize" and select chip model from dropdown menu in popup.
- Use "Autoflash", "Read & Save" or "Erase"


Credits
-------
[WCHSoftGroup](https://github.com/WCHSoftGroup) for [ch34xser_macos](https://github.com/WCHSoftGroup/ch34xser_macos)

[Flashrom](https://www.flashrom.org/Flashrom) for [flashrom](https://github.com/flashrom/flashrom)
