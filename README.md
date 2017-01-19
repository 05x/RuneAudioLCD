# RuneAudioLCD

RuneAudioLCD is a python script used on RuneAudio player for displaying playback information on LCD screen and controlling of player via hardware buttons and IR remote.  

This repository aim to merge the original repositoy (https://github.com/RandyCupic/RuneAudioLCD) with modded version of it called "RuneAudioLCDMod" (https://github.com/lukazgur/RuneAudioLCDMod)

## Modifications done by lukazgur on "RuneAudioLCDMod"
- code migrated to Python 3,
- implementation of direct pins connection for LCD display (I2C is already implemented in original script),
- selection of display screens with hardware button,
- control of backlight ON/OFF with hardware button.

## Modifications made here
- fix for i2c displays (parallel displays not tested after modifications)
- add GPIO namming mode option in start.py
- some cleanning

## Features
### Display features
- can be turned off (to only use buttons and/or remote)
- support for 20x4 and 16x2 displays connected via I2C
- 3 different screens for 20x4 LCD, 6 for 16x2 LCD respectively
- current song and artist info, with scrolling
- elapsed time and song duration, with listened percentage (only for local files)
- play, pause or stop icon
- shows wheter it's playing radio or file, with bitrate in kbps
- shows volume, random, repeat and single status, on change
- Ethernet and Wi-Fi IP address, if connected
- system uptime, and music play time
- current date and time, CPU temperature and RAM usage (used/total)

### Button features
- can be turned off (to only use display and/or remote)
- play/pause, volume up/down, previous, next and stop buttons
- each button can be turned on/off (possibility of using only some of listed buttons)

### IR remote features
- can be turned off (to only use display and/or buttons)
- power off and reboot options
- play, pause, volume up/down, previous, next and stop options
- repeat, single, shuffle options
- switch through different screens (display modes)
- turn on/off LCD backlight

## Requirements
- Raspberry Pi running RuneAudio (http://www.runeaudio.com/)
- 16x2 or 20x4 I2C LCD display (not neccesarry)
- up to 8 hardware push buttons (not neccessarry)
- IR receiver (not neccessarry)
- Python 3 installed
- installed and working LIRC (required for IR remote to work)
- Adafruit LCD char library installed for parallel display.
- script for IR remote which sends required strings via pipeline on button presses

## Installation
TODO : detail installation procedure (for all dependencies)

The easiest solution to run the RuneAudioLCDMod python script every time you turn on RuneAudio player is to setup a deamon
that executes python script. Bash script and service definition are included in repository.
- create a shell script such as /usr/bin/control_script.sh
- create a service file in /lib/systemd/control_script.service
- make systemd aware of your new service:
  - systemctl daemon-reload
  - systemctl enable control_script.service (if error with symbolic link -> run systemctl enable "FULLPATHTOSERVICE")
  - systemctl start control_script.service
- reboot the RPI to see script in action.

#### Useful commands
- systemctl status control_script.service
- systemctl stop control_script.service
- systemctl start control_script.service
- systemctl disable control_script.service

Services "log":
- journalctl /usr/lib/systemd/systemd -b
