"""!
@file led.py

@brief
This is the code used during the testing phase of the VocalEyes product which involved using an led to check where the process is at the time.
"""

## @package RPi.GPIO 
# Import Raspberry Pi GPIO library to be used to identify and use pins within Raspberry Pi
import RPi.GPIO as GPIO

## @package time
#This packaged is mostly used for button debouncing.
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(40, GPIO.OUT)

def blink():
    """! 
    This signifies the led that we used to blink.
    """
    GPIO.output(40, True)
    time.sleep(1)
    GPIO.output(40, False)
