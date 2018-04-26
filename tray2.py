#!/usr/bin/python

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import os
import signal
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator

import time
import threading


APPINDICATOR_ID1 = 'myappindicator1'
APPINDICATOR_ID2 = 'myappindicator2'
APPINDICATOR_ID3 = 'myappindicator3'

HEADER = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   version="1.1"
   id="svg3749"
   sodipodi:docname="icon2.svg"
   inkscape:version="0.92.2 5c3e80d, 2017-08-06">
  <metadata
     id="metadata3755">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs3753" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1762"
     inkscape:window-height="1054"
     id="namedview3751"
     showgrid="false"
     inkscape:zoom="34.52"
     inkscape:cx="16.678877"
     inkscape:cy="96.061498"
     inkscape:window-x="158"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="svg3749" />
  <text
     x="0.21737458"
     y="3.1398399"
     id="text3747"'''

FOOTER = '''</text>
</svg>'''

indicator1 = appindicator.Indicator.new(APPINDICATOR_ID1, "", appindicator.IndicatorCategory.SYSTEM_SERVICES)
indicator2 = appindicator.Indicator.new(APPINDICATOR_ID2, "", appindicator.IndicatorCategory.SYSTEM_SERVICES)
indicator3 = appindicator.Indicator.new(APPINDICATOR_ID3, "", appindicator.IndicatorCategory.SYSTEM_SERVICES)


def worker(INDICATOR,COLOR,FILE,SCALE):
      TEMPfile = open(FILE,'r')
      TEMP = TEMPfile.read(5)
      TEMPfile.close()
      TEMP = str(int(TEMP)/SCALE)
      SVG='/home/sinisa/.tray/icon'+TEMP+COLOR+'.svg'
      PNG='/home/sinisa/.tray/icon'+TEMP+COLOR+'.png'
      SVGfile = open(SVG,'w')
      SVGfile.write(HEADER + ' fill="' + COLOR + '">' + TEMP + FOOTER)
      SVGfile.close()
      if not os.path.isfile(PNG):
        os.system('inkscape -z -f ' + SVG + ' -w 16 -j -D -e ' + PNG + ' > /dev/null 2>&1')
	print('Creating ' + PNG)
#      else:
#        print(PNG + ' exists.')
      INDICATOR.set_icon_full(PNG,TEMP)



def loop1():
    while True:
      worker(indicator1,'red','/sys/devices/platform/coretemp.0/hwmon/hwmon1/temp1_input',1000)
      time.sleep(5)

def loop2():
    while True:
      worker(indicator2,'green','/sys/devices/platform/coretemp.0/hwmon/hwmon1/temp2_input',1000)
      time.sleep(5)

def loop3():
    while True:
      worker(indicator3,'blue','/sys/devices/LNXSYSTM:00/LNXSYBUS:00/PNP0C0A:00/power_supply/BAT1/capacity',1)
      time.sleep(5)



def main():
    ROOT=os.getenv("HOME") + '/.tray/'
    if not os.path.exists(ROOT):
      os.mkdir(ROOT)

# izgleda da ne mogu da se naprave vise od 3 indikatora ?!?
    indicator1.set_icon_theme_path("/home/sinisa/.tray/")
    indicator1.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator1.set_menu(build_menu(1))
    
    indicator2.set_icon_theme_path("/home/sinisa/.tray/")
    indicator2.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator2.set_menu(build_menu(2))

    indicator3.set_icon_theme_path("/home/sinisa.tray/")
    indicator3.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator3.set_menu(build_menu(3))


    gui_thread1 = threading.Thread(target=loop1)
    gui_thread1.start()
    gui_thread2 = threading.Thread(target=loop2)
    gui_thread2.start()
    gui_thread3 = threading.Thread(target=loop3)
    gui_thread3.start()


    gtk.main()



def build_menu(X):
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit'+str(X))
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

main()


