import os
import jwt
import sqlite3 as driver
from pydantic import BaseModel
from typing import Optional
from datetime import datetime,timedelta
from passlib.context import CryptContext
DATABASE_URL = "db/chat.db"

class Message(BaseModel):
    message :str

def get_existing_rooms():
    with driver.connect(DATABASE_URL) as chat_db:
        return[
            dict (room=m[0])
            for m in chat_db.execute(f"SELECT DISTINCT(ROOM) FROM MESSAGES").fetchall()
        ]



def get_messages_from_room(room: str, username: str ):
    with driver.connect(DATABASE_URL)  as chat_db:
        return[
            dict(username=m[1], timestamp=m[2][:16], message=m[3])
            for m in chat_db.execute(
                f"SELECT * FROM MESSAGES WHERE room='{room}'"
            ).fetchall()
        ]
    
def create_tables():
    db = driver.connect(DATABASE_URL)
    cursor= db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS MESSAGES (ROOM TEXT, NAME TEXT, DATE TEXT, MESSAGE TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS USER(USER TEXT PRIMARY KEY, PASSWORD TEXT);")
    db.commit()
    

def clear_chat_table():
    db = driver.connect(DATABASE_URL)
    cursor= db.cursor()
    cursor.execute("DELETE FROM MESSAGES;")
    db.commit()
    return "Cleared Tables"


def add_message(room: str, message: str, username: str):
    with driver.connect(DATABASE_URL) as chat_db:
        chat_db.execute(
            f"INSERT INTO ROOM VALUES ('{room}','{username}', '{datetime.now()}', '{message}') "
        )
        chat_db.commit()


def get_messages(room: str):
    with driver.connect(DATABASE_URL) as chat_db:
        return[
            dict(room=x[0], username=x[1], timestamp=x[2], message=x)
            for x in chat_db.execute(
                f"SELECT * FROM MESSAGES WHERE room='{room}'"
            ).fetchall()]


def post_message_to_room(room: str, message: Message, username: str):
    with driver.connect(DATABASE_URL) as mdb:
        mdb.execute(
            f"INSERT INTO MESSAGES VALUES ('{room}', '{username}' , '{datetime.now()}','{message.message}')"
        )
        mdb.commit()
        