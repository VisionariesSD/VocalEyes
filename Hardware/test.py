from picamera import PiCamera
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
#import led
import CV_algo
import time
import subprocess

#DEFINE BUTTONS:
Capture_Button = 11              #Pin 11 on Board = Capture/Start Button
Lang_Change_Button = 18          #Pin 18 on Board = change language button
Button_Pause = 13                #Pin 13 on Board = Pause/Play button
Button_VolUp = 15                #Pin 15 on Board = Volume Up
Button_VolDown = 16              #Pin 16 on Board = Volume Down
Button_Stop = 22                 #Pin 22 on Board = Stop process
Spd_Change = 24                  #Pin 24 = Speed change

#GLOBAL VARIABLES:
lang_index = 0           #DEFINES THE CURRENT INDEX FOR LANGUAGE IN lang_array
lang_options = 3         #DEFINES TOTAL NO. OF LANGUAGE OPTIONS
spd_options = 3          #DEFINES TOTAL NO. OF SPEED OPTIONS
spd_ind = 1              #DEFINES CURRENT VALUE OF SPEED FROM spd_arr
spd_arr = [0.7,1,1.3]    #ARRAY THAt DEFINES SPEED CHANGE OPTIONS


#---------------------------------------------FUNCTIONS-----------------------------------------------#
#Function to change the language: (from lang_array)
def LangChange(lang_index):
    print('Changed languages')
    CV_algo.playCue('/home/pi/SoundBites/lang_change.mp3')
    lang_index = (lang_index + 1) % lang_options
    return lang_index

#Function to change the speed: (from spd_array)
def Speed_Button(channel):
    if (CV_algo.CheckforVLC()):
        global spd_ind
        spd_ind = (spd_ind + 1) % spd_options
        print('speed Changed')
        CV_algo.SpeedChange(spd_arr[spd_ind])
    else:
        #Executes if VLC process not detected (i.e., image has not been processed yet)
        print('No VLC right now')
        
        
#----------------------------PUSHBUTTON CONFIGURATION----------------------------------------#
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


#-----------------------------INTERRUPT HANDLER CONFIGURATION--------------------------------#
GPIO.add_event_detect(Button_Pause, GPIO.RISING, callback= CV_algo.PlayPause, bouncetime=1500)
GPIO.add_event_detect(Button_VolUp, GPIO.RISING, callback= CV_algo.VolumeUp, bouncetime=1500)
GPIO.add_event_detect(Button_VolDown, GPIO.RISING, callback= CV_algo.VolumeDown, bouncetime=1500)
GPIO.add_event_detect(Button_Stop, GPIO.RISING, callback= CV_algo.StopPlayback, bouncetime=1500)
GPIO.add_event_detect(Spd_Change, GPIO.RISING, callback= Speed_Button, bouncetime=1500)


#---------------------------------------CAMERA SETUP---------------------------------------------------#
camera = PiCamera()
time.sleep(2)
print("Start Now")
CV_algo.playCue('/home/pi/SoundBites/Device_ready.mp3')

#DEBUG LINES FOR TESTING CODE:
#led.blink()
#led.blink()

# MAIN FUNCTIONALITY: Run forever
while True:
    #When the button is pressed take a picture, save it and call the comp vision algorithm to process it.
    if GPIO.input(Capture_Button) == True:
        camera.capture("/home/pi/Pictures/test.png")
        print("Picture Captured")
        CV_algo.playCue('/home/pi/SoundBites/Picture_captured.mp3')
        #led.blink()              #DEBUG FUNCTION
        CV_algo.CV(lang_index)
    
    #If the language change button is clicked change the language index
    elif GPIO.input(Lang_Change_Button) == True:
        lang_index = LangChange(lang_index)
        print(CV_algo.languages[lang_index])
        time.sleep(0.5)