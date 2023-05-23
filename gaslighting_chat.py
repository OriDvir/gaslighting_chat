from utils import read_file, write_file

from sys import argv
import argparse
from googletrans import Translator

TRANSLATE_URL = 'translate.googleapis.com'

def search_gaslighting():
	pass

def parse_chat():
	pass

def translate_chat(chat_path):
	data = read_file(chat_path)
	translator = Translator(service_urls=[TRANSLATE_URL])
	translated_data = []
	for line in data:
		translated_data.append(translator.translate(text=line, dest='en', src='he').text)
	write_file(chat_path + ".translated", translated_data)
	return translated_data

def gaslighting_chat(chat_path, translate):
	translate_data = translate_chat(chat_path) if translate else read_file(chat_path) 

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--chat_path", required=True, type=str)
	parser.add_argument("-t", "--translate", required=False, default=True, type=bool)
	args = parser.parse_args()
	gaslighting_chat(args.chat_path, args.translate)
