from email.policy import default
from importlib.resources import contents
from consts import DATABASE, MSG_DB
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os 

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime)
    sender = Column(String)
    content = Column(String)


class Sender(Base):
    __tablename__ = 'senders'
    sender = Column(String, primary_key=True)
    you_counter = Column(Integer, default=0)
    force_counter = Column(Integer, default=0)
    lie_counter = Column(Integer, default=0)
    money_counter = Column(Integer, default=0)
    alimony_counter = Column(Integer, default=0)
    final_score = Column(Integer, default=0)


class MessagePerWord(Base):
    __tablename__ = 'message_per_word'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String)
    word = Column(String)
    msg_id = Column(Integer)


class DataBase():
    def __init__(self, db=MSG_DB):
        self._db_name = db
        # Create the SQLite engine
        self.engine = create_engine(self._db_name)
        
        if not os.path.exists(self._db_name.split("sqlite:///")[-1]):
            # Create tables
            Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    @classmethod
    def get_db(cls, db_name):
        return DataBase(DATABASE.format(db_name=db_name))

    def close(self):
        self.session.close()
    #### Messages ####

    def insert_msg(self, datetime=None, sender=None, content=None):
        if datetime is not None and sender is not None and content is not None:
            msg_obj = Message(datetime=datetime, sender=sender, content=content)
            self.session.add(msg_obj)
        elif isinstance(datetime, Message):
            self.session.add(datetime)
        else:
            return
        self.session.commit()

    def get_all_msgs(self):
        return self.session.query(Message).all()

    def get_msgs_by_dates(self, start_datetime, end_datetime):
        messeges = self.session.query(Message).filter(Message.datetime.between(start_datetime, end_datetime)).all()
        return messeges

    #### Senders ####

    def init_sender(self, sender):
        if sender not in [x.sender for x in self.get_senders()]:
            sender_obj = Sender(sender=sender)
            self.session.add(sender_obj)
            self.session.commit()

    def _increment_counter(self, sender, counter_attr):
        sender_obj = self.session.query(Sender).filter_by(sender=sender).first()
        counter_value = getattr(sender_obj, counter_attr)
        setattr(sender_obj, counter_attr, counter_value + 1)
        self.session.commit()

    def _inc_counter(self, sender, counter_attr, word, msg_id):
        self._increment_counter(sender, counter_attr)
        mpw_obj = MessagePerWord(sender=sender, word=word, msg_id=msg_id)
        self.session.add(mpw_obj)
        self.session.commit() 

    def inc_counter(self, sender, msg_id, pharse):
        self._inc_counter(sender, f'{pharse}_counter', pharse, msg_id)

    def get_counter(self, sender, pharse):
        sender_obj = self.session.query(Sender).filter_by(sender=sender).first()
        counter_attr = f'{pharse}_counter'
        return getattr(sender_obj, counter_attr)

    def get_senders(self):
        return self.session.query(Sender).all()

    def update_score(self, sender, score):
        sender = self.session.query(Sender).filter_by(sender=sender).first()
        sender.score = score
        self.session.commit()

    #### Message Per Word ####
    def get_msgs_per_word(self, sender, word):
        query = self.session.query(MessagePerWord).filter_by(sender=sender, word=word)
        ids = [result.id for result in query]
        msg_query = self.session.query(Message).filter(Message.id.in_(ids))
        messages = msg_query.all()
        return messages

    #### Chat ####
    def get_chat_score(self):
        senders = self.get_senders()
        return {sender.sender:sender.final_score for sender in senders}