from typing import List

from consts import GASLIGHTING_PHRASES


class Message:
    def __init__(self):
        self.date = ""
        self.sender = ""
        self.content = ""
        self.score = 0


def calculate_message_score(message: Message):
    for word in GASLIGHTING_PHRASES:
        if word in message.content:
            message.score += 1


def calculate_all_messages_score(messages: List[Message]):
    for message in messages:
        calculate_message_score(message)
