import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

GPIO.setup(40, GPIO.OUT)

def blink():
    GPIO.output(40, True)
    time.sleep(1)
    GPIO.output(40, False)
