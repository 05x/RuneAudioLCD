#########  LCD DISPLAY + BUTTONS FOR RUNE AUDIO  #########
# Written by: Randy Cupic (XploD)                        #
# Contact: randy2841@hotmail.com                         #
# Modified by: Luka Žgur								 #
# Contact: luka.zgur2@gmail.com							 #
# Schematic, details and tutorial: /                     #
##########################################################

import RPi.GPIO as GPIO
import mpd_client, ir_remote, time, buttons

#########  MPD PARAMETERS  ##############
# Only if you know what you're doing!
HOST = 'localhost'
PORT = '6600'
PASSWORD = False
CON_ID = {'host':HOST, 'port':PORT}
#########################################


############## GPIO numbering mode ######################################################
# Here you can specify the pin numbering mode for lcd and buttons                       #
# There is two pin numbering mode avalaible:                                            #
#  - GPIO.BOARD : Pin number is the same as pin number on board                         #
#  - GPIO.BCM   : BCM pin numbering (take a look on http://pinout.xyz/ for reference)   #

GPIO_NUMBERING_MODE = GPIO.BOARD

#########################################################################################

################### LCD DISPLAY  ########################################################
# Here you can specify your LCD settings and pins   									#
# Where your LCD is connected              	        									#
# Or connect it to these default pins  													#

# If you want to use LCD display, put to True, otherwise put to False
LCD_ENABLE = True

# This program supports I2C and parallel connection for display
# Choose between I2C and parallel: 0 - for I2C, 1 - for parallel
DISPLAY_TYPE = 0

# Pins for parallel display connection
LCD_RS = 37
LCD_EN = 33
LCD_D4 = 29
LCD_D5 = 31
LCD_D6 = 32
LCD_D7 = 38
LCD_BL = 36

# Specify I2C display address (usually 0x27)
I2C_DISPLAY_ADDRESS = 0X38

# This program generates LCD output dynamically
# Which means that it support both 20x4 and 16x2 LCDs
# Specify LCD size (for example 20x4 or 16x2 LCD
LCD_COLUMNS = 16
LCD_ROWS = 2

# Specify scrolling period (for artist and title) in SECONDS
# WARNING: By decreasing scrolling_period, CPU usage increases fast
SCROLLING_PERIOD = 0.3

# When the song changes, how much time will pass before scrolling starts, in SECONDS
SCROLLING_START = 1

# If you don't want to scroll web radio station name, put to false
WEBRADIO_SCROLL = True

# How much the volume/shuffle/repeat/single status screen will last before
# returning to normal display, IN seconds
TEMPORARY_SCREEN_PERIOD = 3

# DYNAMIC LCD BACKLIGHT - enable this if you want the LCD backlight to go off
# After the music has been paused or stopped for a specific period
# To disable it, put timeout to 0, any other positive value will enable it
BACKLIGHT_TIMEOUT = 5

#########################################################################################

################### BUTTONS  ############################################################
# Here you can specify your button pins        											#
# Where your buttons are connected              										#
# Or connect them using these default pins      										#
# BUTTONS ARE PULLED UP, so connect buttons to GROUND 									#

# If you want to use buttons, put to True, otherwise put to False
BUTTONS_ENABLE = True

# Change the pin number, to specify where you connected them
# If you don't want to use one of the buttons, put False as values
# For example, PLAY_BUTTON = False
PLAY_BUTTON = 11
NEXT_BUTTON = 13
PREV_BUTTON = 15
VDN_BUTTON = False
VUP_BUTTON = False
STOP_BUTTON = 16
MODE_BUTTON = 18
PAUSE_BUTTON = 7

# Specify time to ignore button after press (in miliseconds)
BOUNCE_TIME = 200

#########################################################################################

############## IR REMOTE ############################################
# Remote is used to switch between different screens
# And to turn on/off LCD backlight
# It uses LIRC for this so you need to install and configure LIRC
# It receives command through pipeline so in your LIRC for example:
# begin
# prog = irexec
# button = KEY_MUTE
# config = echo "KEY_MUTE" > /tmp/irpipe
# repeat = 0
# end

# If you want to use remote, put to True, otherwise put to False
# WARNING: Don't enable it if you don't have working LIRC!!!
REMOTE_ENABLE = False

# Specify pipeline name (in upper example this is "/tmp/irpipe"
IR_PIPELINE = '/tmp/irpipe'
#####################################################################

# Initialize MPD client
mpdcl = mpd_client.mpd_client(CON_ID, PASSWORD)

# Start it
mpdcl.start()

# Set GPIO numbering mode
GPIO.setmode(GPIO_NUMBERING_MODE)

# If enabled, initialize display instance
if LCD_ENABLE:
	# I2C display is chosen
	if (DISPLAY_TYPE == 0):
		import i2c_display
		display = i2c_display.i2c_display(I2C_DISPLAY_ADDRESS, LCD_ROWS, LCD_COLUMNS, TEMPORARY_SCREEN_PERIOD, SCROLLING_PERIOD, None)
	elif(DISPLAY_TYPE == 1):
		lcd_pins = [
			LCD_RS,
			LCD_EN,
			LCD_D4,
			LCD_D5,
			LCD_D6,
			LCD_D7,
			LCD_BL
		]
		import parallel_display
		display = parallel_display.parallel_display(I2C_DISPLAY_ADDRESS,LCD_ROWS, LCD_COLUMNS, TEMPORARY_SCREEN_PERIOD, SCROLLING_PERIOD, lcd_pins)

	# Let MPD and display know for each other
	display.register(mpdcl)
	mpdcl.register(display)

	# Start display thread
	display.start()

# If remote is enabled, initialize it and start it's thread
if REMOTE_ENABLE:
	remote = ir_remote.remote(IR_PIPELINE)
	remote.start()

	# Let it know about display, if display is enabled
	if LCD_ENABLE:
		remote.register_display(display)

# If buttons are enabled, initialize them
if BUTTONS_ENABLE:
	button_pins = {
		'PLAY_BUTTON': PLAY_BUTTON,
		'NEXT_BUTTON': NEXT_BUTTON,
		'PREV_BUTTON': PREV_BUTTON,
		'VDN_BUTTON': VDN_BUTTON,
		'VUP_BUTTON': VUP_BUTTON,
		'STOP_BUTTON': STOP_BUTTON,
		'MODE_BUTTON': MODE_BUTTON,
		'PAUSE_BUTTON': PAUSE_BUTTON
	}

	btn = buttons.buttons(button_pins, BOUNCE_TIME)

	if LCD_ENABLE:
		btn.register_display(display)
	
	# Register MPD client
	btn.register(mpdcl)

# Wait for MPD client thread to finish
mpdcl.join()

# If LCD is enabled, wait for it's thread to finish
if LCD_ENABLE:
	display.join()
	
# If remote is enabled, wait for it's thread to finish
if REMOTE_ENABLE:
	remote.join()
	
# If buttons are enabled, wait for it's thread to finish
if BUTTONS_ENABLE:
	btn.join()
