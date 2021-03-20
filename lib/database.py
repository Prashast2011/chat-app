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

def get_message_from_room():
    db = driver.connect(DATABASE_URL)
    cursor = db.cursor()
    result = cursor.execute("SELECT DATE,NAME,MESSAGE FROM ROOM;")
    return result.fetchall()


def create_tables():
    db = driver.connect(DATABASE_URL)
    cursor= db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ROOM (ROOM TEXT, NAME TEXT, DATE TEXT, MESSAGE TEXT);")
 #   cursor.execute("CREATE TABLE IF NOT EXISTS USER(USER TEXT PRIMARY KEY, PASSWORD TEXT);")
    

def clear_chat_table():
    db = driver.connect(DATABASE_URL)
    cursor= db.cursor()
    cursor.execute("DELETE FROM ROOM;")
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
                f"SELECT * FROM ROOM WHERE room='{room}'"
            ).fetchall()]