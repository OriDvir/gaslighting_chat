from sys import argv
import argparse
from googletrans import Translator

TRANSLATE_URL = 'translate.googleapis.com'

def search_gaslighting():
	pass

def parse_chat():
	pass

def translate_chat(chat_path):
	with open(chat_path, "rt") as chat:
		data = chat.readlines()
	translator = Translator(service_urls=[TRANSLATE_URL])
	translated_data = []
	for line in data:
		translated_data.append(translator.translate(text=line, dest='en', src='he').text)
	return translated_data

def gaslighting_chat(chat_path):
	translate_data = translate_chat(chat_path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--chat_path", required=True)
	args = parser.parse_args()
	gaslighting_chat(args.chat_path)
