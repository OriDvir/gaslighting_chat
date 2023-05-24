from consts import GASLIGHTING_PHRASES
from database import Message, DataBase


def calculate_message_score(message: Message, db: DataBase):
    for phrase in GASLIGHTING_PHRASES:
        if phrase in message.content:
            db.inc_counter(message.sender, message.id, phrase)


def calculate_chat_score(db: DataBase, word_counter: int):
    # total of problematic word (for each person)
    total = 0
    # go to the sender row in senders
    for sndr in db.get_senders():
        total += sndr.you_counter
        total += sndr.force_counter
        total += sndr.lie_counter
        total += sndr.money_counter
        total += sndr.alimony_counter
        # update score field for each sender
        db.update_score(sndr.sender,  total // (word_counter // 2))


def calculate_all_messages_score(db: DataBase):
    word_counter = 0
    messages = db.get_all_msgs()
    for message in messages:
        word_counter += len(message.content)
        calculate_message_score(message, db)
    calculate_chat_score(db, word_counter)
