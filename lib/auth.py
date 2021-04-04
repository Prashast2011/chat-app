from jose import jwt

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

def is_valid_user(username: str, password: str):
    return True

def get_user_token(username: str):
    return jwt.encode({"username": username}, SECRET_KEY)

def get_user_from_token(token: str):
    return jwt.decode(token, SECRET_KEY)["username"]