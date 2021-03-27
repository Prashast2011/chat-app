from .auth import *
from fastapi import FastAPI, Depends, status, Form
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from .database import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

app.mount("/ui", StaticFiles(directory="ui"), name= "static")




@app.get("/")
def root():
    return'hello world'

@app.get("/favicon.ico")
def get_favicon():
    return FileResponse("ui/images/favicon.ico")


oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/user")
def get_user(token: str = Depends(oath2_scheme)):
    return get_user_from_token(token)


@app.get("/room/{room}")
def get_room(room: str, username: str = Depends(get_user)):
    return get_messages(room)

@app.get("/db")
def get_db():
    return create_tables()

@app.get("/reset")
def clear_db():
    return clear_chat_table()

@app.post("/room/{room}")
def post_room(room: str, message: Message, username:str=Depends(get_user)):
    add_message(room, message.message, username)

'''#@app.post("/signup")
def add_user(user_data:UserData):
    return create_user(user_data)

@app.post("/token")
def check_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = UserData(user=form_data.username, password = form_data.password)
    if verify_user(user_data):
        return {"access_token": create_access_token(user_data.user), "token_type": "bearer"}
'''

@app.post("/login")
def post_login(username: str = Form(...), password: str = Form(...)):
    if is_valid_user(username, password):
        response = RedirectResponse("ui/room.html", status.HTTP_302_FOUND)
        response.set_cookie(key="token", value=get_user_token(username))
        return response
    else: 
        return RedirectResponse("ui/login.html", status.HTTP_302_FOUND)
