"""!
@mainpage VocalEyes Assist for the Blind

@section Overview 
VocalEyes will be a device/wearable that will include a camera and a speaker module. 
The major goal of the VocalEyes is to help the visually impaired. 
The visual eyes will recognize an object that the user directs it at (via the camera module) and will output audio information (via the speaker module) about what the object is. 
(eg: in case of text it will readout the text).

@section Working Directories
For working directories we have the following included:

(For more detailed explanations for these working directories, either click on the link, if available, or use the Files section above.)
- Documentation: This folder provides all files necessary for documentation used with doxygen. (This is not included within the Files section as it is unnecessary to code documentation.)
    - html
        - This includes all files for html output of documentation.
    - latex
        - This includes all files for latex output of documentation.
- Hardware: This folder provides all files necessary regarding to hardware functionality.
    - camera.py
    - driver.py
    - led.py
- Software: This folder provides all files necessary regarding to software functionality
    - convert_to_speech.py
    - CV_algo.py
- SoundBites: This includes all Sound Files that are used within this project
    - Device_ready.mp3 
    - lang_change.mp3 
    - No_VLC.mp3 
    - Picture_captured.mp3 
    - speech_output.mp3 
    - Stopped.mp3 

@file Device_ready.mp3 @brief This tells that the device is ready and is used during startup.
@file lang_change.mp3 @brief This tells that the user has changed languages.
@file No_VLC.mp3 @brief This tells the user that there is no VLC detected at that there is no audio currently being output.
@file Picture_captured.mp3 @brief This tells the user that they have captured a picture.
@file speech_output.mp3 @brief This is the file that is used for the speech output from the input picture.
@file Stopped.mp3 @brief This tells the user that the audio is stopped and that they must take another picture to continue.

@file driver.py

@brief
This is the script that serves as the main driver for the rest of the functions and code. 
This is the script, as well, that will be run off of boot as to not complicate any of the further process.
"""
## @package driver
# This namespace is used whenever referring to the driver script.

## @package RPi.GPIO 
# Import Raspberry Pi GPIO library to be used to identify and use pins within Raspberry Pi
import RPi.GPIO as GPIO 

## @package subprocess 
# subprocess package to be used to call the other main python script
import subprocess

##  Startup_Button to be the same as Capture Button
Startup_Button = 11 

# Ignore warning for now
GPIO.setwarnings(False) 

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD) 

# Set pin 11 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(Startup_Button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

while True: # Run forever
    # When the button is pressed take a picture and call the comp vision algorithm to process it.
    if GPIO.input(Startup_Button) == True:
        GPIO.cleanup()
        subprocess.run("python3 camera.py", shell=True)