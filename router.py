from datetime import datetime, timedelta
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends

from gaslighting_chat import gaslight_chat
from database import DataBase

router = APIRouter()

def get_db_session() -> Session:
    db = DataBase.get_db("messages") 
    try:
        yield db
    finally:
        db.close()


## init
@router.get("/init/{chat_path}")
async def init_chat(chat_path : str, translate: bool = True):
    gaslight_chat(chat_path, translate)
    return {'chat_path': chat_path, 'translate': translate}

## get score
@router.get("/db/get_score")
def read_items(db: DataBase = Depends(get_db_session)):
    # Use the 'db' session to interact with the database
    return db.get_chat_score()

## word counter
@router.get("/db/get_word_count/{word}")
def read_items(word: str, db: DataBase = Depends(get_db_session)):
    # Use the 'db' session to interact with the database
    senders = db.get_senders()
    return {sender.sender:db.get_counter(sender.sender, word) for sender in senders}

## give word - get lines
@router.get("/db/get_lines/{word}")
def read_items(word: str, db: DataBase = Depends(get_db_session)):
    # Use the 'db' session to interact with the database
    senders = db.get_senders()
    return {sender.sender:[(msg.datetime, msg.content) for msg in db.get_msgs_per_word(sender.sender, word)] for sender in senders}

## git datetime - get 2 minutes before and after
@router.get("/db/get_context/{date_time}")
def read_items(date_time: datetime, minutes: int = 3, db: DataBase = Depends(get_db_session)):
    # Use the 'db' session to interact with the database
    minutes_before = date_time - timedelta(minutes=minutes)
    minutes_after = date_time + timedelta(minutes=minutes)
    return db.get_msgs_by_dates(minutes_before, minutes_after)
