# /etc/init.d/test.py
### BEGIN INIT INFO
# Provides:          test.py
# Required-Start:    $remote_fs $syslog $network
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

from picamera import PiCamera
import time
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import led
import CV_algo

#DEFINE BUTTONS:
Capture_Button = 11
Lang_Change_Button = 18
Button_Pause = 13 # Pin 13 on Board = Pause/Play button
Button_VolUp = 15 # Pin 15 on Board = Volume Up
Button_VolDown = 16 #Pin 16 on Board = Volume Down
Button_Stop = 22 #Pin 22 on Board = Stop process
Spd_Change = 24 #Pin 24 = Speed change

#lang_index = the language text is translated to in the languages array
lang_index = 0
#audio_flag = False
spd_ind = 1
spd_arr = [0.7,1,1.3]

def LangChange(lang_index):
    print('Changed languages')
    lang_index = (lang_index + 1) % 3
    return lang_index

def Speed_Button(channel):
    global spd_ind
    spd_ind = (spd_ind + 1) % 3
    out = ""
    print('speed Changed')
#     out = subprocess.check_output(["pidof","vlc"])
    try:
        out = subprocess.check_output(["pidof","vlc"])
    except:
        print("NO VLC")
    if out != "" :
        CV_algo.SpeedChange(spd_arr[spd_ind])
        
        

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(Capture_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(Spd_Change, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(Lang_Change_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 11 to be an input pin and set initial value to be pulled low (off)


#SET ALL THE BUTTONS AS PULL DOWN
GPIO.setup(Button_Pause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_VolUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_VolDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_Stop, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#INTERRUPT HANDLER FOR pause button: 
GPIO.add_event_detect(Button_Pause, GPIO.RISING, callback= CV_algo.PlayPause, bouncetime=100)
GPIO.add_event_detect(Button_VolUp, GPIO.RISING, callback= CV_algo.VolumeUp, bouncetime=100)
GPIO.add_event_detect(Button_VolDown, GPIO.RISING, callback= CV_algo.VolumeDown, bouncetime=100)
GPIO.add_event_detect(Button_Stop, GPIO.RISING, callback= CV_algo.StopPlayback, bouncetime=100)
GPIO.add_event_detect(Spd_Change, GPIO.RISING, callback= Speed_Button, bouncetime=100)

camera = PiCamera()
time.sleep(2)

led.blink()
led.blink()

while True: # Run forever
    #When the button is pressed take a picture and call the comp vision algorithm to process it.
    if GPIO.input(Capture_Button) == True:
        camera.capture("/home/pi/Pictures/test.png")
        print("Picture Captured")
        led.blink()
        CV_algo.CV(lang_index)
              
    elif GPIO.input(Lang_Change_Button) == True:
        lang_index = LangChange(lang_index)
        print(lang_index)
        time.sleep(0.5)