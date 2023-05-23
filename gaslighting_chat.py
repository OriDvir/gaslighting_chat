from sys import argv
import argparse


def search_gaslighting():
	pass

def parse_chat():
	pass

def translate_chat():
	pass

def gaslighting_chat(chat_path):
	print(chat_path)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--chat_path", required=True)
	args = parser.parse_args()
	gaslighting_chat(args.chat_path)
