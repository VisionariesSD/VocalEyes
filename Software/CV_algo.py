"""!
@file CV_algo.py

@brief
This is the code used during the entire processing of the CV algorithm. This is the main section of code that handles all image, translation, and audio processing for the device.
"""

## @package convert_to_speech
# This package is used for speech translation module through gTTS.
import convert_to_speech               

## @package cv2
# This package is used for all image handling and image processing.
import cv2                             

## @package pytesseract
# This package is used for the optical character recognition to retrieve text from a picture.
import pytesseract      

## @package subprocess 
# subprocess package to be used to call another process as a thread.
import subprocess    

## @package time
#This packaged is mostly used for button debouncing.
import time                           

## @package googletrans
# This package is ued for the translation functionality of the processing.
from googletrans import Translator     

## @package led
# This is the led.py script located within Software that was used for testing.
#import led                            

## @package pygame
# This package is used to output audio cues for the user.
import pygame                         


#------------------------------GLOBAL VARIABLES------------------------------------------------#
#USES GOOGLE TRANSLATE LANGUAGE CODES NOT TESSERACT LANGUAGE CODES
#Cycles through 3 languages: english, hindi, telegu
#To add more languages: add the appropriate code and change value of land_options variable accordingly

## This is the languages array that is used for language translation and selection
languages = ['en', 'hi', 'te']

#--------------------------INTERRUPT ROUTINES AND OTHER FUNCTIONS------------------------------#
#Function to play audio cues for button presses:
def playCue(fn):
    """!
    Function to play audio cues for button presses

    @param fn   This is the soundbite that is loaded in and is ready to be used as an audio cue

    @return     Technically no return in the function but an audio cue is output to the user
    """
    pygame.mixer.init()
    pygame.mixer.music.load(fn)
    pygame.mixer.music.play()
    
#Interrupt Routine TO PAUSE/PLAY THE VLC player
def PlayPause(channel):
    """!
    Function to pause audio on button press

    @param channel      Current audio channel that is being used.

    @return     Technically no return in the function but the current output audio will be paused
    """
    subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause', shell = True)
    print('PAUSE BUTTON PRESSED')
    time.sleep(1) #For debouncing    

#Interrupt Routine TO STOP THE VLC player output
def StopPlayback(channel):   
    """!
    Function to stop all audio on button press

    @param channel      Current audio channel that is being used.

    @return     Technically no return in the function but the current output audio will be stopped.
    """ 
    #EndOutput will direct to the first program
    EndOutput()
    print('STOP BUTTON PRESSED')
    time.sleep(1) #For debouncing

#Interrupt Routine to increase the volume using amixer
def VolumeUp(channel):
    """!
    Function to increase volume on button press

    @param channel      Current audio channel that is being used.

    @return     Technically no return in the function but the current volume will be increased.
    """
    print('Volume increased')
    subprocess.run('amixer set Master 10%+',shell = True)
    #subprocess.run('amixer -D pulse sset Master 10%+',shell = True)
    time.sleep(1) #For debouncing
    
#Interrupt Routine to decrease the volume using amixer    
def VolumeDown(channel):
    """!
    Function to decrease volume on button press

    @param channel      Current audio channel that is being used.

    @return     Technically no return in the function but the current volume will be decreased
    """
    print('Volume decreased')
    subprocess.run('amixer set Master 10%-',shell = True)
    #subprocess.run('amixer -D pulse sset Master 10%-',shell = True)
    time.sleep(1) #For debouncing

#Function to check if VLC process is running: (Used in Spd_Change and EndOutput functions)
def CheckforVLC():
    """!
    Function to check if VLC process is running: (Used in Spd_Change and EndOutput functions) 
    """
    out = ""
    try:
        out = subprocess.check_output(["pidof","vlc"])
    except:
        pass
    if out != "" :
        return True
    else:
        playCue('/home/pi/SoundBites/No_VLC.mp3')
        return False
    
#function to change speed output:
def SpeedChange(x):
    """!
    Function to change speed on button press

    @param x    Current speed setting that needs the audio to be set to 

    @return     Technically no return in the function but the current audio output will have its speed changed
    """
    subprocess.run('dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Set string:org.mpris.MediaPlayer2.Player string:Rate variant:double:%f' % x, shell = True)
    time.sleep(0.5)
    
#function to end output:
def EndOutput():
    """!
    Function to end all VLC output.
    """
    if (CheckforVLC()):
        subprocess.run('killall vlc', shell = True)
        playCue('/home/pi/SoundBites/Stopped.mp3')
    else:
        print("No VLC Stopped.")
    
#MAIN Computer Vision algorithm----------------------------------------------->
def CV(l):
    """!
    Function that serves as the main CV algorithm as well as the picture-to-audio processing.

    @param l    Current language index setting that needs to be used for the languages array.

    @return     Technically no return in the function but the requested input picture will have its audio output to the user in the correct translation.
    """

    ##l is the language index and is set in the main program and passed into CV
    lang_index=l                     
    #led.blink()                     #!Debug Line

    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #!FOR TESTING SHOULD BE UNNECESSARY WITH LINUX

    #----------------------------------------------------------------Read in image----------------------------------------------------------------
    ##This is the current image that was captured from camera.py
    img = cv2.imread('/home/pi/Pictures/input.png')
    #img = cv2.imread('skew.jpg')  #!FOR TESTING

    #-----------------------------------------------------Perform preprocessing of the image------------------------------------------------------

    #Grayscale conversion
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Gaussian blur conversion
    gaussian = cv2.GaussianBlur(grayscale, (1,1), 0)

    #Threshold conversion
    ret, threshold = cv2.threshold(grayscale,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #!FOR TESTING
    #cv2.imshow('test.png',rotated)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #---------------------------------------------------------Convert the image to text---------------------------------------------------------
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang="eng+hin+tel", config=custom_config) #TODO: Need to fix the language part
    
    #!FOR TESTING
    #led.blink()
    #led.blink()
    #print(text) 
    
    ##This is the translator object to be used for translation.
    translator = Translator()

    ##This is the translation generated from the translate function from googletrans
    translation = translator.translate(text, dest=languages[lang_index])

    #!FOR TESTING
    print(translation.text)

    #---------------------------------------------------------Convert the text to an mp3--------------------------------------------------------
    convert_to_speech.txt_to_mp3(translation.text, languages[lang_index]) #use the convert_to_speech.py to achieve mp3 file

    #-------------------------------------------------------------Play the audio----------------------------------------------------------------
    subprocess.run('killall vlc', shell = True) #first terminate all vlc outputs
    subprocess.run('cvlc /home/pi/Pictures/speech_output.mp3 --play-and-exit', shell = True) #PLAY IN VLC