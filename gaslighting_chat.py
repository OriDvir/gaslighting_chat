from utils import read_file, write_file
from score_calculator import calculate_all_messages_score
from consts import TRANSLATE_URL
from database import Message, Sender, DataBase

import argparse
from googletrans import Translator
import re

class Data:
    def __init__(self, db, data):
        self._db = db
        self._unparsed_data = data

    def parse_chat(self):
        # for parsing the message we define the pattern of each part of the message
        date_pattern = r"\d{1,2}[/\.]\d{1,2}[/\.]\d{2,4}, \d{1,2}:\d{2}(?: [APM]{2})?"
        sender_pattern = r" - ([^:]+):"
        message_pattern = r": (.*)"

        current_msg = None
        for line in self._unparsed_data:
            # if there is a match with date pattern we are at the beginning of the message
            if re.match(date_pattern, line) and re.findall(sender_pattern, line) and re.findall(message_pattern, line):
                if current_msg:
                    self._db.Messeges.insert_msg(current_msg)

                # When a line matches the date pattern, we create a Message
                current_msg = Message()
                current_msg.datetime = re.findall(date_pattern, line)[0]
                current_msg.sender = re.findall(sender_pattern, line)[0]
                current_msg.content = re.findall(message_pattern, line)[0]

            # if subsequent lines do not match the date pattern, we append them to the current message's
            # content until a new date is encountered.
            else:
                if current_msg:
                    current_msg.content += line.strip()

        # add msg to the parsed data
        if current_msg:
            self._db.Messeges.insert_msg(current_msg)

        # for i, data in enumerate(self.parsed_data, 1):
        #    print(str(i) + ". " + "Date:" + data.date + " Sender:" + data.sender + " Content:" + data.content + " Score:" + str( data.score))


def translate_chat(chat_path):
    data = read_file(chat_path)
    translator = Translator(service_urls=[TRANSLATE_URL])
    translated_data = []
    for line in data:
        try:
            translated_data.append(translator.translate(text=line, dest='en', src='he').text)
        except TypeError as e:
            pass
    write_file(chat_path + ".translated", translated_data)
    return translated_data


def gaslighting_chat(chat_path, translate):
    translate_data = translate_chat(chat_path) if translate else read_file(chat_path)
    db = DataBase()
    dt = Data(db, translate_data)
    dt.parse_chat()
    calculate_all_messages_score(db)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--chat_path", required=True, type=str)
    parser.add_argument("-t", "--translate", required=False, default=True, type=bool)
    args = parser.parse_args()
    gaslighting_chat(args.chat_path, args.translate)
