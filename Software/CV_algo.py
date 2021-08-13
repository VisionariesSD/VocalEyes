import convert_to_speech               #SPEECH TRANSLATION MODULE THROUGH gTTS
import cv2                             #FOR IMAGE PROCESSING 
import pytesseract                     #FOR IMAGE PROCESSING  
import subprocess                      #TO CALL PROCESSES AND RUN THEM AS A THREAD
import time                            #USED TO REMOVE MULTIPLE INTERRUPT CAlLS ON SINGLE BUTTON PRESS 
from googletrans import Translator     #FOR CONVERSION BETWEEN LANGUAGES
#import led                            #VISUAL CUE FOR TESTING
import pygame                          #AUDIO CUES FOR THE USER   


#------------------------------GLOBAL VARIABLES------------------------------------------------#
#USES GOOGLE TRANSLATE LANGUAGE CODES NOT TESSERACT LANGUAGE CODES
#Cycles through 3 languages: english, hindi, telegu
#To add more languages: add the appropriate code and change value of land_options variable accordingly
languages = ['en', 'hi', 'te']

#--------------------------INTERRUPT ROUTINES AND OTHER FUNCTIONS------------------------------#
#Function to play audio cues for button presses:
def playCue(fn):
    pygame.mixer.init()
    pygame.mixer.music.load(fn)
    pygame.mixer.music.play()
    
#Interrupt Routine TO PAUSE/PLAY THE VLC player
def PlayPause(channel):
    subprocess.run('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause', shell = True)
    print('PAUSE BUTTON PRESSED')
    time.sleep(1) #For debouncing    

#Interrupt Routine TO STOP THE VLC player output
def StopPlayback(channel):    
    #EndOutput will direct to the first program
    EndOutput()
    print('STOP BUTTON PRESSED')
    time.sleep(1) #For debouncing

#Interrupt Routine to increase the volume using amixer
def VolumeUp(channel):
    print('Volume increased')
    subprocess.run('amixer set Master 10%+',shell = True)
    #subprocess.run('amixer -D pulse sset Master 10%+',shell = True)
    time.sleep(1) #For debouncing
    
#Interrupt Routine to decrease the volume using amixer    
def VolumeDown(channel):
    print('Volume decreased')
    subprocess.run('amixer set Master 10%-',shell = True)
    #subprocess.run('amixer -D pulse sset Master 10%-',shell = True)
    time.sleep(1) #For debouncing

#function to check if VLC process is running: (Used in Spd_Change and EndOutput functions)
def CheckforVLC():
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
    subprocess.run('dbus-send --print-reply --session --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2 org.freedesktop.DBus.Properties.Set string:org.mpris.MediaPlayer2.Player string:Rate variant:double:%f' % x, shell = True)
    time.sleep(0.5)
    
#function to end output:
def EndOutput():
    if (CheckforVLC()):
        subprocess.run('killall vlc', shell = True)
        playCue('/home/pi/SoundBites/Stopped.mp3')
    else:
        print("No VLC Stopped.")
    
#MAIN Computer Vision algorithm----------------------------------------------->
def CV(l):
    lang_index=l                     #l is set in the main program and passed into CV
    #led.blink()                     #Debug Line

    #pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #!FOR TESTING SHOULD BE UNNECESSARY WITH LINUX

    #----------------------------------------------------------------Read in image----------------------------------------------------------------
    img = cv2.imread('/home/pi/Pictures/input.png')
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
    #led.blink()
    #led.blink()
    #print(text) #!FOR TESTING
    
    translator = Translator()

    translation = translator.translate(text, dest=languages[lang_index])
    print(translation.text)

    #---------------------------------------------------------Convert the text to an mp3--------------------------------------------------------
    convert_to_speech.txt_to_mp3(translation.text, languages[lang_index])

    #-------------------------------------------------------------Play the audio----------------------------------------------------------------
    subprocess.run('killall vlc', shell = True) #first terminate all vlc outputs
    subprocess.run('cvlc /home/pi/Pictures/speech_output.mp3 --play-and-exit', shell = True) #PLAY IN VLC