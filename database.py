from email.policy import default
from importlib.resources import contents
from consts import DATABASE
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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
    def __init__(self):
        self._db_name = DATABASE
        # Create the SQLite engine
        self.engine = create_engine(self._db_name)

        # Create tables
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

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

    def inc_you_counter(self, sender, msg_id):
        self._inc_counter(sender, 'you_counter', 'you', msg_id)

    def inc_force_counter(self, sender, msg_id):
        self._inc_counter(sender, 'force_counter', 'force', msg_id)

    def inc_lie_counter(self, sender, msg_id):
        self._inc_counter(sender, 'lie_counter', 'lie', msg_id)

    def inc_money_counter(self, sender, msg_id):
        self._inc_counter(sender, 'money_counter', 'money', msg_id)

    def inc_alimony_counter(self, sender, msg_id):
        self._inc_counter(sender, 'alimony_counter', 'alimony', msg_id)

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