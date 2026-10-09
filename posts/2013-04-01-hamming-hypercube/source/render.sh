#!/bin/zsh
# render.sh name width height  -> name.png at 2x
f=$1; w=$2; h=$3
print "<html><body style='margin:0'>$(cat $f.svg)</body></html>" >| $f.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=$w,$h --screenshot=$PWD/$f.png file://$PWD/$f.html >/dev/null 2>&1
ls -la $f.png
