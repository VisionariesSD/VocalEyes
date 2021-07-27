import convert_to_speech
import cv2
import pytesseract
import numpy as np
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from googletrans import Translator
import led

#DEFINE flages:
#speed = 1 #default speed is 1x

#USES GOOGLE TRANSLATE LANGUAGE CODES NOT TESSERACT LANGUAGE CODES
languages = ['en', 'hi', 'te']
# lang_index = test.lang_index

#Interrupt Routine TO PAUSE/PLAY THE VLC player
def PlayPause(channel):  
    subprocess.call('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause', shell = True)
    print('PAUSE BUTTON PRESSED')
    time.sleep(2) #For debouncing
    
#Interrupt Routine TO PAUSE/PLAY THE VLC player
def StopPlayback(channel):    
    #EndOutput will direct to the first program
    EndOutput()
    print('STOP BUTTON PRESSED')
    time.sleep(1.5) #For debouncing


def VolumeUp(channel):
    print('Volume increased')
    subprocess.call('amixer set Master 10%+',shell = True)
    time.sleep(1.5) #For debouncing
    
    
def VolumeDown(channel):
    print('Volume decreased')
    subprocess.call('amixer set Master 10%-',shell = True)
    time.sleep(1.5) #For debouncing

    
#function to change speed output:
def SpeedChange(x):
    subprocess.call('dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Set string:org.mpris.MediaPlayer2.Player string:Rate variant:double:%f' % x, shell = True)

    
def EndOutput():
    subprocess.call('killall vlc', shell = True)
    #subprocess.call('python /home/pi/test.py', shell = True)
    
#TODO: NEED TO WORK ON THE SETTINGS REGARDING LANGUAGE AND SPEED
#SETTINGS HANDLING SECTION

def CV(l):
    lang_index=l
    led.blink()

    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #!FOR TESTING SHOULD BE UNNECESSARY WITH LINUX

    #----------------------------------------------------------------Read in image----------------------------------------------------------------
    img = cv2.imread('/home/pi/Pictures/cnn.png')
    #img = cv2.imread('skew.jpg')  #!FOR TESTING

    #-----------------------------------------------------Perform preprocessing of the image------------------------------------------------------

    #Grayscale conversion
    #grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Gaussian blur conversion
    #gaussian = cv2.GaussianBlur(grayscale, (1,1), 0)

    #Threshold conversion
    #ret, threshold = cv2.threshold(grayscale,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    #!FOR TESTING
    #cv2.imshow('test.png',rotated)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #---------------------------------------------------------Convert the image to text---------------------------------------------------------
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(img, lang="eng+hin+tel", config=custom_config) #TODO: Need to fix the language part
    led.blink()
    led.blink()
    #print(text) #!FOR TESTING
    
    translator = Translator()

    translation = translator.translate(text, dest=languages[lang_index])
    print(translation.text)

    #TODO: NEED TO IMPLEMENT THE TRANSLATION
    #---------------------------------------------------------Convert the text to an mp3--------------------------------------------------------
    convert_to_speech.txt_to_mp3(translation.text, languages[lang_index])

    #-------------------------------------------------------------Play the audio----------------------------------------------------------------
    subprocess.call('killall vlc', shell = True) #first terminate all vlc outputs
    subprocess.call('cvlc /home/pi/Pictures/speech_output.mp3', shell = True) #PLAY IN VLC
    #subprocess.call('python /home/pi/test.py', shell = True)
    #subprocess.call('echo done_showing', shell = True)