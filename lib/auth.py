from jose import jwt
from .database import driver, DATABASE_URL

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

def is_user_exist(username):
    with driver.connect(DATABASE_URL) as mdb:
        return ( 
            len(
                mdb.execute(
                    f"SELECT * FROM USER WHERE USER='{username}'"
                ).fetchall()
            )
            > 0
        )


def is_valid_password(username, password):
    with driver.connect(DATABASE_URL) as mdb:
        return(
            len(
                mdb.execute(
                    f"SELECT * FROM USER WHERE USER='{username}' AND PASSWORD='{password}'"
                ).fetchall()
            )
            >0
        )

def create_user(username, password):
    with driver.connect(DATABASE_URL) as mdb:
        mdb.execute(f"INSERT INTO USER VALUES('{username}','{password}')")
        mdb.commit()


def is_valid_user(username: str, password: str):
    if is_user_exist(username):
        return is_valid_password(username, password)
    else:
        create_user(username, password)
        return True


def get_user_token(username: str):
    return jwt.encode({"username": username}, SECRET_KEY)


def get_user_from_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY)["username"]
    except:
        return "Anonymus"
