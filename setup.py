"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['assets/QuickFlash.py']
DATA_FILES = ['assets/ApplicationStub.icns', 'assets/1.png', 'assets/flashrom', '/usr/local/opt/libusb/lib/libusb-1.0.dylib', '/usr/local/opt/libusb/lib/libusb-1.0.0.dylib']
OPTIONS = {
    'iconfile': 'assets/ApplicationStub.icns', 
    'packages': ['usb'], 
    'includes': ['usb'],
    'plist': {
        'CFBundleShortVersionString': '0.6.0',
        'CFBundleVersion': '0.6.0',
        'NSHumanReadableCopyright': '© Copyright 2023 RestlessGoose',
        'CFBundleName': 'QuickFlash Beta',
        'CFBundleDisplayName': 'QuickFlash Beta'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', 'pyusb'],
)
