from typing import List

from consts import GASLIGHTING_PHRASES
from database import Message, DataBase


def calculate_message_score(message: Message):
    for word in GASLIGHTING_PHRASES:
        if word in message.content:
            message.score += 1


def calculate_all_messages_score(db: DataBase):
    messages = db.Messeges.get_all_msgs()
    for message in messages:
        calculate_message_score(message)
