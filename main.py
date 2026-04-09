from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel
from typing import Optional
import time

app = FastAPI()

class User(SQLModel):
    id: int
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

class UserCreate(SQLModel):
    username: str
    password: str
    email: Optional[str] = None
    is_active: bool = True

class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class LoginData(SQLModel):
    username: str
    password: str

db_users = [
    User(id=1, username="admin", password="ad12", email="admin@uide.edu.ec", is_active=True),
    User(id=2, username="student", password="st13", email="student@uide.edu.ec", is_active=True),
    User(id=3, username="guest", password="gu23", email="guest@uide.edu.ec", is_active=True)
]

next_id = 4

failed_attempts = {}
blocked_users = {}

MAX_ATTEMPTS = 999999
BLOCK_TIME = 30

@app.get("/")
def root():
    return {"message": "API de usuarios funcionando"}

@app.post("/users")
def create_user(user: UserCreate):
    global next_id

    for u in db_users:
        if u.username == user.username:
            raise HTTPException(status_code=400, detail="El username ya existe")

    new_user = User(
        id=next_id,
        username=user.username,
        password=user.password,
        email=user.email,
        is_active=user.is_active
    )

    db_users.append(new_user)
    next_id += 1

    return {"message": "Usuario creado correctamente", "user": new_user}

@app.get("/users")
def get_users():
    return db_users

@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in db_users:
        if user.id == user_id:
            return user

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate):
    for user in db_users:
        if user.id == user_id:
            if data.username is not None:
                user.username = data.username
            if data.email is not None:
                user.email = data.email
            if data.is_active is not None:
                user.is_active = data.is_active

            return {"message": "Usuario actualizado correctamente", "user": user}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in db_users:
        if user.id == user_id:
            db_users.remove(user)
            return {"message": "Usuario eliminado correctamente"}

    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/login")
def login(data: LoginData):
    current_time = time.time()

    if data.username in blocked_users:
        if current_time < blocked_users[data.username]:
            return {"message": "Usuario bloqueado temporalmente"}
        else:
            del blocked_users[data.username]

    for user in db_users:
        if user.username == data.username and user.password == data.password:
            failed_attempts[data.username] = 0
            return {"message": "Login successful"}

    if data.username not in failed_attempts:
        failed_attempts[data.username] = 0

    failed_attempts[data.username] += 1

    if failed_attempts[data.username] >= MAX_ATTEMPTS:
        blocked_users[data.username] = current_time + BLOCK_TIME
        failed_attempts[data.username] = 0
        return {"message": "Demasiados intentos fallidos, usuario bloqueado por 30 segundos"}

    return {"message": "Invalid username or password"}
