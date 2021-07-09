from picamera import PiCamera
import time
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import led

#DEFINE BUTTONS:
Capture_Button = 11

#CAMERA_CLICK BUTTON AND CAMERA INITIALIZATION:
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)
camera = PiCamera()
time.sleep(2)


#BUTTON Configutration:
# Gnd-----Res-------Button-------Pin11

while True: # Run forever
    #When the button is pressed take a picture and call the comp vision algorithm to process it.
    if GPIO.input(Capture_Button) == True:
        #print("Button was pushed!")
        time.sleep(0.5)
        camera.capture("/home/pi/Pictures/test.jpg")
        print("Picture Captured")
        led.blink()
        subprocess.call('python3 /home/pi/CV_algo.py', shell = True)