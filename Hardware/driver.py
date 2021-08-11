import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import subprocess

Capture_Button = 11

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    #When the button is pressed take a picture and call the comp vision algorithm to process it.
    if GPIO.input(Capture_Button) == True:
        GPIO.cleanup()
        #subprocess.run('cvlc /home/pi/SoundBites/Device_ready.mp3', shell = True) #PLAY IN VLC
        #subprocess.run('killall vlc', shell = True) #first terminate all vlc outputs
        subprocess.run("python3 test.py", shell=True)