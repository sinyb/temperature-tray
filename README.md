# temperature-tray
display up to 3 temperatures/other important values (like battery charge) in tray using python and appindicator lib, updated every 5 seconds

Requirements:
- python 2
- python-gtk
- libappindicator
- python2-appindicator
- inkscape (to create any missing numbers)

Install:
- git pull https://github.com/sinyb/temperature-tray temperature-tray/
- copy .tray directory to your home dir
- modify tray2.py:
  - find "/home/sinisa" and replace that with your home dir
  - find your sensors in "/sys/devices/" and change where appropriate 
     - I used "find /sys -name temp*", then picked 2 of them
     - also used "find /sys -name BAT*", then found which file contains charge info
  - also change scaling factor on the same lines
  - (optional) copy tray2.py into some bin/ directory (like: /usr/local/bin)
  - make tray2.py auto-start in your desktop config (for KDE: System Settings -> Startup&Shutdown -> Autostart -> Add Program)

Log off then log on again

Chanegelog:
0.1 initial release, most of the config must be done manualy inside program


