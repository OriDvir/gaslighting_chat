from consts import GASLIGHTING_PHRASES
from database import Message, DataBase


def calculate_message_score(message: Message, db: DataBase):
    for phrase in GASLIGHTING_PHRASES:
        if phrase in message.content:
            if phrase == "you":
                db.inc_you_counter(message.sender, message.id)
            elif phrase == "force":
                db.inc_force_counter(message.sender, message.id)
            elif phrase == "lie":
                db.inc_lie_counter(message.sender, message.id)
            elif phrase == "money":
                db.inc_money_counter(message.sender, message.id)
            elif phrase == "alimony":
                db.inc_alimony_counter(message.sender, message.id)


def calculate_chat_score(db: DataBase, word_counter):
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
        db.update_score(sndr.sender, (word_counter // 2) // total)


def calculate_all_messages_score(db: DataBase):
    word_counter = 0
    messages = db.get_all_msgs()
    for message in messages:
        word_counter += len(message.content)
        calculate_message_score(message, db)
    calculate_chat_score(db, word_counter)
