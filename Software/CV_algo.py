import convert_to_speech
import cv2
import pytesseract
import numpy as np

#TODO: NEED TO WORK ON THE SETTINGS REGARDING LANGUAGE AND SPEED

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe' #!FOR TESTING SHOULD BE UNNECESSARY WITH LINUX

#----------------------------------------------------------------Read in image----------------------------------------------------------------
img = cv2.imread('/home/pi/Pictures/test.jpg')
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




#subprocess.call('echo done_showing', shell = True)