from picamera import PiCamera
import time
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 5 to be an input pin and set initial value to be pulled low (off)
camera = PiCamera()
time.sleep(2)

while True: # Run forever
    if GPIO.input(11) == GPIO.HIGH:
        #print("Button was pushed!")
        time.sleep(1)
        camera.capture("/home/pi/Pictures/test.jpg")
        print("Picture Captured")
        subprocess.call('python /home/pi/CV_algo.py', shell = True)