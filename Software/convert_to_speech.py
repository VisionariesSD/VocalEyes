from gtts import gTTS
import requests

def txt_to_mp3(file_name, language):

	# need this disabled for the api to transmit data to google 
	requests.packages.urllib3.disable_warnings() 

	# open file containing text
	fp = open(file_name, 'r')
	
	# read each line of text into a list
	txt = fp.readlines()

	# string for text without new lines characters
	remove_newline = ""
	
	# loop through removing new lines and making string for audio output
	for temp0 in txt:

		remove_newline = remove_newline + temp0
		
	# pass string, language, and speed of speech to api for conversion to mp3
	tts = gTTS(text=remove_newline, lang=language, slow=False)
	
	# save mp3 file in current directory
	tts.save('speech_output.mp3')
