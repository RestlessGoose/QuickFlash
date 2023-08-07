#!/bin/bash

mkdir bin
sudo rm -rf build/ dist/
sudo python3 setup.py py2app
wait
sudo mv "dist/QuickFlash Beta.app" "bin/QuickFlash Beta.app"

app_file="bin/QuickFlash Beta.app"
dmg_file="bin/QuickFlash-Beta-v0_6_.dmg"
alias_name="QuickFlash Beta"
sudo ln -s "/Applications" "bin/"
sudo hdiutil create -volname "$alias_name" -fs HFS+ -srcfolder "bin/" "$dmg_file"
wait
sudo hdiutil attach "$dmg_file"
wait
sudo hdiutil convert "$dmg_file" -format UDZO -o "bin/QuickFlash-Beta-v0_6_0.dmg"
wait
sudo hdiutil detach "/Volumes/QuickFlash Beta"
sudo rm -rf "bin/QuickFlash-Beta-v0_6_.dmg"
sudo rm -rf build/ dist/ bin/Applications