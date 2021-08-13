"""!
@file convert_to_speech.py

@brief
This is the code used during the text-to-audio processing of the CV algorithm.
"""
## @package gtts
# This package is the google text-to-speech package allowing us to use the Google Translate API for audio output in the correct dialect.
from gtts import gTTS

## @package requests
# This package is used so we can transmit data to the Google Translate API.
import requests

def txt_to_mp3(txt, language):
	"""! 
    This function is used so we can take the text as well as the selected language and "return" an mp3 file with correct text and dialect.

	@param txt		This is the translated text that is ready for audio output.
	@param language		This is the current language selection that is used for translation as well as finding the correct dialect.

	@return		Technically there is no return in the function itself but the function creates an mp3 file for audio output.		
    """

	# need this disabled for the api to transmit data to google 
	requests.packages.urllib3.disable_warnings() 
		
	# pass string, language, and speed of speech to api for conversion to mp3
	tts = gTTS(text=txt, lang=language) 
	
	# save mp3 file in current directory
	tts.save('/home/pi/Pictures/speech_output.mp3')

