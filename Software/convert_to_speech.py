from gtts import gTTS
import requests

def txt_to_mp3(txt, language):

	# need this disabled for the api to transmit data to google 
	requests.packages.urllib3.disable_warnings() 
		
	# pass string, language, and speed of speech to api for conversion to mp3
	tts = gTTS(text=txt, lang=language, slow=False) #TODO: Need to fix the language part
	
	# save mp3 file in current directory
	tts.save('/home/pi/Pictures/speech_output.mp3')

	#tts.save('speech_output.mp3') #!FOR TESTING
