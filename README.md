# QuickFlash
### Simple Python tool to easily utilize flashrom via a graphical interface. 

### Disclaimer: I am not responsible for bricked devices, data loss, dead chips, thermonuclear war, or the current economic crisis caused by you using this piece of software. Please use with caution while keeping in mind that this is *alpha stage* software and is not guaranteed to have 100% stability. And also as of right now, it's been tested only on MacOS. (Windows may work but is untested so use at your own risk!)

## Screenshot
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/dark.png?raw=true">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/RestlessGoose/QuickFlash/blob/main/Extra/Screenshots/light.png?raw=true">
  <img alt="Read & Save option">
</picture>


Prerequisites
-------------
- Preferably a Mac or a hackintosh
- CH341A programmer
- CH34xVCPDriver
- flashrom
- Python 3

Preparation
-----------
1. Download and install [CH34xVCPDriver](https://github.com/WCHSoftGroup/ch34xser_macos) by following their instructions.
2. Open terminal and paste in `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`, to install [Homebrew](https://brew.sh/). Skip this step if you already have it.
3. Install flashrom: enter `brew install flashrom` into terminal after homebrew is installed.

Usage
-----
1. Plug in CH341A programmer
2. Run QuickFlash
3. Hit "Initialize" and select chip model from dropdown menu in popup.
4. Use "Autoflash", "Read & Save" or "Erase & Blank check". You do not have to hit Reset every time you want to use them.


Credits
-------
[WCHSoftGroup](https://github.com/WCHSoftGroup) for [ch34xser_macos](https://github.com/WCHSoftGroup/ch34xser_macos)

[Flashrom](https://www.flashrom.org/Flashrom) for [flashrom](https://github.com/flashrom/flashrom)
