from typing import List

from consts import GASLIGHTING_PHRASES
from massage import Message


def calculate_message_score(message: Message):
    for word in GASLIGHTING_PHRASES:
        if word in message.content:
            message.score += 1


def calculate_all_messages_score(messages: List[Message]):
    for message in messages:
        calculate_message_score(message)
