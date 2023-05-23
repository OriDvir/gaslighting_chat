from email.policy import default
from importlib.resources import contents
from consts import DATABASE
from sqlalchemy import create_engine, Column, Integer, String, DateTime 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    datetime = Column(DateTime, primary_key=True) 
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

class DataBase():
    def __init__(self):
        self._db_name = DATABASE
        # Create the SQLite engine
        self.engine = create_engine(self._db_name) 

        # Create tables
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    class Messeges:
        def insert_msg(self, datetime=None, sender=None, content=None):
            if datetime is not None and sender is not None and content is not None:
                msg_obj = Message(datetime=datetime, sender=sender, content=content)
                self.session.add(msg_obj)
            elif isinstance(datetime, Message):  # Assume 'datetime' is a Message object
                self.session.add(datetime)
            else:
                return
            self.session.commit()

        def get_all_msgs(self):
            return self.session.query(Message).all()

        def get_msgs_by_dates(self, start_datetime, end_datetime):
            messeges = self.session.query(Message).filter(Message.datetime.between(start_datetime, end_datetime)).all()
            return messeges


    class Senders:
        def _increment_counter(self, sender, counter_attr):
            sender_obj = self.session.query(Sender).filter_by(sender=sender).first()
            counter_value = getattr(sender_obj, counter_attr)
            setattr(sender_obj, counter_attr, counter_value + 1)
            self.session.commit()

        def init_sender(self, sender):
            sender_obj = Sender(sender=sender)
            self.session.add(sender_obj)
            self.session.commit() 

        def inc_you_counter(self, sender):
            self._increment_counter(sender, 'you_counter')

        def inc_force_counter(self, sender):
            self._increment_counter(sender, 'force_counter')

        def inc_lie_counter(self, sender):
            self._increment_counter(sender, 'lie_counter')

        def inc_money_counter(self, sender):
            self._increment_counter(sender, 'money_counter')

        def inc_alimony_counter(self, sender):
            self._increment_counter(sender, 'alimony_counter')

        def get_sender(self, sender):
            sender_obj = self.session.query(Sender).filter_by(sender=sender).first()
            return sender_obj

        def update_score(self, sender, score):
            sender = self.session.query(Sender).filter_by(sender=sender).first()
            sender.score = score
            self.session.commit()
