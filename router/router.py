from unicodedata import name
from unittest import result
from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.users import users
from typing import List
from werkzeug.security import generate_password_hash, check_password_hash

user = APIRouter()


@user.get("/")
def root():
    return {"HI": "jolas"}


@user.get("/show/users", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result


@user.get("/show/user/{user_id}", response_model=UserSchema)
def get_user(user_id: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result


@user.post("/create/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["password"] = generate_password_hash(data_user.password, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
        return Response(status_code=HTTP_201_CREATED)


@user.put("/edit/user/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: str,):
    with engine.connect() as conn:
        encrypt_pass = generate_password_hash(data_update.password, "pbkdf2:sha256:30", 30)
        result = conn.execute(users.update().values(name=data_update.name, 
        username=data_update.username, password=encrypt_pass).where(users.c.id == user_id))
        result = conn.execute(users.select().where(users.c.id == user_id)).first()
        return result


@user.delete("/delete/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str,):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id)).first()
        return Response(status_code=HTTP_204_NO_CONTENT)


@user.post("/login")
def login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result is not None:
            check_passw = check_password_hash(result[3], data_user.password)
            if check_passw:
                return "Success"
            return "Denied"