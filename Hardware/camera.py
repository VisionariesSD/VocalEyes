"""!
@file camera.py

@brief
This is the script that serves as the driver for the full camera functionality as well as the picture-to-audio processing.
This is the script, uses functions from CV_algo.py in order to provide the full device functionality.
"""
## @package camera
# This namespace is used whenever referring to the camera module.

## @package picamera
# this package is used to startup the camera from code
from picamera import PiCamera

## @package RPi.GPIO 
# Import Raspberry Pi GPIO library to be used to identify and use pins within Raspberry Pi
import RPi.GPIO as GPIO 

## @package led
# This is the led.py script located within Software that was used for testing.
#import led #! used for testing

## @package CV_algo
# This is the CV_algo.py script located within Software that is imported to allow use of its various functions.
import CV_algo

## @package time
#This packaged is mostly used for button debouncing.
import time

#DEFINE BUTTONS:
## Pin 11 on Board = Capture/Start Button 
Capture_Button = 11              

## Pin 18 on Board = change language button
Lang_Change_Button = 18          

## Pin 13 on Board = Pause/Play button
Button_Pause = 13                

## Pin 15 on Board = Volume Up
Button_VolUp = 15                

## Pin 16 on Board = Volume Down
Button_VolDown = 16              

## Pin 22 on Board = Stop process
Button_Stop = 22                 

## Pin 24 = Speed change
Spd_Change = 24                  

#GLOBAL VARIABLES:
##DEFINES THE CURRENT INDEX FOR LANGUAGE IN lang_array
lang_index = 0           

##DEFINES TOTAL NO. OF LANGUAGE OPTIONS
lang_options = 3         

##DEFINES TOTAL NO. OF SPEED OPTIONS
spd_options = 3          

##DEFINES CURRENT VALUE OF SPEED FROM spd_arr
spd_ind = 1              

##ARRAY THAt DEFINES SPEED CHANGE OPTIONS
spd_arr = [0.7,1,1.3]    


#---------------------------------------------FUNCTIONS-----------------------------------------------#
#Function to change the language: (from lang_array)
def LangChange(lang_index):
    """! Changes the index of the lang_index variable for the languages array (located in CV_algo.py)

    @param lang_index   The current value for the language array index

    @return The new value of the language array index
    """
    print('Changed languages') #! USED FOR TESTING
    CV_algo.playCue('/home/pi/SoundBites/lang_change.mp3') #once the button has been pressed play audio cue for the user
    lang_index = (lang_index + 1) % lang_options #change the value of land_index
    return lang_index

#Function to change the speed: (from spd_array)
def Speed_Button(channel):
    """! Changes the value of the spd_ind variable for the spd_arr array

    @param channel  The current, if any, audio channel that is being used.
    
    """
    if (CV_algo.CheckforVLC()): #if there is currently audio being output to the user change the spd_ind
        global spd_ind
        spd_ind = (spd_ind + 1) % spd_options
        print('speed Changed') #! USED FOR TESTING
        CV_algo.SpeedChange(spd_arr[spd_ind]) #change the speed using the CV_algo function
    else:
        #Executes if VLC process not detected (i.e., image has not been processed yet)
        print('No VLC right now') #! USED FOR TESTING
        
        
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
##Initalize the camera so that we can use it for picture taking
camera = PiCamera()
time.sleep(2)
print("Start Now") #! USED FOR TESTING
CV_algo.playCue('/home/pi/SoundBites/Device_ready.mp3')

#!DEBUG LINES FOR TESTING CODE:
#led.blink()
#led.blink()

# MAIN FUNCTIONALITY: Run forever
while True:
    #When the button is pressed take a picture, save it and call the comp vision algorithm to process it.
    if GPIO.input(Capture_Button) == True:
        camera.capture("/home/pi/Pictures/input.png")
        print("Picture Captured")
        CV_algo.playCue('/home/pi/SoundBites/Picture_captured.mp3') #play audio cue to the user that the picture has been captured
        #led.blink() #!DEBUG FUNCTION
        CV_algo.CV(lang_index) #set the current language index to the CV function and call the CV function
    
    #If the language change button is clicked change the language index
    elif GPIO.input(Lang_Change_Button) == True:
        lang_index = LangChange(lang_index)
        print(CV_algo.languages[lang_index])
        time.sleep(0.5)