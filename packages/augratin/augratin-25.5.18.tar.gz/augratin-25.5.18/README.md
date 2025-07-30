# AuGratin

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)  [![Python: 3.8+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)  [![Made With:PyQt5](https://img.shields.io/badge/Made%20with-PyQt5-red)](https://pypi.org/project/PyQt5/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/augratin)

![logo](https://github.com/mbridak/augratin/raw/master/augratin/data/k6gte.augratin.svg)

- [AuGratin](#augratin)
  - [Why AuGratin](#why-augratin)
  - [What is AuGratin](#what-is-augratin)
  - [Recent changes](#recent-changes)
  - [Installing, Updating, Running, Removing](#installing-updating-running-removing)
  - [Features](#features)
  - [What to do if your map is blank](#what-to-do-if-your-map-is-blank)
  - [What to do if omnirig fails to connect](#what-to-do-if-omnirig-fails-to-connect)
  - [CAT control and things](#cat-control-and-things)

## Why AuGratin

AuGratin is an extension to an earlier program called POTAto. And since it's made from POTAto, I called it AuGratin.

## What is AuGratin

To answer this you must know what [POTA](https://parksontheair.com) is.
[POTA](https://parksontheair.com) is Parks On The Air.
A year round activity of many amateur radio operators or HAMS.
The Activator, will set up a radio station in a state/national park and make as many contacts as they can.
Other Radio Amateurs also known as Hunters or Chasers, will seek out and try to contact as many Activators as they can.

AuGratin allows A [POTA](https://parksontheair.com) Hunter to easily log contacts with Activators.
It pulls latest [POTA](https://parksontheair.com) spots. Displays them in a compact interface.
Once a spot is clicked on AuGratin will talk to either rigctld, flrig, or OmniRig to change the radio to the correct
frequency and mode. It will pre-populate All the fields needed for logging the contact.
All contacts are stored in an ADIF file in your home directory,
which you can then import into your normal logging program. It also broadcasts QSOs via standard UDP protocol which is reconized by most major loggers for automatic import.

![screenshot](https://github.com/mbridak/augratin/raw/master/pic/screenshot.png)

## Recent changes

- [25-5-18] Updated Omnirig CAT to sync both VFOs to use diversity tuning. Setting Mode of the SUB reciever is acheived through an omnirig hack of the .ini file. Removed use of depricated pkgutil.getloader(). Migrate from Qt5 to Qt6.
- [23-12-22] Added UDP broadcast of ADIF info for popular logging software integration (tested with HRD)
- [23-5-26] Added Ubuntu dark mode if adwaita-qt is installed.
- [23-5-18] Fix crashes related to if flrig running w/ no radio, or flrig closes. Add dialog message window to initial startup if CAT control failed. For some reason I was missing the 17m band. Added back band selector for those who have CAT.
- [23-5-17] Reworked bandmap display. Spots with QRT in comment are now muted. Center bandmap on RX freq when changing vfo or zooming display. Provided Non CAT control users to change bands.
- [23-5-15] Start big code changes to impliment better bandmap.
- [23-3-28] Merged in changes from @barryshaffer KK7JXG to add support for Omnirig on windows.
- [23-3-7] Reduced network timeout for spot pulls from 15 to 5 seconds. Safer dictionary key access.
- [23-2-17] Repackaged for PyPi and pip install

## Installing, Updating, Running, Removing

```bash
# install
pip install augratin

# update
pip install -U augratin

# remove
pip uninstall augratin

# running
augratin
```

## Features

- UDP broadcasting of QSOs for integration into logging software
- Shows spots on a band map
- You can filter spots by mode.
- Pulls in park and activator information.
- Clicked spots, tune your radio with flrig, rigctld or OmniRig to the activator and sets the mode automatically.
- ~~Double clicked spots adds Activator to a persistent watchlist.~~
- Displays bearing to contact.

When you press the "Log it" button the adif information is appended to `POTA_Contacts.adi` in your home folder.

## What to do if your map is blank

Not sure why, but the map may not work if you let pip install PyQt5 and PyQtWebEngine automatically. If your map is blank, try:

```bash
pip uninstall PyQt5
pip uninstall PyQtWebEngine
```

Then install them through your package manager.

```bash
#fedora
sudo dnf install python3-qt5 python3-qt5-webengine

#ubuntu
sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine
```

## What to do if omnirig fails to connect

On occasion the win32 cache files can get corrupted preventing connection to omnirig. If omnirig was previously working but the continues to fail try erasing the cache files located here: C:\Users\username*\AppData\Local\Temp\gen_py\python version*

## CAT control and things

If no command line options are given, the program will check if either flrig, rigctld or OmniRig are running on the computer. It will setup CAT control to whichever it finds first.

You can force it to use either with commandline options.

`-r` will force rigctld with default host:port of localhost:4532.

`-f` will force flrig with default host:port of localhost:12345.

`-2` will force 'Rig2' with OmniRig.

`-s SERVER:PORT` will specify a non-standard host and port.

`-u UDP_SERVER:PORT` will specify a desired UDP server and port - Default is localhost:2333.
