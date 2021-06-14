import convert_to_speech
import cv2
import pytesseract
import numpy as np
import subprocess
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

#DEFINE PIN nos for the buttons:
Button_Pause = 13 # Pin 13 on Board = Pause/Play button
Button_VolUp = 15 # Pin 15 on Board = Volume Up
Button_VolDown = 16 #Pin 16 on Board = Volume Down

#DEFINE flages:
audio_flag = False #Used to 

#Interrupt Routine TO PAUSE/PLAY THE VLC player
def PlayPause(channel):    
    if (audio_flag):
        #ONLY Allow pausing when the audio has been processed
        print('Audio flag up')
        subprocess.call('dbus-send --type=method_call --dest=org.mpris.MediaPlayer2.vlc /org/mpris/MediaPlayer2   org.mpris.MediaPlayer2.Player.PlayPause', shell = True)
    print('BUTTON PRESSED')
    time.sleep(1) #For debouncing


def VolumeUp(channel):
    print('Volume increased')
    subprocess.call('amixer set Master 10%+',shell = True)
    time.sleep(1.5) #For debouncing
    
    
def VolumeDown(channel):
    print('Volume increased')
    subprocess.call('amixer set Master 10%-',shell = True)
    time.sleep(1.5) #For debouncing
    
#TODO: NEED TO WORK ON THE SETTINGS REGARDING LANGUAGE AND SPEED

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #!FOR TESTING SHOULD BE UNNECESSARY WITH LINUX

#SETTING UP ALL BUTTONS:
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

#SET ALL THE BUTTONS AS PULL DOWN
GPIO.setup(Button_Pause, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_VolUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_VolDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#INTERRUPT HANDLER FOR pause button: 
GPIO.add_event_detect(Button_Pause, GPIO.RISING, callback= PlayPause, bouncetime=100)
GPIO.add_event_detect(Button_VolUp, GPIO.RISING, callback= VolumeUp, bouncetime=100)
GPIO.add_event_detect(Button_VolDown, GPIO.RISING, callback= VolumeDown, bouncetime=100)


    
#----------------------------------------------------------------Read in image----------------------------------------------------------------
img = cv2.imread('/home/pi/Pictures/testocr.png')
#img = cv2.imread('skew.jpg')  #!FOR TESTING

#-----------------------------------------------------Perform preprocessing of the image------------------------------------------------------

#Grayscale conversion
grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Gaussian blur conversion
gaussian = cv2.GaussianBlur(grayscale, (1,1), 0)

#Threshold conversion
ret, threshold = cv2.threshold(gaussian,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

#Correcting any possible skew in the image
coords = np.column_stack(np.where(threshold > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

(h, w) = threshold.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(threshold, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

#ERROR ON ROTATING SO IGNORING THE ROTATION FOR NOW
rotated = img

#!FOR TESTING
#cv2.imshow('test.png',rotated)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#---------------------------------------------------------Convert the image to text---------------------------------------------------------
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(rotated, lang=None, config=custom_config) #TODO: Need to fix the language part

#print(text) #!FOR TESTING

#---------------------------------------------------------Convert the text to an mp3--------------------------------------------------------
convert_to_speech.txt_to_mp3(text, 'en')


#-------------------------------------------------------------Play the audio----------------------------------------------------------------
subprocess.call('killall vlc', shell = True) #first terminate all vlc outputs
audio_flag = True
subprocess.call('cvlc /home/pi/Pictures/speech_output.mp3', shell = True) #PLAY IN VLC
audio_flag = False



#subprocess.call('echo done_showing', shell = True)